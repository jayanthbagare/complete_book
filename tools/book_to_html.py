#!/usr/bin/env python3
"""
Convert BOOK.md -> BOOK.html (with Mermaid diagrams) -> BOOK.pdf.

MD->HTML uses python-markdown. Mermaid code fences are rewritten to
<pre class="mermaid"> so mermaid.js (loaded from CDN) renders them in the
browser. The HTML->PDF step is done separately by headless Chrome.

Heading anchors use GitHub's slug rules (shared with build_book.py), so the
book's internal links resolve in the HTML exactly as they do on GitHub.

Usage:
    pip install markdown
    python tools/build_book.py             # assemble BOOK.md first
    python tools/book_to_html.py           # writes BOOK.html next to BOOK.md
    # PDF (headless Chrome/Chromium; virtual-time budget lets Mermaid render):
    chromium --headless --disable-gpu --no-pdf-header-footer \
      --virtual-time-budget=20000 --print-to-pdf=BOOK.pdf BOOK.html
"""
import re
import sys
from pathlib import Path

import markdown

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_book import slugify  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "BOOK.md"
OUT_HTML = ROOT / "BOOK.html"

CSS = """
:root { --ink:#1a1a1a; --muted:#555; --rule:#ddd; --accent:#0b5fff; --code-bg:#f6f8fa; }
* { box-sizing: border-box; }
body {
  font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: var(--ink); line-height: 1.55; max-width: 820px; margin: 0 auto;
  padding: 24px 36px 64px; font-size: 15px;
}
h1, h2, h3, h4 { line-height: 1.25; font-weight: 700; }
h1 { font-size: 2.0rem; margin: 0.2em 0 0.4em; }
h2 { font-size: 1.5rem; margin-top: 1.6em; padding-bottom: .25em; border-bottom: 2px solid var(--rule); page-break-before: always; }
h2:first-of-type { page-break-before: avoid; }
h3 { font-size: 1.18rem; margin-top: 1.4em; color: #111; }
h4 { font-size: 1.02rem; margin-top: 1.2em; }
p, li { font-size: 15px; }
a { color: var(--accent); text-decoration: none; }
blockquote {
  margin: 1em 0; padding: .6em 1em; border-left: 4px solid var(--accent);
  background: #f3f6ff; color: #222; border-radius: 4px;
}
code { background: var(--code-bg); padding: .12em .35em; border-radius: 4px; font-size: .88em;
  font-family: "SF Mono", Menlo, Consolas, monospace; }
pre { background: var(--code-bg); padding: 12px 14px; border-radius: 6px; overflow-x: auto;
  font-size: .82em; line-height: 1.45; page-break-inside: avoid; }
pre code { background: none; padding: 0; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 13.5px;
  page-break-inside: avoid; }
th, td { border: 1px solid var(--rule); padding: 6px 9px; text-align: left; vertical-align: top; }
th { background: #f2f2f2; }
tr:nth-child(even) td { background: #fafafa; }
hr { border: none; border-top: 1px solid var(--rule); margin: 2em 0; }
.mermaid { background: #fff; text-align: center; margin: 1.2em 0; page-break-inside: avoid; }
@page { size: A4; margin: 16mm 14mm; }
"""

HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>{css}</style>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({{ startOnLoad: true, theme: "neutral", securityLevel: "loose",
    flowchart: {{ htmlLabels: true, useMaxWidth: true }} }});
  // Signal for the PDF step: set a flag once all diagrams have rendered.
  window.__mermaidDone = false;
  window.addEventListener("load", async () => {{
    try {{ await mermaid.run(); }} catch (e) {{ console.error(e); }}
    window.__mermaidDone = true;
  }});
</script>
</head>
<body>
{body}
</body>
</html>
"""


def convert() -> Path:
    if not SRC.exists():
        sys.exit(f"ERROR: {SRC} not found")
    text = SRC.read_text(encoding="utf-8")

    # Protect ```mermaid fences: markdown would escape them as code. Swap to a
    # placeholder token, convert the rest, then inject <pre class="mermaid">.
    mermaid_blocks: list[str] = []

    def _stash(m: re.Match) -> str:
        mermaid_blocks.append(m.group(1))
        return f"\n\nMERMAIDPLACEHOLDER{len(mermaid_blocks) - 1}ENDPLACEHOLDER\n\n"

    # Match ```mermaid ... ``` (and 4-backtick wrappers are left alone — they are
    # documentation templates, not diagrams to render).
    text = re.sub(r"```mermaid\n(.*?)\n```", _stash, text, flags=re.S)

    html_body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "toc", "sane_lists", "attr_list"],
        extension_configs={"toc": {"slugify": lambda value, separator: slugify(value)}},
    )

    # Re-inject the mermaid diagrams.
    for i, block in enumerate(mermaid_blocks):
        placeholder = f"MERMAIDPLACEHOLDER{i}ENDPLACEHOLDER"
        # markdown may wrap the placeholder in <p>...</p>; replace both forms.
        pre = f'<pre class="mermaid">\n{block}\n</pre>'
        html_body = html_body.replace(f"<p>{placeholder}</p>", pre)
        html_body = html_body.replace(placeholder, pre)

    title = "From Problem to Agent — The Complete Field Book"
    OUT_HTML.write_text(
        HTML_TEMPLATE.format(title=title, css=CSS, body=html_body), encoding="utf-8"
    )
    print(f"Wrote {OUT_HTML}  ({len(mermaid_blocks)} mermaid diagrams)")
    return OUT_HTML


if __name__ == "__main__":
    convert()
