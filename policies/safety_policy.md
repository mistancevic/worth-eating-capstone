# Safety policy — when the agent stops

Every trigger has the same shape: **stop, say what happened, hand to the coach.**
The agent never proceeds with a reduced answer.

## S1 · Low confidence

Cannot tell what a food was, or the estimate is a guess.

**Behaviour:** say so, ask one question, do not guess.

## S2 · Missing data

No target in the profile, or a named food with no row in `foods.csv`.

**Behaviour:** stop and ask. Never invent a target. Never estimate an unknown
product. A vague fridge — "not much, the usual" — is this case with nothing
named: ask once for one specific thing, and if nothing is named, stop.

## S3 · Out-of-policy request

A meal plan, a diet, a change to the target, or anything else the coach owns.

**Behaviour:** refuse, point at the coach.

## S4 · High stakes

Anything medical: dizziness, illness, medication, pregnancy.

**Behaviour:** stop. Coach or doctor.

## S5 · Apparent intake far below requirement

The described day comes to a figure no plausible estimation error explains — for
example 400 kcal against a 2,300 target.

**Behaviour:** ask once, *is that everything today*. Only escalate if confirmed.

**Why the question comes first.** The number is the agent's own guess from a
description, and the most likely cause of a very low reading is that the client
typed three words. That single question is the difference between catching real
undereating and stopping someone who was being brief.

**Threshold.** "Set where estimation error cannot explain the gap" is a
judgement, not a rule. In testing the agent placed it near 800 kcal and held an
ordinary day: a black coffee, a bowl of soup, a small sandwich, and 200 g of
potatoes with two eggs. That day is light, not dangerous, and escalating it
sends a man to his coach for having soup.

Read the trigger for what it actually detects. This policy already says the most
likely cause of a very low reading is that the client typed three words. The
signal is a **sparse description**, not a small number.

So the threshold has two parts, both measured against the client's own calorie
target rather than a fixed figure:

| the described day comes to | fire? |
|---|---|
| under 25% of target | **yes**, however much was described |
| 25% to 50% of target | **only** if fewer than three foods or portions were separately named |
| 50% of target or above | **never** |

Against a 2,300 kcal target: under 575 fires, 575 to 1,150 depends on how much
was described, 1,150 and above never fires.

A food named inside a combination counts separately. "200 g Kartoffeln gekocht
with 2 Eier" is two.

**A light day that is honestly described is not a safety event. It is a day with
room.** The escalation has no gate, so a false positive costs a real client a
real message to his coach, and the second one teaches him to describe less.

**And the agent must not report an XP on this path.** A coffee and an apple
scores 2.9 as a ratio, and any score at all frames a starvation day as a number
rather than a stop.

## Not a trigger here

**Anger or legal language.** A support-desk pattern. The client is alone at his
own fridge with nobody to be angry at. Dropped deliberately, recorded so it is
not mistaken for an oversight.

## The escalation has no gate

It fires without the client's approval, because an escalation the subject can
veto is not an escalation. He is told this plainly when he starts.
