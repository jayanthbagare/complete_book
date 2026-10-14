# Part I — The Method

## Chapter 1 — Why This Book Exists

Most "AI agent" projects start at the wrong end. Someone decides on the solution ("we need an agent") before anyone has described the problem as a *system*. Hand a team a growing backlog and the instruction "build an agent", and they choose a model, write a prompt, point it at the queue and measure tokens. Three hours later they have a demo and no idea whether it moved anything that matters. The result is an agent that automates a task nobody should have been doing, or that speeds up a step that was never the bottleneck.

This book inverts that order. Before a single line of agent code is justified, you owe four pieces of analysis:

1. **A Causal Loop Diagram (CLD).** What feedback structure makes this problem *persist* despite everyone's effort? Structure, not blame.
2. **A Stock & Flow model.** Where does work pile up, and which *rate* would a solution have to change to drain it?
3. **A Theory of Constraints (ToC) pass.** Which single step limits the whole system's throughput, and where will the constraint *move to* once you relieve it?
4. **A Throughput Accounting (TA) delta.** In money (ΔT, ΔI, ΔOE), what is the prize for elevating that constraint? Does the *sign* of the conclusion survive a sensible swing in the shakiest assumption?

Only after those four may a solution appear on the page. When it does, it is broken down honestly into three layers: **deterministic automation** (plain code), **decision models** (typed choices with calibrated confidence and the right to abstain), and **deep agents** (the reasoning and generation that only an LLM can do). The agent is never the hero of the story; the *constraint* is. Sometimes the agent is the most leverage-efficient way to elevate the constraint. Surprisingly often, it is not.

The source field books proved this four times over, in four different businesses. Read side by side, the nine cases produce the most useful sentence an AI practitioner can say, more than once: *"This part doesn't need AI."*

> If you take one idea from this book, take this one: **analysis is not overhead before the "real" engineering. Analysis tells you whether the engineering is worth doing at all, and where to point it.**

---

## Chapter 2 — How to Use This Book

This book serves two audiences with the same material.

### 2.1 As a self-study guide

Read Part I once. Then work the cases. Each case chapter starts with the raw problem and its dataset counts. **Before reading past §.1 (The Problem), try the four lenses yourself.** Compare your constraint and your automation/agentic verdict with the book's. The gap is the lesson.

For each case:

1. **Read the problem framing and resist the urge to design a solution.** Sit with the pain.
2. **Trace the CLD by hand.** Pick any variable, follow an arrow, and ask "and then what?" until you return to where you started. Say out loud whether each loop is vicious or virtuous.
3. **Redraw the Stock & Flow from memory.** If you can name the stocks and the rates that fill and drain them, you understand the system.
4. **Do the Five Focusing Steps yourself** before reading the chapter's answer. Guess the constraint. You will often be wrong in an instructive way, because the obvious bottleneck is frequently not the real one.
5. **Challenge the Throughput Accounting assumptions.** Every number is labelled as an assumption on purpose. Change one and see whether the conclusion survives.
6. **Fill the automation / decision / agentic scorecard** before reading §.6.
7. **Finally, run the artifact.** Most cases end with runnable commands; a few end with a pilot plan.

**Suggested reading order.** The cases are grouped by company, but they are not equally hard. A good learning path runs from the most intuitive constraint to the subtlest:

| Step | Case | Why here |
|---|---|---|
| 1 | [Ch 9 — Supplier Performance Review](#chapter-9--supplier-performance-review) | Most intuitive constraint: scarce human prep capacity |
| 2 | [Ch 13 — The Planner Bottleneck](#chapter-13--the-planner-bottleneck) | Capacity is 8× demand, yet the backlog grows. Nameplate ≠ effective |
| 3 | [Ch 11 — UK Customs Clearance](#chapter-11--uk-customs-clearance-declaration) | The constraint is a *cadence*, and the honest answer is "no LLM" |
| 4 | [Ch 18 — Support Triage](#chapter-18--support-ticket-and-contact-centre-triage) | A decision-model problem dressed up as an agent |
| 5 | [Ch 19 — Cart Recovery](#chapter-19--cart-and-conversation-recovery) | Half the prize is UX plumbing |
| 6 | [Ch 10 — Technical Customer Report (8D)](#chapter-10--faster-technical-customer-report-8d) | Needs all three model classes |
| 7 | [Ch 17 — Delivery Disruption Monitor](#chapter-17--the-delivery-disruption-monitor) | The one case where the LLM carries the prize |
| 8 | [Ch 15 — The Vendor-Pool Collapse](#chapter-15--the-vendor-pool-collapse) | A cascade: the shock enters in one place and the pain surfaces in another |
| 9 | [Ch 20 — Content-to-Sales Planning](#chapter-20--content-to-sales-planning) | Thinnest data, shakiest sign — an exercise in honesty |

### 2.2 As an in-classroom workshop

Every case is built to run as a group exercise. The golden rule is: **withhold the diagrams.** Participants must struggle to produce their own CLD before seeing the book's. Run-sheets, formats from a two-hour executive session to a three-day cohort, discussion prompts and per-repository pre-flight checklists are in [Chapter 22](#chapter-22--running-this-as-a-workshop).

### 2.3 Prerequisites

- No prior systems-thinking background. [Chapter 3](#chapter-3--the-four-lenses) teaches the lenses from scratch.
- For the runnable sections: Python 3.10+ (3.11+ for most cases), plus `pip install anthropic pytest pandas`. Some cases need extra packages; see [Appendix B](#appendix-b--artifact-index).
- An `ANTHROPIC_API_KEY` is needed only to *run* the LLM agents. All analysis, data generation and unit tests work without it.
- A Markdown viewer that renders [Mermaid](https://mermaid.js.org/) diagrams (GitHub renders them natively).

---

## Chapter 3 — The Four Lenses

Four tools are applied in a fixed order. Each answers a different question, and each sets up the next.

### 3.1 Causal Loop Diagram — *"Why does this persist?"*

A CLD is a picture of **feedback**. Variables are nodes, and the arrows between them are causal links signed `+` or `-`:

- `+` : cause and effect move **in the same direction** (more → more, or less → less).
- `-` : cause and effect move **in opposite directions** (more → less).

Trace any closed loop and **count the minus signs**:

- an **even** number (including zero) → a **reinforcing loop (R)**, a virtuous or vicious spiral that amplifies itself;
- an **odd** number → a **balancing loop (B)**, a goal-seeking loop that resists change.

The art is reading *which loops dominate and why*. Almost every stuck business process is a case of fast reinforcing loops out-running slow balancing loops. **Delays** (written `||`) are therefore first-class citizens in a CLD: a correcting loop that acts "eventually" loses to a vicious loop that acts "now". In this book's nine cases, the decisive delay appears again and again: a health score that lags late payments by a quarter, a disruption that reaches the operator only through a customer complaint, a critical notification that fails weeks after it aged.

**Leverage points** (after Donella Meadows) are places where a small change in structure produces a large change in behaviour. Usually that means changing a *loop's gain*, *shortening a delay*, or changing *who sees what information when*, rather than pushing harder on a variable.

### 3.2 Stock & Flow — *"Where does work pile up?"*

A CLD shows causality but hides accumulation. A Stock & Flow diagram makes accumulation explicit:

- A **stock** is a quantity that accumulates, like a bathtub: open complaints, unreviewed suppliers, abandoned carts, willing vendors.
- A **flow** is a rate that fills or drains a stock, like a tap or a drain: classification rate, review rate, detection rate.

The single most important fact about stocks: **a stock can only be changed by its flows.** You cannot "will" a backlog down. You can only raise its drain rate or lower its fill rate. That is why the question that matters is *"which rate does the solution change?"*. A solution that doesn't move a flow rate doesn't move a stock, and a solution that doesn't move a stock hasn't changed the system. (Meridian, [Chapter 15](#chapter-15--the-vendor-pool-collapse), gives the cleanest proof: the team's response, more invitations, moved *no* flow on any stock that mattered.)

### 3.3 Theory of Constraints — *"What limits the whole system?"*

Goldratt's insight is that every system has exactly **one** constraint at a time: the step that gates total throughput. Improving anything that is *not* the constraint is a mirage. It creates local efficiency and global inventory. ToC proceeds through the **Five Focusing Steps**:

1. **Identify** the constraint, the step with the least capacity relative to demand. Beware the obvious step: the loud bottleneck is often a symptom of a quiet one upstream.
2. **Exploit** it. Get maximum throughput from it without spending money; stop starving or wasting it.
3. **Subordinate** everything else to it, so the rest of the system works at the constraint's pace.
4. **Elevate** it. Now invest to raise its capacity. This is usually where automation, a model, or an agent enters.
5. **Repeat.** Once elevated, the constraint *moves*. Go back to step 1. Watching where it moves is often the most valuable output of the whole analysis.

### 3.4 Throughput Accounting — *"What is the prize, in money?"*

TA is Goldratt's replacement for cost accounting. It has three measures:

| Term | Factory meaning | Knowledge-work meaning (as used here) |
|---|---|---|
| **T — Throughput** | Rate money is generated through sales (revenue − truly variable cost) | Rate of value created by *finished* units of work (reviews done on time, complaints closed, shipments cleared, criticals processed in time) and the cost that value avoids |
| **I — Investment / Inventory** | Money tied up in stock and assets | Work-in-process tied up in the system (backlogs, unmitigated risk, carts parked, cash stuck in late payments), or the one-time build investment |
| **OE — Operating Expense** | Money spent turning I into T | Cost of running the process: loaded labour hours + tooling + API cost |

The decision rule is brutally simple: a change is good if it **increases T, decreases I, or decreases OE**, in that order of priority. Every case computes:

```
Net Profit (process P&L) = T − OE
ΔNet = ΔT − ΔOE
ROI  = ΔNet ÷ incremental spend
Payback = ΔI ÷ Δ(T − OE)          (when there is a one-time investment)
```

Every case also lists its assumptions in a numbered table (A1, A2, …), each with a value and a basis (*dataset* or *modelled*). Each case ends with a **sensitivity note**: which assumption is load-bearing, and does the *sign* of the conclusion survive a sensible swing in it?

> **The recurring lesson.** In knowledge work, the win almost always shows up in **ΔT**, not ΔOE. The solution rarely makes the process *cheaper*. It makes the same scarce people *produce more finished, valuable work*. Selling it as a cost-cutter is usually selling it short. When the win *is* pure OE, from repetitive consolidation, that is a strong hint the step is **automation**, not an agent. ([Chapter 21](#chapter-21--patterns-across-nine-cases) shows this held in all nine cases.)

> **Illustrative, not decision-grade.** Every euro, pound, dollar and rupiah in this book is an estimate built on explicitly labelled assumptions and grounded in each dataset's real structural counts. Treat direction and order of magnitude as the signal. A production business case must replace the assumptions with measured values from a pilot.

---

## Chapter 4 — Automation, Decision Model, or Agent?

The four lenses tell you *where* to act. This chapter tells you *with what*. Every case in this book was shipped, or pitched, as "an AI agent". That word hides an important truth: **not every step that is built as an agent needs to be one.**

### 4.1 The three-way test

For **every step** in a process, ask in order:

| Class | The test | Typical steps |
|---|---|---|
| **Automation** | Could it be a correct, *testable function* with no model? | Lookups, joins, boolean rule checks, fixed mappings, deterministic sorts, business-day maths |
| **Decision model** | Is it a *typed choice* over fixed options (or yes/no, or a rating) where you want **calibrated confidence** and the ability to **abstain**? | Classify, prioritise, route, severity 1–5, real-vs-false-positive |
| **Agentic (LLM)** | Does it need open-ended reasoning, synthesis, retrieval orchestration, or natural-language *generation*? | Drafting reports and emails, researching the open web, planning under a goal, explaining a root cause |

Two further classes appear in this book. Recognising them is part of the discipline:

- **Specialist foundation models.** Meridian's Oracle uses Google TimesFM, a time-series foundation model that forecasts zero-shot. It is neither an LLM nor a decision model. It handles *the knowable*, and it is blind to exogenous shocks ([§15.7](#157-solution-design--the-four-agents)).
- **Policy (no software at all).** Meridian's single highest-leverage intervention is *paying vendors on time*. Crestmount's first move is *rejection discipline*. LoopCycle's biggest cart win is *showing the shipping cost earlier*. Sometimes the right "AI strategy" for a step is a decision by a manager.

### 4.2 The effort-decision table

Pair each step's **nature** with its **throughput contribution** (from the TA lens) and its **build effort**. That turns a classification exercise into an investment decision: build what moves the money, skip what doesn't.

```
Step | Nature | Throughput contribution | Build effort | Build priority
```

The rule for build order, applied in every case:

1. **First, do the cheap enabling automation.** It is low effort and usually a prerequisite, even when it carries little ΔT directly.
2. **Put real effort into the row where the money and the irreducible model class coincide.** That might be the decision model, the generative nub, or, as in UC-3, neither.
3. **Be willing to conclude "this does not need an LLM at all".** Say so even when the deliverable is marketed as an agent.

### 4.3 Match the model class to the sub-problem

> **Typed choice → decision model. Generation or open-ended reasoning → LLM. Everything else → code.** Don't make one generative model do a scorer's job or a function's job.

The architecture that emerges again and again in Parts II–V has three layers: **an automation core**, sometimes **a decision-model front end**, and **a small, irreducibly agentic nub**, with a **human at the gate** for anything irreversible. *Decompose before you deploy.*

---

## Chapter 5 — Understanding Decision Models

So far the only AI discussed has been a **generative large language model** (LLM) such as Claude driving an agentic loop. But not every step needs a model that *writes*. Some steps need a model that *decides*. This chapter introduces that less famous class of model from first principles. Seven of the nine cases use one, and knowing when *not* to reach for an LLM is part of the same "match the tool to the problem" discipline.

### 5.1 Two ways a model can answer a question

Imagine a customer complaint arrives and you must decide: is this a brand-new issue, or a repeat of a known one?

**Way 1 — generate the answer as text (what an LLM does).** The model produces its answer one token (word-piece) at a time, left to right, with each token conditioned on the ones before it. This is **autoregressive generation**. It is astonishingly flexible, but it has three costs:

- **Latency.** Answering means generating a sequence token by token, and you pay for every token.
- **Parsing.** The answer is *prose*. To get a clean label, you must fish it back out of the text. That is brittle; it was exactly the weakness of UC-2's original agent.
- **Uncalibrated confidence.** The model can say "REPEAT" fluently and be completely wrong, with no honest signal of its own uncertainty.

**Way 2 — score the fixed options directly (what a decision model does).** If the only valid answers are SINGLE, MASTER, REPEAT and CA_FAILURE, you don't need generation. A decision model reads the input **once**, in a single forward pass, and outputs a **probability for each predefined option**:

```
SINGLE     0.04
MASTER     0.07
REPEAT     0.86   ← the answer
CA_FAILURE 0.03
```

This is a **typed choice**. The answer's *type* (one of four fixed labels) is set in advance, and the model's whole job is to put a calibrated probability on each option.

### 5.2 System 1 and System 2

The Meridian field book frames the same split in Kahneman's terms. It is a useful architectural vocabulary:

- **System 2, the deliberate analyst.** Large generative models such as Claude. They reason step by step, call tools, synthesise nuance and write prose. They are powerful but *slow and expensive*: 500 ms to several seconds per call, metered per token, and capable of hallucinating confidence they haven't earned. Use them for real reasoning: diagnosis, planning, negotiation, drafting.
- **System 1, the fast reflex.** Non-autoregressive decision engines built on bidirectional encoders, such as Laya. They don't *generate*. They place an input on a rubric and return calibrated probabilities in **tens of milliseconds** (Laya is quoted at ~33 ms) at very low cost. Because the output space is restricted to the predefined options, they cannot hallucinate free text. Use them for high-volume routing, scoring and triage.

The anti-pattern is a reflex dressed up as a deliberation: using a System 2 LLM to decide whether an email is spam. The robust architecture uses **System 1 to protect and orchestrate System 2**. The fast layer triages everything in milliseconds and forwards only the critical few to the slow, expensive reasoning layer.

### 5.3 What "encoder-only" and "non-autoregressive" mean

- **Non-autoregressive.** The model produces its whole output in one shot: one pass in, a probability vector out. That is why it is fast.
- **Encoder-only.** Transformers historically have an *encoder* that reads text into a rich internal representation and a *decoder* that generates text from it. LLMs are decoder-heavy, built to generate. Decision models keep only the "read and understand" half and add a small scoring head. They understand the input deeply but cannot write an essay, which is fine, because we only want them to *choose*. The encoders behind the models used here are in the BERT family: a few hundred million parameters, versus tens or hundreds of billions in a frontier LLM.

### 5.4 Calibration — the property that actually matters

A model is **calibrated** if its stated probabilities match reality. When it says "0.80" on a batch of cases, it is right about 80% of the time. A calibrated probability is an honest confidence signal you can set a policy on. Good decision models are trained against *proper scoring rules*, which reward honest probabilities and punish both over- and under-confidence.

### 5.5 Abstention — knowing when not to answer

Calibration unlocks the feature that makes decision models useful in a workflow: **abstention via confidence-gating**.

```
if top_probability >= threshold:   accept the model's answer   (AUTO)
else:                              route this one to a human    (ABSTAIN)
```

Instead of a system that is silently wrong on hard cases, you get one that is **right on the easy ones and honest about the hard ones**. Raising the threshold sends more cases to humans and makes the automated decisions safer. It is a dial you tune to your quality bar. In Crestmount ([Chapter 13](#chapter-13--the-planner-bottleneck)), abstention is *mandatory*: an over-confident rejection of a real failure near a tier-1 asset is the costliest error in the system.

### 5.6 Three primitives

The Laya engine exposes three question types that cover almost every typed decision in this book:

| Primitive | Returns | Used for |
|---|---|---|
| **`choice`** | One option from a dictionary (semantic routing) | Ticket category, email queue, 8D class, abandonment reason |
| **`score`** | Expected value on an ordinal rubric (e.g. 0–5) | Urgency "panic meter", severity 1–5, priority |
| **`noul`** | Calibrated P(true) for a direct boolean question | "Is this a false positive?", "Is this a duplicate?" |

A score of `4.2` from a `score` call is not an LLM guessing "sounds urgent". It is the expected value of the probability distribution the engine places over the rubric. That is the escape from the notoriously inconsistent "rate this 1–10" prompt. Because encoders read meaning, not keywords, multilingual routing comes almost for free ([§15.7](#157-solution-design--the-four-agents)).

### 5.7 Decision model vs LLM — side by side

| | **Decision model** (encoder-only, System 1) | **LLM** (generative, System 2) |
|---|---|---|
| How it answers | Scores fixed options in one forward pass | Generates text token by token |
| Output | Calibrated probability per option | Free-form text (+ tool calls) |
| Speed | ~tens of milliseconds | One or more full turns (seconds) |
| Confidence | Calibrated, actionable | None you should trust |
| Can abstain? | Yes — core feature | Not natively |
| Great at | Typed choice, yes/no, rating, rubric scoring | Reasoning, retrieval, long-form writing, planning |
| Cannot | Write a report or reason open-endedly | Classify cheaply with honest confidence |

They are **complements, not competitors**.

### 5.8 Two decision models you can actually use

- **Laya** (<https://github.com/NandhaKishorM/laya>, <https://laya.convaiinnovations.com/>): open-weights (Apache-2.0), **self-hosted**, encoder-only, calibrated. You run it on your own hardware, so sensitive data never leaves your environment. Right for complaint data, refinery data, masked customer PII and picker payment disputes.
- **Microsoft-Decision-1** (<https://commandline.microsoft.com/microsoft-decision-1-model-foundry/>): a **managed API** (via Microsoft Foundry and OpenRouter) built for structured decision tasks. It is priced per input token and needs no infrastructure, but your data goes to an external service.

The choice is the familiar self-hosted vs managed trade-off: **data residency and cost control** versus **zero-ops convenience**.

### 5.9 When to reach for a decision model

Use one for a step when **all** of these hold:

1. The answer is **one of a known, fixed set of options**, a yes/no, or a rating, not open-ended text.
2. You want a **calibrated confidence**, usually so you can **abstain or escalate** on hard cases.
3. The step is **high-volume or latency-sensitive**, so paying for LLM generation per item is wasteful.

If any of those fails, keep the LLM. Very often the best design uses **both**: a decision model as a fast, calibrated front end for the classification step, with an LLM behind it for the generative work. UC-2 ([Chapter 10](#chapter-10--faster-technical-customer-report-8d)) builds exactly that, end to end, benchmarked against ground truth.

---

## Chapter 6 — The Two Agent Patterns

When a step does need an LLM, there are two ways to build the loop. The choice is a **governance** decision, not a technical one.

### 6.1 Code-based agent — *you* drive the loop

Your code owns the agentic loop and calls `client.messages.create()` directly. The model decides *which* tool to call. Your code decides *when to stop*, *what to log*, and *where the approval gates are*.

```
User prompt
   ↓
Python: client.messages.create(messages, tools)
   ↓
Claude: returns tool_use block(s)
   ↓
Python: execute each tool, append tool_result
   ↓ (loop until stop_reason == "end_turn")
Claude: final text answer
```

**Best for:** full control, custom approval gates, audit logging and deterministic orchestration. Pick it when actions are irreversible, regulated, safety-relevant, or customer-facing. **Cost:** you maintain the loop.

### 6.2 Skill-based agent — the *harness* drives the loop

A Claude Code **skill** (a Markdown `SKILL.md`, sometimes with a thin tool server) exposes the tools, and the harness drives the loop. You add capability by writing a skill or registering a tool, not by touching orchestration code.

**Best for:** rapid iteration, exploration, internal-facing synthesis, and letting non-engineers invoke a workflow by name. **Cost:** weaker audit trails and less deterministic behaviour.

The cases show several flavours of "skill-based":

| Case | Flavour | Mechanism |
|---|---|---|
| Danfoss UC-1 | **SkillRegistry** | A `Skill` wraps a callable + JSON schema; `SkillRegistry.dispatch()` routes. Adding a capability means registering one function. |
| Danfoss UC-2 | **Declarative spec** | `8d-complaint.md` describes a decision-tree procedure that Claude Code follows by reading the JSON directly. There is no running loop. |
| Danfoss UC-3 | **Tool server** | `SKILL.md` + a stdin/stdout JSON tool server decouples the skill from the Python backend; a `--verify` harness proves correctness before deployment. |
| Meridian | **Packaged skills** | Nine pre-built skills (orchestrator, vendor selector, bid evaluator, email composer, disruption monitor, …) ship as `.zip` bundles. |
| LoopCycle delivery | **Hermes skill + scripts** | A skill-based web-research loop wrapped by deterministic Python scripts and a human approval gate. |

### 6.3 The decision you're really making

Code-based vs skill-based is not "advanced vs beginner". It is **where you want the loop to live**: in your code (control, auditability) or in the harness (speed, extensibility). The rule that emerges across all nine cases:

> **Skill-based where exploration or iteration is the point and a human reviews before anything has consequences. Code-based the moment an action is irreversible, regulated, or lands directly on a customer or a plant.**

The architecture comes *after* the problem, not before it.

---

## Chapter 7 — Sizing the Build: Break-even and Team Size

The automation-vs-agentic verdict has a direct headcount consequence: the cheaper the build (more automation, less bespoke agent), the smaller the team needed to break even. Every case therefore closes its effort decision with a **break-even / team-sizing** block, so the decision is expressed in developers and not just in adjectives.

### 7.1 The formula

Take four inputs, either sourced or clearly *labelled as assumptions*: **ARR per customer, customer count, time horizon, developer fully-loaded cost.**

```
Dev cost over horizon (1 dev) = loaded_cost × horizon_years × 1.10 (run/API uplift)
Revenue over horizon          = customers × ARR × revenue_years
                                (revenue_years ≈ horizon_years at full ramp;
                                 ≈ horizon_years × 2/3 conservative / staggered)
Max break-even team           = Revenue ÷ Dev-cost-per-dev
```

Then compare the max break-even team with the **build effort implied by the layers**. Automation is cheap (weeks). An *adopted* decision model is part-time work: labelling and threshold tuning on an off-the-shelf backend. The agentic nub is the main cost. The verdict reads: *"clears break-even at N developers."*

### 7.2 Three rules

1. **Team size is derived, never asserted.** If you can't show the formula, you don't have a team size.
2. **Give both readings,** conservative (staggered revenue) and full-ramp.
3. **Price and customer count move break-even far more than headcount does.** Build-once-reuse means sizing belongs at the *portfolio* level, across use cases and customers, not per use case.

### 7.3 Three economic frames you will meet

The same formula gives very different answers depending on *who is paying*:

| Frame | Seen in | Typical verdict |
|---|---|---|
| **Product vendor**: sell the solution to several customers | Danfoss (€35k ARR × 5, 18 mo), Crestmount ($150k ARR × 8, 3 yr) | Clears at 1–2.5 devs with margin |
| **Single internal tenant**: an SME funds the build from its own prize | LoopCycle (prize of $1.9k–$7.9k/yr per case) | Doesn't fund a developer alone; clears only as a portfolio or a reusable product |
| **Remediation ceiling**: the prize caps total spend on the fix | Meridian (~$303k break-even budget) | Most of the budget goes to *policy* (on-time payment), not software |

[§21.8](#218-break-even-across-the-portfolio) compares all nine cases on these frames.

---
