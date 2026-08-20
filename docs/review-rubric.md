# Review rubric

There is no faculty reviewer for this project. This is the substitute.

**It is not a Moe persona.** A persona would invent opinions he never held, and
they would then get acted on as if they were faculty guidance. This is a rubric
extracted from his two recorded reviews of PlateMate, and every criterion cites
the sentence it came from. That makes it checkable. A persona is not.

Sources: the Faculty Feedback sections of `DISCOVERY.md` and `DESIGN.md` in
`AI-Capstone-Project`, July 2026.

---

## The shape of a review

Both of his reviews have the same skeleton, which is what makes this extractable
rather than invented.

1. Two or three **specific strengths**, named in product terms
2. **Exactly two refinements** — never a list
3. Refinement one is always **scope**
4. Refinement two is always the **harm surface**
5. A **build directive**, not just an opinion
6. **Conditional approval** to proceed

---

## The criteria

### 1 · Does the metric map to the failure the product exists to prevent?

> "you picked a primary metric that maps directly to the failure the product
> exists to prevent (no-skip rate, not some vanity accuracy number)"

Fails on: accuracy scores, satisfaction, engagement, anything that could look
good while the product does nothing.

### 2 · Are thresholds data, not prompt text?

> "you encoded the tolerance threshold as data rather than burying it in a
> prompt (±10g protein / ±150 kcal)"

Any number the behaviour depends on must live somewhere it can be read, changed
and tested. A number inside a prompt string is not a rule, it is a suggestion.

### 3 · Is the judgement separated from the arithmetic?

> "you correctly identified that the multi-day averaging principle is coaching,
> not math — that's a real product insight"

Say which parts are computed, which are model judgement, and which stay human.

### 4 · Scope: is this one loop, or a lot of surface?

> "an orchestrator plus a nutrition agent plus a sleep-and-recovery agent plus
> stubbed fitness agents is a lot of surface for one prototype"

> "get case 1 and case 7 running end to end before you touch the tier pair,
> prove the loop first, then earn the complexity"

Stubs cost time and prove nothing. Name the one demo-worthy moment and cut back
to what proves it.

### 5 · Harm surface: is the dangerous path concrete or described?

The heaviest criterion. He spent more words here than on everything else
combined.

> "this product is a macro-optimizer talking to people who care intensely about
> macros, and that is a real harm surface — the same reasoning that produces a
> smart lunch swap can produce a compensatory-restriction suggestion for a user
> who shouldn't receive one"

> "make this concrete: what specific language patterns does the agent refuse to
> generate, what triggers a hard stop versus a soft coach nudge... Write that
> rule explicitly, and put it in your eval set"

Three tests: **what exact language is refused**, **what separates a hard stop
from a nudge**, and **is it in the eval set**. Listing a risk as an escalation
trigger is not enough — that is what he said was already there and still not
sufficient.

### 6 · Pre-authored language wherever a bad sentence could do damage

> "pre-authored language on every path where a bad sentence could do damage"

If the wording carries the safety, the model does not get to write it.

### 7 · One-way safety, enforced structurally

> "a deterministic floor the model cannot bypass, an LLM that can only add stops
> and never clear them"

The constraint should hold because of what the output is allowed to contain, not
because the model behaves.

### 8 · Single source of truth

> "Rejecting silent preference learning so the coach stays the single source of
> truth was the right call too."

Nothing learns quietly in a way that moves a target the coach set.

---

## Standing findings on the Discovery answers

Applied 2026-08-20, against `discovery-prd.md`.

**Criterion 1 — pass.** *Nights not hungry at eleven* is the failure itself, not
a proxy for it. The two build metrics underneath it include a refusal rate, which
is what stops an always-answering agent from scoring perfectly.

**Criterion 4 — pass, with one watch.** One loop, one agent, no orchestrator, no
stubs. Tighter than PlateMate was at the same stage. The thing that could balloon
is the shop-real food list.

**Criterion 5 — the real gap. Two of them.**

*Who decided Tom is safe to receive this?* The coach set his target, so screening
presumably happened offline. It is written down nowhere. In PlateMate that
boundary was explicit; here it is assumed.

*The no-room state has no eval case of its own.* It is named as a Design problem,
which is correct, but his pattern is: write the rule, then put it in the eval set
beside the escalation case. Right now the eval list has escalation and no-room
listed, but no known-good wording attached to either.

And this workflow is exposed in a way PlateMate was not: **it speaks every
night**, not only when a day breaks. It is also safer in one way — it can only
ever add food. Both facts belong in the Design answer, stated rather than
implied.

**Criteria 2, 3, 6, 7, 8** — not yet testable. They are Design questions and
should be re-run when the Design answers exist.

---

## How to use it

Run it at the end of each phase, before moving on. Two refinements, not a list —
if more than two things are wrong, the phase is not finished.

**And a warning about who runs it.** Claude helped write these answers, so Claude
reviewing them is weak. The criteria are mechanical enough for Milan to apply
directly, and that is the better use.
