# The variants

A record of every version of the big idea, where each one actually got to, and
what was killed.

Structured on Ash Maurya's Model / Prioritize / Test timeline, because it asks a
question nothing else in this project has asked: **given every variant side by
side, at the stage each has actually earned, which one gets the next two weeks?**

Reconstructed from the repos and the working notes. Where I am inferring rather
than reading it off something, it says so. Correct anything that is wrong.

## The big idea

**Help someone reach a protein target without turning them into a bookkeeper.**

Every variant below is that idea aimed at a different customer, arriving through
a different channel, or doing a different job.

## The variants

| | variant | customer | the job | furthest stage reached |
|---|---|---|---|---|
| V1 | **PlateMate** | coached client | the plan broke today, adapt it | prototype built, faculty-approved Discovery and Design |
| V2 | **Worth Eating** | coached client at the fridge at night | name one thing to add | prototype built, three real people consulted |
| V3 | **No coach at all** | self-coached, home gym, paper habit sheet | same job, nobody to escalate to | modelled, one real conversation |
| V4 | **The household cook** | the person who actually cooks | make the family meal carry protein | modelled only |
| V5 | **The coach's instrument** | the coach, not the client | see which nights went wrong before week six | modelled only |
| V6 | **Meal engineering by macro density** | someone building muscle or losing fat | design the meal forward from protein density | modelled only, never tested |

### V1 — PlateMate

The capstone that earned the certificate. An orchestrator agent reads a broken
day and routes it to a nutrition agent, with a sleep and recovery agent
consulted when a late dinner is really a sleep question, and anything medical
escalated to the human coach. Skipping is never the default.

Channel is the coach. The coach is also the payer, which was never examined.

### V2 — Worth Eating

Narrower than V1 on purpose. One moment, one question, one addition. The XP
score — protein divided by calories times one hundred — is the mechanism, and
the add-only rule is the safety property.

This is the only variant with real people attached: D, M and R. D's line about
uninstalling Carbon because it *"didn't give him a proper way to live his day"*
is the single strongest piece of evidence anywhere in this project, and it
belongs to this variant.

The `worth-eating-capstone` repo is **not** a seventh variant. It is V2 re-run
on synthetic data to learn the method properly. Same variant, second pass, for
a different reason.

### V3 — No coach at all

D's actual situation. Trains five times a week at home, logs training days on a
printed Atomic Habits sheet, and has no coach to escalate to.

This matters more than it looks. Every escalation path in V1 and V2 ends at a
coach. Remove the coach and the whole safety design has nowhere to send
anything. That is not a small edit; it is a different product.

### V4 — The household cook

M cooks for the family, does not know what protein is, and is motivated to
learn. She is the person whose decisions actually set the protein content of
every meal in that house, and no variant so far is aimed at her.

Never modelled beyond noticing it.

### V5 — The coach's instrument

The `With the plan` journey bottoms at the six-week review, where nothing has
moved and neither party can say which nights went wrong. V5 sells to the coach
instead of the client: show them the nights.

Different customer, different payer, different price, and it attacks the deepest
valley on the map directly. Never modelled.

### V6 — Meal engineering by macro density

**The one still waiting for a test.**

Not rescue, construction. Design the meal forward from macro density, with
protein density as the north star, because protein is the lever for both muscle
gain and fat loss at the same time. The user builds a plate that hits the number
by design rather than discovering at eleven at night that it did not.

It inverts V2. V2 answers *what do I add to what already happened*. V6 answers
*what do I build so it does not happen*. Same XP mechanism, opposite direction
in time, and a customer who is planning rather than repairing.

Never stress-tested for desirability, viability or feasibility.

## What was killed, and where

These are feature-level kills inside V1 and V2 rather than whole variants. Every
one died on paper, which is the cheap side of the diagram.

| killed | stage | why |
|---|---|---|
| Self-serve XP card issuance | on paper | a card is a clinical number; nobody should issue themselves one |
| Zoned food list, good and bad | on paper | it is a restriction mechanic wearing a scoring costume |
| Live food database call at runtime | design | a prototype should not depend on a request that can be slow, rate-limited or missing the item. Open Food Facts became the source for building the file instead |
| Coach-messaging tool | design | actually sending a message is a consequence, and consequences need a gate |
| Anger and legal-language escalation | design | a support-desk pattern. This client is alone at his own fridge with nobody to be angry at |
| A Google Sheet PRD | develop | ten of twenty rows drifted between the sheet and the repo on PlateMate. One source of truth |

## The uncomfortable part

Maurya's second point is the one that applies here.

> If you test your variants sequentially, one at a time, you never actually
> compare them. You work on whichever one you happened to open, and the one you
> happened to open is usually the one you already liked.

That is what has happened. **V1 was built because it was open. V2 was built
because it was next. V3 through V6 have never been placed beside them.**

And the honest reading of the furthest-stage column is harsher than it looks.
Two prototypes exist and one certificate has been earned, but faculty approval
is not customer validation, and a synthetic persona cannot fail you. Measured
against this timeline:

- **No variant has cleared Customer/Problem Fit.** V2 comes closest, on three
  people the author already knows.
- **Nothing has been killed at the Prioritize gate**, because nothing was ever
  put through it. The six kills above are features, not variants.
- **The cheapest pivot available has not been taken yet.** V3 through V6 could
  each be stress-tested on paper in an afternoon.

## The question this file exists to answer

Not *is Worth Eating validated*. It is:

**Given V1 through V6 side by side, at the stage each has actually earned, which
one gets the next two weeks?**

V6 is the one you are holding. V5 attacks the deepest valley on the journey map.
V3 breaks the safety design and is therefore the fastest to kill or keep. None
of them has been compared with the two that got built.

That comparison has not been made. It should be, and it costs an afternoon.
