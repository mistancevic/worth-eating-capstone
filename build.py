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
Exactly these six labeled fields, in this order, and nothing else. Each field begins on its own line with the label written exactly as shown, then a colon and a space. Plain text only: no markdown, no asterisks, no bold, no bullets, no headings, no blank line between the label and its text.
  Today:      protein of target, kcal of budget, and the score against his 6.5
              When a named food has no row in FOODS and the day cannot be totalled, Today still carries what IS confirmed: the resolved items with their kcal and protein, their subtotal, and the word incomplete. No score - a score on a partial day is a lie. Do not make him wait for a number he can already have.
              On the undereating path Today stays a dash. That path is a stop, and arithmetic on screen turns a stop into a calculation.
              A dash otherwise means nothing at all is known.
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
When Status is HELD or REFUSED-ESCALATE, Add and After that are dashes. The agent never proceeds with a reduced answer.
A request the coach owns is refused even when the rest of the message is ordinary food. Do not answer the food half and refuse the other.

WHY is the only field Tom is not meant to read, and it is the only place a reference belongs. Name the data you actually used and the policy line you actually applied, as short references separated by semicolons. Not prose, not an explanation of your thinking, no apology, and never addressed to Tom. Cite policies by identifier: S1 to S5 from the safety policy, O1 to O5 from the output rules. Shape:
  Why: FOODS Skyr Natur 11 g/100 g; PORTIONS Sandwich medium; fit check 4/4; portion closes gap in full; O2.
A field with nothing to say still appears, with a dash after the colon. Never omit a label.

A candidate for Add must pass four tests: it closes the protein gap, it stays inside the calories left, it carries at least 26 g of protein, and the day lands at or above 6.5 once it is included. Fail any one and try the next candidate.

PORTION - the size is part of the answer, not an afterthought:
  - Name the portion that closes the gap in full, not the smallest one that clears the tests.
  - If no portion closes the gap in full inside the calories left, name the largest that does fit and still passes the other three tests, and say plainly how much protein is still short.
  - In the same line, name the least that still lands the day at or above 6.5, worded as a fallback for a night when the full portion is more than he wants.
  - If the two come out the same, name one.
Both figures are additions. Never word the fallback as eating less, saving calories, cutting back, or making up for anything.

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
<title>Worth Eating &mdash; build p06</title>
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
</style>
</head>
<body>
<h1>Worth Eating &mdash; build p06</h1>
<p>Prompt 05: the reply arrives in a strict format and gets parsed. Each field
renders with its label, and a sixth field, Why, names the data and the policy
line behind the answer. It is for a reviewer, not for Tom, so it sits below the
rule. If the shape is wrong the raw text is shown with a notice rather than a
crash. Styling still comes later.</p>
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
    "FOODS (per 100 g): " + JSON.stringify(FOODS.map(f => ({
      name: f.name, kcal: +f.kcal_per_100g, protein: +f.protein_g_per_100g,
      fat: +f.fat_g_per_100g, fibre: +f.fibre_g_per_100g, xp: +f.xp}))),
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
  const clashes = statusClash(kind, parsed);
  const rows = FIELDS.filter(f => f !== "Status").map(f =>
    "<dt" + (f === "Why" ? " class='why'" : "") + ">" + f + "</dt>" +
    "<dd" + (f === "Why" ? " class='why'" : "") + ">" + esc(parsed[f] || "\u2014") + "</dd>"
  ).join("");
  out.innerHTML = meta +
    "<div class='status " + kind + "'>" + esc(st || "no status given") + "</div>" +
    (clashes.length ? "<div class='err'><b>status disagrees with the body.</b> " +
       clashes.map(esc).join(" ") + "</div>" : "") +
    "<dl class='fields'>" + rows + "</dl>";
}

// The agent declares its own status, so the status is not a check on its own.
// This compares the declaration against the reply it sits on. A contradiction
// is shown rather than resolved: guessing which half is right would be the
// same mistake as letting the agent grade itself.
function statusClash(kind, p) {
  const out = [];
  const citesSafety = /\bS[1-5]\b/.test(p["Why"] || "");
  const dash = t => !t || /^[-\u2013\u2014\s.]*$/.test(t);
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
