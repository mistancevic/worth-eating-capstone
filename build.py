#!/usr/bin/env python3
"""Generates index.html from data/ and policies/.

A dev tool, not part of the prototype. index.html stays the single
self-contained file the kit asks for; this script exists so the inlined
constants can never drift from the CSVs they came from.
"""
import csv, json

def rows(p): return list(csv.DictReader(open(p)))

FOODS   = rows('data/foods.csv')
PORTIONS= rows('data/portions.csv')
HISTORY = rows('data/history.csv')
EVENINGS= rows('data/evenings.csv')
EVALS   = rows('data/eval_cases.csv')
POLICIES= {'safety_policy.md': open('policies/safety_policy.md').read(),
           'output_rules.md' : open('policies/output_rules.md').read()}
CARD = {"name":"Tom","kcal":2300,"protein_g":150,"xp":6.5,
        "meal_trigger_g":26,"fat_floor_g":55,"fibre_g":32}

SYSTEM_PROMPT = """ROLE
The agent is hired to name what to add to a late meal so Tom reaches his coach's protein target, within the coach's numbers and a rule that it may only ever add food, escalating when the message is not about food, when the day's intake is far below target, or when it is not confident.

CONTEXT
Use only the embedded constants. Never invent a fact, a food, or a number.
  CARD      - Tom's card, issued by his coach: 2300 kcal, 150 g protein, Personal XP 6.5, meal trigger 26 g, fat floor 55 g, fibre 32 g. Never recalculate any of it.
  FOODS     - named products with protein, calories, fat, fibre per 100 g and an XP. A food not in FOODS has no numbers.
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
Exactly these five labeled fields, nothing else:
  Today:      protein of target, kcal of budget, and the score against his 6.5
  Left:       protein and kcal remaining
  Add:        one item from what he actually has, with grams, kcal, its own XP, and whether it clears the 26 g meal trigger
  After that: the day re-scored with the addition included
  Note:       usually empty

A candidate for Add must pass four tests: it closes the protein gap, it stays inside the calories left, it carries at least 26 g of protein, and the day lands at or above 6.5 once it is included. Fail any one and try the next candidate.

Fat and fibre are floors, not fields. They break ties between candidates that already pass, and appear in Note only when a floor will be missed.

ESCALATION
Stop, state the reason, and hand to the coach when:
  - LOW CONFIDENCE: it cannot tell what a food was. Say so, ask one question, do not guess.
  - MISSING DATA: no target, or a named food with no row in FOODS. Ask. Never invent. A vague fridge is this case with nothing named: ask once for one specific thing, then stop.
  - OUT OF POLICY: a meal plan, a diet, a change to the target, or anything else the coach owns. Refuse, point at the coach.
  - HIGH STAKES: anything medical. Stop. Coach or doctor.
  - APPARENT INTAKE FAR BELOW REQUIREMENT: a described day no estimation error explains, such as 400 kcal against 2300. Ask once, "is that everything today". Only escalate if confirmed. Report no XP on this path.

Anger or legal language is not a trigger here. It is a support-desk pattern and this client is alone at his own fridge. Dropped deliberately.

WORDING
Every sentence on a stopping path is pre-authored in output_rules.md. Use it as written."""

HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Worth Eating &mdash; build p03</title>
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
</style>
</head>
<body>
<h1>Worth Eating &mdash; build p03</h1>
<p>Prompt 03: the system prompt and the settings panel. Still no API calls and
still no styling &mdash; both arrive later in the playbook.</p>

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

<h2>Cases &mdash; <code>evenings.csv</code></h2>
<p class="lbl">Highlighted rows are seeded for an eval case. The linked eval row is shown underneath.</p>
<div id="cases"></div>

<h2>History &mdash; <code>history.csv</code></h2>
<div class="wrap"><table id="hist"></table></div>

<h2>Foods &mdash; <code>foods.csv</code></h2>
<div class="wrap"><table id="foods"></table></div>

<h2>Portions &mdash; <code>portions.csv</code></h2>
<div class="wrap"><table id="ports"></table></div>

<script>
const MODEL = "claude-sonnet-4-5";
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
  "<tr><th>Fat floor</th><td>" + CARD.fat_floor_g + " g</td></tr>" +
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

document.getElementById("cases").innerHTML = EVENINGS.map(e => {
  const ev = EVAL_CASES.find(c => c.evening_id === e.id);
  return "<div class='case" + (ev ? " seed" : "") + "'>" +
    "<b>" + e.id + "</b> &middot; " + e.day_type + " day" +
    "<div class='lbl'>ate today</div>" + e.ate_today +
    "<div class='lbl'>in the fridge</div>" + e.in_fridge +
    (ev ? "<div class='lbl'>linked eval case &mdash; " + ev.id + " (" + ev.type + ")</div>" +
          ev.expected_behavior : "") +
    "</div>";
}).join("");

tbl("hist", HISTORY, ["date", "kcal", "protein_g"]);
tbl("foods", FOODS, ["name", "kcal_per_100g", "protein_g_per_100g", "fat_g_per_100g", "fibre_g_per_100g", "xp", "typical_location"]);
tbl("ports", PORTIONS, ["food", "variant", "kcal", "protein_g", "fat_g", "fibre_g", "xp"]);
</script>
</body>
</html>
"""

for k, v in {"__CARD__": json.dumps(CARD), "__FOODS__": json.dumps(FOODS),
             "__PORTIONS__": json.dumps(PORTIONS), "__HISTORY__": json.dumps(HISTORY),
             "__EVENINGS__": json.dumps(EVENINGS), "__EVALS__": json.dumps(EVALS),
             "__POLICIES__": json.dumps(POLICIES),
             "__SYSPROMPT__": json.dumps(SYSTEM_PROMPT)}.items():
    HTML = HTML.replace(k, v)

open('index.html', 'w').write(HTML)
print("index.html", len(HTML), "bytes")
