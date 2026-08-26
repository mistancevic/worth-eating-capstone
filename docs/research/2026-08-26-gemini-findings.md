# Research pass 2 — tracker abandonment, run on Gemini

Recorded 2026-08-26T14:40:42Z. Run by Milan on Gemini after
[pass 1](2026-08-26-tracker-abandonment.md) came back empty from this container.

Report kept verbatim at
[`2026-08-26-gemini-tracker-quitting-raw.txt`](2026-08-26-gemini-tracker-quitting-raw.txt).
25 cited Reddit threads across r/loseit, r/MacroFactor, r/1200isplenty, r/Fitness
and r/nutrition.

## What it changed

**One of our two claims is wrong. The other is right for the wrong reason.**

### Eleven days was wrong. It is about a month.

`Before the plan` put the tracker-deletion valley at eleven days. Nothing in the
corpus is that short. The documented durations:

| | |
|---|---|
| "Started about a month ago" | quit before her period |
| "from january until mid-march" | roughly ten weeks, ended by a herniated disc |
| "almost 6 months" | lost 25 lb, then stressful weeks |
| "252 day MFP streak" | ended it deliberately |
| "365 days tracked" | the Fitbit broke |
| "over the last 2 years" | "a bit of a menty b over the spring" |

The distribution is **bimodal, not short**. People fail in the first weeks or
they last for years and then break. Eleven days was invented and has been
corrected to **about a month** on the slide and in `journeys.md`.

The stage stays where it is on the curve — the valley is real and it is the
deepest one. Only the number moved.

### The valley is real. My stated cause is not what anyone says.

I wrote that the tool "told him what he had eaten and never once told him what
to do about it." That is a good product argument. **Nobody in the corpus says
it.** Not once.

What they actually say, in their own words:

**Cognitive load.** *"I was checking my app after every bite and eating turned
into math homework."* That is the single best line in the report and it is a
different failure from the one I described. Not "it did not help me," but "it
turned eating into admin."

**The precision trap.** *"I tried losing weight for years by being super precise
and calorie counting only to result in binges when I accidentally went 1 calorie
over. Then decided to give it up and immediately dropped weight because I felt
much less pressure."*

**All-or-nothing collapse.** *"because I'm an awful 100% or nothing kind of
person, I chose nothing."*

**Environmental chaos**, which is Tom exactly: *"survived a wildfire,
remediation and all that, and I have two kids and FT job… so I stopped tracking
calories."* And: *"no kitchen at times and at others relying on someone else to
cook."*

**The shame loop.** *"I have deleted the app multiple times but it keeps getting
reinstalled in moments of weakness."* And: *"I'm coming to terms with the fact
that it encourages those unhealthy impulses in me."*

The callout on the slide has been rewritten to the reported causes rather than
my inferred one.

## The finding that cuts against our own design

One quote is aimed straight at a rule we added yesterday:

> *"After all 499 vs 500 deficit is virtually the same, but seeing you went over
> your limit is very demotivating and may make you quit."*

At p06c we added a rule that Note reports how far under the calorie budget the
day lands, on the grounds that he is entitled to know. On CASE-8 it produced
*"That still leaves you around 1,200 under your 2,300."*

**That is the same shape as the sentence this corpus says makes people quit.** A
number he missed, printed at the moment he cannot do anything about it.

The reasoning behind the rule still holds — a day that hits protein and lands
600 kcal short is a real failure the score cannot see. But the delivery is now
in question, and the evidence is against the current wording. It goes on the
open list rather than being quietly kept.

## What it supports that we already believed

**Escalation to a human is the documented exit.** *"she told me to stop tracking
my macros, and to start intuitive eating."* A dietitian, not the app, ended it.
Our S3 rule that the coach owns the target is the same instinct.

**Graduation is a real outcome, not a fantasy.** *"A calorie tracker is the
training wheels of nutrition."* Discovery says the tool should make itself
unnecessary. Somebody in r/Fitness said it first and better.

**Streaks are a prison, not a retention mechanic.** *"I just ended a 252 day MFP
streak, stopping counting every calorie is actually my goal rn."* We have no
streak. Keep it that way, and this is why.

## The finding I did not expect, and it belongs to V6

r/Fitness has a whole cohort quitting for the opposite reason. Not restriction
fatigue. **Eating fatigue.**

> *"To hell with MF's maintenance target right now, I stopped tracking my food
> some weeks ago. I just eat. And eat and eat and eat. I can't be bothered to
> log it all right now, I just slam food all day long."*

> *"I decided I was tired of eating, and stopped tracking my calories, and just
> eating 'until full, plus a bit more and two protein shakes per day'."*

These people are not struggling to eat less. They are struggling to eat **enough
protein without more volume**, and they quit because the logging is overhead on
a problem the logging does not solve.

That is [V6](../variants.md) — meal engineering by macro density, segment S6 — described by
its own customer, unprompted, in a subreddit we included for a different reason.
It is the strongest signal in the whole report and it is not about V2 at all.

## Provenance, honestly

**I have not verified a single quote.** This container's egress policy refuses
`reddit.com`, which is why pass 1 returned nothing, so I cannot open any of the
25 cited threads to check the text against the source.

Two things look off and should be checked before any of this is quoted publicly:

- The report says the window is summer 2026, but cites a thread titled
  *"European Accountability Challenge: 4th March 2026"*.
- Citation 15 has a Reddit id of `3grmdg`, which is a much older post than the
  stated window.

The substance reads as genuine Reddit material and the community profiles are
recognisably accurate. But this is a synthesis, the quotes are second-hand at my
end, and it should be treated as strong evidence rather than as verified
evidence until someone opens the threads.
