# Appendices

## Appendix A — Glossary

| Term | Meaning |
|---|---|
| **8D** | Eight Disciplines problem-solving process (D1–D8) used in quality management (Danfoss UC-2) |
| **Abstention / confidence-gating** | Accepting a model's answer only above a confidence threshold; below it, the case goes to a human |
| **Agentic (LLM)** | A step that needs open-ended reasoning, synthesis, retrieval orchestration or natural-language generation |
| **Automation** | A step that can be a correct, testable function with no model (lookup, join, rule, sort, maths) |
| **Autoregressive** | Generates a sequence step by step, each step conditioned on the previous ones (how LLMs produce text) |
| **Balancing loop (B)** | A goal-seeking loop with an odd number of `-` signs; resists change |
| **Break-even team** | The *derived* maximum number of developers a prize funds = revenue over horizon ÷ dev cost per dev over horizon |
| **Calibration** | A model's stated probabilities match reality (right ~80% of the time when it says 0.80) |
| **CLD** | Causal Loop Diagram: a signed feedback map of a system |
| **Code-based agent** | Your code drives the agentic loop (e.g. via the Anthropic SDK); auditable, deterministic, testable |
| **Constraint migration** | After elevating the constraint, a *new* step becomes the constraint (ToC Step 5) |
| **Decision model** | A non-generative, encoder-only model that scores fixed options in one forward pass, returning a calibrated probability per option and able to abstain (e.g. Laya, Microsoft-Decision-1) |
| **Delay (`||`)** | A lag in a loop; why vicious loops out-run corrective ones |
| **Encoder-only** | A transformer that keeps the "read/understand" half and omits the text generator |
| **Five Focusing Steps** | Identify → Exploit → Subordinate → Elevate → Repeat |
| **Flow** | A rate that fills or drains a stock (a tap or a drain): the *only* way a stock changes |
| **Foundation forecaster** | A time-series model pre-trained on very large corpora that forecasts zero-shot (e.g. TimesFM in Meridian's Oracle) |
| **GTS / CDS** | SAP Global Trade Services export / CDS supplementary View (Danfoss UC-3 sources) |
| **Leverage point** | (Meadows) A structural place where a small change yields a large change in behaviour: loop gain, delay length, information flow |
| **LLM** | Large Language Model: a generative, autoregressive model (e.g. Claude) |
| **Net (process)** | T − OE; **ΔNet** = ΔT − ΔOE |
| **Non-autoregressive** | Produces its whole output in one forward pass, with no step-by-step loop |
| **Payback** | ΔI ÷ Δ(T − OE), expressed in time |
| **Policy (as a solution class)** | A step whose best fix is a human decision rather than software (e.g. paying vendors on time) |
| **PPM / OTD** | Parts Per Million defects / On-Time Delivery % (Danfoss UC-1 KPIs) |
| **Reinforcing loop (R)** | A self-amplifying loop with an even number of `-` signs; a vicious or virtuous spiral |
| **ROI** | ΔNet ÷ incremental spend |
| **Sensitivity** | Whether the conclusion's *sign* survives a swing in the load-bearing assumption |
| **Skill-based agent** | A Claude Code (or Hermes) skill; the harness drives the loop. Fast iteration, weaker audit trail |
| **Stock** | A quantity that accumulates (a bathtub): open tickets, abandoned carts, willing vendors |
| **System 1 / System 2** | (Kahneman, as used in Meridian) Fast calibrated reflex (decision model) vs slow deliberate reasoning (LLM) |
| **T / I / OE** | Throughput / Investment (Inventory) / Operating Expense, from Goldratt's Throughput Accounting |
| **ToC** | Theory of Constraints: every system has exactly one gating step at a time |
| **Typed choice** | A decision whose valid answers are a fixed, known set of options |
| **ΔT win vs ΔOE win** | Amplifying a scarce resource vs cutting cost; knowledge work usually favours ΔT |

## Appendix B — Artifact Index

### Danfoss — [`jayanthbagare/PBC2.0`](https://github.com/jayanthbagare/PBC2.0) *(private)*

| Case | README | Analysis | Agents / entry points | Offline verification |
|---|---|---|---|---|
| UC-1 SPR | [`uc_1/README.md`](https://github.com/jayanthbagare/PBC2.0/blob/main/usecases/uc_1/README.md) | [`uc_1/analysis/`](https://github.com/jayanthbagare/PBC2.0/tree/main/usecases/uc_1/analysis) | `agent_code_based.py`, `agent_skill_based.py` | `python test_agents.py --category unit` |
| UC-2 8D | [`uc_2/README.md`](https://github.com/jayanthbagare/PBC2.0/blob/main/usecases/uc_2/README.md) | [`uc_2/analysis/`](https://github.com/jayanthbagare/PBC2.0/tree/main/usecases/uc_2/analysis) (incl. `decision-model-architecture.md`) | `agents/complaint_agent.py`, `agents/decision_classifier.py`, `skills/8d-complaint.md` | `pytest tests/`, `decision_classifier.py --benchmark` |
| UC-3 Customs | [`uc_3/README.md`](https://github.com/jayanthbagare/PBC2.0/blob/main/usecases/uc_3/README.md) | [`uc_3/analysis/`](https://github.com/jayanthbagare/PBC2.0/tree/main/usecases/uc_3/analysis) | `agent_code_based.py`, `agent_skill_based.py`, `.claude/skills/customs-clearance/SKILL.md` | `agent_skill_based.py --verify` (29 tests) |
| Method | — | [`.claude/skills/usecase-field-book/SKILL.md`](https://github.com/jayanthbagare/PBC2.0/blob/main/.claude/skills/usecase-field-book/SKILL.md): the reusable skill that generates chapters in this house style and defines the mega-book assembly rules this edition follows | — | — |

Each `analysis/` folder contains `systems-thinking-cld.md`, `systems-thinking-stock-flow.md`, `theory-of-constraints.md` and `throughput-accounting.md`, the full loop-by-loop and line-by-line treatments that the Danfoss chapters summarise.

### Crestmount — [`jayanthbagare/synthetic_oil_gas`](https://github.com/jayanthbagare/synthetic_oil_gas)

| Artifact | Location | Purpose |
|---|---|---|
| Workshop brief | [`README.md`](https://github.com/jayanthbagare/synthetic_oil_gas/blob/main/README.md) | The scene, the task, the evaluation rubric |
| Data generator | [`data_generator/generate_data.py`](https://github.com/jayanthbagare/synthetic_oil_gas/blob/main/data_generator/generate_data.py) | Seed-42 canonical dataset + SQLite DB (14 tables, FK-validated) |
| Agent framework | [`data_generator/agents/`](https://github.com/jayanthbagare/synthetic_oil_gas/tree/main/data_generator/agents) | `TriageAgent`, `ContextGatherer`, `PlannerAssistant`, `Evaluator` |
| Agent runner | [`data_generator/run_agents.py`](https://github.com/jayanthbagare/synthetic_oil_gas/blob/main/data_generator/run_agents.py) | Pipeline + eval report (`output/agent_eval_report.md`) |
| Dashboard | [`data_generator/dashboard/app.py`](https://github.com/jayanthbagare/synthetic_oil_gas/blob/main/data_generator/dashboard/app.py) | Streamlit bottleneck / backlog / cost views |
| Schemas | [`data_generator/output/*_schema.md`](https://github.com/jayanthbagare/synthetic_oil_gas/tree/main/data_generator/output) | Column descriptions |
| Summary | [`data_generator/output/SUMMARY.md`](https://github.com/jayanthbagare/synthetic_oil_gas/blob/main/data_generator/output/SUMMARY.md) | Facilitator sanity-check metrics (*older than the book; see Appendix C*) |

### Meridian — [`itsbharathp/RFQ_Agent_Workshop`](https://github.com/itsbharathp/RFQ_Agent_Workshop)

| Artifact | Location | Purpose |
|---|---|---|
| Dataset | [`output_v2/`](https://github.com/itsbharathp/RFQ_Agent_Workshop/tree/main/output_v2) | 24 CSVs, 18 months |
| Challenges | [`challenges/`](https://github.com/itsbharathp/RFQ_Agent_Workshop/tree/main/challenges) | 6 challenges (01 ToC, 02 Throughput, 03 Watchdog, 04 Tactician, 06 Oracle, 07 Front Door), each with `BRIEFING.md` + `starter.py` |
| Skills | [`skills/`](https://github.com/itsbharathp/RFQ_Agent_Workshop/tree/main/skills) | 9 pre-built Claude skills (`.zip`): orchestrator, vendor selector/finalizer, bid evaluator, email composer/tracker, disruption monitor, tactician planner, vendor watchdog |
| Demos | [`demo/`](https://github.com/itsbharathp/RFQ_Agent_Workshop/tree/main/demo) | Laya routing demos (incidents, vendor risk, compliance, localisation), pipeline flowcharts, `SYSTEM_1_VS_SYSTEM_2.md` |
| Solutions | [`solutions/`](https://github.com/itsbharathp/RFQ_Agent_Workshop/tree/main/solutions) | PDFs for Challenges 1–4; guides + code for 6 and 7 |

### LoopCycle — [`itsbharathp/LoopCycle`](https://github.com/itsbharathp/LoopCycle)

| Case | Datasets | Shipped artifact | Entry point |
|---|---|---|---|
| Ch 17 Delivery | [`hermes-delivery-disruption-monitor/examples/`](https://github.com/itsbharathp/LoopCycle/tree/main/Data/Agent/hermes-delivery-disruption-monitor/examples) (100 orders, answer key, sample findings) | **Hermes skill** (`SKILL.md`) + 4 Python scripts + references | `scripts/load_orders.py` → `assess_orders.py` → `evaluate_against_key.py` |
| Ch 18 Support | [`Data/CallCentre_Ticket_Data/`](https://github.com/itsbharathp/LoopCycle/tree/main/Data/CallCentre_Ticket_Data) (37 tickets, 155 messages, 26 calls) | Design only (pilot plan) | Label → Laya → shadow-run |
| Ch 19 Cart | [`Data/Sales_Data/Abandoned_Carts/`](https://github.com/itsbharathp/LoopCycle/tree/main/Data/Sales_Data/Abandoned_Carts) (1,326 checkouts, 979 conversations, platform funnels) | Design only (staged pilot) | Stage 1 automation → Stage 2 decision model |
| Ch 20 Content | [`Data/Post_Data/`](https://github.com/itsbharathp/LoopCycle/tree/main/Data/Post_Data) + `post_sales_lift.csv` (8) + comments (1,515) | Design only (analytics-first) | `attribution_table()` → `rank_posts()` |
| Context | [`docs/`](https://github.com/itsbharathp/LoopCycle/tree/main/docs), [`Prestentations/`](https://github.com/itsbharathp/LoopCycle/tree/main/Prestentations) | Agent prompt, combined FAQ, data dictionary and strategy decks | — |

## Appendix C — Editor's Notes and Reconciliations

This edition was assembled from the four source `BOOK.md` files following the *mega-book assembly* rules in PBC2.0's `usecase-field-book` skill: shared front matter written once, one chapter per case with consistent `N.1`–`N.8` numbering, and a cross-case synthesis. Changes from the sources are listed here so that every figure stays traceable.

### C.1 Verification performed

| Source | What was checked | Result |
|---|---|---|
| Meridian | Bids/RFQ (m5, m15), T-margin pre/post, actual vs counterfactual T, T lost, vendor arc counts, recomputed from `output_v2/` | **Reproduced exactly** (6.40 / 4.50; 20.0% / 16.4%; $1,622,124; $1,910,780; $288,656 ±$1 rounding; 15/4/3/1/1) |
| LoopCycle | Row counts (2,867 orders, 37 tickets, 1,326 checkouts, 979 conversations, 8 lift events / 972 orders); the Ch 20 snippet run against the data | **Reproduced exactly** |
| LoopCycle | All TA arithmetic in Chapters 17–20 | Consistent, with the exceptions in C.2 |
| Danfoss UC-2 | Book TA table against `uc_2/analysis/throughput-accounting.md` | **Mislabelled net gain**; corrected (C.2) |
| Danfoss UC-1, UC-3 | Internal TA arithmetic (T + I constant, ROI ratios) | Consistent |
| Crestmount | TA arithmetic (A1 × A3 × A4, payback, ROI, break-even) | Consistent. **The dataset could not be regenerated in the editing environment** (numpy unavailable), so the dataset-anchored counts are taken from the source book unverified |
| All | Every Causal Loop Diagram, loop by loop (closed cycles enumerated, minus signs counted) | See C.3 |

### C.2 Corrections and restatements

1. **Danfoss UC-2 net gain.** The source book's TA table showed ΔOE ≈ −€260k and ΔT ≈ +€370k with "Net gain ≈ +€426k". In the underlying model, **€426k is the net gain *excluding* the warranty term** (€161,280 report value + €260,208 OE + €5,184 carry). The full net is **≈ +€797k/yr** (ROI ≈ 28.7×; 9.4× on OE alone). Chapter 10 shows both figures.
2. **Crestmount `SUMMARY.md` is out of date.** The committed facilitator summary (generated 2026-06-30) shows 1,869 open, ~104/wk inflow and $25.8M rolling-12-month downtime cost. The source book (2026-10-14), computed from the live DB, shows 1,866, ~154/wk and $24.1M. This edition uses the book's figures and tells facilitators to verify against the regenerated DB (§22.5).
3. **Crestmount stock labels.** The source Stock & Flow diagram labelled "Open notifications: 1866" and "In-review: 781" as separate stocks, but 1,866 is open *plus* in-review. Relabelled as ~1,085 open + 781 in review.
4. **Crestmount scenario vs data.** The workshop README narrates ~1,900 notifications/week and ~600/week backlog growth. The dataset shows ~154/week. This edition follows the data and flags the difference (Chapter 12).
5. **LoopCycle cart and content ROI.** The source computed ROI as ΔT ÷ ΔOE (~8×, ~16×). Restated with the house formula ΔNet ÷ incremental spend (~7.4×, ~15×); both values are shown.
6. **LoopCycle support sensitivity.** The source said the sign "survives down to ~28% residual breach". Under its own model, the OE saving (≈ 6.9M IDR) keeps Net positive **even with no change in breach rate**, so the restated claim is stronger and simpler.
7. **LoopCycle content concentration.** Added: one post carries 56% of attributed orders (verified from the CSV).
8. **Meridian automation-vs-agentic and break-even** (§15.6) are **new in this edition**, derived only from figures in the source and labelled where modelled ($150k/dev is an editor's assumption). The Meridian constraint migration (§15.4 step 5) is likewise an editor's reading of the Oracle chapter.

### C.3 Causal-loop sign check

Each diagram's closed loops were enumerated and classified by counting minus signs (even → R, odd → B).

| Diagram | Source label | As drawn | Treatment |
|---|---|---|---|
| Meridian | B1 "admin firefighting" | **Reinforcing** (4 minus signs; the source text says 3) | Relabelled **R3** |
| Meridian | B2 "response-rate governor" | Is R1 traced in its virtuous direction (2 minus signs; the source says 1) | Explained: no balancing loop closes; the recovery comes from outside the structure |
| Danfoss UC-2 | B1 closure drains repeats; B2 satisfaction pressure | **Reinforcing** as drawn (both need an omitted edge) | Sign-check note added (§10.2) |
| Danfoss UC-1 | B1 review-controls-risk | Path closes as reinforcing; only the adoption loops (B3) balance | Sign-check note added (§9.2) |
| LoopCycle cart | R2 "confidence erosion" | **Balancing** (1 minus sign) | Relabelled **B3, the confidence ceiling** (a limit to growth) |
| LoopCycle delivery, support | R2/B1/B2 | Open causal chains (no return edge drawn) | Noted in the text as narrative loops / exogenous levers |
| Crestmount, LoopCycle content, Danfoss UC-3 (R1, R2, B2) | — | Match their labels | — |

These are kept as teaching material rather than silently redrawn. §21.6 explains why the pattern ("the brake is the intervention") matters.

### C.4 Things this edition did *not* change

- **Model identifiers** (e.g. `claude-opus-4-8` in Danfoss) are reproduced as in the source code.
- **Company facts** for Danfoss (headcount, H1 2026 sales, workforce split) are as stated in the source book and were not re-verified.
- **Currencies** are not converted. Danfoss is in € (UC-3 in £), Crestmount and Meridian in $, LoopCycle in IDR.
- **Synthetic data.** All four datasets are synthetic. The businesses are fictional (Crestmount, Meridian, LoopCycle) or used as a realistic setting (Danfoss); case-specific people and vendors come from the synthetic datasets.

## Appendix D — Sources and Credits

| Part | Source repository | Owner | Commit used | Visibility |
|---|---|---|---|---|
| II — Danfoss | [`PBC2.0`](https://github.com/jayanthbagare/PBC2.0) — *From Problem to Agent: A Systems-Thinking Field Book* | jayanthbagare | `44b8ba1` | private |
| III — Crestmount | [`synthetic_oil_gas`](https://github.com/jayanthbagare/synthetic_oil_gas) — *The Crestmount Field Book* | jayanthbagare | `abe2ff6` | public |
| IV — Meridian | [`RFQ_Agent_Workshop`](https://github.com/itsbharathp/RFQ_Agent_Workshop) — *The Meridian Industrial Systems Field Book* | itsbharathp | `b2fc751` | public |
| V — LoopCycle | [`LoopCycle`](https://github.com/itsbharathp/LoopCycle) — *The LoopCycle Field Book* | itsbharathp | `666047f` | public |

**Method.** Systems thinking after Donella Meadows (*Thinking in Systems*; leverage points). Theory of Constraints and Throughput Accounting after Eliyahu M. Goldratt (*The Goal*; the Five Focusing Steps). System 1 / System 2 after Daniel Kahneman (*Thinking, Fast and Slow*).

**Models and tools.** **Claude** (Anthropic) drives the LLM agents. **Laya**, the open-weights (Apache-2.0) decision engine used across the decision-model layers, was created by **Nandakishor Mukkunnoth**, Founder & CEO of **ConvAI Innovations** (<https://laya.convaiinnovations.com/>, <https://github.com/NandhaKishorM/laya>). **Microsoft-Decision-1** is a managed decision-model API. **TimesFM** is Google's open time-series foundation model. **Hermes** hosts the LoopCycle delivery skill.

---

*End of the Complete Field Book. Find the constraint, then build at it. And when the constraint moves, go back to [Chapter 3](#chapter-3--the-four-lenses) and begin again.*
