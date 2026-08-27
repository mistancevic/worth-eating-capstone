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

BUILD = 'p07'

def rows(p): return list(csv.DictReader(open(p)))

FOODS   = rows('data/foods.csv')
PORTIONS= rows('data/portions.csv')
HISTORY = rows('data/history.csv')
EVENINGS= rows('data/evenings.csv')
EVALS   = rows('data/eval_cases.csv')
POLICIES= {'safety_policy.md': open('policies/safety_policy.md').read(),
           'output_rules.md' : open('policies/output_rules.md').read()}
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
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Worth Eating &mdash; build __BUILD__</title>
<style>
  body { font-family: system-ui, sans-serif; margin: 1rem; line-height: 1.45; max-width: 60rem; }
  h1 { font-size: 1.3rem; } h2 { font-size: 1.05rem; margin-top: 1.6rem; }
  table { border-collapse: collapse; font-size: .85rem; width: 100%; }
  td, th { border: 1px solid #999; padding: 3px 6px; text-align: left; vertical-align: top; }
  .case { border: 1px solid #999; padding: .6rem; margin: .5rem 0; }
  .seed { background: #ffe; }
  .lbl { font-size: .75rem; text-transform: uppercase; letter-spacing: .05em; color: #555; }
  .wrap { overflow-x: auto; }
  code { background: #eee; padding: 0 3px; }
  fieldset { border: 2px solid #333; padding: .7rem; }
  input[type=password] { width: 100%; max-width: 24rem; padding: .4rem; font-family: monospace; }
  button { padding: .4rem .8rem; margin-right: .4rem; }
  #keystate { font-weight: bold; }
  pre { white-space: pre-wrap; font-size: .78rem; background: #f4f4f4; padding: .6rem; overflow-x: auto; }
  .out { margin-top: .5rem; border-top: 1px dashed #999; padding-top: .5rem; }
  .err { background: #fee; border: 1px solid #c00; padding: .5rem; }
  .busy { color: #666; font-style: italic; }
  dl.fields { display: grid; grid-template-columns: max-content 1fr; gap: .35rem .8rem;
              margin: .5rem 0 0; font-size: .9rem; }
  dl.fields dt { font-weight: bold; white-space: nowrap; }
  dl.fields dd { margin: 0; }
  .status { display: inline-block; font-size: .78rem; font-weight: bold; letter-spacing: .04em;
            padding: .15rem .5rem; margin: .4rem 0 .1rem; border: 1px solid; }
  .status.ok { color: #17501f; background: #eaf5ec; border-color: #6a9a75; }
  .status.held { color: #6a4a00; background: #fdf5e2; border-color: #b99a45; }
  .status.refused { color: #7a1717; background: #fdeceb; border-color: #c06a66; }
  .status.unknown { color: #444; background: #eee; border-color: #999; }
  dl.fields dt.why, dl.fields dd.why { color: #555; font-size: .8rem; border-top: 1px dotted #bbb;
              padding-top: .35rem; margin-top: .15rem; }

  /* The gate. Nothing is finished until one of these is clicked. */
  .gate { margin-top: .6rem; border-top: 1px solid #999; padding-top: .5rem; }
  .gate .lbl { margin-bottom: .3rem; }
  .gate button { font-size: .85rem; }
  .gate button.approve { border: 1px solid #6a9a75; background: #eaf5ec; }
  .gate button.edit    { border: 1px solid #999; }
  .gate button.esc     { border: 1px solid #c06a66; background: #fdeceb; }
  .verdict { display: inline-block; font-size: .78rem; font-weight: bold; letter-spacing: .04em;
             padding: .15rem .5rem; border: 1px solid; }
  .verdict.approved, .verdict.ok       { color: #17501f; background: #eaf5ec; border-color: #6a9a75; }
  .verdict.edited                      { color: #333;    background: #eee;    border-color: #999; }
  .verdict.escalated, .verdict.refused { color: #7a1717; background: #fdeceb; border-color: #c06a66; }
  .verdict.pending, .verdict.held      { color: #6a4a00; background: #fdf5e2; border-color: #b99a45; }
  .verdict.replaced, .verdict.reopened,
  .verdict.unknown                     { color: #444;    background: #eee;    border-color: #999; }
  .reason { font-size: .85rem; color: #444; margin-top: .3rem; }
  .escbox input { width: 100%; max-width: 26rem; padding: .35rem; font: inherit; font-size: .85rem; }
  dl.fields dd textarea { width: 100%; box-sizing: border-box; font: inherit; font-size: .85rem;
              padding: .3rem; min-height: 2.6rem; }
  dl.fields dd.locked { color: #555; }
  .edited-flag { font-size: .72rem; text-transform: uppercase; letter-spacing: .05em; color: #777; }

  /* The run log. */
  #log td { font-size: .8rem; }
  #log td.t { white-space: nowrap; font-variant-numeric: tabular-nums; }
  #logsum { font-size: .85rem; }
  #logsum b { font-variant-numeric: tabular-nums; }
</style>
</head>
<body>
<h1>Worth Eating &mdash; build __BUILD__</h1>
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

<h2>Settings</h2>
<fieldset>
  <legend>Anthropic API key</legend>
  <p id="keystate">checking&hellip;</p>
  <input type="password" id="apikey" placeholder="sk-ant-..." autocomplete="off" spellcheck="false">
  <p>
    <button id="save">Save key</button>
    <button id="clear">Clear key</button>
  </p>
  <p class="lbl">Stored in this browser's localStorage only. It is never written
  into this file, never sent anywhere except the Anthropic API when a run
  happens, and clearing it removes it.</p>
</fieldset>

<h2>System prompt</h2>
<p class="lbl">The <code>SYSTEM_PROMPT</code> constant, printed so the RULES
section can be checked against the PRD word for word.</p>
<details><summary>show</summary><pre id="sysprompt"></pre></details>

<h2>Client card &mdash; <code>client_profile.md</code></h2>
<div id="card"></div>

<h2>Policy files loaded</h2>
<ul id="policies"></ul>

<h2>What loaded</h2>
<table id="counts"></table>

<h2>Run log</h2>
<p>Every run lands here the moment it returns, marked <b>awaiting review</b>. It
stays that way until somebody approves, edits or escalates it. An unreviewed run
is meant to be conspicuous: a log that only listed decided runs would hide the
one case nobody looked at, which is the only case worth hiding.</p>
<p id="logsum"></p>
<div class="wrap"><table id="log"></table></div>
<p class="lbl">This session only. A reload restores it from the tab; closing the
tab clears it. Nothing here leaves the device.</p>

<h2>Cases</h2>
<p>Two kinds of id, and they are not the same thing. <b>CASE-n</b> is an eval
case in <code>eval_cases.csv</code>: an expected answer. <b>EVE-nn</b> is an
evening in <code>evenings.csv</code>: an input. A case points at an evening, and
the Run button lives on the evening.</p>
<div class="wrap" id="caseindex"></div>
<p class="lbl">Graded cases first, in case order. Highlighted cards carry one.</p>
<div id="cases"></div>

<h2>History &mdash; <code>history.csv</code></h2>
<div class="wrap"><table id="hist"></table></div>

<h2>Foods &mdash; <code>foods.csv</code></h2>
<div class="wrap"><table id="foods"></table></div>

<h2>Portions &mdash; <code>portions.csv</code></h2>
<div class="wrap"><table id="ports"></table></div>

<script>
const MODEL = "claude-opus-5";
const MAX_TOKENS = 16000;   // thinking is on by default and spends from this budget
const EFFORT = "high";      // low | medium | high | xhigh | max
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

document.getElementById("cases").innerHTML = ORDERED.map(e => {
  const ev = EVAL_CASES.find(c => c.evening_id === e.id);
  return "<div class='case" + (ev ? " seed" : "") + "'>" +
    "<b>" + e.id + "</b> &middot; " + e.day_type + " day" +
    (ev ? " &middot; <b>" + ev.id + "</b>" : " &middot; not graded") +
    "<div class='lbl'>ate today</div>" + e.ate_today +
    "<div class='lbl'>in the fridge</div>" + e.in_fridge +
    (ev ? "<div class='lbl'>" + ev.id + " &mdash; " + ev.type + "</div>" +
          ev.expected_behavior : "") +
    "<p><button class='run' data-id='" + e.id + "'>Run</button></p>" +
    "<div class='out' id='out-" + e.id + "'></div>" +
    "</div>";
}).join("");

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
  if (status === 400) return "The request was refused as malformed. Raw response below.";
  if (status >= 500) return "Anthropic returned a server error. Not your fault, try again.";
  return "Unexpected response (" + status + "). Raw response below.";
}

async function runCase(id) {
  const e = EVENINGS.find(x => x.id === id);
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
        messages: [{role: "user", content: userMessage(e)}]
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
  drawRun(newRun(e.id, meta, parsed, kind, statusClash(kind, parsed)));
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

function newRun(eveId, meta, parsed, kind, clashes) {
  // A re-run replaces what is on screen. If the previous run for this evening
  // was never reviewed, say so in the log rather than deleting the row: a run
  // nobody looked at is exactly the thing the log exists to show.
  RUNLOG.forEach(r => {
    const p = RUNS[r];
    if (p.eveId === eveId && p.action === "pending") {
      p.action = "replaced";
      p.reason = "re-run before anyone reviewed it";
    }
  });
  const rid = "r" + (++RUN_SEQ);
  const c = CASE_OF[eveId];
  RUNS[rid] = {
    rid: rid, eveId: eveId, caseId: c ? c.id : "", at: clockNow(), meta: meta, kind: kind,
    agent: parsed["Status"] || "no status given",
    fields: Object.assign({}, parsed),
    original: Object.assign({}, parsed),
    clashes: clashes, action: "pending", reason: "", changed: [], mode: ""
  };
  RUNLOG.push(rid);
  return rid;
}

function fieldsHtml(r) {
  return FIELDS.filter(f => f !== "Status").map(f => {
    const why = f === "Why";
    const editing = r.mode === "edit" && TOM_READS.indexOf(f) >= 0;
    const body = editing
      ? "<textarea data-f=\"" + f + "\">" + esc(r.fields[f] || "") + "</textarea>"
      : esc(r.fields[f] || "\u2014") +
        (r.changed.indexOf(f) >= 0 ? " <span class='edited-flag'>edited</span>" : "");
    return "<dt" + (why ? " class='why'" : "") + ">" + f + "</dt>" +
           "<dd class='" + (why ? "why" : "") + (editing ? "" : " locked") + "'>" + body + "</dd>";
  }).join("");
}

function gateHtml(r) {
  const b = (cls, act, label) =>
    "<button class='" + cls + "' data-act='" + act + "' data-r='" + r.rid + "'>" + label + "</button>";

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
    out.innerHTML = r.meta +
      "<div class='status " + r.kind + "'>" + esc(r.agent) + "</div>" +
      (r.clashes.length ? "<div class='err'><b>status disagrees with the body.</b> " +
         r.clashes.map(esc).join(" ") + "</div>" : "") +
      "<dl class='fields'>" + fieldsHtml(r) + "</dl>" +
      gateHtml(r);
    out.querySelectorAll(".gate button").forEach(b => {
      b.onclick = () => gateClick(b.dataset.act, b.dataset.r);
    });
    // On a phone the keyboard covers the button, so the keyboard's own key works.
    const box = out.querySelector(".escbox input");
    if (box) {
      box.onkeydown = ev => { if (ev.key === "Enter") { ev.preventDefault(); gateClick("sendesc", r.rid); } };
      box.focus();
    }
  }
  renderLog();
  saveLog();
}

function gateClick(act, rid) {
  const r = RUNS[rid];
  const out = document.getElementById("out-" + r.eveId);

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
                 reopened: "reopened"};
  el.innerHTML =
    "<tr><th>time</th><th>case</th><th>evening</th><th>agent decided</th>" +
    "<th>human action</th><th>note</th></tr>" +
    RUNLOG.slice().reverse().map(rid => {
      const r = RUNS[rid];
      return "<tr><td class='t'>" + r.at + "</td><td>" + esc(r.caseId || "\u2014") + "</td>" +
        "<td>" + esc(r.eveId) + "</td>" +
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
  const dash = t => !t || /^[-\u2013\u2014\s.]*$/.test(t);
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

document.querySelectorAll("button.run").forEach(b => {
  b.onclick = () => runCase(b.dataset.id);
});

tbl("hist", HISTORY, ["date", "kcal", "protein_g", "xp"]);
tbl("foods", FOODS, ["name", "kcal_per_100g", "protein_g_per_100g", "fat_g_per_100g", "fibre_g_per_100g", "xp", "typical_location"]);
tbl("ports", PORTIONS, ["food", "variant", "kcal", "protein_g", "fat_g", "fibre_g", "xp"]);

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

for k, v in {"__BUILD__": BUILD,
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
