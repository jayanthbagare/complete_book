#!/usr/bin/env python3
"""
Assemble book/*.md -> BOOK.md and verify it.

Checks:
  * code fences are balanced and every ```mermaid block is closed
  * every internal link (#anchor) resolves to a heading, using GitHub's slug rules
    (headings inside code fences are ignored)
  * --loops: enumerate every Causal Loop Diagram's closed loops and classify each
    as reinforcing (even number of '-' edges) or balancing (odd)

Usage:
    python tools/build_book.py            # build + verify, non-zero exit on errors
    python tools/build_book.py --loops    # also print the CLD loop sign check
"""
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARTS = sorted((ROOT / "book").glob("*.md"))
OUT = ROOT / "BOOK.md"

FENCE = re.compile(r"^\s*```")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
LINK = re.compile(r"\]\(#([^)\s]+)\)")
EDGE = re.compile(r"^\s*(\w+)(?:[\[\(\{][^\]\)\}]*[\]\)\}]+)?\s*-->\|\s*([+-])\s*\|\s*(\w+)", re.M)


def slugify(text: str) -> str:
    """GitHub-style heading anchor."""
    text = re.sub(r"`([^`]*)`", r"\1", text)            # inline code keeps its text
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links keep their label
    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def scan(lines):
    """Yield (lineno, line, in_fence, fence_lang) for every line."""
    in_fence, lang = False, ""
    for n, line in enumerate(lines, 1):
        if FENCE.match(line):
            if not in_fence:
                in_fence, lang = True, line.strip()[3:].strip()
            else:
                in_fence, lang = False, ""
            yield n, line, None, lang
            continue
        yield n, line, in_fence, lang


def verify(text: str) -> list[str]:
    errors = []
    lines = text.splitlines()
    slugs, seen = set(), Counter()
    links = []
    open_fence_at = None
    for n, line, in_fence, _ in scan(lines):
        if in_fence is None:                       # a fence line toggles state
            open_fence_at = None if open_fence_at else n
            continue
        if in_fence:
            continue
        m = HEADING.match(line)
        if m:
            s = slugify(m.group(2))
            slugs.add(s if not seen[s] else f"{s}-{seen[s]}")
            seen[s] += 1
        links += [(n, a) for a in LINK.findall(line)]
    if open_fence_at:
        errors.append(f"unclosed code fence opened at line {open_fence_at}")
    for n, anchor in links:
        if anchor not in slugs:
            errors.append(f"line {n}: broken anchor #{anchor}")
    return errors


def loop_report(text: str) -> list[str]:
    out = []
    for i, block in enumerate(re.findall(r"```mermaid\n(.*?)```", text, re.S)):
        edges = EDGE.findall(block)
        if not edges:
            continue
        adj = {}
        for a, sign, b in edges:
            adj.setdefault(a, []).append((b, sign))
        nodes = sorted({a for a, _, _ in edges} | {b for _, _, b in edges})
        rank = {v: k for k, v in enumerate(nodes)}
        cycles = []

        def dfs(start, v, path, signs):
            for w, s in adj.get(v, []):
                if w == start:
                    cycles.append((path, signs + [s]))
                elif rank[w] > rank[start] and w not in path:
                    dfs(start, w, path + [w], signs + [s])

        for v in nodes:
            dfs(v, v, [v], [])
        first = block.strip().splitlines()[1].strip() if block.count("\n") > 1 else ""
        out.append(f"diagram {i} ({len(edges)} signed edges; starts '{first[:40]}'): {len(cycles)} closed loops")
        for path, signs in cycles:
            minus = signs.count("-")
            kind = "R" if minus % 2 == 0 else "B"
            out.append(f"    {kind} ({minus} minus) " + " -> ".join(path + [path[0]]))
    return out


def main() -> int:
    if not PARTS:
        print("no parts found under book/", file=sys.stderr)
        return 1
    text = "\n".join(p.read_text(encoding="utf-8").rstrip() + "\n" for p in PARTS)
    OUT.write_text(text, encoding="utf-8")
    errors = verify(text)
    mermaid = len(re.findall(r"^\s*```mermaid", text, re.M))
    print(f"wrote {OUT.relative_to(ROOT)}: {len(PARTS)} parts, {len(text.splitlines())} lines, "
          f"{len(text.split())} words, {mermaid} mermaid diagrams")
    if "--loops" in sys.argv:
        print("\n".join(loop_report(text)))
    for e in errors:
        print("ERROR", e, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
