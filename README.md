# From Problem to Agent — The Complete Field Book

A superset book that merges four "From Problem to Agent" field books into one. Nine cases from four companies are walked through the same arc: **Causal Loop Diagram → Stock & Flow → Theory of Constraints → Throughput Accounting → Automation vs Decision Model vs Agent → Solution Design**. A cross-case synthesis then shows what none of the individual books could.

**Read it:** on the website — **https://jayanthbagare.github.io/complete_book/** — or as a single file, [`BOOK.md`](BOOK.md) (renders on GitHub, including the Mermaid diagrams).

| Part | Company | Cases | Source |
|---|---|---|---|
| I | — | The method, written once | all four |
| II | Danfoss | Supplier Performance Review · 8D Technical Customer Report · UK Customs Clearance | [`jayanthbagare/PBC2.0`](https://github.com/jayanthbagare/PBC2.0) (private) |
| III | Crestmount Refinery | The Planner Bottleneck | [`jayanthbagare/synthetic_oil_gas`](https://github.com/jayanthbagare/synthetic_oil_gas) |
| IV | Meridian Industrial Systems | The Vendor-Pool Collapse (Watchdog · Tactician · Oracle · Front Door) | [`itsbharathp/RFQ_Agent_Workshop`](https://github.com/itsbharathp/RFQ_Agent_Workshop) |
| V | LoopCycle Nusantara | Delivery Monitor · Support Triage · Cart Recovery · Content Planning | [`itsbharathp/LoopCycle`](https://github.com/itsbharathp/LoopCycle) |
| VI | — | Patterns across nine cases · Running it as a workshop | new |

The headline finding of the merged edition: all nine cases were pitched as "AI agents", yet the LLM is the primary value carrier in only **3**, shares the prize in **1**, is a thin final layer in **4**, and doesn't belong in the critical path at all in **1**. See Chapter 21.

## Layout

```
book/                 source chapters, one file per part (edit these)
tools/build_book.py   assembles book/*.md → BOOK.md; checks fences, internal anchors,
                      and (with --loops) classifies every CLD loop as R or B
tools/build_site.py   book/*.md → _site/ (multi-page website: sidebar, search, dark mode, Mermaid)
tools/site_assets/    the website's CSS and JavaScript
tools/book_to_html.py BOOK.md → BOOK.html (Mermaid rendered client-side) → PDF via headless Chrome
.github/workflows/    builds _site/ and deploys it to GitHub Pages on every push to main
BOOK.md               the assembled book (generated; commit it so GitHub renders it)
```

## Build

```bash
python tools/build_book.py            # rebuild BOOK.md and verify (non-zero exit on errors)
python tools/build_book.py --loops    # also print the causal-loop sign check

pip install markdown                  # website and HTML / PDF edition
python tools/build_site.py            # website → _site/
python -m http.server -d _site 8000   # preview at http://localhost:8000

python tools/book_to_html.py
chromium --headless --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=20000 --print-to-pdf=BOOK.pdf BOOK.html
```

## Website

The site is rebuilt and deployed by `.github/workflows/pages.yml` on every push to `main` that touches
`book/` or `tools/`. One-time setup: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
The workflow fails if `BOOK.md` was not rebuilt after editing `book/`.

Corrections and reconciliations against the source books are listed in Appendix C of the book.
