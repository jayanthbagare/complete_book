#!/usr/bin/env python3
"""
Build a static, multi-page website from book/*.md for GitHub Pages.

  index.html           title page (front matter + table of contents)
  chapter-NN.html      one page per chapter (part banner on a part's first chapter)
  appendix-x.html      one page per appendix
  assets/              style.css, site.js, search-index.js

Cross-page links are rewritten: "#chapter-9--..." becomes "chapter-09.html#chapter-9--...".
Mermaid diagrams render client-side. Search runs offline from an embedded index.

Usage:
    pip install markdown
    python tools/build_site.py            # writes _site/
    python -m http.server -d _site 8000   # preview at http://localhost:8000
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

import markdown

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_book import HEADING, LINK, PARTS, scan, slugify, verify  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
ASSETS = Path(__file__).resolve().parent / "site_assets"
SITE_TITLE = "From Problem to Agent"
SUBTITLE = "The Complete Field Book"
REPO_URL = "https://github.com/jayanthbagare/complete_book"
MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"

CHAPTER = re.compile(r"^## Chapter (\d+) — (.+)$")
APPENDIX = re.compile(r"^## Appendix ([A-Z]) — (.+)$")
PART = re.compile(r"^# (Part [IVX]+ — .+|Appendices)$")


def split(text: str):
    """Split the book into the front page and one page per chapter/appendix."""
    lines = text.splitlines()
    pages, part, part_intro = [], None, []
    front, cur = [], None
    for _, line, in_fence, _ in scan(lines):
        if in_fence is False:
            if m := PART.match(line):
                part, part_intro, cur = m.group(1), [], None
                continue
            m_ch, m_ap = CHAPTER.match(line), APPENDIX.match(line)
            if m_ch or m_ap:
                if m_ch:
                    num, title = m_ch.groups()
                    slug, label = f"chapter-{int(num):02d}", f"Chapter {num}"
                else:
                    num, title = m_ap.groups()
                    slug, label = f"appendix-{num.lower()}", f"Appendix {num}"
                intro = "\n".join(part_intro).strip()
                cur = {"file": f"{slug}.html", "label": label, "title": title, "part": part,
                       "part_intro": intro if intro.strip("-\n ") else "", "lines": [line]}
                part_intro = []
                pages.append(cur)
                continue
        if cur is not None:
            cur["lines"].append(line)
        elif part is not None:
            part_intro.append(line)
        else:
            front.append(line)
    for p in pages:
        p["body"] = "\n".join(p.pop("lines")).rstrip().rstrip("-").rstrip()
    return "\n".join(front), pages


def heading_slugs(md_text: str) -> set[str]:
    slugs = set()
    for _, line, in_fence, _ in scan(md_text.splitlines()):
        if in_fence is False and (m := HEADING.match(line)):
            slugs.add(slugify(m.group(2)))
    return slugs


def render(md_text: str, own: set[str], where: dict[str, str]) -> tuple[str, list]:
    """Markdown -> HTML with mermaid preserved, links rewritten, tables wrapped."""
    blocks: list[str] = []

    def stash(m):
        blocks.append(m.group(1))
        return f"\n\nMERMAIDBLOCK{len(blocks) - 1}END\n\n"

    md_text = re.sub(r"```mermaid\n(.*?)\n```", stash, md_text, flags=re.S)
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "toc", "sane_lists", "attr_list"],
        extension_configs={"toc": {"slugify": lambda v, s: slugify(v), "toc_depth": "2-3"}},
    )
    body = md.convert(md_text)
    for i, b in enumerate(blocks):
        pre = f'<div class="diagram"><pre class="mermaid">\n{html.escape(b)}\n</pre></div>'
        body = body.replace(f"<p>MERMAIDBLOCK{i}END</p>", pre).replace(f"MERMAIDBLOCK{i}END", pre)

    def relink(m):
        anchor = m.group(1)
        if anchor in own or anchor not in where:
            return m.group(0)
        return f'href="{where[anchor]}#{anchor}"'

    body = re.sub(r'href="#([^"]+)"', relink, body)
    body = body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    body = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', body)
    return body, md.toc_tokens


def plain(html_text: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", html_text))).strip()


def nav_html(pages, current: str) -> str:
    out = [f'<a class="nav-home{" active" if current == "index.html" else ""}" href="index.html">Title page &amp; contents</a>']
    part, opened = None, False
    for p in pages:
        if not opened or p["part"] != part:
            if opened:
                out.append("</ol></div>")
            opened = True
            part = p["part"]
            name = (part or "").split(" — ")
            head = f'<span class="nav-part-num">{html.escape(name[0])}</span>'
            if len(name) > 1:
                head += f'<span class="nav-part-name">{html.escape(name[1])}</span>'
            out.append(f'<div class="nav-part"><div class="nav-part-title">{head}</div><ol>')
        cls = ' class="active" aria-current="page"' if p["file"] == current else ""
        num = p["label"].split()[-1]
        out.append(f'<li><a href="{p["file"]}"{cls}><span class="nav-num">{num}</span>'
                   f'<span>{html.escape(p["title"])}</span></a></li>')
    out.append("</ol></div>")
    return "\n".join(out)


def page_toc(tokens) -> str:
    items = []
    for t in tokens:
        for c in t.get("children", []):
            items.append(f'<li><a href="#{c["id"]}">{html.escape(html.unescape(c["name"]))}</a></li>')
    if not items:
        return ""
    return f'<nav class="page-toc" aria-label="On this page"><div class="page-toc-title">On this page</div><ol>{"".join(items)}</ol></nav>'


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='7' fill='%231f5f8b'/><path d='M8 22 L14 10 L18 18 L24 8' stroke='white' stroke-width='3' fill='none' stroke-linecap='round' stroke-linejoin='round'/></svg>">
<link rel="stylesheet" href="assets/style.css">
<script>
  try {{ var t = localStorage.getItem("theme"); if (t) document.documentElement.dataset.theme = t; }} catch (e) {{}}
</script>
</head>
<body class="{body_class}">
<a class="skip" href="#content">Skip to content</a>
<header class="topbar">
  <button class="menu-btn" aria-label="Open navigation" aria-expanded="false" aria-controls="sidebar">
    <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
  </button>
  <a class="brand" href="index.html"><span class="brand-title">{site_title}</span><span class="brand-sub">{subtitle}</span></a>
  <div class="search">
    <input id="search" type="search" placeholder="Search the book…" autocomplete="off" aria-label="Search the book">
    <kbd>/</kbd>
    <div id="search-results" class="search-results" role="listbox" hidden></div>
  </div>
  <button class="theme-btn" aria-label="Toggle dark mode" title="Toggle dark mode">
    <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z" fill="currentColor"/></svg>
  </button>
  <a class="repo-link" href="{repo}" target="_blank" rel="noopener" aria-label="Source on GitHub" title="Source on GitHub">
    <svg viewBox="0 0 16 16" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
  </a>
</header>
<div class="layout">
  <aside id="sidebar" class="sidebar" aria-label="Book contents">
    <nav>{nav}</nav>
  </aside>
  <div class="scrim" hidden></div>
  <main id="content" class="content">
    <article class="prose">
{part_banner}
{body}
    </article>
    {pager}
    <footer class="footer">
      <p>Assembled from four field books — see <a href="appendix-d.html">Appendix D — Sources and Credits</a>.
      Built from <a href="{repo}" target="_blank" rel="noopener">{repo_short}</a>.</p>
    </footer>
  </main>
  {toc}
</div>
<script src="assets/search-index.js" defer></script>
<script src="assets/site.js" defer></script>
<script src="{mermaid}" defer></script>
</body>
</html>
"""


def write_page(path, *, title, description, body, nav, toc="", part_banner="", pager="", body_class=""):
    path.write_text(TEMPLATE.format(
        title=html.escape(title), description=html.escape(description), body=body, nav=nav, toc=toc,
        part_banner=part_banner, pager=pager, body_class=body_class, site_title=SITE_TITLE,
        subtitle=SUBTITLE, repo=REPO_URL, repo_short=REPO_URL.split("github.com/")[-1], mermaid=MERMAID,
    ), encoding="utf-8")


def main() -> int:
    text = "\n".join(p.read_text(encoding="utf-8").rstrip() + "\n" for p in PARTS)
    if errors := verify(text):
        print("\n".join(errors), file=sys.stderr)
        return 1
    front, pages = split(text)

    # Where does every heading live?
    where: dict[str, str] = {}
    for s in heading_slugs(front):
        where[s] = "index.html"
    for p in pages:
        p["slugs"] = heading_slugs(p["body"]) | heading_slugs(p["part_intro"])
        for s in p["slugs"]:
            where.setdefault(s, p["file"])

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    for f in ASSETS.iterdir():
        shutil.copy(f, OUT / "assets" / f.name)
    (OUT / ".nojekyll").write_text("")

    index_entries = []

    # Title page: drop the markdown TOC list (the sidebar and the contents grid replace it).
    front_md = re.sub(r"## Table of Contents\n.*?\n---\n", "", front, count=1, flags=re.S)
    front_body, _ = render(front_md, heading_slugs(front_md), where)
    contents = ['<section class="contents-grid" aria-label="Contents">']
    part, opened = None, False
    for p in pages:
        if not opened or p["part"] != part:
            if opened:
                contents.append("</ol></div>")
            opened = True
            part = p["part"]
            contents.append(f'<div class="contents-part"><h3>{html.escape(part or "")}</h3><ol>')
        contents.append(f'<li><a href="{p["file"]}"><span class="nav-num">{p["label"].split()[-1]}</span>'
                        f'{html.escape(p["title"])}</a></li>')
    contents.append("</ol></div></section>")
    front_body = front_body.replace("<hr />", "", 1)
    first_h3 = front_body.find("<h3")
    hero_end = front_body.find("</h3>") + len("</h3>") if first_h3 != -1 else 0
    hero = (f'<header class="hero">{front_body[:hero_end]}'
            f'<p class="hero-cta"><a class="btn" href="{pages[0]["file"]}">Start reading →</a>'
            f'<a class="btn btn-ghost" href="chapter-21.html">Jump to the synthesis</a></p></header>')
    front_html = hero + front_body[hero_end:] + '<h2 id="contents">Contents</h2>' + "\n".join(contents)
    write_page(OUT / "index.html", title=f"{SITE_TITLE} — {SUBTITLE}",
               description="Systems thinking, Theory of Constraints and Throughput Accounting for deciding where AI belongs — nine cases from four companies.",
               body=front_html, nav=nav_html(pages, "index.html"), body_class="home")
    index_entries.append({"t": "Title page & contents", "u": "index.html", "s": "", "x": plain(front_html)[:4000]})

    for i, p in enumerate(pages):
        body, tokens = render(p["body"], p["slugs"], where)
        banner = ""
        if p["part_intro"] or (i == 0 or pages[i - 1]["part"] != p["part"]):
            intro_html = render(p["part_intro"], p["slugs"], where)[0] if p["part_intro"] else ""
            banner = (f'<div class="part-banner"><div class="part-kicker">{html.escape(p["part"] or "")}</div>'
                      f'{intro_html}</div>')
        prev_p = pages[i - 1] if i else None
        next_p = pages[i + 1] if i + 1 < len(pages) else None
        pager = '<nav class="pager" aria-label="Chapter navigation">'
        pager += (f'<a class="prev" href="{prev_p["file"]}"><span>← {prev_p["label"]}</span>{html.escape(prev_p["title"])}</a>'
                  if prev_p else '<a class="prev" href="index.html"><span>←</span>Title page</a>')
        if next_p:
            pager += f'<a class="next" href="{next_p["file"]}"><span>{next_p["label"]} →</span>{html.escape(next_p["title"])}</a>'
        pager += "</nav>"
        write_page(OUT / p["file"], title=f'{p["label"]} — {p["title"]} · {SITE_TITLE}',
                   description=f'{p["label"]}: {p["title"]}. {p["part"] or ""}', body=body,
                   nav=nav_html(pages, p["file"]), toc=page_toc(tokens), part_banner=banner, pager=pager)

        # Search index: one entry per h3 section (or the whole page if none).
        sections = re.split(r'(?=<h[23] id=")', body)
        for sec in sections:
            m = re.match(r'<h([23]) id="([^"]+)">(.*?)</h\1>', sec, re.S)
            heading = plain(m.group(3)) if m else p["title"]
            anchor = f'#{m.group(2)}' if m else ""
            index_entries.append({"t": f'{p["label"]} — {p["title"]}', "u": p["file"] + anchor,
                                  "s": heading if m and m.group(1) == "3" else "", "x": plain(sec)[:4000]})

    (OUT / "assets" / "search-index.js").write_text(
        "window.SEARCH_INDEX=" + json.dumps(index_entries, ensure_ascii=False, separators=(",", ":")) + ";",
        encoding="utf-8")

    # 404 page
    write_page(OUT / "404.html", title=f"Not found · {SITE_TITLE}", description="Page not found",
               body='<h1>Page not found</h1><p>That page is not part of the book. <a href="index.html">Back to the contents</a>.</p>',
               nav=nav_html(pages, ""))

    # Sanity: block tags balance on every page (a stray close tag breaks the layout grid).
    unbalanced = []
    for f in OUT.glob("*.html"):
        h = re.sub(r"<pre.*?</pre>", "", f.read_text(encoding="utf-8"), flags=re.S)
        for tag in ("div", "ol", "ul", "nav", "aside", "main", "article", "header", "table"):
            opens, closes = len(re.findall(rf"<{tag}[\s>]", h)), h.count(f"</{tag}>")
            if opens != closes:
                unbalanced.append(f"{f.name}: <{tag}> opened {opens}, closed {closes}")

    # Sanity: every internal link in the generated site resolves.
    ids = {}
    for f in OUT.glob("*.html"):
        ids[f.name] = set(re.findall(r'id="([^"]+)"', f.read_text(encoding="utf-8")))
    broken = []
    for f in OUT.glob("*.html"):
        for target in re.findall(r'href="([^"#:]*\.html)?#([^"]+)"', f.read_text(encoding="utf-8")):
            page, anchor = target[0] or f.name, target[1]
            if anchor not in ids.get(page, set()):
                broken.append(f"{f.name} → {page}#{anchor}")
    print(f"wrote {OUT.relative_to(ROOT)}/: {len(pages) + 2} pages, {len(index_entries)} search entries")
    for b in broken + unbalanced:
        print("BROKEN", b, file=sys.stderr)
    return 1 if broken or unbalanced else 0


if __name__ == "__main__":
    sys.exit(main())
