# The variants

Every version of the big idea, the bet each one makes, who it is aimed at, and
where it actually got to.

Structured on Ash Maurya's Model / Prioritize / Test timeline, because it asks a
question nothing else here has asked: **given every variant side by side, at the
stage each has actually earned, which one gets the next two weeks?**

Reconstructed from the repos and working notes. Where I am inferring rather than
reading it off something, it says so.

---

## The big idea

**Help someone reach a protein target without turning them into a bookkeeper.**

Everything below is that idea aimed at a different segment, arriving through a
different channel, paid for by a different person, or doing a different job.

## The framing, and why it changes per segment

The same mechanism — protein density, the XP score, an addition rather than a
subtraction — is framed differently depending on who is holding it. That is not
marketing gloss. It changes what the product has to do.

| framing | for whom | what the product must therefore do |
|---|---|---|
| **Rescue** | the day already broke | read what happened, name one addition |
| **Construction** | the day has not happened yet | design a plate forward from density |
| **Instrumentation** | someone else is accountable | show a third party which days went wrong |
| **Translation** | the person cooking is not the person with the target | turn a target into a family meal |

V1 and V2 are Rescue. V6 is Construction. V5 is Instrumentation. V4 is
Translation. V3 is Rescue with the escalation destination removed, which is why
it is not a small edit.

---

## The segments

| | segment | who is in it | who pays |
|---|---|---|---|
| S1 | **Coached client, mid-programme** | pays a coach, has a target, the plan keeps breaking | the coach, bundled |
| S2 | **Self-coached, time-poor** | full-time job, young children, trains when possible, no professional in the loop | themselves |
| S3 | **Never-tracked, protein-curious** | has heard protein matters, has no number, has never logged | themselves |
| S4 | **Tracked and quit** | logged for weeks or years, stopped, now flying blind | themselves |
| S5 | **The household cook** | sets the protein content of every meal in the house, often has no target of their own | the household |
| S6 | **Deliberate build or cut** | eating to a purpose, and eating enough is the hard part | themselves |
| S7 | **Online nutrition coaches** | 10 to 100 clients, finds out too late when one drifts | the coach, as a tool |

S4 is the one we did not name until the evidence forced it. Pass 2 proved it
exists in volume and is articulate about the pain. Nothing is currently aimed
at it.

---

## The variants

| | variant | segment | framing | hypothesis | evidence |
|---|---|---|---|---|---|
| V1 | PlateMate | S1 | Rescue | plan-adaptation beats plan-abandonment | none |
| V2 | Worth Eating | S1 · S2 | Rescue | the fridge at night is the moment worth owning | 3 people known to the author |
| V3 | No coach at all | S2 | Rescue | the job survives with nobody to escalate to | 1 conversation |
| V4 | The household cook | S5 | Translation | fix the family meal, not the late plate | 1 observation |
| V5 | The coach's instrument | S7 | Instrumentation | coaches pay to see the nights before week six | none |
| V6 | Meal engineering by density | S6 | Construction | the constraint is protein per unit of volume, not logging | **unprompted customer language** |

### V1 — PlateMate

**Hypothesis:** a coached client whose day has broken will adapt it rather than
write it off, if the agent never once suggests skipping.

An orchestrator reads the broken day and routes it to a nutrition agent, with a
sleep and recovery agent for late dinners and anything medical escalated to the
coach.

Channel is the coach. The coach is also the payer, which was never examined —
that is a whole pricing assumption sitting untested underneath the variant that
got the most work.

**Stage:** prototype built, Discovery and Design faculty-approved. Faculty
approval is not customer validation.

### V2 — Worth Eating

**Hypothesis:** the single moment worth owning is the fridge after the children
are in bed, and one named addition is worth more than a plan.

Narrower than V1 on purpose. The XP score is the mechanism, the add-only rule is
the safety property.

The only variant with real people attached: D, M and R. D uninstalling Carbon
because it *"didn't give him a proper way to live his day"* is still the
strongest single piece of evidence in the project.

`worth-eating-capstone` is **not** a seventh variant. It is V2 re-run on
synthetic data to learn the method. Same variant, second pass, different reason.

**Stage:** prototype built, three real people consulted.

### V3 — No coach at all

**Hypothesis:** the same job works with nobody to escalate to, if something else
absorbs the escalations.

D's actual situation. Trains five times a week at home, logs training on a
printed Atomic Habits sheet, has no coach.

Every escalation path in V1 and V2 terminates at a coach. Remove the coach and
`S3` out-of-policy, `S4` high-stakes and a confirmed `S5` have nowhere to go.
That is not an edit, it is a different safety design — which also makes this the
**fastest variant to kill or keep**, because it either has an answer to that or
it does not.

**Stage:** modelled, one real conversation.

### V4 — The household cook

**Hypothesis:** raising the protein in the meal the household already eats beats
repairing one person's plate at eleven at night.

M cooks for the family, does not know what protein is, and is motivated to
learn. She sets the protein content of every meal in that house. Nothing is
aimed at her.

Pass 2 gave this an unexpected nudge: *"no kitchen at times and at others
relying on someone else to cook"* is a real reported reason people stop being
able to manage their own intake.

**Stage:** modelled only.

### V5 — The coach's instrument

**Hypothesis:** coaches will pay to see which nights went wrong before the
six-week review, rather than after it.

`With the plan` bottoms at **-45** at that review — the lowest point in the
whole client relationship, where nothing has moved and neither party can say
which nights caused it. V5 attacks that point directly, and sells to the person
who is paid to care about it.

Different segment, different payer, different price. Never modelled.

Pass 2 is quietly supportive: the one documented case of someone being taken off
tracking was *"she told me to stop tracking my macros"* — a dietitian, not an
app. The authority in this space is a person.

**Stage:** modelled only.

### V6 — Meal engineering by macro density

**Hypothesis:** for someone in a deliberate build or cut, the binding constraint
is protein per unit of volume and effort, not logging. Design the plate forward
from density and the number takes care of itself.

Not rescue, construction. It inverts V2: V2 asks *what do I add to what already
happened*, V6 asks *what do I build so it does not happen*. Same mechanism,
opposite direction in time, and a customer who is planning rather than
repairing.

**This is the update this file was missing.** As of 2026-08-26 it is the only
variant with a customer describing the problem unprompted, from
[pass 2](research/2026-08-26-gemini-findings.md):

> *"I decided I was tired of eating, and stopped tracking my calories, and just
> eating 'until full, plus a bit more and two protein shakes per day'."*

> *"I can't be bothered to log it all right now, I just slam food all day long."*

These people are not struggling to eat less. They are struggling to eat enough
protein without more volume, and the logging is overhead on a problem the
logging does not solve. They showed up in a subreddit included to catch people
*leaving* tracking, and described a different problem entirely.

**Stage:** modelled, never stress-tested, and now better evidenced than the two
that were built.

---

## What was killed, and where

Feature-level kills inside V1 and V2, not whole variants. All died on paper,
which is the cheap side of the diagram.

| killed | stage | why |
|---|---|---|
| Self-serve XP card issuance | on paper | a card is a clinical number; nobody issues themselves one |
| Zoned food list, good and bad | on paper | a restriction mechanic wearing a scoring costume |
| Live food database call at runtime | design | a prototype should not depend on a request that can be slow, rate-limited or missing the item |
| Coach-messaging tool | design | sending a message is a consequence, and consequences need a gate |
| Anger and legal-language escalation | design | a support-desk pattern; this client is alone at his own fridge |
| A Google Sheet PRD | develop | ten of twenty rows drifted on PlateMate. One source of truth |

---

## Evidence, honestly

| variant | customer evidence |
|---|---|
| V1 | none |
| V2 | three people the author already knows |
| V3 | one conversation |
| V4 | one observation, plus an indirect quote from pass 2 |
| V5 | none directly; the journey map and one pass-2 quote both point at it |
| V6 | **unprompted customer language, from strangers** |

Measured against Maurya's timeline:

- **No variant has cleared Customer/Problem Fit.** V2 comes closest, on people
  the author knows, which is the weakest form of evidence there is.
- **Nothing has been killed at the Prioritize gate**, because nothing was put
  through it. The six kills above are features.
- **The variant with the best evidence is the one that has never been tested.**

## The uncomfortable part

> If you test your variants sequentially, one at a time, you never actually
> compare them. You work on whichever one you happened to open, and the one you
> happened to open is usually the one you already liked.

V1 was built because it was open. V2 because it was next. V3 through V6 have
never been placed beside them, and the first time outside evidence entered this
project it landed on V6 rather than on either of the two with prototypes.

## Open, and what would move it

**Pass 3 is in flight** and it tests `S3`, the never-tracked protein-curious
segment that V2 and V3 both assume. It is written to hunt for disconfirmation:
if that segment turns out to be mildly curious rather than in pain, then Tom is
not the customer and `S4` — tracked and quit, which pass 2 proved exists in
volume — is where V2 should be re-aimed.

The comparison still costs an afternoon. Four variants, stress-tested on paper
for desirability, viability and feasibility, side by side. It remains the
cheapest pivot available and it has still not been taken.
