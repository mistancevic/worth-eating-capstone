# Discovery

Run with the Discovery Companion v0.2, in `discovery-companion/`.

## The start prompt

Verbatim from `STUDENT_START_PROMPT.md`:

```text
I am starting the Discovery phase of my Agentic AI Capstone.

Read START_HERE.md, AGENTS.md, and 01_DISCOVERY.md.

Help me choose my own capstone project. Do not recommend Northstar Home as my project. Northstar Home is only an example.

Ask me one question at a time. Grill me until I have a safe, specific, demoable agentic workflow.

Then help me write self-contained Discovery PRD answers for:
1. User
2. Workflow
3. Trigger
4. Current process
5. Pain points
6. Agent opportunity
7. Synthetic data plan
8. Human boundary
9. Success metric
10. Initial demo idea

After the Discovery PRD answers are complete, stop and tell me not to move to Design yet.
```

## How this runs

From `AGENTS.md`. One question at a time. After each answer: assess it briefly,
say how to improve it, ask the next one. Grill on vague users, vague workflows,
unsafe data, generic chatbot ideas, no visible demo, too much autonomy, no human
boundary, no success metric.

Stop when the ten PRD answers are done. Do not touch Design.

## Three lists, and they are not the same

**The interview** — `01_DISCOVERY.md` Step 4. What gets asked.

1. Who is the specific user?
2. What event starts the workflow?
3. What does the user do today?
4. Where does the workflow slow down or fail?
5. What decision should the agent help with?
6. What should the agent not be allowed to do?
7. What data can you safely use?
8. What output will the demo show?
9. What metric would show value?
10. What would make this clearly agentic?

**The Grill** — `PROJECT_IDEA_GRILL.md`. A pressure test, plus a Go / No-Go
filter. Used to break the idea, not to build it.

**The PRD fields** — what gets written at the end. Ten self-contained answers,
no link-outs.

---

# Parked workflows

Named during the interview, not chosen.

**Adapting a plan when the day breaks.** This is PlateMate. Built, submitted,
under review. Rebuilding it would teach the path and nothing else.

**Scoring a plate that already exists and naming what is missing.** Reactive.
One look, one answer. It is what the real app is being built around, and it is
the one that keeps failing the agentic test because there is no loop in it.

---

# Answers

## 0 · The workflow

Deciding what to eat so the day's protein target is met, with whatever is
available. Not cooking from scratch — choosing, ordering, or grabbing.

Where it breaks: the last meal of the day. It is when the day gets decided and
it is the meal people are most tired for. A late plate of bread, cheese and oily
salad is a pile of calories carrying almost no protein.

## 1 · Who is the specific user?

**Tom. 34, backend developer in Munich. Trains three times a week.**

Has a coach, and the coach gave him a calorie and protein target. He does not
cook much. On a normal evening he orders something or grabs bread and cheese on
the way home. At 9pm the coach is not answering.

Settled 2026-08-20.

**Also considered, not chosen:** Tom before any coach — no target, no idea what
he needs, only that the internet keeps talking about protein. That is a lower
literacy level and a different product. It would need the agent to set the
target itself, which is the one thing the safety boundary should not practise.

## 2 · What event starts the workflow?

**Tom opens the fridge after putting the kids to bed.**

Around nine, every night, whether the day went to plan or not. Nothing has to be
detected and no disruption has to occur — the event is simply that the day is
nearly over and he has not eaten enough protein.

Settled 2026-08-20.

Two things this pins down. The persona gains children, which is why the meal is
late, why he is tired, and why the fridge has leftovers in it. And the trigger is
predictable rather than reactive, which is the opposite of PlateMate — that one
fired when a day broke.

**Open underneath it:** how Tom knows he is behind. He logs nothing. Parked for
question 7.

## 3 · What does the user do today?

1. Feeds the kids. Does not eat with them.
2. Puts them to bed.
3. Sits with the laptop until hunger hits.
4. By then it is late.
5. Opens the fridge.
6. Sees kid leftovers, bread, cheese — whatever needs no cooking.
7. Takes that and eats it standing up.
8. Never thinks about the number.

Settled 2026-08-20.

**The correction that matters is step 8.** Tom has a coach and a target, and the
target is inert. It is in a PDF on his phone. He read it once. It has never been
in his head at the fridge door.

That is a stronger problem than having no number at all. The gap is not
information, it is that the number never travels to the moment the decision gets
made.

**And his own standard is low but genuinely met.** In his words: eating something
at that hour is already a good step. He is not failing by his own measure. He is
clearing a bar he set. Anything built here has to raise the bar without telling
him he has been doing it wrong.

**Also note:** hunger interrupts him. He does not decide to eat.

## 4 · Where does the workflow slow down or fail?

*Open.*
