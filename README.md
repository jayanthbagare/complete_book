# From Problem to Agent — The Complete Field Book

A superset book that merges four "From Problem to Agent" field books into one. Nine cases from four companies are walked through the same arc: **Causal Loop Diagram → Stock & Flow → Theory of Constraints → Throughput Accounting → Automation vs Decision Model vs Agent → Solution Design**. A cross-case synthesis then shows what none of the individual books could.

**Read it:** [`BOOK.md`](BOOK.md) (renders on GitHub, including the Mermaid diagrams).

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
tools/book_to_html.py BOOK.md → BOOK.html (Mermaid rendered client-side) → PDF via headless Chrome
BOOK.md               the assembled book (generated; commit it so GitHub renders it)
```

## Build

```bash
python tools/build_book.py            # rebuild BOOK.md and verify (non-zero exit on errors)
python tools/build_book.py --loops    # also print the causal-loop sign check

pip install markdown                  # optional: HTML / PDF edition
python tools/book_to_html.py
chromium --headless --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=20000 --print-to-pdf=BOOK.pdf BOOK.html
```

Corrections and reconciliations against the source books are listed in Appendix C of the book.
