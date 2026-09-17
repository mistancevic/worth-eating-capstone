#!/usr/bin/env python3
"""Generates index.html from data/ and policies/.

A dev tool, not part of the prototype. index.html stays the single
self-contained file the kit asks for; this script exists so the inlined
constants can never drift from the CSVs they came from.

It writes the same file twice: index.html, which is always the newest
build, and builds/<BUILD>.html, which is frozen. GitHub Pages serves both,
so an old build can be reopened instead of rebuilt from memory.
"""
import csv, json, os, re

BUILD = 'p10'

def rows(p): return list(csv.DictReader(open(p)))

FOODS   = rows('data/foods.csv')
PORTIONS= rows('data/portions.csv')
HISTORY = rows('data/history.csv')
EVENINGS= rows('data/evenings.csv')
EVALS   = rows('data/eval_cases.csv')
POLICIES= {'safety_policy.md': open('policies/safety_policy.md').read(),
           'output_rules.md' : open('policies/output_rules.md').read()}
# Every rule identifier that actually exists, read out of the two policy files
# rather than typed here, so it cannot drift from them. A citation is resolved
# against this: a hallucinated S7 has nowhere to land.
RULES = {}
for _fn, _text in POLICIES.items():
    for _m in re.finditer(r'^## ([SO]\d+)\s*[\u00b7.-]\s*(.+)$', _text, re.M):
        RULES[_m.group(1)] = {'title': _m.group(2).strip(), 'file': _fn}

CARD = {"name":"Tom","kcal":2300,"protein_g":150,"xp":6.5,
        "meal_trigger_g":26,"fat_min_g":55,"fibre_g":32,"flex_kcal":230}

SYSTEM_PROMPT = """ROLE
The agent is hired to name what to add to a late meal so Tom reaches his coach's protein target, within the coach's numbers and a rule that it may only ever add food, escalating when the message is not about food, when the day's intake is far below target, or when it is not confident.

CONTEXT
Use only the embedded constants. Never invent a fact, a food, or a number.
  CARD      - Tom's card, issued by his coach: 2300 kcal, 150 g protein, Personal XP 6.5, meal trigger 26 g, fat minimum 55 g, fibre 32 g, and a flex of 230 kcal either side of the calorie budget. Never recalculate any of it.
  FOODS     - named products, one row each, sent whole. kcal_per_100g, protein_g_per_100g, fat_g_per_100g, fibre_g_per_100g and xp are per 100 g. max_serving_g is the most of that food a person eats in one sitting, in grams, and is a hard ceiling on what you may name. unit_g is the weight of one of them where the food is countable - one banana, one egg - and is blank where it is not. note carries anything that matters about the product and overrides a generic assumption. A food not in FOODS has no numbers.
  PORTIONS  - composite foods in three sizes. Used to resolve a description, never to guess.
  HISTORY   - the last seven days as date, kcal, protein. Used to compute room. Never used to comment.
  POLICIES  - safety_policy.md and output_rules.md, which override anything inferred.

XP is protein divided by calories times one hundred. It is a density, not a total. Scoring 6.5 on a plate only reaches 150 g if the day also lands near 2300 kcal, so both are tracked.

RULES - the agent must not:
  - suggest removing anything, eating less, skipping anything, saving calories, or making up for anything. The only action it may ever name is adding food.
  - give a verdict on a food. A low score means the plate needs a partner.
  - report an XP on the undereating path.
  - write any sentence that could be read as "do not eat".
  - comment on a streak, a trend, or a comparison to yesterday. History is used to compute, never to comment.
  - invent a target, or estimate a product that is not in FOODS.
  - diagnose anything.
  - push, notify, or speak unprompted.

OUTPUT
Exactly these six labeled fields, in this order, and nothing else. Each field begins on its own line with the label written exactly as shown, then a colon and a space. Plain text only: no markdown, no asterisks, no bold, no bullets, no headings, no blank line between the label and its text.
  Today:      protein of target, kcal of budget, and the score against his 6.5
              When a named food has no row in FOODS and the day cannot be totalled, Today still carries what IS confirmed: the resolved items with their kcal and protein, their subtotal, and the word incomplete. No score - a score on a partial day is a lie. Do not make him wait for a number he can already have.
              On the undereating path Today stays a dash. That path is a stop, and arithmetic on screen turns a stop into a calculation.
              A dash otherwise means nothing at all is known.

COUNTABLE FOODS
When he names a food by count rather than weight - "a banana", "two eggs", "an apple" - multiply unit_g by the count. Do not estimate a weight of your own; the column exists so the same sentence resolves the same way every night.
A food named by count with no unit_g and no weight is MISSING DATA. Ask, do not guess.
  Left:       protein and kcal remaining
  Add:        one item from what he actually has, with grams, kcal, its own XP, and whether it clears the 26 g meal trigger
  After that: the day re-scored with the addition included
  Note:       usually empty
  Why:        one line for the reviewer, never for Tom
  Status:     OK, HELD, or REFUSED-ESCALATE - decided last, after the work

STATUS is the boundary made visible. Exactly one of:
  OK                        an answer was given. This includes a night with nothing to add, because a finished day is an answer.
  HELD - <rule>             stopped and asked one question. Nothing has been escalated yet. Use for S1 and S2, and for the first response on S5.
  REFUSED-ESCALATE - <rule> refused and handed to the coach with no gate. Use for S3, S4, and a confirmed S5.
Name the rule by identifier and add a short reason, for example: REFUSED-ESCALATE - S4 medical symptoms reported.
What each status does to the fields:
  OK                        every field speaks normally.
  REFUSED-ESCALATE          Today, Left, Add and After that are ALL dashes. Only Note and Why speak. A score printed beside "I have been dizzy since lunch" is grotesque, and on an out-of-policy request the arithmetic IS the reduced answer the policy forbids.
  HELD - S2                 Today keeps the confirmed partial, marked incomplete, with no score. Left, Add and After that are dashes.
  HELD - S1 or S5           Today, Left, Add and After that are all dashes. On S1 you cannot tell what the food was; on S5 arithmetic on screen turns a stop into a calculation.
The agent never proceeds with a reduced answer.
A request the coach owns is refused even when the rest of the message is ordinary food. Do not answer the food half and refuse the other.

WHY is the only field Tom is not meant to read, and it is the only place a reference belongs. Name the data you actually used and the policy line you actually applied, as short references separated by semicolons. Not prose, not an explanation of your thinking, no apology, and never addressed to Tom. Cite policies by identifier: S1 to S5 from the safety policy, O1 to O5 from the output rules. Shape:
  Why: FOODS Skyr Natur 11 g/100 g; PORTIONS Sandwich medium; fit check 4/4; portion closes gap in full; O2.
Every reference must RESOLVE. Name a food or a portion exactly as it is written in FOODS or PORTIONS, character for character, because the page looks each one up and shows a tag that is red when it finds nothing. Cite a rule only by an identifier that exists in the two policy files: S1 to S5 and O1 to O5, and nothing else. If you want to say something no rule covers, say it in words rather than inventing an identifier for it. A citation nobody can follow is worse than no citation, because it looks like grounding.

Why ends with a fixed tail: two spaces, then `applied:` and the identifiers of the rules that ACTUALLY FIRED, comma separated, or `applied: none`. A rule you checked and found clear does not go in the tail; say that in the prose part instead. The tail is read by the page, so it must end that LINE and contain nothing but identifiers.
  Why: FOODS Skyr Natur 11 g/100 g; fit check 4/4; S5 clear at 78% of target  applied: O1, O2

The tail ends the Why line. It does not end the reply. **Why is never the last field. Status always follows it on the next line, and the last line of every reply is Status.** A reply that stops after Why is incomplete and will be rejected.

A field with nothing to say still appears, with a dash after the colon. Never omit a label.

A candidate for Add must pass four tests: it closes the protein gap, it stays inside the calories left, it carries at least 26 g of protein, and the day lands at or above 6.5 once it is included. Fail any one and try the next candidate.

PORTION - the size is part of the answer, not an afterthought:
  - Name the portion that closes the gap in full, not the smallest one that clears the tests.
  - If no portion closes the gap in full inside the calories left, name the largest that does fit and still passes the other three tests, and say plainly how much protein is still short.
  - In the same line, name the least that still lands the day at or above 6.5, worded as a fallback for a night when the full portion is more than he wants.
  - If the two come out the same, name one.
  - Never name more than max_serving_g of a food. That column is the most of it a person eats in one sitting, and a number above it is arithmetic rather than an answer. 675 g of egg is eleven eggs and nobody eats eleven eggs.
  - When max_serving_g will not close the gap, name max_serving_g ITSELF, not some smaller amount that feels more reasonable. The cap is already the judgement about what is reasonable; shading it down again just underfeeds him twice. Then say plainly how much protein is still short. A short honest answer beats a complete impossible one.
Both figures are additions. Never word the fallback as eating less, saving calories, cutting back, or making up for anything.

ROUNDING
Name a portion he could put on a kitchen scale: round to the nearest 5 g, and to the nearest 10 g above 200 g. Round DOWN wherever rounding up would break a ceiling, whether that ceiling is max_serving_g or the calories he has left. 445 kcal of Gouda inside 451 left is an answer; 452 is not.
Round everything else to whole grams and whole calories. Then make the printed numbers agree with each other: if you say the day lands at 88 g of 150, the shortfall you name is 62 g, not 63. Derive each figure from the one you printed, never from the unrounded number behind it, or the reply contradicts itself inside a single sentence.

Fat and fibre are minimums, not fields. They break ties between candidates that already pass. In Note, measure both against the day as it will stand AFTER the addition, and name EVERY minimum that day still misses, not the first one you reach. Two missed minimums is two sentences. Reporting one of two is worse than reporting neither, because it reads as though the other was checked and cleared.

WHERE THE DAY LANDS ON CALORIES
Protein is the target; calories are the other half of it, and the score cannot see them. XP is a density, so a day can reach 150 g of protein and still leave him hundreds of calories short, and the score will read beautifully while he goes to bed underfed.

So after the addition, compare the day's calories to the budget:
  - Inside the flex either way: nothing to say.
  - More than the flex below the budget: say it in Note, as a plain statement of how much room is left. "That still leaves you around 600 under your 2,300" is a fact about the day, not an instruction, and there is nothing to do about it tonight beyond knowing.
  - Where two candidates both pass all four tests, prefer the one that brings the day closer to the budget.
Never turn this into a demand, a target to hit, or a reason to eat more than he wants. It is information he is entitled to, not a second goal.

ESCALATION
Stop, state the reason, and hand to the coach when:
  - LOW CONFIDENCE: it cannot tell what a food was. Say so, ask one question, do not guess.
  - MISSING DATA: no target, or a named food with no row in FOODS. Ask. Never invent. A vague fridge is this case with nothing named: ask once for one specific thing, then stop.
  - OUT OF POLICY: a meal plan, a diet, a change to the target, or anything else the coach owns. Refuse, point at the coach.
  - HIGH STAKES: anything medical. Stop. Coach or doctor.
  - APPARENT INTAKE FAR BELOW REQUIREMENT: fire under 25% of the calorie target whatever was described; between 25% and 50% only when fewer than three foods or portions were separately named; never at or above 50%. A food named inside a combination counts separately. Ask once, "is that everything today". Only escalate if confirmed. Report no XP on this path. A light day that is honestly described is a day with room, not a safety event.

Anger or legal language is not a trigger here. It is a support-desk pattern and this client is alone at his own fridge. Dropped deliberately.

WORDING
Every sentence on a stopping path is pre-authored in output_rules.md. Use it as written.

POLICIES - the full text of both files follows. It overrides anything inferred above.

--- safety_policy.md ---
""" + POLICIES["safety_policy.md"] + """
--- output_rules.md ---
""" + POLICIES["output_rules.md"]

HTML = r"""<!doctype html>
<html lang="en" data-skin="ops">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Worth Eating &mdash; build __BUILD__</title>
<style>
/* ═══════════════════════════════════════════════════════════════════
   AGENTIC AI CAPSTONE — LOCKED DESIGN TOKENS  v0.3
   The look ships in the box. Nobody chooses a font.

   RULES (for the AI building the prototype):
   - Inline this file into index.html. Use ONLY these tokens.
   - No new colors. No new fonts. No emoji as icons.
   - Skins switch by setting data-skin="ops" | "studio" | "term" on <html>.
   - Never render body text below 13px (--fs-0).
   ═══════════════════════════════════════════════════════════════════ */

:root {
  /* type */
  --font-ui: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --font-mono: ui-monospace, "SF Mono", SFMono-Regular, Menlo, Consolas, monospace;
  --fs-0: 13px;  /* meta, log lines — absolute floor */
  --fs-1: 14px;  /* body */
  --fs-2: 16px;  /* emphasized body, buttons */
  --fs-3: 20px;  /* panel titles */
  --fs-4: 28px;  /* page title, stat numbers */
  --lh: 1.5;

  /* spacing & shape */
  --sp-1: 4px; --sp-2: 8px; --sp-3: 12px; --sp-4: 16px; --sp-5: 24px; --sp-6: 32px;
  --radius: 10px;
  --radius-sm: 6px;
  --border-w: 1px;

  /* status colors — shared across all skins */
  --ok: #1FA971;        /* pass / approved */
  --warn: #D98E04;      /* needs work / pending */
  --danger: #D64545;    /* fail / escalate / refused */
  --info: #3B82F6;      /* running / info */
}

/* ── SKIN: OPERATIONS (dark) — default ─────────────────────────── */
:root, [data-skin="ops"] {
  --bg: #0F1420;         /* page */
  --bg-raise: #171E2E;   /* panels, cards */
  --bg-inset: #0B0F18;   /* wells, log */
  --line: #263049;       /* borders */
  --ink: #E8EDF7;        /* headings, primary text */
  --ink-2: #9AA6BF;      /* secondary text */
  --ink-3: #5E6A85;      /* meta */
  --accent: #6C8CFF;     /* brand accent: buttons, active states */
  --accent-ink: #FFFFFF; /* text on accent */
  --chip: #1E2740;       /* tags, chips */
  --shadow: 0 1px 2px rgba(0,0,0,.4), 0 12px 32px -12px rgba(0,0,0,.55);
  --font-body: var(--font-ui);
}

/* ── SKIN: STUDIO (light) ──────────────────────────────────────── */
[data-skin="studio"] {
  --bg: #F6F7FB;
  --bg-raise: #FFFFFF;
  --bg-inset: #EEF0F6;
  --line: #E1E5EF;
  --ink: #131A2A;
  --ink-2: #4C5670;
  --ink-3: #8B93A9;
  --accent: #4056C9;
  --accent-ink: #FFFFFF;
  --chip: #EDF0FA;
  --shadow: 0 1px 2px rgba(19,26,42,.06), 0 12px 28px -14px rgba(19,26,42,.18);
  --font-body: var(--font-ui);
}

/* ── SKIN: TERMINAL (mono) ─────────────────────────────────────── */
[data-skin="term"] {
  --bg: #0C0F0C;
  --bg-raise: #121712;
  --bg-inset: #080B08;
  --line: #223122;
  --ink: #D7F5DC;
  --ink-2: #8FBE97;
  --ink-3: #567A5D;
  --accent: #35D07F;
  --accent-ink: #06130A;
  --chip: #16301E;
  --shadow: 0 0 0 1px rgba(53,208,127,.08), 0 12px 32px -14px rgba(0,0,0,.7);
  --font-body: var(--font-mono);
}

/* ═══ BASE ═══ */
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--ink);
  font-family: var(--font-body); font-size: var(--fs-1); line-height: var(--lh);
}

/* ═══ LAYOUT ═══ */
.topbar {
  display: flex; align-items: center; gap: var(--sp-3);
  padding: var(--sp-3) var(--sp-5);
  background: var(--bg-raise); border-bottom: var(--border-w) solid var(--line);
}
.topbar .product { font-size: var(--fs-2); font-weight: 700; letter-spacing: .01em; }
.topbar .meta { color: var(--ink-3); font-size: var(--fs-0); margin-left: auto; }

.console {
  display: grid; grid-template-columns: 300px 1fr 320px;
  gap: var(--sp-4); padding: var(--sp-4); align-items: start;
  min-height: calc(100vh - 58px);
}
@media (max-width: 1100px) { .console { grid-template-columns: 1fr; } }

.panel {
  background: var(--bg-raise); border: var(--border-w) solid var(--line);
  border-radius: var(--radius); box-shadow: var(--shadow);
}
.panel-head {
  padding: var(--sp-3) var(--sp-4); border-bottom: var(--border-w) solid var(--line);
  font-size: var(--fs-0); font-weight: 700; letter-spacing: .12em; text-transform: uppercase;
  color: var(--ink-2);
}
.panel-body { padding: var(--sp-4); }

/* ═══ STAGE LABELS — the loop, named on screen ═══ */
.stage {
  display: inline-flex; align-items: center; gap: var(--sp-2);
  font-size: var(--fs-0); font-weight: 700; letter-spacing: .14em; text-transform: uppercase;
  color: var(--accent); margin: var(--sp-4) 0 var(--sp-2);
}
.stage::before {
  content: attr(data-n); display: inline-flex; align-items: center; justify-content: center;
  width: 20px; height: 20px; border-radius: 50%;
  background: var(--accent); color: var(--accent-ink);
  font-size: 11px; letter-spacing: 0;
}

/* ═══ CARDS (case list) ═══ */
.case-card {
  padding: var(--sp-3) var(--sp-4); border: var(--border-w) solid var(--line);
  border-radius: var(--radius-sm); background: var(--bg-raise);
  cursor: pointer; margin-bottom: var(--sp-2);
}
.case-card:hover { border-color: var(--accent); }
.case-card.active { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent) inset; }
.case-card .id { font-family: var(--font-mono); font-size: var(--fs-0); color: var(--ink-3); }
.case-card .title { font-weight: 600; }

/* ═══ CHIPS (one-click demo cases, citations) ═══ */
.chip {
  display: inline-flex; align-items: center; gap: var(--sp-1);
  padding: 4px 12px; border-radius: 999px;
  background: var(--chip); color: var(--ink-2);
  border: var(--border-w) solid var(--line);
  font-size: var(--fs-0); font-weight: 600; cursor: pointer;
}
.chip:hover { color: var(--ink); border-color: var(--accent); }
.chip.cite { cursor: default; font-family: var(--font-mono); }

/* ═══ OUTPUT FIELDS — labeled, judgeable in under a minute ═══ */
.field { display: grid; grid-template-columns: 160px 1fr; gap: var(--sp-3); padding: var(--sp-2) 0; border-bottom: var(--border-w) solid var(--line); }
.field:last-child { border-bottom: 0; }
.field .k { font-size: var(--fs-0); font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--ink-3); padding-top: 2px; }
.field .v { color: var(--ink); }
.field .v.why { color: var(--ink-2); font-style: italic; }

/* ═══ STATUS BADGES ═══ */
.badge {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 3px 10px; border-radius: 999px;
  font-size: var(--fs-0); font-weight: 700; letter-spacing: .04em;
}
.badge::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: currentColor; }
.badge.ok      { color: var(--ok);     background: color-mix(in srgb, var(--ok) 14%, transparent); }
.badge.warn    { color: var(--warn);   background: color-mix(in srgb, var(--warn) 14%, transparent); }
.badge.danger  { color: var(--danger); background: color-mix(in srgb, var(--danger) 14%, transparent); }
.badge.info    { color: var(--info);   background: color-mix(in srgb, var(--info) 14%, transparent); }
.badge.neutral { color: var(--ink-2);  background: var(--chip); }

/* ═══ BUTTONS — the human gate ═══ */
.btn {
  display: inline-flex; align-items: center; gap: var(--sp-2);
  padding: 8px 18px; border-radius: var(--radius-sm);
  border: var(--border-w) solid var(--line);
  background: var(--bg-raise); color: var(--ink);
  font-family: var(--font-body); font-size: var(--fs-1); font-weight: 700;
  cursor: pointer;
}
.btn:hover { border-color: var(--accent); }
.btn:disabled { opacity: .45; cursor: not-allowed; }
.btn.primary { background: var(--accent); border-color: var(--accent); color: var(--accent-ink); }
.btn.approve { background: var(--ok); border-color: var(--ok); color: #fff; }
.btn.danger  { background: transparent; border-color: var(--danger); color: var(--danger); }
.btn.danger:hover { background: var(--danger); color: #fff; }

/* ═══ THE BOUNDARY LINE — quiet, permanent ═══ */
.boundary-note {
  font-size: var(--fs-0); color: var(--ink-3);
  border-left: 2px solid var(--accent); padding-left: var(--sp-3);
  margin-top: var(--sp-3);
}

/* ═══ RUN LOG ═══ */
.log {
  background: var(--bg-inset); border: var(--border-w) solid var(--line);
  border-radius: var(--radius-sm); padding: var(--sp-3);
  font-family: var(--font-mono); font-size: var(--fs-0);
  max-height: 420px; overflow: auto;
}
.log .row { display: flex; gap: var(--sp-3); padding: 3px 0; color: var(--ink-2); }
.log .row .t { color: var(--ink-3); flex: none; }
.log .row .action-approve  { color: var(--ok); }
.log .row .action-edit     { color: var(--warn); }
.log .row .action-escalate { color: var(--danger); }

/* ═══ EVALS ═══ */
.evals-table { width: 100%; border-collapse: collapse; font-size: var(--fs-1); }
.evals-table th {
  text-align: left; font-size: var(--fs-0); letter-spacing: .1em; text-transform: uppercase;
  color: var(--ink-3); padding: var(--sp-2) var(--sp-3); border-bottom: var(--border-w) solid var(--line);
}
.evals-table td { padding: var(--sp-3); border-bottom: var(--border-w) solid var(--line); vertical-align: top; }

.scoreboard { display: flex; gap: var(--sp-4); margin-bottom: var(--sp-4); }
.stat {
  flex: 1; padding: var(--sp-4); text-align: center;
  background: var(--bg-raise); border: var(--border-w) solid var(--line); border-radius: var(--radius);
}
.stat .n { font-size: var(--fs-4); font-weight: 800; line-height: 1.1; }
.stat .l { font-size: var(--fs-0); letter-spacing: .1em; text-transform: uppercase; color: var(--ink-3); }
.stat.ok .n { color: var(--ok); } .stat.warn .n { color: var(--warn); } .stat.danger .n { color: var(--danger); }

/* ═══ STATES ═══ */
.thinking { display: inline-flex; align-items: center; gap: var(--sp-2); color: var(--info); font-weight: 600; }
.thinking::before { content: ""; width: 12px; height: 12px; border: 2px solid var(--info); border-top-color: transparent; border-radius: 50%; animation: spin .8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.empty {
  padding: var(--sp-6); text-align: center; color: var(--ink-2);
}
.empty .headline { font-size: var(--fs-3); font-weight: 700; color: var(--ink); margin-bottom: var(--sp-2); }

.error-note {
  padding: var(--sp-3) var(--sp-4); border-radius: var(--radius-sm);
  border: var(--border-w) solid var(--danger);
  background: color-mix(in srgb, var(--danger) 8%, transparent);
  color: var(--danger); font-size: var(--fs-1);
}

/* ═══ Worth Eating: behaviour classes, expressed only in the tokens above ═══ */
.topbar .product { color: var(--ink); }
.topbar .meta code { font-family: var(--font-mono); color: var(--ink-2); }
.console { align-items: start; }
.case-card .sub { color: var(--ink-2); font-size: var(--fs-0); margin-top: 2px; }
.case-card .badge { margin-top: var(--sp-2); }
.case-panel { display: none; }
.case-panel.selected { display: block; }
.case-panel h3 { margin: 0 0 var(--sp-2); font-size: var(--fs-3); }
.case-panel h3 .day { color: var(--ink-2); font-weight: 400; font-size: var(--fs-1); }
.lbl { font-size: var(--fs-0); text-transform: uppercase; letter-spacing: .08em; color: var(--ink-3);
       font-weight: 700; margin-top: var(--sp-3); }
.expect { color: var(--ink-2); font-size: var(--fs-1); }
.out { margin-top: var(--sp-4); border-top: var(--border-w) solid var(--line); padding-top: var(--sp-3); }
.err { padding: var(--sp-3) var(--sp-4); border-radius: var(--radius-sm);
       border: var(--border-w) solid var(--danger);
       background: color-mix(in srgb, var(--danger) 8%, transparent); color: var(--ink); font-size: var(--fs-1); }
.err b { color: var(--danger); }
.busy { display: inline-flex; align-items: center; gap: var(--sp-2); color: var(--info); font-weight: 600; }
.busy::before { content: ""; width: 12px; height: 12px; border: 2px solid var(--info);
                border-top-color: transparent; border-radius: 50%; animation: spin .8s linear infinite; }
pre { white-space: pre-wrap; font-family: var(--font-mono); font-size: var(--fs-0);
      background: var(--bg-inset); border: var(--border-w) solid var(--line);
      border-radius: var(--radius-sm); padding: var(--sp-3); overflow-x: auto; color: var(--ink-2); }
code { font-family: var(--font-mono); background: var(--chip); padding: 0 4px; border-radius: 4px; }
.wrap { overflow-x: auto; }
table { border-collapse: collapse; font-size: var(--fs-0); width: 100%; }
td, th { border-bottom: var(--border-w) solid var(--line); padding: var(--sp-2) var(--sp-2);
         text-align: left; vertical-align: top; }
th { font-size: var(--fs-0); letter-spacing: .1em; text-transform: uppercase; color: var(--ink-3); }

/* the answer, then the fields */
.headline { font-size: var(--fs-2); line-height: 1.4; margin: var(--sp-2) 0 var(--sp-3); color: var(--ink); }
dl.fields { margin: 0; }
dl.fields dt, dl.fields dd { margin: 0; }
dl.fields dt { font-size: var(--fs-0); font-weight: 700; letter-spacing: .08em; text-transform: uppercase;
               color: var(--ink-3); padding-top: var(--sp-2); }
dl.fields dd { padding: 2px 0 var(--sp-2); border-bottom: var(--border-w) solid var(--line); color: var(--ink); }
dl.fields dd:last-of-type { border-bottom: 0; }
dl.fields dd textarea { width: 100%; box-sizing: border-box; font: inherit; font-size: var(--fs-1);
               padding: var(--sp-2); min-height: 2.8em; background: var(--bg-inset); color: var(--ink);
               border: var(--border-w) solid var(--line); border-radius: var(--radius-sm); }
.edited-flag { font-size: var(--fs-0); text-transform: uppercase; letter-spacing: .06em; color: var(--warn); }
.followed { font-size: var(--fs-0); text-transform: uppercase; letter-spacing: .06em; color: var(--ink-3);
            margin: var(--sp-1) 0 var(--sp-2); }

/* citations: fired, checked, record, unresolved */
.cites { margin-top: var(--sp-3); }
.cite { display: inline-flex; padding: 2px 10px; margin: 0 var(--sp-1) var(--sp-1) 0; border-radius: 999px;
        font-family: var(--font-mono); font-size: var(--fs-0); border: var(--border-w) solid var(--line);
        background: var(--chip); color: var(--ink-2); }
.cite.ok  { color: var(--ok); border-color: var(--ok); background: color-mix(in srgb, var(--ok) 12%, transparent); font-weight: 700; }
.cite.off { color: var(--ink-3); }
.cite.rec { color: var(--ink-2); }
.cite.bad { color: var(--danger); border-color: var(--danger); background: color-mix(in srgb, var(--danger) 10%, transparent); font-weight: 700; }
.cites .err { margin-top: var(--sp-2); font-size: var(--fs-0); }

details.whybox { margin-top: var(--sp-3); border-top: var(--border-w) solid var(--line); padding-top: var(--sp-2); }
details.whybox summary { cursor: pointer; font-size: var(--fs-0); letter-spacing: .08em; text-transform: uppercase;
                         color: var(--ink-3); font-weight: 700; }
details.whybox .whytext { color: var(--ink-2); font-size: var(--fs-0); margin-top: var(--sp-2); font-family: var(--font-mono); }

/* the second turn: predefined answers only */
.replybox { margin-top: var(--sp-3); border-top: var(--border-w) dashed var(--warn); padding-top: var(--sp-3); }
.replybox .btn { margin: 0 var(--sp-2) var(--sp-2) 0; }
.replybox .cannot { color: var(--ink-2); font-size: var(--fs-0); margin: var(--sp-1) 0 0; }

/* the gate */
.gate { margin-top: var(--sp-4); border-top: var(--border-w) solid var(--line); padding-top: var(--sp-3); }
.gate .lbl { margin: 0 0 var(--sp-2); }
.gate .btn { margin: 0 var(--sp-2) var(--sp-2) 0; }
.verdict { display: inline-flex; align-items: center; gap: 6px; padding: 3px 10px; border-radius: 999px;
           font-size: var(--fs-0); font-weight: 700; letter-spacing: .04em; }
.verdict::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: currentColor; }
.verdict.approved, .verdict.continued, .verdict.ok { color: var(--ok); background: color-mix(in srgb, var(--ok) 14%, transparent); }
.verdict.edited, .verdict.pending, .verdict.held   { color: var(--warn); background: color-mix(in srgb, var(--warn) 14%, transparent); }
.verdict.escalated, .verdict.refused                { color: var(--danger); background: color-mix(in srgb, var(--danger) 14%, transparent); }
.verdict.replaced, .verdict.reopened, .verdict.unknown { color: var(--ink-2); background: var(--chip); }
.reason { font-size: var(--fs-1); color: var(--ink-2); margin-top: var(--sp-2); }
.escbox input { width: 100%; max-width: 26rem; padding: var(--sp-2); font: inherit; font-size: var(--fs-1);
                background: var(--bg-inset); color: var(--ink); border: var(--border-w) solid var(--line);
                border-radius: var(--radius-sm); }

/* status badge on a result */
.status { display: inline-flex; align-items: center; gap: 6px; padding: 3px 10px; border-radius: 999px;
          font-size: var(--fs-0); font-weight: 700; letter-spacing: .04em; margin: var(--sp-2) 0; }
.status::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: currentColor; }
.status.ok      { color: var(--ok);     background: color-mix(in srgb, var(--ok) 14%, transparent); }
.status.held    { color: var(--warn);   background: color-mix(in srgb, var(--warn) 14%, transparent); }
.status.refused { color: var(--danger); background: color-mix(in srgb, var(--danger) 14%, transparent); }
.status.unknown { color: var(--ink-2);  background: var(--chip); }

/* the right rail */
.rail-note { color: var(--ink-2); font-size: var(--fs-0); margin: 0 0 var(--sp-3); }
#sweep { font-size: var(--fs-1); margin: var(--sp-2) 0; }
.swnote { color: var(--ink-2); font-size: var(--fs-0); }
.swfail { color: var(--danger); font-size: var(--fs-0); }
#logsum { font-size: var(--fs-0); color: var(--ink-2); margin: var(--sp-2) 0; }
#logsum b { color: var(--ink); font-variant-numeric: tabular-nums; }
.log table td { font-size: var(--fs-0); color: var(--ink-2); border-bottom-color: var(--line); }
.log table td.t { white-space: nowrap; font-variant-numeric: tabular-nums; color: var(--ink-3); }
.settings input[type=password] { width: 100%; padding: var(--sp-2); font-family: var(--font-mono);
        font-size: var(--fs-1); background: var(--bg-inset); color: var(--ink);
        border: var(--border-w) solid var(--line); border-radius: var(--radius-sm); margin-bottom: var(--sp-2); }
.settings .btn { margin-right: var(--sp-2); }
#keystate { font-size: var(--fs-0); color: var(--ink-2); margin-top: var(--sp-2); }

/* everything the agent was given, out of the way */
details.reference { margin: 0 var(--sp-4) var(--sp-6); }
details.reference > summary { cursor: pointer; color: var(--ink-2); font-size: var(--fs-0);
        letter-spacing: .1em; text-transform: uppercase; font-weight: 700; padding: var(--sp-3) 0; }
details.reference h2 { font-size: var(--fs-2); margin: var(--sp-5) 0 var(--sp-2); }
details.reference p { color: var(--ink-2); max-width: 70ch; }
details.reference ul { color: var(--ink-2); }
</style>
</head>
<body>
<div class="topbar">
  <span class="product">Worth Eating</span>
  <span class="verdict" id="keybadge">checking&hellip;</span>
  <span class="meta">build <code>__BUILD__</code> &middot; <span id="modelmeta"></span></span>
</div>

<div class="console">
  <aside class="panel">
    <div class="panel-head">Cases</div>
    <div class="panel-body" id="caselist"></div>
  </aside>

  <main class="panel">
    <div class="panel-head">Work area</div>
    <div class="panel-body" id="cases"></div>
  </main>

  <aside class="panel">
    <div class="panel-head">Run log</div>
    <div class="panel-body">
      <p class="rail-note">Every run lands here the moment it returns, marked
      <b>awaiting review</b>, and stays that way until somebody approves, edits or
      escalates it. A log that only listed decided runs would hide the one case
      nobody looked at.</p>
      <p><button class="btn primary" id="runall">Run all graded cases</button>
      <button class="btn" id="stopall" hidden>Stop</button></p>
      <p id="sweep"></p>
      <p id="logsum"></p>
      <div class="log"><table id="log"></table></div>
      <p class="lbl" style="margin-top:var(--sp-3)">This session only. A reload restores it; closing the tab clears it.</p>

      <div class="panel-head" style="margin:var(--sp-5) calc(-1 * var(--sp-4)) var(--sp-3); border-top:var(--border-w) solid var(--line)">Settings</div>
      <div class="settings">
        <p class="rail-note">Anthropic API key. Stored in this browser only, never written into the page.</p>
        <input type="password" id="apikey" placeholder="sk-ant-..." autocomplete="off" spellcheck="false">
        <p><button class="btn" id="save">Save key</button><button class="btn" id="clear">Clear key</button></p>
        <p id="keystate">checking&hellip;</p>
      </div>
    </div>
  </aside>
</div>

<details class="reference">
<summary>What the agent was given, and how this page got here</summary>

<h2>System prompt</h2>
<p>The <code>SYSTEM_PROMPT</code> constant, printed so the rules can be read rather than trusted.</p>
<details><summary>show</summary><pre id="sysprompt"></pre></details>

<h2>Client card &mdash; <code>client_profile.md</code></h2>
<div id="card"></div>

<h2>Policy files loaded</h2>
<ul id="policies"></ul>

<h2>What loaded</h2>
<table id="counts"></table>

<h2>Cases and evenings</h2>
<p>Two kinds of id, and they are not the same thing. <b>CASE-n</b> is an eval
case in <code>eval_cases.csv</code>: an expected answer. <b>EVE-nn</b> is an
evening in <code>evenings.csv</code>: an input. A case points at an evening, and
the Run button lives on the evening.</p>
<div class="wrap" id="caseindex"></div>

<h2>History &mdash; <code>history.csv</code></h2>
<div class="wrap"><table id="hist"></table></div>

<h2>Foods &mdash; <code>foods.csv</code></h2>
<div class="wrap"><table id="foods"></table></div>

<h2>Portions &mdash; <code>portions.csv</code></h2>
<div class="wrap"><table id="ports"></table></div>

<h2>Build notes, newest first</h2>
<p>Prompt 07: a person has to sign off. Under every answer are three buttons
&mdash; Approve, Edit, Escalate &mdash; and nothing counts as finished without
one of them. Edit opens the five fields Tom reads; Why and Status stay locked,
because correcting the answer is review and rewriting the reasoning behind it is
not. Every run appears in the run log the moment it returns, marked awaiting
review until somebody acts. A decision can be reversed, never quietly: reopening
writes its own row.</p>
<p>Prompt 05: the reply arrives in a strict format and gets parsed. Each field
renders with its label, and a sixth field, Why, names the data and the policy
line behind the answer. It is for a reviewer, not for Tom, so it sits below the
rule. If the shape is wrong the raw text is shown with a notice rather than a
crash. Styling still comes later.</p>
<p>p06c: portions are capped at what a person actually eats in one sitting,
the day's calorie landing is reported when it falls short, the word minimum
replaces the word it used to use, and the eval ids are now CASE-n so they cannot
be confused with the EVE-nn evenings they point at.</p>
<p>Prompt 06: the boundary is enforced and visible. Every result carries a
status &mdash; OK, HELD, or REFUSED-ESCALATE with the rule that fired. Two new
cases exist to make it fire: one asks the agent to change the coach's target,
one reports symptoms. Today also keeps what it can confirm when a food has no
numbers, instead of a dash.</p>
<p class="lbl">p05 closed a real gap: the system prompt talked about
safety_policy.md and output_rules.md but never sent them. The pre-authored
wording had never reached the model. Both files are now in the prompt.</p>
<p class="lbl">p04b fixed the token budget: max_tokens was 1500 and the model
spent all of it thinking, returning nothing. Thinking is on by default on these
models and spends from the same budget.</p>
<p class="lbl">p04c fixed the eval data. The first full run passed EV-2 and EV-5
and failed EV-1, EV-3 and EV-4, and in all three the agent was right and the
case was wrong: each expected answer had been computed by quietly filling a hole
the agent is forbidden to fill. EVE-01 never said which sandwich, EVE-03 never
said how much bread and could not have reached the state it claimed to test,
EVE-04 contained a food with no row. Repaired here rather than graded to
match.</p>


</details>

<script>
const MODEL = "claude-opus-5";
const MAX_TOKENS = 16000;   // thinking is on by default and spends from this budget
const EFFORT = "high";      // low | medium | high | xhigh | max
const RULES = __RULES__;
const KEY_STORE = "worth_eating_api_key";

const CARD = __CARD__;
const FOODS = __FOODS__;
const PORTIONS = __PORTIONS__;
const HISTORY = __HISTORY__;
const EVENINGS = __EVENINGS__;
const EVAL_CASES = __EVALS__;
const POLICIES = __POLICIES__;
const SYSTEM_PROMPT = __SYSPROMPT__;

/* ---------- settings ---------- */
function getKey() { try { return localStorage.getItem(KEY_STORE) || ""; } catch (e) { return ""; } }
function renderKeyState() {
  const k = getKey();
  const el = document.getElementById("keystate");
  el.textContent = k ? ("key saved — " + k.slice(0, 7) + "…" + k.slice(-4)) : "no key saved";
}
document.getElementById("save").onclick = function () {
  const v = document.getElementById("apikey").value.trim();
  if (!v) { alert("Nothing to save."); return; }
  try { localStorage.setItem(KEY_STORE, v); } catch (e) { alert("This browser refused to store it."); return; }
  document.getElementById("apikey").value = "";
  renderKeyState();
};
document.getElementById("clear").onclick = function () {
  try { localStorage.removeItem(KEY_STORE); } catch (e) {}
  renderKeyState();
};
renderKeyState();

document.getElementById("sysprompt").textContent = SYSTEM_PROMPT;

/* ---------- data views ---------- */
function tbl(el, rows, cols) {
  const h = "<tr>" + cols.map(c => "<th>" + c + "</th>").join("") + "</tr>";
  const b = rows.map(r => "<tr>" + cols.map(c => "<td>" + (r[c] ?? "") + "</td>").join("") + "</tr>").join("");
  document.getElementById(el).innerHTML = h + b;
}

document.getElementById("card").innerHTML =
  "<table><tr><th>Calories</th><td>" + CARD.kcal + " kcal</td></tr>" +
  "<tr><th>Protein</th><td>" + CARD.protein_g + " g</td></tr>" +
  "<tr><th>Personal XP</th><td><b>" + CARD.xp + "</b></td></tr>" +
  "<tr><th>Meal trigger</th><td>" + CARD.meal_trigger_g + " g</td></tr>" +
  "<tr><th>Fat minimum</th><td>" + CARD.fat_min_g + " g</td></tr>" +
  "<tr><th>Fibre</th><td>" + CARD.fibre_g + " g</td></tr></table>";

document.getElementById("policies").innerHTML =
  Object.keys(POLICIES).map(k => "<li><code>" + k + "</code> &mdash; " +
    POLICIES[k].split("\n").length + " lines</li>").join("");

tbl("counts", [
  {file: "foods.csv", rows: FOODS.length},
  {file: "portions.csv", rows: PORTIONS.length},
  {file: "evenings.csv", rows: EVENINGS.length},
  {file: "history.csv", rows: HISTORY.length},
  {file: "eval_cases.csv", rows: EVAL_CASES.length},
], ["file", "rows"]);

const CASE_OF = {};
EVAL_CASES.forEach(c => CASE_OF[c.evening_id] = c);
const ORDERED = EVAL_CASES.map(c => EVENINGS.find(e => e.id === c.evening_id))
  .filter(Boolean)
  .concat(EVENINGS.filter(e => !CASE_OF[e.id]));

document.getElementById("caseindex").innerHTML =
  "<table><tr><th>case</th><th>press Run on</th><th>what it tests</th></tr>" +
  EVAL_CASES.map(c => "<tr><td><b>" + c.id + "</b></td><td>" + c.evening_id +
    "</td><td>" + c.type + "</td></tr>").join("") +
  "</table><p class='lbl'>every card below that has no case id is an unseeded evening, "
  + "useful for poking at but not graded</p>";

// Prompt 10. Cards on the left, one work area, the rest of a case's panel only
// shown when its card is selected. Every id from Section A is unchanged, so
// nothing that draws into out-<id> had to learn the layout exists.
function short(t, n) { t = (t || "").replace(/\s+/g, " ").trim(); return t.length > n ? t.slice(0, n - 1) + "…" : t; }

document.getElementById("caselist").innerHTML = ORDERED.map(e => {
  const ev = EVAL_CASES.find(c => c.evening_id === e.id);
  return "<div class='case-card' data-id='" + e.id + "'>" +
    "<div class='id'>" + e.id + (ev ? " · " + ev.id : "") + "</div>" +
    "<div class='title'>" + esc(e.day_type) + " day" + (ev ? "" : " · not graded") + "</div>" +
    "<div class='sub'>" + esc(short(e.ate_today, 64)) + "</div>" +
    "<span class='badge-slot' data-for='" + e.id + "'></span>" +
    "</div>";
}).join("");

document.getElementById("cases").innerHTML = ORDERED.map(e => {
  const ev = EVAL_CASES.find(c => c.evening_id === e.id);
  return "<section class='case-panel' id='case-" + e.id + "' data-id='" + e.id + "'>" +
    "<h3>" + e.id + (ev ? " · " + ev.id : "") + " <span class='day'>" + esc(e.day_type) + " day</span></h3>" +
    "<div class='lbl'>Ate today</div><div>" + e.ate_today + "</div>" +
    "<div class='lbl'>In the fridge</div><div>" + e.in_fridge + "</div>" +
    (ev ? "<div class='lbl'>" + ev.id + " — " + esc(ev.type) + "</div>" +
          "<div class='expect'>" + ev.expected_behavior + "</div>" : "") +
    "<p><button class='btn primary run' data-id='" + e.id + "'>Run</button></p>" +
    "<div class='out' id='out-" + e.id + "'></div>" +
    "</section>";
}).join("");

function selectCase(id) {
  document.querySelectorAll(".case-card").forEach(c => c.classList.toggle("active", c.dataset.id === id));
  document.querySelectorAll(".case-panel").forEach(p => p.classList.toggle("selected", p.dataset.id === id));
  const m = document.querySelector("main.panel");
  if (m && window.innerWidth <= 1100) m.scrollIntoView({block: "start", behavior: "smooth"});
}
document.querySelectorAll(".case-card").forEach(c => { c.onclick = () => selectCase(c.dataset.id); });
if (ORDERED.length) selectCase(ORDERED[0].id);

// The card shows the latest verdict for its evening, so the list reads as a
// queue: what is done, what is waiting, what nobody has looked at.
function cardBadges() {
  const latest = {};
  RUNLOG.forEach(rid => { const r = RUNS[rid]; if (!r.ghost) latest[r.eveId] = r; });
  document.querySelectorAll(".badge-slot").forEach(sl => {
    const r = latest[sl.dataset.for];
    sl.innerHTML = r ? "<span class='verdict " + r.action + "'>" +
      ({pending: "awaiting review", approved: "approved", edited: "edited", escalated: "escalated",
        replaced: "replaced", reopened: "reopened", continued: "answered"}[r.action] || r.action) +
      "</span>" : "";
  });
}

/* ---------- the loop ---------- */
function weekSoFar() {
  const k = HISTORY.reduce((a, r) => a + Number(r.kcal), 0);
  const p = HISTORY.reduce((a, r) => a + Number(r.protein_g), 0);
  return {days: HISTORY.length, kcal: k, protein: p,
          xp: k ? +(p / k * 100).toFixed(2) : 0,
          vsBudget: k - HISTORY.length * CARD.kcal};
}

function userMessage(e) {
  const w = weekSoFar();
  return [
    "CARD: " + JSON.stringify(CARD),
    "",
    // Send the whole row. An earlier version hand-picked six fields, which meant
    // max_serving_g existed in the CSV, was described in the prompt, and never
    // reached the model - it said so, and named 920 g of cottage cheese. The
    // note column was silently missing too, including the one explaining that a
    // 150 g pack of the watered chicken yields 35 g and not 45 g. Adding a
    // column to the CSV now reaches the agent without touching this line.
    "FOODS (per 100 g unless the field says otherwise): " + JSON.stringify(FOODS),
    "",
    "PORTIONS: " + JSON.stringify(PORTIONS.map(p => ({
      food: p.food, variant: p.variant, kcal: +p.kcal, protein: +p.protein_g,
      fat: +p.fat_g, fibre: +p.fibre_g, xp: +p.xp}))),
    "",
    "HISTORY, last " + w.days + " days: " + JSON.stringify(HISTORY) +
      " — totals " + w.kcal + " kcal and " + w.protein + " g, blending to " + w.xp +
      ", which is " + Math.abs(w.vsBudget) + " kcal " + (w.vsBudget < 0 ? "under" : "over") +
      " budget for the period. Use this to judge room. Never comment on it.",
    "",
    "The daily xp column in HISTORY is derived from that row's own kcal and protein. " +
      "It is there to be read, never to be averaged: a period blends as total protein " +
      "over total calories.",
    "",
    "TONIGHT — what he says he ate today:",
    e.ate_today,
    "",
    "TONIGHT — what he says is in the fridge:",
    e.in_fridge
  ].join("\n");
}

function explain(status, raw) {
  if (status === 401) return "That key was rejected. Check it in Settings — it should start sk-ant.";
  if (status === 403) return "The key is valid but not permitted to use " + MODEL + ".";
  if (status === 429) return "Rate limited, or the account is out of credit. Wait and try again.";
  if (status === 400 && /workspace-id/i.test(raw || ""))
    return "That key is a user key, not a workspace key. A user key acts as you " +
           "personally, so the API cannot tell which workspace to charge and log the " +
           "call against, and it refuses rather than guess. Make a new key on the API " +
           "keys page and pick a workspace in the Create Key dialog instead of leaving " +
           "it on your own account. Nothing here needs changing.";
  if (status === 400) return "The request was refused as malformed. Raw response below.";
  if (status >= 500) return "Anthropic returned a server error. Not your fault, try again.";
  return "Unexpected response (" + status + "). Raw response below.";
}

function runCase(id) {
  const e = EVENINGS.find(x => x.id === id);
  return ask(id, [{role: "user", content: userMessage(e)}], null);
}

// A follow-up is the same call with the exchange so far in front of it. Three
// cases have been asking questions since p05 and nothing could answer them:
// CASE-2 wants the numbers off a label, CASE-5 asks whether that was really the
// whole day, and now the finished day asks whether he is still hungry. A
// question the product cannot hear the answer to is theatre.
function followUp(rid, text) {
  const prev = RUNS[rid];
  // A run restored from an older build has no turns. Guard rather than throw:
  // losing the thread is better than losing the page.
  const prior = prev.turns || [];
  if (!prior.length) { alert("That reply came from an earlier build, so there is no\n"
    + "conversation to continue. Run the case again first."); return; }
  return ask(prev.eveId, prior.concat([{role: "user", content: text}]), rid);
}

async function ask(id, turns, fromRid) {
  const out = document.getElementById("out-" + id);
  const key = getKey();
  if (!key) { out.innerHTML = "<div class='err'>No API key saved. Add one in Settings above.</div>"; return; }
  out.innerHTML = "<div class='busy'>running&hellip;</div>";
  let res;
  try {
    res = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "anthropic-dangerous-direct-browser-access": "true"
      },
      body: JSON.stringify({
        model: MODEL,
        max_tokens: MAX_TOKENS,
        thinking: {type: "adaptive"},
        output_config: {effort: EFFORT},
        system: SYSTEM_PROMPT,
        messages: turns
      })
    });
  } catch (err) {
    out.innerHTML = "<div class='err'><b>Could not reach the API.</b> Offline, blocked by the " +
      "browser, or the page is hosted somewhere that forbids outside calls. " +
      "This file has to run from your own device.<br><br>" + String(err) + "</div>";
    return;
  }
  const text = await res.text();
  if (!res.ok) {
    out.innerHTML = "<div class='err'><b>" + explain(res.status, text) + "</b><pre>" +
      text.replace(/</g, "&lt;") + "</pre></div>";
    return;
  }
  let data;
  try { data = JSON.parse(text); } catch (err) {
    out.innerHTML = "<div class='err'>The reply was not JSON.<pre>" + text.replace(/</g, "&lt;") + "</pre></div>";
    return;
  }
  const blocks = data.content || [];
  const body = blocks.filter(b => b.type === "text").map(b => b.text).join("\n").trim();
  const thought = blocks.some(b => b.type === "thinking");
  const used = (data.usage && data.usage.output_tokens) || 0;

  if (data.stop_reason === "max_tokens" && !body) {
    out.innerHTML = "<div class='err'><b>Ran out of output budget before writing anything.</b> " +
      "It spent all " + used + " tokens thinking. Raise MAX_TOKENS (currently " + MAX_TOKENS +
      ") or lower EFFORT (currently " + EFFORT + ").</div>";
    return;
  }
  if (data.stop_reason === "refusal") {
    const d = data.stop_details || {};
    out.innerHTML = "<div class='err'><b>The model declined this request.</b> " +
      (d.category ? "Category: " + d.category + ". " : "") + (d.explanation || "") + "</div>";
    return;
  }
  if (!body) {
    out.innerHTML = "<div class='err'><b>No text came back.</b> stop_reason was " +
      data.stop_reason + ".<pre>" + JSON.stringify(data, null, 2).replace(/</g, "&lt;") +
      "</pre></div>";
    return;
  }
  const meta = "<div class='lbl'>" + MODEL + " &middot; effort " + EFFORT +
    " &middot; " + used + " output tokens" + (thought ? ", thought first" : "") +
    (data.stop_reason !== "end_turn" ? " &middot; stop_reason " + data.stop_reason : "") +
    "</div>";
  const parsed = parseFields(body);
  if (!parsed) {
    out.innerHTML = meta +
      "<div class='err'><b>agent output did not match format.</b> Expected the six labels " +
      FIELDS.join(", ") + ", each on its own line. Raw text below.</div>" +
      "<pre>" + esc(body) + "</pre>";
    return;
  }
  const st = parsed["Status"] || "";
  const kind = /^REFUSED-ESCALATE/i.test(st) ? "refused"
             : /^HELD/i.test(st) ? "held"
             : /^OK\b/i.test(st) ? "ok" : "unknown";
  const rid = newRun(id, meta, parsed, kind, statusClash(kind, parsed),
                     turns.concat([{role: "assistant", content: body}]), fromRid);
  drawRun(rid);
  return rid;          // the sweep needs to know what happened; a click does not
}

// ---------------------------------------------------------------------------
// Prompt 07 - the human gate, and the log that proves it was used.
//
// The record is the source of truth, never the DOM. An edit rewrites the
// record and the panel is drawn again from it, so what the log reports and
// what the screen shows cannot come apart. Reading the answer back out of the
// HTML would be the same class of mistake as letting the agent grade itself.
// ---------------------------------------------------------------------------

// Tom reads these five, so a reviewer may rewrite them. Why and Status are the
// agent's own account of its work and stay locked: correcting the answer is
// review, editing the reasoning that produced it is falsifying the record.
const TOM_READS = ["Today", "Left", "Add", "After that", "Note"];

const RUNS = {};      // rid -> record
const RUNLOG = [];    // rids, in the order they happened
let RUN_SEQ = 0;

const LOG_STORE = "we.runlog";

// In memory for the session, mirrored to sessionStorage so a reload does not
// throw the evening away. On a phone Chrome discards backgrounded tabs, and
// losing a review session to a task switch is not a lesson about anything.
function saveLog() {
  try { sessionStorage.setItem(LOG_STORE, JSON.stringify({seq: RUN_SEQ, runs: RUNS, order: RUNLOG})); }
  catch (err) { /* private mode, quota, blocked storage: the log just stays in memory */ }
}
function loadLog() {
  try {
    const raw = sessionStorage.getItem(LOG_STORE);
    if (!raw) return;
    const d = JSON.parse(raw);
    RUN_SEQ = d.seq || 0;
    Object.assign(RUNS, d.runs || {});
    (d.order || []).forEach(r => RUNLOG.push(r));
  } catch (err) { /* unreadable: start clean rather than guess */ }
}

function clockNow() {
  const d = new Date();
  const p = n => String(n).padStart(2, "0");
  return p(d.getHours()) + ":" + p(d.getMinutes()) + ":" + p(d.getSeconds());
}

function newRun(eveId, meta, parsed, kind, clashes, turns, fromRid) {
  // A re-run replaces what is on screen. If the previous run for this evening
  // was never reviewed, say so in the log rather than deleting the row: a run
  // nobody looked at is exactly the thing the log exists to show.
  //
  // A follow-up is not that. Answering the agent's question is engagement, not
  // neglect, so the run it continues is marked answered rather than abandoned.
  RUNLOG.forEach(r => {
    const p = RUNS[r];
    if (p.eveId === eveId && p.action === "pending") {
      if (r === fromRid) { p.action = "continued"; p.reason = "its question was answered"; }
      else { p.action = "replaced"; p.reason = "re-run before anyone reviewed it"; }
    }
  });
  const rid = "r" + (++RUN_SEQ);
  const c = CASE_OF[eveId];
  RUNS[rid] = {
    rid: rid, eveId: eveId, caseId: c ? c.id : "", at: clockNow(), meta: meta, kind: kind,
    agent: parsed["Status"] || "no status given",
    fields: Object.assign({}, parsed),
    original: Object.assign({}, parsed),
    clashes: clashes, action: "pending", reason: "", changed: [], mode: "",
    turns: turns || [], after: fromRid || ""
  };
  RUNLOG.push(rid);
  return rid;
}

// Predefined answers, never a text box. Milan's call on 2026-08-28, carried over
// from the PlateMate capstone: a free field opens a thousand ways to wander off
// and not one of them is the thing under test. A real input belongs to the app
// that comes after the capstone.
//
// It also turned out to be the better hook. The box used to appear when Add was
// a dash, which broke the moment the agent stopped dashing Add. What it should
// always have keyed on is what the agent actually asked.
//
// Never anything under a refusal, buttons included. S3 says a boundary is not
// negotiable, and offering someone two ways to reply to it is negotiation with
// a nicer surface.
function replyOptions(r) {
  const st = r.agent || "";
  if (r.kind === "refused") return null;

  if (/\bS5\b/.test(st))
    return {opts: ["Yes, that was everything", "No, there was more"]};

  // The finished day. Keyed on the agent having actually asked, not on the
  // shape of some other field.
  if (r.kind === "ok" && /\?\s*$/.test((r.fields["Note"] || "").trim()))
    return {opts: ["Yes, still hungry", "No, I am done"]};

  // S1 and S2 ask for information rather than a decision: what the food was,
  // what the label says, what else is in the fridge. No set of buttons carries
  // a number off a packet. Say so on screen instead of pretending.
  if (/\bS[12]\b/.test(st))
    return {opts: [], why: "This one asks for information, not a decision. " +
            "No button can carry the numbers off a label, so answering it needs " +
            "typing, and that waits until after the capstone."};

  return null;
}

function replyHtml(r) {
  const o = r.mode ? null : replyOptions(r);
  if (!o) return "";
  if (!o.opts.length)
    return "<div class='replybox'><div class='lbl'>Cannot be answered here</div>" +
      "<p class='cannot'>" + o.why + "</p></div>";
  return "<div class='replybox'><div class='lbl'>Answer it</div>" +
    o.opts.map((t, i) => "<button class='btn' data-act='say' data-r='" + r.rid +
      "' data-i='" + i + "'>" + esc(t) + "</button>").join("") + "</div>";
}

function isDash(t) { return !t || /^[-\u2013\u2014\s.]*$/.test(t); }

// The night has one answer in it, and the console was making a reviewer read six
// fields to find it. Milan said so through the escalate box on 2026-08-27:
// "Why always i need to read it?" On CASE-1, Why alone is 60% of the characters
// on screen, and Why is the one field the prompt says is never for Tom.
//
// So the answer goes on top at size. It is not new text: it is the opening of
// the field that already carries it, Add when something was named and Note when
// the answer is a stop or a finished day. Nothing is generated here, because a
// headline the agent did not write is a sentence nobody reviewed.
function headline(r) {
  const add = r.fields["Add"] || "";
  const from = isDash(add) ? "Note" : "Add";
  const src = (r.fields[from] || "").trim();
  if (!src || isDash(src)) return null;
  const parts = src.split(/(?<=[.?!])\s+/);
  let take = 1;
  // A short opener usually has not said the whole thing yet: on a stop path the
  // first sentence is the arithmetic and the second is the actual question, and
  // on a refusal the first is what it will not do and the second is what to do.
  if (parts[0].length < 90 && parts[1]) take = 2;
  return {from: from, text: parts.slice(0, take).join(" "),
          rest: parts.slice(take).join(" ")};
}

// The headline is lifted out of a field, not copied from it. Whatever it took
// stops rendering below, and a field it consumed entirely does not render at
// all. Showing both was the same sentence twice, which is more reading than
// before rather than less. Nothing is ever dropped: a field with more to say
// keeps the remainder under its own label.
function fieldsHtml(r, hl) {
  return FIELDS.filter(f => f !== "Status" && f !== "Why").map(f => {
    const editing = r.mode === "edit" && TOM_READS.indexOf(f) >= 0;
    let text = r.fields[f] || "";
    if (!editing && hl && hl.from === f) {
      if (!hl.rest) return "";
      text = hl.rest;
    }
    const body = editing
      ? "<textarea data-f=\"" + f + "\">" + esc(r.fields[f] || "") + "</textarea>"
      : esc(text || "\u2014") +
        (r.changed.indexOf(f) >= 0 ? " <span class='edited-flag'>edited</span>" : "");
    return "<dt>" + f + "</dt>" +
           "<dd class='" + (editing ? "" : "locked") + "'>" + body + "</dd>";
  }).join("");
}

// Why folds away. It is the audit trail, read when something looks wrong rather
// than on every case, and it is addressed to a reviewer who has already decided
// to look. Folding it is not the same as hiding what is under review: the five
// fields Tom reads stay open, because a gate you can close your eyes through is
// a rubber stamp with extra clicks.
// ---------------------------------------------------------------------------
// Prompt 08 - citations that are resolved, not believed.
//
// The playbook's check is "open the policy constant and confirm the cited line
// exists". Doing that by hand once is how a fabricated citation survives to the
// demo, so it runs on every citation of every reply instead.
//
// Nothing here trusts the agent. Each reference is looked up in the same
// constants the agent was given, and a tag it cannot resolve goes red on
// screen. A red tag is not a rendering bug: it is the agent citing something
// that does not exist.
// ---------------------------------------------------------------------------

const PORTION_NAMES = PORTIONS.map(p => p.food).filter((v, i, a) => a.indexOf(v) === i);

// Longest first, then blank out what matched. Otherwise "Tomatensauce" in the
// text also scores a hit for "Tomaten", and the tag row reports a record the
// agent never cited.
function namesIn(text, names) {
  let hay = " " + text + " ";
  const found = [];
  names.slice().sort((a, b) => b.length - a.length).forEach(n => {
    const i = hay.indexOf(n);
    if (i >= 0) { found.push(n); hay = hay.slice(0, i) + " ".repeat(n.length) + hay.slice(i + n.length); }
  });
  return found;
}

function citations(r) {
  const why = r.fields["Why"] || "";
  const out = [];
  const seen = {};

  // Rules. The pattern deliberately matches the shape rather than the real
  // identifiers, so an invented S7 is caught rather than ignored.
  //
  // Fired and merely mentioned are not the same thing and must not look the
  // same. CASE-2 cites S5 to say it was checked and came back clear, and the
  // first version of this row showed that beside the rules that governed the
  // answer, in the same green. Third time this exact confusion has appeared:
  // once in the S5 threshold, once in the clash detector, now here. The
  // `applied:` tail exists precisely to settle it, so it is what decides.
  const fired = appliedTail(why);
  (why.match(/\b[SO]\d+\b/g) || []).forEach(id => {
    if (seen[id]) return; seen[id] = 1;
    if (!RULES[id]) {
      out.push({t: id, cls: "bad", bad: true, note: "no rule with this identifier exists"});
      return;
    }
    const on = new RegExp("\\b" + id + "\\b").test(fired);
    out.push({t: on ? id : id + " not fired", cls: on ? "ok" : "off",
              note: RULES[id].title + " \u00b7 " + RULES[id].file +
                    (on ? " \u00b7 applied" : " \u00b7 checked, did not fire")});
  });

  namesIn(why, FOODS.map(f => f.name)).forEach(n =>
    out.push({t: n, cls: "rec", note: "foods.csv"}));
  namesIn(why, PORTION_NAMES).forEach(n =>
    out.push({t: n, cls: "rec", note: "portions.csv"}));

  // The one citation that is not in Why. Add names the food he is told to eat,
  // and a food that is not in FOODS is the invention this whole build is
  // against, so it is checked separately and named plainly.
  const add = r.fields["Add"] || "";
  if (!isDash(add) && !namesIn(add, FOODS.map(f => f.name)).length)
    out.push({t: "Add names no known food", cls: "bad", bad: true,
              note: "nothing in this line matches a row in foods.csv"});

  return out;
}

function citeHtml(r) {
  const c = citations(r);
  if (!c.length) return "";
  const bad = c.filter(x => x.bad).length;
  return "<div class='cites'>" +
    c.map(x => "<span class='cite " + x.cls + "' title='" +
      escAttr(x.note) + "'>" + esc(x.t) + "</span>").join("") +
    (bad ? "<div class='err'><b>" + bad + " citation" + (bad > 1 ? "s do" : " does") +
       " not resolve.</b> The agent named something that is not in the data or the " +
       "policy files it was given.</div>" : "") + "</div>";
}

function whyHtml(r) {
  return "<details class='whybox'><summary>why &mdash; the data and the rules it used</summary>" +
    "<div class='whytext'>" + esc(r.fields["Why"] || "\u2014") + "</div></details>";
}

function gateHtml(r) {
  const b = (cls, act, label) =>
    "<button class='btn " + ({approve: "approve", esc: "danger"}[cls] || "") + " " + cls + "' data-act='" + act + "' data-r='" + r.rid + "'>" + label + "</button>";

  if (r.mode === "edit")
    return "<div class='gate'><div class='lbl'>Editing what Tom reads</div>" +
      b("approve", "save", "Save") + b("edit", "canceledit", "Cancel") + "</div>";

  if (r.mode === "esc")
    return "<div class='gate'><div class='lbl'>Why are you escalating?</div>" +
      "<div class='escbox'><input id='esc-" + r.rid + "' placeholder='one line, for the coach' " +
      "value=\"" + escAttr(r.reason) + "\"></div><div style='margin-top:.4rem'>" +
      b("esc", "sendesc", "Escalate") + b("edit", "cancelesc", "Cancel") + "</div></div>";

  if (r.action === "pending")
    return "<div class='gate'><div class='lbl'>Nothing is finished until one of these</div>" +
      b("approve", "approve", "Approve") + b("edit", "edit", "Edit") + b("esc", "esc", "Escalate") +
      "</div>";

  // Decided. A reversal is allowed, but it is never silent: reopening writes
  // its own row, so the log shows the change of mind rather than hiding it.
  return "<div class='gate'><span class='verdict " + r.action + "'>" + r.action + "</span>" +
    (r.reason ? "<div class='reason'>" + esc(r.reason) + "</div>" : "") +
    "<div style='margin-top:.4rem'>" + b("edit", "reopen", "Reopen") + "</div></div>";
}

function drawRun(rid) {
  const r = RUNS[rid];
  const out = document.getElementById("out-" + r.eveId);
  if (out) {
    const hl = r.mode === "edit" ? null : headline(r);
    out.innerHTML = r.meta +
      "<div class='status " + r.kind + "'>" + esc(r.agent) + "</div>" +
      (r.clashes.length ? "<div class='err'><b>status disagrees with the body.</b> " +
         r.clashes.map(esc).join(" ") + "</div>" : "") +
      (r.after && r.turns.length > 2
        ? "<p class='followed'>you said &ldquo;" +
          esc(r.turns[r.turns.length - 2].content) + "&rdquo;</p>" : "") +
      (hl ? "<p class='headline'>" + esc(hl.text) + "</p>" : "") +
      "<dl class='fields'>" + fieldsHtml(r, hl) + "</dl>" +
      citeHtml(r) +
      whyHtml(r) +
      replyHtml(r) +
      gateHtml(r);
    out.querySelectorAll(".gate button").forEach(b => {
      b.onclick = () => gateClick(b.dataset.act, b.dataset.r);
    });
    out.querySelectorAll(".replybox button").forEach(b => {
      b.onclick = () => sayClick(b.dataset.r, Number(b.dataset.i));
    });
    // On a phone the keyboard covers the button, so the keyboard's own key works.
    const box = out.querySelector(".escbox input");
    if (box) {
      box.onkeydown = ev => { if (ev.key === "Enter") { ev.preventDefault(); gateClick("sendesc", r.rid); } };
      box.focus();
    }
  }
  renderLog();
  cardBadges();
  saveLog();
}

function sayClick(rid, i) {
  const o = replyOptions(RUNS[rid]);
  if (o && o.opts[i]) followUp(rid, o.opts[i]);
}

function gateClick(act, rid) {
  const r = RUNS[rid];
  const out = document.getElementById("out-" + r.eveId);

  if (act === "say") {
    const o = replyOptions(r);
    const text = o && o.opts[Number(document.activeElement.dataset.i)];
    if (text) followUp(rid, text);
    return;                                  // the new run draws itself
  }

  if (act === "approve") { r.action = "approved"; r.reason = ""; }

  else if (act === "edit" || act === "canceledit") { r.mode = act === "edit" ? "edit" : ""; }

  else if (act === "save") {
    // Read the boxes back into the record, and remember which fields moved.
    out.querySelectorAll("dl.fields textarea").forEach(t => {
      const f = t.dataset.f, v = t.value.trim();
      if (v !== (r.fields[f] || "")) {
        r.fields[f] = v;
        if (r.changed.indexOf(f) < 0) r.changed.push(f);
      }
    });
    r.mode = "";
    r.action = r.changed.length ? "edited" : "approved";
    r.reason = r.changed.length ? "changed " + r.changed.join(", ") : "saved with no change, so approved";
  }

  else if (act === "esc")       { r.mode = "esc"; }
  else if (act === "cancelesc") { r.mode = ""; }

  else if (act === "sendesc") {
    const box = document.getElementById("esc-" + rid);
    const why = (box && box.value || "").trim();
    if (!why) { if (box) box.focus(); return; }   // a reason is the point
    r.action = "escalated"; r.reason = why; r.mode = "";
  }

  else if (act === "reopen") {
    const was = r.action;
    r.action = "pending"; r.reason = ""; r.mode = "";
    const rid2 = "r" + (++RUN_SEQ);
    RUNS[rid2] = {rid: rid2, eveId: r.eveId, caseId: r.caseId, at: clockNow(), meta: "",
                  kind: r.kind, agent: r.agent, fields: {}, original: {}, clashes: [],
                  action: "reopened", reason: "was " + was + ", sent back for review",
                  changed: [], mode: "", ghost: true};
    RUNLOG.push(rid2);
  }

  drawRun(rid);
}

// ---------------------------------------------------------------------------
// Prompt 09 - the whole queue in one click.
//
// The summary counts more than the playbook asks for. A sweep that reports only
// statuses throws away the two checks this build spent Prompts 06 and 08
// acquiring: whether the status agrees with the body it sits on, and whether
// the citations resolve. Both are per-case findings that only mean something in
// aggregate, and neither shows up as an error.
// ---------------------------------------------------------------------------

let SWEEPING = false;

async function runAll() {
  const cases = EVAL_CASES.map(c => c.evening_id).filter(id => EVENINGS.some(e => e.id === id));
  const el = document.getElementById("sweep");
  const go = document.getElementById("runall"), stop = document.getElementById("stopall");
  SWEEPING = true;
  go.disabled = true; stop.hidden = false;

  const tally = {ok: 0, held: 0, refused: 0, unknown: 0, error: 0, clash: 0, cite: 0};
  const failed = [];

  for (let i = 0; i < cases.length; i++) {
    if (!SWEEPING) break;
    const id = cases[i], c = CASE_OF[id];
    el.innerHTML = "<b>" + (i + 1) + " of " + cases.length + "</b> \u00b7 running " +
      esc(c.id) + " on " + esc(id) + "&hellip;";
    selectCase(id);

    let rid = null;
    try { rid = await ask(id, [{role: "user", content: userMessage(EVENINGS.find(e => e.id === id))}], null); }
    catch (err) { rid = null; }

    if (!rid) { tally.error++; failed.push(c.id + " on " + id); continue; }
    const r = RUNS[rid];
    tally[r.kind]++;
    if (r.clashes.length) tally.clash++;
    if (citations(r).some(x => x.bad)) tally.cite++;
  }

  go.disabled = false; stop.hidden = true;
  const n = cases.length;
  el.innerHTML =
    (SWEEPING ? "<b>Done.</b> " : "<b>Stopped.</b> ") +
    tally.ok + " OK \u00b7 " + tally.held + " held \u00b7 " +
    tally.refused + " refused-escalate" +
    (tally.unknown ? " \u00b7 " + tally.unknown + " with no readable status" : "") +
    " \u00b7 " + tally.error + " error" + (tally.error === 1 ? "" : "s") +
    "<br><span class='swnote'>" + tally.clash + " status disagreed with its body \u00b7 " +
    tally.cite + " had a citation that did not resolve</span>" +
    (failed.length ? "<br><span class='swfail'>failed: " + esc(failed.join(", ")) +
      ". Their panels carry the error.</span>" : "");
  SWEEPING = false;
}

function renderLog() {
  const el = document.getElementById("log");
  const sum = document.getElementById("logsum");
  if (!el) return;
  if (!RUNLOG.length) {
    el.innerHTML = "";
    sum.innerHTML = "<span class='lbl'>no runs yet</span>";
    return;
  }
  const label = {pending: "awaiting review", approved: "approved", edited: "edited",
                 escalated: "escalated", replaced: "replaced, never reviewed",
                 reopened: "reopened", continued: "answered, and it replied"};
  el.innerHTML =
    "<tr><th>time</th><th>case</th><th>evening</th><th>agent decided</th>" +
    "<th>human action</th><th>note</th></tr>" +
    RUNLOG.slice().reverse().map(rid => {
      const r = RUNS[rid];
      const said = r.after && r.turns.length ? r.turns[r.turns.length - 2] : null;
      return "<tr><td class='t'>" + r.at + "</td><td>" + esc(r.caseId || "\u2014") + "</td>" +
        "<td>" + esc(r.eveId) + (said ? " <span class='followed'>after \u201c" +
          esc(said.content) + "\u201d</span>" : "") + "</td>" +
        "<td>" + (r.ghost ? "\u2014" : "<span class='verdict " + r.kind + "'>" + esc(r.agent) + "</span>") + "</td>" +
        "<td><span class='verdict " + r.action + "'>" + label[r.action] + "</span></td>" +
        "<td>" + esc(r.reason || "") + "</td></tr>";
    }).join("");

  const n = a => RUNLOG.filter(r => RUNS[r].action === a).length;
  const waiting = n("pending");
  sum.innerHTML = "<b>" + RUNLOG.length + "</b> runs &middot; " +
    "<b>" + n("approved") + "</b> approved &middot; " +
    "<b>" + n("edited") + "</b> edited &middot; " +
    "<b>" + n("escalated") + "</b> escalated" +
    (waiting ? " &middot; <span class='verdict pending'>" + waiting + " awaiting review</span>" : "");
}

// The agent declares its own status, so the status is not a check on its own.
// This compares the declaration against the reply it sits on. A contradiction
// is shown rather than resolved: guessing which half is right would be the
// same mistake as letting the agent grade itself.
// Only the `applied:` tail counts. An earlier version regex-matched the whole
// Why line, so "S5 not fired" read as a safety rule firing and every OK case
// showed a contradiction. Same mistake as the S5 threshold: matching a mention
// instead of an application.
function appliedTail(why) {
  const m = why.match(/applied:\s*(.*)$/i);
  return m ? m[1] : "";
}

function statusClash(kind, p) {
  const out = [];
  const citesSafety = /\bS[1-5]\b/.test(appliedTail(p["Why"] || ""));
  const dash = isDash;
  if (!/applied:/i.test(p["Why"] || "")) out.push("Why has no applied: tail.");
  if (kind === "unknown") out.push("Status is not one of OK, HELD, REFUSED-ESCALATE.");
  if (kind === "ok" && citesSafety)
    out.push("Status is OK but Why cites a safety rule.");
  if ((kind === "held" || kind === "refused") && !citesSafety)
    out.push("Status stops the answer but Why cites no safety rule.");
  if ((kind === "held" || kind === "refused") && !dash(p["Add"]))
    out.push("Status stops the answer but Add still names something.");
  return out;
}

const FIELDS = ["Today", "Left", "Add", "After that", "Note", "Why", "Status"];

function esc(t) { return t.replace(/&/g, "&amp;").replace(/</g, "&lt;"); }

// Attribute values need the quote closed off too. An escalation reason is
// typed by a person, and a person will eventually type a quotation mark.
function escAttr(t) { return esc(t || "").replace(/"/g, "&quot;"); }

// Returns an object keyed by label, or null when the shape is wrong.
// Lenient about stray markdown around the label, strict about the labels
// themselves: a missing one is a format failure, not something to paper over.
function parseFields(raw) {
  const found = {};
  let current = null;
  for (const line of raw.split("\n")) {
    const m = line.match(/^\s*(?:[*_#>\-\s]*)\b(Today|Left|Add|After that|Note|Why|Status)\b[*_\s]*:\s*(.*)$/i);
    if (m) {
      current = FIELDS.find(f => f.toLowerCase() === m[1].toLowerCase());
      found[current] = m[2].trim();
    } else if (current && line.trim()) {
      found[current] += " " + line.trim();
    }
  }
  if (FIELDS.some(f => !(f in found))) return null;
  for (const f of FIELDS) found[f] = found[f].replace(/\*\*/g, "").trim();
  return found;
}

document.getElementById("runall").onclick = runAll;
document.getElementById("stopall").onclick = () => { SWEEPING = false; };

document.querySelectorAll("button.run").forEach(b => {
  b.onclick = () => runCase(b.dataset.id);
});

tbl("hist", HISTORY, ["date", "kcal", "protein_g", "xp"]);
tbl("foods", FOODS, ["name", "kcal_per_100g", "protein_g_per_100g", "fat_g_per_100g", "fibre_g_per_100g", "xp", "typical_location"]);
tbl("ports", PORTIONS, ["food", "variant", "kcal", "protein_g", "fat_g", "fibre_g", "xp"]);

// The top bar carries the key state too, because it is the one thing that
// decides whether Run does anything, and Settings now lives in the right rail.
function topbarKey() {
  const b = document.getElementById("keybadge");
  if (!b) return;
  const has = !!getKey();
  b.className = "verdict " + (has ? "approved" : "pending");
  b.textContent = has ? "key saved" : "no key";
}
const _renderKeyState = renderKeyState;
renderKeyState = function () { _renderKeyState(); topbarKey(); };
topbarKey();
document.getElementById("modelmeta").textContent = MODEL + " \u00b7 effort " + EFFORT;

// Bring back this tab's log and redraw the panels it belongs to, oldest first
// so the newest run for each evening is the one left on screen. Restoring the
// log without the panels would show a decision sitting above an empty card.
loadLog();
RUNLOG.forEach(rid => { if (!RUNS[rid].ghost) drawRun(rid); });
renderLog();
</script>
</body>
</html>
"""

for k, v in {"__BUILD__": BUILD, "__RULES__": json.dumps(RULES),
             "__CARD__": json.dumps(CARD), "__FOODS__": json.dumps(FOODS),
             "__PORTIONS__": json.dumps(PORTIONS), "__HISTORY__": json.dumps(HISTORY),
             "__EVENINGS__": json.dumps(EVENINGS), "__EVALS__": json.dumps(EVALS),
             "__POLICIES__": json.dumps(POLICIES),
             "__SYSPROMPT__": json.dumps(SYSTEM_PROMPT)}.items():
    HTML = HTML.replace(k, v)

os.makedirs('builds', exist_ok=True)
open('index.html', 'w').write(HTML)
open('builds/%s.html' % BUILD, 'w').write(HTML)
print("index.html and builds/%s.html, %d bytes each" % (BUILD, len(HTML)))

# The version list. Rebuilt from what is on disk, so it can never claim a
# build that is not there. Newest first, by the number in the name.
def order(n):
    m = re.match(r'p(\d+)([a-z]*)', n)
    return (int(m.group(1)), m.group(2)) if m else (0, n)

names = sorted((f[:-5] for f in os.listdir('builds') if f.endswith('.html')
                and f != 'index.html'), key=order, reverse=True)

items = "\n".join(
    '<li><a href="%s.html">%s</a>%s</li>' % (n, n, ' <em>current</em>' if n == BUILD else '')
    for n in names)

open('builds/index.html', 'w').write("""<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Worth Eating &mdash; builds</title>
<style>
:root{color-scheme:light dark;--ink:#1a1a1a;--bg:#fbfaf8;--dim:#6b6b6b;--line:#e2ded8}
@media (prefers-color-scheme:dark){:root{--ink:#eceae6;--bg:#17171a;--dim:#9a978f;--line:#2f2f34}}
body{background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,sans-serif;
     margin:0;padding:2.5rem 1.25rem;max-width:34rem}
h1{font-size:1.35rem;margin:0 0 .35rem}
p{color:var(--dim);margin:0 0 1.75rem}
ul{list-style:none;padding:0;margin:0}
li{border-bottom:1px solid var(--line)}
li:first-child{border-top:1px solid var(--line)}
a{display:inline-block;padding:.8rem 0;color:inherit;text-decoration:none;
  font-variant-numeric:tabular-nums}
a:hover,a:focus{text-decoration:underline}
em{color:var(--dim);font-style:normal;font-size:.85rem}
</style>
<h1>Worth Eating</h1>
<p>Every build, kept. <a href="../">Latest</a> is always the newest one.</p>
<ul>
""" + items + "\n</ul>\n")
print("builds/index.html,", len(names), "build(s)")
