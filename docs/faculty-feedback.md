# The real feedback, against the rubric that stood in for it

PlateMate's capstone feedback arrived on 2026-09-09. The certificate is dated
2026-08-08.

**Total 14 of 15.** Problem & Discovery 4.5 · AI Solution & Evaluation **5** ·
Storytelling, Clarity & Overall Delivery 4.5.

This file exists because [`review-rubric.md`](review-rubric.md) was built to
stand in for exactly this document, and it has now been graded against the real
thing. Quotes below are cleaned of ligature damage from the PDF extraction
(`ofteen` → `often`, `Thee` → `The`); nothing else is changed.

---

## The rubric was right about the things it covered

Five of its eight criteria show up in the final feedback almost word for word.
They were extracted from two interim reviews written a month earlier, which means
these are stable convictions rather than one-off remarks.

| rubric criterion | what the faculty actually wrote |
|---|---|
| **1** metric maps to the failure | *"your no-skip metric maps directly to the job the product must perform"* |
| **3** judgement separated from arithmetic | *"assigns calorie and protein arithmetic to code, uses the model for situational interpretation"* |
| **5** harm surface made concrete | *"the frozen safety policy, three-client pilot, coach-owned escalations, and one-missed-escalation stop rule create an unusually disciplined validation environment"* |
| **7** one-way safety, structural | *"a deterministic gate that operates before model exposure"* |
| **8** single source of truth | *"respects an important ownership boundary — the coach sets the plan and targets"* |

Criterion 7 is the sharpest match. The rubric said *"a deterministic floor the
model cannot bypass"*; the feedback said *"before model exposure"*. Same idea,
arrived at independently.

**And the dimension the rubric pushed hardest on is the one that scored full
marks.** Criteria 2 to 8 are nearly all about solution and evaluation, and that
is the 5. The two 4.5s are the dimensions the rubric barely touches.

---

## What it missed, and this is the part worth keeping

### It has no storytelling criterion at all

A third of the grade is *Storytelling, Clarity & Overall Delivery*, and the
rubric has nothing on it. Not a weak criterion. None.

That is not carelessness, it is where the rubric came from: both source reviews
were interim product reviews, so they talked about product. The final grade
covers presentation too.

What the faculty praised there is specific and learnable:

> *"A specific 3 p.m. moment makes the planning gap vivid, the ice cream and team
> dinner turn macro recalculation into a relatable decision, and the
> 150-calorie/35-gram constraint gives the demo real texture."*

> *"The four-minute pacing is deliberate, and the closing thought — that a plan
> must survive the days it was not written for — elevates PlateMate from meal
> suggestion to sustained adherence without overstating what the prototype
> decides."*

A named moment, a decision anyone recognises, one hard number, deliberate pacing,
and a closing line that says what the thing is for. **Worth Eating has no
equivalent of any of that**, and it is a third of the marks.

### It predicted refinements that a final grade does not contain

The rubric's shape says *exactly two refinements: scope, then harm surface*. The
real feedback has **none**. It is all strengths.

That is the difference between a formative review and a summative one, not a
failure of the rubric — but it means the rubric cannot be used to predict a
grade. It predicts what a reviewer will push on mid-build, which is a different
and still useful job.

### It did not anticipate the single most striking sentence

> *"Correcting the happy-path expectation instead of changing a system that was
> behaving as designed is a particularly mature iteration."*

The faculty singled out **not grading to the output** as the most mature thing in
the whole project.

That is the exact discipline this build broke and had to repair. At p06 I changed
CASE-5's expected day from 141 kcal to 114 to match what the model returned, and
recorded it in [`develop.md`](develop.md) as *"exactly the failure I had been
warning about"*. At p06g the mirror image happened: CASE-4's expected 127 g of
Gouda was **mine and wrong**, the model's 125 g was right, and the CSV settled
which of the two situations I was in.

The rubric did not contain this criterion because neither interim review
mentioned it. It is now criterion 9.

---

## What this changes for Worth Eating

**Stop hardening the part that already scores full marks.** Nine prompts have
gone into evals, boundaries, citations and the human gate. That is dimension 2,
the 5. Every remaining mark is in Discovery and in Delivery.

**Discovery is already moving**, through the mismatch frame filed in
[`variants.md`](variants.md). That work is pointed at the right dimension.

**Delivery is untouched and is a third of the grade.** Worth Eating needs its own
3 p.m. moment. It has candidates and has never chosen one: the 21:35 feeding that
carries 13.5 g against a 26 g trigger, and the night Tom picks at the children's
pasta and the day moves from 33 g to 46 g. Those are the ice cream and the team
dinner. Section B of the Develop playbook is where they get a screen.

**Criterion 9 goes into the rubric**, because it is now the highest-praised thing
in a graded capstone and it is the one this build has already got wrong once.
