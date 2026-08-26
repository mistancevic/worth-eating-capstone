# Research pass 1 — tracker abandonment

**Result: zero items. Blocked at the network layer, not at the query.**

Filed anyway, because a null run with a known cause is a result, and because
the next person to try this needs to know not to.

## Timing

| | |
|---|---|
| Started | 2026-08-26T09:37:39Z |
| Engine finished | 56.4 s later |
| Recorded | 2026-08-26T09:40:02Z |
| Wall clock, end to end | about 2 min 23 s |

## What this was for

Two claims on `docs/journeys.md` are ours, not anyone else's:

1. **Before the plan** puts the deepest valley at eleven days, when he deletes
   the tracker.
2. That valley is caused by a tool that records rather than rescues, which is
   the argument the whole add-only rule rests on.

The pass was meant to find verbatims — a real quote to pin under that valley,
so three invented NPS numbers become three claims someone actually made.

## The prompt

Run as `/last30days`, on Claude Code, in this remote container.

```
people quitting food tracking apps — how many days they lasted, what
finally made them delete it, and what they did instead. Focus on
r/loseit, r/fitness, r/nutrition, r/MacroFactor, r/1200isplenty.
I want verbatim quotes, not summaries.
```

### Pre-flight

The topic is a behaviour, not a named entity, so no X handle or GitHub
resolution applied. The one real risk was the skill's Class 3 trap: nobody
writes *"I am quitting food tracking apps."* They write *"I deleted
MyFitnessPal."* So the plan was built in the community's vocabulary rather than
the question's.

Three peer subreddits were added to the five given, chosen because they are
where people land **after** quitting: `CICO`, `xxfitness`, `intuitiveeating`.

### The query plan sent to the engine

| label | search query | weight |
|---|---|---|
| primary | deleted calorie counting app stopped logging food | 1.0 |
| burnout | tracking burnout quit counting macros exhausted | 0.8 |
| instead | stopped counting calories what I do instead | 0.7 |
| duration | how long did you track before you stopped streak broke | 0.6 |

`intent: opinion` · `freshness: balanced_recent` · `cluster_mode: debate`

### The command

```bash
python3.13 ${SKILL_DIR}/scripts/last30days.py \
  "people quitting food tracking apps" \
  --emit=compact --plan "$QUERY_PLAN_FILE" \
  --subreddits=loseit,fitness,nutrition,MacroFactor,1200isplenty,CICO,xxfitness,intuitiveeating \
  --save-dir="$LAST30DAYS_MEMORY_DIR" --save-suffix=v3
```

## What came back

Nothing. Raw output preserved at
[`2026-08-26-last30days-raw.md`](2026-08-26-last30days-raw.md).

| source | items |
|---|---|
| Reddit | 0 |
| Hacker News | 0 |
| Polymarket | 0 |
| GitHub | 0 |

## Why

Not the query. **The container's egress policy refuses the hosts.** From the
agent proxy's own failure log during the run:

```
connect_rejected · gateway answered 403 to CONNECT · www.reddit.com:443
connect_rejected · gateway answered 403 to CONNECT · hn.algolia.com:443
connect_rejected · gateway answered 403 to CONNECT · gamma-api.polymarket.com:443
```

GitHub failed differently — `CERTIFICATE_VERIFY_FAILED`, because the engine's
`urllib` calls do not pick up the proxy CA bundle. That one is fixable. The
403s are not: the proxy README says plainly that a policy denial must be
reported rather than retried or routed around, so it was not retried.

X and YouTube were never in play either. No browser exists in a headless
container to read x.com cookies from, and `yt-dlp` is not installed.

**So `/last30days` cannot reach Reddit from this session at all.** That is not a
one-off and re-running it will not help.

## What this changes

My earlier recommendation was to run the verbatim pass here and send only the
quantitative questions elsewhere. That is now backwards.

**Both passes go elsewhere.** The three prompts are unchanged and still right,
but they need a tool that can reach Reddit:

- **The verbatims** — Gemini, which grounds well on Reddit, or ChatGPT. Three
  narrow passes rather than one broad one: tracker abandonment, coaching plans
  that stopped being followed, eating late because the day ran out.
- **The numbers** — deep research in either, for median days before people stop
  logging, and attrition rate and timing in paid nutrition coaching.

What this session *can* still do is `WebSearch`, which reached the open web
fine during pre-research. That is the weaker instrument for this question —
it finds articles about the behaviour, not people describing it — but it is not
nothing, and it is the fallback if running the passes elsewhere stalls.

## What stays true regardless

Nothing from any of this goes into `data/*.csv`. Research lands in `docs/` with
a citation. The synthetic rule covers the world the prototype runs on, not
whether the problem is real.

And the two claims are still unsupported. Eleven days and the six-week collapse
remain our reading, marked as such on both slides, until someone finds evidence
either way.
