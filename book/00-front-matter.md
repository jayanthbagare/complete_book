# From Problem to Agent — The Complete Field Book

### Systems Thinking, Theory of Constraints and Throughput Accounting for Deciding Where AI Belongs — Nine Cases from Four Companies

*A self-study guide and workshop companion that merges four field books into one: Danfoss (procurement, quality, customs), Crestmount Refinery (maintenance planning), Meridian Industrial Systems (procurement under shock), and LoopCycle Nusantara (consumer commerce).*

---

> **How to read this book.** Every case is walked through the same disciplined arc. First we *understand the system* (Causal Loop Diagram → Stock & Flow). Then we *find where it hurts* (Theory of Constraints). Then we *quantify the prize* (Throughput Accounting). Then we *decide honestly what each step needs*: plain automation, a calibrated decision model, or an LLM agent. Only then do we *design the solution*. The analysis earns the solution. We never start with "let's add an AI agent". When we get there at all, we have already shown that it attacks the constraint.
>
> Part I teaches the method once. Parts II–V apply it to nine cases in four very different businesses. Part VI reads the nine side by side. The cross-case patterns are this book's most valuable finding, and no single source book could show them.

> **A note on the numbers.** Every figure comes from the dataset behind its case and is either *dataset-anchored* or *labelled as a modelled assumption*. Each case keeps its own currency (€, £, $, IDR) and its own period (per year, per month, per window). The cases are **not** converted to a common unit. Compare them by *direction, ratio and sign*, not by absolute size. Where this edition corrects or reconciles a source figure, the change is listed in [Appendix C](#appendix-c--editors-notes-and-reconciliations).

---

## Table of Contents

**Part I — The Method**
- [Chapter 1 — Why This Book Exists](#chapter-1--why-this-book-exists)
- [Chapter 2 — How to Use This Book](#chapter-2--how-to-use-this-book)
- [Chapter 3 — The Four Lenses](#chapter-3--the-four-lenses)
- [Chapter 4 — Automation, Decision Model, or Agent?](#chapter-4--automation-decision-model-or-agent)
- [Chapter 5 — Understanding Decision Models](#chapter-5--understanding-decision-models)
- [Chapter 6 — The Two Agent Patterns](#chapter-6--the-two-agent-patterns)
- [Chapter 7 — Sizing the Build: Break-even and Team Size](#chapter-7--sizing-the-build-break-even-and-team-size)

**Part II — Danfoss: Procurement, Quality and Logistics**
- [Chapter 8 — Meet Danfoss](#chapter-8--meet-danfoss)
- [Chapter 9 — Supplier Performance Review](#chapter-9--supplier-performance-review)
- [Chapter 10 — Faster Technical Customer Report (8D)](#chapter-10--faster-technical-customer-report-8d)
- [Chapter 11 — UK Customs Clearance Declaration](#chapter-11--uk-customs-clearance-declaration)

**Part III — Crestmount Refinery: Maintenance Planning**
- [Chapter 12 — Meet Crestmount Refinery](#chapter-12--meet-crestmount-refinery)
- [Chapter 13 — The Planner Bottleneck](#chapter-13--the-planner-bottleneck)

**Part IV — Meridian Industrial Systems: Procurement Under Shock**
- [Chapter 14 — Meet Meridian Industrial Systems](#chapter-14--meet-meridian-industrial-systems)
- [Chapter 15 — The Vendor-Pool Collapse](#chapter-15--the-vendor-pool-collapse)

**Part V — LoopCycle Nusantara: Consumer Commerce**
- [Chapter 16 — Meet LoopCycle Nusantara](#chapter-16--meet-loopcycle-nusantara)
- [Chapter 17 — The Delivery Disruption Monitor](#chapter-17--the-delivery-disruption-monitor)
- [Chapter 18 — Support Ticket and Contact-Centre Triage](#chapter-18--support-ticket-and-contact-centre-triage)
- [Chapter 19 — Cart and Conversation Recovery](#chapter-19--cart-and-conversation-recovery)
- [Chapter 20 — Content-to-Sales Planning](#chapter-20--content-to-sales-planning)

**Part VI — Synthesis**
- [Chapter 21 — Patterns Across Nine Cases](#chapter-21--patterns-across-nine-cases)
- [Chapter 22 — Running This as a Workshop](#chapter-22--running-this-as-a-workshop)

**Appendices**
- [Appendix A — Glossary](#appendix-a--glossary)
- [Appendix B — Artifact Index](#appendix-b--artifact-index)
- [Appendix C — Editor's Notes and Reconciliations](#appendix-c--editors-notes-and-reconciliations)
- [Appendix D — Sources and Credits](#appendix-d--sources-and-credits)

---

### The nine cases at a glance

| # | Company | Case | Domain | Actual constraint | Honest verdict |
|---|---|---|---|---|---|
| 9 | Danfoss | Supplier Performance Review | Procurement | Judgement-heavy meeting prep | Hybrid, leaning agentic |
| 10 | Danfoss | Technical Customer Report (8D) | Quality | Engineer classification + drafting labour | Hybrid — needs all three model classes |
| 11 | Danfoss | UK Customs Clearance | Logistics | Once-daily batch cadence | **Automation** — no LLM needed |
| 13 | Crestmount | Planner Bottleneck | Maintenance | Planner attention spent on noise and context-gathering | Hybrid, decision-model-heavy |
| 15 | Meridian | Vendor-Pool Collapse | Procurement | Responding / bidding vendor pool | Hybrid — and the top lever is a *policy* |
| 17 | LoopCycle | Delivery Disruption Monitor | Last-mile logistics | Detection latency | Hybrid, agentic nub |
| 18 | LoopCycle | Support Triage | Customer service | Triage latency + accuracy | Decision-model-heavy |
| 19 | LoopCycle | Cart Recovery | E-commerce | Checkout friction + reply latency | Automation-first hybrid |
| 20 | LoopCycle | Content-to-Sales Planning | Marketing | Broken attribution / learning loop | Decision model + measurement, **not** generative |

---
