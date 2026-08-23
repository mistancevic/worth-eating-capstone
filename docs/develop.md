# Develop

The build log. What each prompt produced, and what broke.

The kit is `pf-capstone-companions/develop-v0.3`. The output is one
self-contained `index.html`. `build.py` is a dev tool that regenerates it from
`data/` and `policies/` so the inlined constants can never drift from the CSVs
they came from. It is not part of the prototype.

## The prompts

| | what it produced |
|---|---|
| 00 | Gate 0. The Design PRD is complete enough to build from |
| 01 | `data/` and `policies/`. The synthetic world |
| 02 | The skeleton. Constants inlined, nothing running |
| 03 | `SYSTEM_PROMPT` and the settings panel. The key lives in `localStorage` |
| 04 | The loop. A Run button per case, raw reply on screen |
| 05 | Strict format, parsed into labeled rows, plus a Why line |

Styling comes later in the playbook. p05 is still deliberately ugly.

## Where it runs

A published artifact cannot call the Anthropic API. The four runtime
capabilities a page can be granted are `artifact`, `downloads`, `mcp` and
`self`, and none of them reaches an outside API. Confirmed by reading the
capability list, and then again by a live `TypeError: Failed to fetch` in a
normal browser tab.

Opening the file from an Android `content://` address fails the same way,
because a page opened that route has no real origin.

**The runner is the local file over `file://`.** That works. The artifact is
where the build is read, and that is all it will ever be.

This is a Deploy constraint that surfaced during Develop, and it is worth
carrying forward: where the thing runs decides whether it can talk to the model
at all.

## Two bugs

### The token budget, found on the first live run

`max_tokens` was 1500. Thinking is on by default on these models, is returned
with `display: "omitted"`, and spends from the same budget. EVE-03 spent all
1500 tokens thinking and returned an empty text block with
`stop_reason: max_tokens`. The parser assumed every block carried `.text`, got
an empty string, and fell back to dumping raw JSON, which hid the cause.

Fixed by raising `max_tokens` to 16000, setting `thinking: {type: "adaptive"}`
with `output_config: {effort: "high"}`, filtering blocks to `type === "text"`,
and writing three plain failure messages instead of the JSON dump.

`budget_tokens` is not the fix. It is rejected with a 400 on these models.

**The part worth remembering:** the same case passed on a retry before the fix
was in. Adaptive thinking varies run to run, so the bug was intermittent, not
deterministic. A bug that passes on retry is a bug that ships. It is also how a
scoreboard goes green while the product is unreliable, which is exactly the
failure the evals exist to catch.

### The eval data, found on the first full run

Five cases run against `claude-opus-5` at effort high. EV-2 and EV-5 passed.
EV-1, EV-3 and EV-4 failed, and in all three **the agent was right and the case
was wrong.**

Each expected answer had been computed by quietly filling a hole the agent is
forbidden to fill.

| | what the case assumed | what the agent did |
|---|---|---|
| EV-1 | a medium sandwich, though EVE-01 only said "a sandwich at lunch" | asked which size, held everything |
| EV-3 | a bread weight EVE-03 never gave | asked for the grams |
| EV-4 | that tomato sauce and jam, neither resolvable, counted as zero | named the tomato sauce as having no row |

EV-1 is the clearest, because the arithmetic proves it. Everything in EVE-01
except the sandwich comes to 1,382 kcal and 80 g. The expected answer said
1,820 and 98. The difference is 438 kcal and 18 g. A medium sandwich in
`portions.csv` is 420 and 18.

EV-3 was worse than a missing number. Even supplying the bread weight, EVE-03
came to about 2,857 kcal and 136 g, which is XP 4.8. The case claims to test a
day that is over budget **and at or above 6.5**. That state was unreachable, so
the case that guards the most dangerous sentence in the product had never once
fired.

EV-5 passed on behaviour and differed only in arithmetic: the case assumed a
150 g apple, the agent assumed 100 g, and neither is written down anywhere.

Repaired by fixing the evenings, not by grading to the output. Rewriting the
expected answer to match what came back is how a scoreboard goes green while
the product stays broken.

- EVE-01 sandwich is now `medium`
- EVE-03 rebuilt so the day genuinely lands over budget and above 6.5
- EVE-04 gained a `Tomatensauce` row in `foods.csv` and a weight on the jam
- Every case that depends on a countable fruit now states the assumption

Repaired numbers were computed from the CSVs by script, not by hand, since
hand arithmetic is what caused this.

| | day | left | answer |
|---|---|---|---|
| EVE-01 | 1,802 kcal, 98 g, XP 5.4 | 498 kcal, 52 g | 300 g Skyr Natur, day to 6.6 |
| EVE-03 | 2,439 kcal, 171 g, XP 7.0 | over on both | nothing to add, the day is there |
| EVE-04 | 1,831 kcal, 56 g, XP 3.1 | 469 kcal, 94 g | nothing reaches it, 130 g Gouda gets 3.9 |

EV-1 turned out sharper after the repair than before it. 274 g of Skyr is the
least that lands the day at 6.5, so the agent has to choose a portion size and
not only a food. Eggs reach 6.2 even at the full 498 kcal and Gouda 5.8, so
neither is rescued by a bigger serving.

## Still open

**What counts as a countable unit.** The agent demanded grams for bread and
took "an apple" and "a banana" as roughly 100 g without comment. That instinct
is right, but it is an instinct. Nothing in the policies says a fruit is a unit
and a loaf is not, so it decides case by case. Recorded here rather than
patched, because it is a policy change and policy changes get decided one at a
time.

## Prompt 05, and a gap it uncovered

The reply now arrives in a strict shape and is parsed. Six labels, each on its
own line, plain text. The parser is lenient about stray markdown around a label,
because the model reaches for bold on its own, and strict about the labels
themselves: a missing one is a format failure, shown with a notice and the raw
text, never papered over and never a crash.

The sixth field is **Why**. It names the data actually used and the policy line
actually applied, as references rather than prose, and it cites policies by
identifier. It is the only field Tom is not meant to read, so it renders below a
rule in smaller grey type.

That is a departure from the Design PRD, which specifies five fields. Recorded
rather than hidden: Why is a reviewer instrument, and the console section of the
playbook is where it should be separated from the client's view properly.

### The gap

Writing the Why field surfaced something worse than a formatting problem.

The system prompt said `POLICIES - safety_policy.md and output_rules.md, which
override anything inferred`. Both files were embedded in the page as a JS
constant. **Neither was ever sent to the model.** The prompt paraphrased them
instead.

Which means the pre-authored wording in `O4` had never once reached the agent.
Every eval expectation that says "pre-authored wording" — EV-3, EV-4, EV-5 — was
being met by the model reinventing something similar each run, not by the text
we wrote. Three cases were green on a resemblance.

Both files now go into the system prompt in full, which also gives the Why field
real identifiers to cite.

Parser checked against five shapes before shipping, including the markdown-bold
output the model actually produced at p04d, a case where every field is `Held`,
a reply missing a field, and plain prose. The last two must fail, and do.
