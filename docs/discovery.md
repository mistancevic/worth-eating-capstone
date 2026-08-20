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

**The meal that decides the day is chosen when Tom is most tired, hungriest and
least attentive.** What he picks is dilute — bread, cheese, leftovers. Calories
arrive, protein does not.

Five failures stacked on one moment:

1. The number never reaches the fridge door. It is real, and it is in a PDF.
2. Nothing about the choice feels wrong, so nothing corrects it.
3. Hunger is driving. He did not decide to eat, he was interrupted.
4. He never learns he was short, because nothing tells him.
5. The only feedback that exists is six weeks out.

**And the person with the pain is not the person using the thing.** Tom feels
nothing. The coach feels it weeks later when weight and strength have not moved.
That is an adoption problem before it is a product problem.

**Except Tom does feel something, and he does not connect it.**

> Dilute at nine → hungry again at eleven → sleeps badly → five coffees the next
> day.

A twelve-hour loop, already running, every day. That is the opening: the same
signal the coach waits six weeks for is available to Tom tonight, if anything
joins the two ends of it.

Which changes the promise. Not *hit your protein target*, which is the coach's
language and means nothing at 9pm. **Stop being hungry at eleven.** Same action,
and only the second one belongs to Tom.

**Honest caveat for the metric later:** the hunger link is defensible, because
protein is what holds you. Sleep and coffee are downstream and confounded. Hunger
at eleven is the measurable end.

## 5 · What decision should the agent help with?

**What to add so the meal fits — and whether to add anything at all.**

Not what to eat. Tom already has food in front of him. The decision is what goes
beside it.

Settled 2026-08-20, with a caveat from Milan that changed the shape of it: *a
late dinner that is already heavy is itself a problem.*

That caveat mostly dissolves, because a booster is dense by definition. YoPro is
about 23 g for 110 kcal, skyr 33 g for 190. A ratio is exactly what lets protein
be bought cheaply in calories.

But it does not dissolve entirely, and what survives is a third state:

| State | Answer |
|---|---|
| Short on protein, room left in the day | add a booster |
| Already at or above the number | say so, add nothing |
| No room left in the day | say so — tomorrow's lesson, not tonight's fix |

The second state is what stops the tool being a nag. The third is what the
caveat found, and it is the dangerous one: *no room* is one badly written
sentence away from *do not eat*.

## 6 · What should the agent not be allowed to do?

**Never tell him not to eat. Never suggest skipping. Never diagnose.**

Settled 2026-08-20. Two rules added during the interview:

**It never pushes.** It answers when Tom opens it and it is silent otherwise. No
notification at eight saying he is behind. This workflow speaks every night,
where PlateMate only spoke when a day broke, and a tool that comments on every
meal becomes surveillance.

**It escalates.** Not diagnosing is right, but if Tom writes something that is
not a food question — dizzy, has not eaten all day, chest tight — the answer is
the coach or a doctor, not a booster.

---

## The goal, and the line through it

Recorded here because it came up during question 6 and governs everything after.

This is not a protein-counting product. What Tom is short of is energy and
capacity for the day in front of him. Poor meals cost him sleep, the lost sleep
costs him the next day, and the workaround — five coffees — is a loan that gets
repaid with interest.

**But energy is the reason, never the promise.**

| | |
|---|---|
| What the tool can guarantee | the ratio on the plate |
| What it cannot | that he sleeps, or feels good tomorrow |

Sleep depends on the kids, the laptop, the coffees and his training. Protein is
one input. So the sentence Tom hears is *stop being hungry at eleven*, which is
defensible, and never *you will have more energy*, which is not.

This decides the success metric in advance: energy is not measurable here,
hunger at eleven is.

## 7 · What data can you safely use?

All invented. No panel member, no real household, nothing gathered from a person.

**1 · Tom's profile and the coach's target.** Bodyweight, age, training days, and
the calorie and protein numbers the coach set. This is the card, and it arrives
as data rather than being calculated by the agent.

**2 · A food list, shop-real.** Rewe and Edeka products with protein and calories
per 100 g. Including the awkward ones — the prepared chicken breast filled with
water that gives 35 g where a database would claim 45. That detail is where the
value is, and a generic food table does not have it.

**3 · A safety and escalation policy, as a document.** The boundary from question
6 written down, so it can be tested rather than only prompted.

**4 · The day so far, in Tom's own words.** He logs nothing, so he tells the
agent: *"a sandwich, a coffee, some crisps at my desk."*

Settled 2026-08-20.

**This closes the question parked at question 2.** Nothing tracks Tom. He says
what he ate, and turning "a sandwich" into a number is the model's job. Text
only — no photographs, no weights. That is the right simplification for a
capstone and it removes the one part of the demo most likely to fail live.

## 8 · What output will the demo show?

Two runs, one continuous session.

**Run one — the booster.**

1. Tom types what he ate today, in his own words.
2. Tom types what is in the fridge.
3. The agent shows the arithmetic: where he is against the coach's target, and
   what is left.
4. The agent names one thing to add, chosen from what he actually has.

**Run two — no room.**

The same opening, but the day is already spent. The agent says there is nothing
to add tonight and why, and leaves it as tomorrow's lesson rather than tonight's
fix.

Settled 2026-08-20.

**Why two runs.** A demo where everything works proves nothing. PlateMate's was
credible because two of its cases were refused, and the refusals were what people
remembered.

**Carried to Design:** what makes the no-room case safe is the exact wording, not
the logic. *No room* sits one bad sentence away from *do not eat.*

**Carried to eval:** escalation is not on screen in either run. That is fine for a
demo, but it has to appear in the eval cases or the boundary is decorative.

## 9 · What metric would show value?

**How many nights Tom is not hungry at eleven.**

His own signal, same night, and the exact promise made at question 4. Not energy,
which the tool cannot control and cannot measure.

Settled 2026-08-20.

**It cannot be measured in this capstone**, because synthetic Tom never gets
hungry. So there are two, the way PlateMate had a headline metric with support
underneath it.

| | |
|---|---|
| **Outcome** | nights not hungry at eleven — real users, later |
| **Build** | share of eval runs where the addition actually closes the gap using only what Tom said he had |
| **Build** | share of runs where it correctly refuses, on no-room and on escalation |

The second build measure exists because a tool that always answers looks perfect
on the first one.

## 10 · What would make this clearly agentic?

It asks what he ate, works out what is left, then decides. As stated that is a
chatbot with a good prompt, and the answer only holds once the decisions are
counted.

**Six decisions in one run:**

1. Is this a food question at all, or does it need escalating
2. What does "a sandwich and a coffee" actually amount to
3. Is there room left in the day — three states, and it must pick one
4. Which item from what he has closes the gap
5. Does that item fit the calories left, or does it pick again
6. Is the answer inside the boundary

Four loops back through five when the first pick does not fit.

**And the one that separates it from a chatbot: it can decide not to answer.** A
chatbot always answers. This has states where refusing is correct and it has to
reach them itself.

It also does not work from the conversation alone. The target comes from the
profile, the food numbers from the list, the boundary from the policy document.
Three sources Tom never typed.

Settled 2026-08-20.
