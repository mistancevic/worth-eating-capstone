# Design

Run with the Design Companion v0.2, in `design-companion/`.

## The start prompt

From the course page, not the zip:

```text
I am starting the Design phase of my Agentic AI Capstone.

Read START_HERE.md, AGENTS.md, and 02_DESIGN.md.

First ask me to paste my completed Discovery PRD answers. If any are missing or vague, help me fix them quickly before we continue.

This is my own project. Do not recommend Northstar Home as my project. Northstar Home is only an example.

Ask me one question at a time. Grill me until my agent has a clear role, target workflow, loop, context plan, tools, memory decision, output format, escalation rules, human approval point, and five eval cases.

Then help me write self-contained Design PRD answers for:
1. Agent role
2. Target workflow
3. Agent loop
4. Inputs and context
5. Tools or simulated tools
6. Memory decision
7. Output format
8. Escalation rules
9. Human approval point
10. Initial eval plan

After the Design PRD answers are complete, stop and tell me not to move to Develop yet.
```

## How this runs

From `AGENTS.md`. One question at a time. After each answer: assess it, say how
to improve it, ask the next. Nothing gets built — Design happens on paper.

Grill on: a fuzzy role that needs a paragraph · context with no named files ·
tools the loop does not need · memory chosen by default rather than by decision
· output as a wall of chat instead of labeled fields · missing escalation
triggers · a gate placed after the consequence · eval cases that could never
fail.

## Step 0 · Discovery answers

Complete, in [`discovery-prd.md`](discovery-prd.md). Nothing sent back for
rework.

Two weaknesses were flagged by [`review-rubric.md`](review-rubric.md), and both
land inside Design rather than needing a Discovery rewrite:

- Nobody has recorded **who decided Tom is safe to receive this**. Belongs in
  Step 9, the approval point.
- The **no-room wording** has no eval case of its own. Belongs in Step 10.

Both are carried forward deliberately. Neither is a reason to reopen Discovery.

---

# Answers

## 1 · Agent role

> **The agent is hired to name what to add to a late meal so Tom reaches his
> coach's protein target, within the coach's numbers and a rule that it may only
> ever add food, escalating when the message is not about food, when the day's
> intake is far below target, or when it is not confident.**

Settled 2026-08-20. 46 words, one sentence.

**Two phrases carry the design.**

*"name what to add"* — not *decide what to eat*. The food is already in front of
him. Anything wider re-opens meal planning, which Discovery ruled out.

*"may only ever add food"* — the one boundary that has to sit in the role
statement rather than in the escalation rules. Everything else here is behaviour
that can drift under a bad prompt. This one is structural: if the only shape the
output can take is an addition, restriction is not reachable.

**Deliberately left out:** *never diagnose* and *never push*. Both real, neither
is what the agent *is*. They belong to Steps 7 and 8.

## 2 · Target workflow

The same evening, with the agent in it.

1. Tom opens the fridge, hungry. He opens the app instead of reaching for the
   bread.
2. He types what he ate today, in his own words.
3. He types what is in the fridge.
4. The agent works out where he stands against the coach's target and how much
   room is left in the day, and shows that arithmetic.
5. The agent names one thing from what he actually has that closes the gap and
   still fits the calories left — or says there is nothing to add tonight, and
   why.
6. Tom accepts it, swaps it, or ignores it.
7. He eats.

Settled 2026-08-20.

**Step 6 is the human gate**, and it sits before the only consequence this
workflow has: Tom putting food in his mouth. That answers Step 9 in advance.

**Step 5 carries the check.** *Still fits the calories left* is what stops the
agent proposing a 600 kcal addition to a day with 200 left. Without it there is
no quality control, which is what Step 3 is really asking about.

**Step 1 is the weakest thing in this design, and it is not a design problem.**
Everything from step 2 onward works. Nothing in step 1 explains why a tired man
at nine at night opens an app instead of eating bread. Discovery already found
why: he feels no pain, his coach does. The only honest answer available is the
promise from Discovery's pain-point answer — *stop being hungry at eleven* — and
that is positioning, not architecture.

Recorded here rather than hidden, because a blueprint that assumes its own
adoption is a blueprint with a hole in step one.

## 3 · Agent loop

**Observe** — Tom's two messages: what he ate today, and what is in the fridge.
Plus his profile and the coach's target, the food list, and the safety policy.

**Decide** — three things, in this order:

1. Is this a food question at all, or does it escalate?
2. What do the described foods amount to in protein and calories?
3. Which of the three day-states applies — short with room, already at target,
   or no room left?

**Act** — the arithmetic, shown. Then either one named addition from what he
actually has, or a statement that there is nothing to add tonight and why.

**Check** — two halves:

- *Correctness.* Does the proposed addition close the protein gap, and does it
  fit inside the calories left? If not, pick again.
- *Shape.* Does the output contain only an addition, and never a removal?

Settled 2026-08-20.

**Why the check has two halves.** The first is arithmetic and it loops — the
first pick often does not fit. The second is a rule about what the output is
allowed to contain, applied at the last moment before handing back. One check
for correctness, one for safety, and they fail differently.

**Why "is this a food question" sits in Decide rather than Observe.** It has to
run before the estimate. The whole point is that some messages must never reach
the arithmetic at all — an agent that computes first and screens second has
already done the thing it was supposed to refuse.

## 4 · Inputs and context

All synthetic. No real person, no real household.

**Facts**

| | |
|---|---|
| `client_profile.md` | Tom's bodyweight, age, training days, and the coach's calorie and protein target. The target arrives as data; the agent never calculates it |
| `foods.csv` | Rewe and Edeka products with protein and calories per 100 g, including the prepared chicken breast filled with water that yields about 35 g per 150 g pack where a generic table would claim 45 |
| *(runtime)* | What Tom ate today and what is in the fridge. Not a file — he types both |

**Rules**

| | |
|---|---|
| `safety_policy.md` | **When to stop.** The escalation triggers and what the agent does at each |
| `output_rules.md` | **What a reply may contain.** The add-only constraint, and the pre-authored wording for the no-room case |

**Examples**

| | |
|---|---|
| `eval_cases.csv` | The five cases with their known-good answers. These double as the worked examples of good output, so the standard and the test are the same artifact |

Settled 2026-08-20.

**Why the rules are two files rather than one.** A stopping rule and a wording
rule get edited by different people for different reasons, and mixing them means
a copy edit can silently move a safety boundary.

It also follows the thing Moe singled out in the PlateMate design review —
*pre-authored language on every path where a bad sentence could do damage.* The
no-room case is that path here, and its wording belongs somewhere it can be
reviewed on its own.

Discovery promised one policy document. This is a deliberate split, not a drift.

## 5 · Tools or simulated tools

All simulated. A CSV standing in for a database is explicitly allowed by the
walkthrough.

| Tool | Serves | What it is |
|---|---|---|
| `foods.csv` lookup | steps 4, 5 | Protein and calories per 100 g for a named product. **Seeded from Open Food Facts barcodes, shipped as a file** |
| Budget calculator | step 4 | Deterministic arithmetic — target minus eaten, for protein and calories |
| Fit check | step 5 | Does this candidate close the protein gap and stay inside the calories left |
| Policy read | throughout | `safety_policy.md` and `output_rules.md` |
| `history.csv` read/append | steps 4, 6 | Two numbers a day for seven days. **Added by the Step 6 memory decision** — see below |

Five tools, mapped to workflow steps. The Blueprint Grill asks which one could
be deleted; the answer is none.

Settled 2026-08-20.

**The fit check stays separate from the budget calculator.** It could fold in —
both are arithmetic. It does not, because it is the loop's *check* step, and
merging the thing that proposes with the thing that verifies is how a check
quietly stops happening.

**Left off, deliberately:**

*A live food API.* Open Food Facts genuinely has these products, including the
Rewe chicken breast, so the earlier reasoning — that no public database carries
it — was wrong. The tool still stays out, for a better reason: a prototype
should not depend on a network call that can be slow, rate-limited, or missing
the item. Open Food Facts is the **source** for building `foods.csv`, not a
runtime tool. The numbers are real even though the client is invented.

*Any storage.* **Reversed by Step 6.** This originally said nothing persists
between runs, on the grounds that handing the agent somewhere to write would
settle the memory question here by accident. Step 6 then decided memory is
required, so `history.csv` is in — deliberately, and with its own reasoning
rather than as a side effect of tooling.

The write happens **after** Tom accepts. Changing a record is a consequence, and
the gate sits before consequences.

*Coach messaging.* Escalation in this prototype means the agent stops and says
so on screen. Actually sending a message is a consequence, and consequences need
a gate.

## 6 · Memory decision

**Seven days of two numbers. Nothing else.**

| | |
|---|---|
| **Remembers** | Date, calories, protein. Seven days rolling |
| **Never remembers** | What Tom typed, what was in his fridge, what was suggested, or anything that could reconstruct a conversation |

Settled 2026-08-20, after an initial answer of *no memory* was overruled.

**Why memory at all.** The method is multi-day by construction: calories average
across a window, protein anchors daily. An agent with no history cannot compute
how much room is left, and a Saturday dinner becomes a failure rather than
something the week absorbs. The first draft of this answer — no memory, forgetting
as a safety property — was simpler and wrong.

**Why two numbers and not the food.** A list of everything someone ate for a week
*is* a food diary, and this product's entire argument is that it is not one. Two
integers a day is a budget. The moment it stores food names, it has become the
thing it exists to replace.

**Why seven days and not three.** Three does not span a weekend. If a Saturday
dinner is meant to be absorbed rather than punished, the window has to reach
across it. Seven is also the outer bound of the method's own averaging range.

**The rule that keeps it safe: it uses history to compute, never to comment.**

| Allowed | Forbidden |
|---|---|
| *You have room tonight, the week is under* | *You have been low three nights running* |

The second sentence is monitoring. It belongs to the coach, because a person can
tell learning from control and a running total cannot. This is the `P-09` boundary
arriving as a memory rule.

## 7 · Output format

*Open.*
