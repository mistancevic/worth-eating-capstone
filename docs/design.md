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

*Open.*
