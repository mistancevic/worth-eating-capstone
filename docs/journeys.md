# The journeys

Discovery, step 4: identify user pain points.

Two maps, in the course slide's layout, plus one that is not a journey map at all
and is kept because it earns its place elsewhere.

They are consecutive. **Before the plan** ends at the moment **With the plan**
begins: he stops trying to solve it himself and pays someone.

| | file | live |
|---|---|---|
| Before the plan | [`journeys/before-the-plan.html`](journeys/before-the-plan.html) | [artifact](https://claude.ai/code/artifact/f05f7a12-084f-4e89-9378-74261e466312) |
| With the plan | [`journeys/with-the-plan.html`](journeys/with-the-plan.html) | [artifact](https://claude.ai/code/artifact/d830df48-eb3f-4ea2-8552-38026087fa09) |
| The night itself | [`journeys/the-night-itself.html`](journeys/the-night-itself.html) | [artifact](https://claude.ai/code/artifact/e48a1043-da29-45ec-a57f-c3c90bc1f35c) |

Everything is synthetic. Tom is invented, and so are the NPS figures — nobody has
surveyed him. They are our reading of how each stage feels, printed on the slide
so the shape can be argued with rather than asserted.

---

## Before the plan

He is on his own. No coach, no target, no tool.

| | |
|---|---|
| NOTICE IT | Trousers stop fitting · Reads that protein matters · Decides to sort it himself |
| FIX IT MYSELF | Buys the powder · Installs a tracker · Deletes the tracker |
| LET IT GO | Eyeballs it instead · Nothing changes · Pays for a coach |

`-30` · `28` · `52` · `38` · `-10` · **`-44`** · `6` · `-36` · `24`

### The finding

The curve peaks at **+52** the moment he decides to handle it himself, which is
the highest point anywhere in either map. He is confident, motivated, and about
to do everything right.

Eleven days later he deletes the tracker at **-44**, the deepest valley on the
map.

**That valley is not ignorance and it is not laziness.** He weighed food. He
scanned barcodes. He did exactly what the tool asked. The tool told him what he
had eaten and never once told him what to do about it, and because it never
failed visibly, the quitting felt like his failure rather than its.

That is the competitor. Not nothing, and not a worse tracker — a tracker that
works exactly as advertised and still loses him inside a fortnight.

The last stretch is quieter and worse. Eyeballing it feels fine at **+6** because
the effort is gone. Six months later, at **-36**, he cannot say whether he was
close or nowhere near, because nothing was ever counted. Trying and failing had
become indistinguishable to him.

### The three pain points

1. **The problem is invisible until it is already large.** Nothing signals
   anything is wrong until a pair of trousers does.
2. **A tracker records the day, it does not rescue it.** Highlighted, because it
   is the alternative this product replaces.
3. **Trying and failing are indistinguishable to him.** Effort with no way to
   know.

---

## With the plan

He has a coach. The relationship runs from the decision to change through to
renewing or drifting away.

| | |
|---|---|
| START MY PLAN | Decide to change · First call with coach · Plan arrives |
| LIVE MY PLAN | Shop and cook to it · The day breaks · Improvise at night |
| KEEP MY PLAN | Weigh-in day · Coach reviews · Renew or drift |

`48` · `66` · **`-12`** · `34` · **`-38`** · `-20` · `6` · **`-45`** · `-18`

### The finding

It peaks at **+66** on the first call, because someone has finally taken the
problem seriously. It falls to **-12** when the plan turns out to be an
attachment.

It collapses to **-38** the first week the day genuinely breaks — work runs
long, the children are served first, and by his turn there is no plan left to
follow, because the plan assumed a day that went as written and his never does.

The lowest point of the whole relationship is **-45** at the six-week review.
Nothing has moved, neither of them can say which nights went wrong, and so it
becomes a conversation about discipline instead of one about food. That is where
clients quit.

### The three pain points

1. **A target that lives in a document is not a target.** He read the PDF once.
2. **The plan has no answer for a broken day.** Highlighted, because this is the
   pain Worth Eating stands in.
3. **The slowest feedback loop we could have built.** The information exists at
   21:20 and arrives six weeks later.

---

## The night itself

Not a journey map. It is one Tuesday, hour by hour, and I built it first by
mistake when the ask was for a journey — a meal timeline is not a journey, and
it had grams on an emotional axis, which is two units on one scale.

Kept, because as a *day* it does something neither map does: every calorie and
gram is read from the same `foods.csv` and `portions.csv` the prototype runs on,
so it and the build cannot drift apart.

| time | what | kcal | protein | running |
|---|---|---|---|---|
| 06:40 | Coffee with milk | 60 | 3.0 | 3.0 |
| 13:10 | A sandwich at the desk, medium | 420 | 18.0 | 21.0 |
| 17:45 | 200 g Nudeln gekocht, off the children's plate | 316 | 11.6 | 32.6 |
| 21:35 | 50 g Vollkornbrot and 40 g Gouda 48% jung | 252 | 13.5 | 46.1 |

**1,048 kcal of 2,300. 46.1 g of 150. XP 4.4.**

The detail worth keeping: the 21:35 feeding carries **13.5 g** against a 26 g
meal trigger. He has eaten, he feels he has eaten, and the day moves from 33 g
to 46 g. That failure hides, because it does not feel like skipping a meal — he
did not skip a meal.

---

## What these change

Nothing in the build yet. They are Discovery evidence and they belong to
`docs/discovery-prd.md`, which they support rather than replace.

Two things they surface that were not written down anywhere before:

**Neither of these has outside evidence yet.** The first attempt to find some
ran on 2026-08-26 and returned zero items, because this container's egress
policy refuses Reddit. See
[`research/2026-08-26-tracker-abandonment.md`](research/2026-08-26-tracker-abandonment.md).
Eleven days and the six-week collapse remain our reading until that changes.

**The competitor is a working tracker, not a missing one.** That belongs in the
problem framing, and it sharpens why the only output shape is an addition: a
record tells him what happened, an addition tells him what to do.

**The six-week review is where the client is actually lost.** The nightly metric
we chose — nights he is not hungry at eleven — is a proxy for surviving that
review. Worth stating explicitly rather than leaving implied.
