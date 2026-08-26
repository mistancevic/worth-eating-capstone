# The variants

Every version of this idea, what each one is betting on, who it is for, and how
far it actually got.

Laid out the way Ash Maurya does it, because his diagram asks a question we have
never asked here: put all the versions next to each other, at the stage each one
has really earned, and then decide which gets the next two weeks.

Pieced together from the repos and the notes. Where I am guessing, it says so.

---

## The big idea

**Help someone eat enough protein without turning them into a bookkeeper.**

Everything below is that same idea, pointed at a different person, sold a
different way, or doing a different job.

## Four ways of framing it

The mechanism never changes. Protein density, the score, and the rule that we
only ever add food. What changes is who is holding it, and that changes what the
thing has to do.

**Rescue.** The day already went wrong. Read what happened, name one thing to
add. That is V1, V2 and V3.

**Construction.** The day has not happened yet. Help him build a plate that
works before he is standing in front of the fridge. That is V6.

**Instrumentation.** He is not the one holding it. His coach is, and she wants
to see which nights went badly. That is V5.

**Translation.** The person cooking is not the person with the target. Turn a
number into a family dinner. That is V4.

Worth saying plainly: those are four different products, not four settings.

---

## Who each one is for

| | who | what they look like | who pays |
|---|---|---|---|
| S1 | **Coached, mid-programme** | pays someone, has a number, keeps falling off | the coach, bundled in |
| S2 | **On his own, no time** | job, small children, trains when he can, nobody advising him | himself |
| S3 | **Never tracked anything** | has heard protein matters, has no number, never logged a meal | himself |
| S4 | **Tracked, then quit** | did it for weeks or years, stopped, now guessing | himself |
| S5 | **The one who cooks** | decides what everyone eats, usually has no target of her own | the household |
| S6 | **Building or cutting on purpose** | eating with intent, and eating enough is the hard bit | himself |
| S7 | **Coaches** | ten to a hundred clients, finds out too late when one drifts | the coach |

S4 only got a name once the evidence forced it. Pass 2 showed there are a lot of
them and they talk about it clearly. Nothing we have is pointed at them.

---

## The versions, and what each is betting

### V1 — PlateMate · for S1 · rescue

**The bet:** if someone's day falls apart, they will fix it instead of writing
it off, as long as nobody ever tells them to skip a meal.

An orchestrator reads the mess and hands it to a nutrition agent, with a sleep
agent for late dinners and anything medical going straight to the coach.

The coach is the channel and also the one paying, and we never looked at that.
There is a whole pricing assumption sitting underneath the version that got the
most work.

**Where it got to:** built, Discovery and Design approved by faculty. Which is
not the same as a customer saying yes.

### V2 — Worth Eating · for S1 and S2 · rescue

**The bet:** the moment worth owning is him standing at the fridge once the
children are asleep. One thing to eat beats a plan.

Tighter than V1 on purpose. The score is the engine, and only-ever-add is what
keeps it safe.

The only version with real people behind it: D, M and R. D uninstalling Carbon
because it *"didn't give him a proper way to live his day"* is still the best
thing anyone has said to us.

`worth-eating-capstone` is not a seventh version. It is V2 run again on made-up
data so we learn the method properly.

**Where it got to:** built, three real people spoken to.

### V3 — Nobody to escalate to · for S2 · rescue

**The bet:** this still works for someone with no coach. But if the agent has to
hand something over, who does it hand it to?

D's actual life. Trains five times a week at home, ticks off training days on a
printed sheet, and has nobody advising him.

Every stopping rule we have ends with *give it to the coach*. Take the coach
away and out-of-policy requests, anything medical, and a confirmed undereating
day all have nowhere to go. That is a different safety design, not a tweak.

It is also **the quickest one to settle**, because it either has an answer to
that question or it does not.

**Where it got to:** on paper, one real conversation.

### V4 — The one who cooks · for S5 · translation

**The bet:** it is easier to put more protein into the dinner the family already
eats than to patch one man's plate at midnight.

M cooks for everyone, does not know what protein is, and wants to learn. She
decides what goes on every plate in that house. Nothing we have is for her.

Pass 2 gave this a nudge from an unexpected direction. One reason people said
they lost control of their eating was *"no kitchen at times and at others
relying on someone else to cook."*

**Where it got to:** on paper.

### V5 — Something for the coach · for S7 · instrumentation

**The bet:** a coach would pay to see which nights went wrong, instead of
finding out six weeks later that nothing moved.

`With the plan` bottoms out at **-45** at that six-week review. It is the lowest
point in the whole relationship, and it is where people quit. This version goes
straight at it and sells to the person whose job it is to care.

Different buyer, different price, never modelled.

Pass 2 quietly supports it. The one case of somebody being taken off tracking
was *"she told me to stop tracking my macros"* — a dietitian, not an app. The
authority here is a person.

**Where it got to:** on paper.

### V6 — Building the meal instead of fixing it · for S6 · construction

**The bet:** the hard part is not logging. It is eating enough protein without
eating more food. Build the plate for that and the number takes care of itself.

This flips V2 around. V2 asks *what do I add to what already happened*. V6 asks
*what do I make so it does not happen*. Same engine, opposite direction, and
somebody who is planning rather than repairing.

**This is what the file was missing.** Since 2026-08-26 it is the only version
where a stranger has described the problem without being asked, from
[pass 2](research/2026-08-26-gemini-findings.md):

> *"I decided I was tired of eating, and stopped tracking my calories, and just
> eating 'until full, plus a bit more and two protein shakes per day'."*

> *"I can't be bothered to log it all right now, I just slam food all day long."*

These people are not trying to eat less. They are trying to get enough protein
in without more volume, and the logging is just extra work on top of a problem
it never solves. They turned up in a subreddit we picked to catch people leaving
tracking apps, and described something else entirely.

**Where it got to:** on paper, never tested, and now better evidenced than
either of the two we built.

---

## Things we killed

These are features inside V1 and V2, not whole versions. All of them died on
paper, which is the cheap place to die.

| what | when | why |
|---|---|---|
| Letting people issue themselves an XP card | on paper | it is a clinical number. Nobody should hand it to themselves |
| A good-foods and bad-foods list | on paper | that is restriction wearing a scoring costume |
| Calling a food database live | design | the prototype should not depend on a request that can be slow, throttled, or missing the item |
| A tool that messages the coach | design | sending a message is a consequence, and consequences need a gate |
| Escalating on anger or legal talk | design | that is a support-desk pattern. He is alone at his own fridge |
| A Google Sheet for the PRD | develop | ten of twenty rows drifted apart on PlateMate. One place for the truth |

---

## What we actually know

| | evidence |
|---|---|
| V1 | nothing |
| V2 | three people you already know |
| V3 | one conversation |
| V4 | one observation, plus one quote pointing sideways at it |
| V5 | nothing direct, though the journey map and one quote both point here |
| V6 | **strangers describing it unprompted** |

Held against Maurya's timeline:

- **None of these has really cleared Customer/Problem Fit.** V2 is closest, on
  people you know, which is the weakest evidence there is.
- **Nothing has ever been killed at the Prioritize gate**, because nothing was
  put through it. The six above are features.
- **The one with the best evidence has never been tested.**

## The awkward bit

> If you test your variants sequentially, one at a time, you never actually
> compare them. You work on whichever one you happened to open, and the one you
> happened to open is usually the one you already liked.

V1 got built because it was open. V2 because it was next. V3 through V6 have
never been put beside them. And the first time real evidence walked into this
project, it landed on V6 rather than on either of the two with prototypes.

## What is open

**Pass 3 is running.** It checks S3, the never-tracked crowd that V2 and V3 both
assume exists. It is written to try to prove us wrong. If those people turn out
to be mildly curious rather than actually bothered, then Tom is not the customer
and V2 should point at S4 instead, where pass 2 already found plenty of people
who are.

The side-by-side comparison still costs an afternoon. Four versions, stress
tested on paper, next to each other. Still the cheapest move available and still
not taken.
