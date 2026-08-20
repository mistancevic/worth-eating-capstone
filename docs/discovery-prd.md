# Discovery PRD answers

Ten self-contained answers. No link-outs — each one stands alone if pasted on its
own.

Completed 2026-08-20 through the Discovery Companion v0.2.

---

## 1 · User

```text
Tom, 34, a backend developer in Munich with two small children. He trains three times a week and has a coach who set him a daily calorie and protein target. He does not cook much. The target exists as a PDF on his phone; he read it once and has never had it in his head while deciding what to eat. Tom is an invented persona, not a real person, and no real client data is used anywhere in this project.
```

## 2 · Workflow

```text
Deciding what to eat late in the evening so the day's protein target is met, using whatever is already in the house. Not cooking from a recipe — choosing and combining what is there, and adding something if the meal falls short. It happens every night, which makes it a daily recurring workflow rather than an occasional one.
```

## 3 · Trigger

```text
Tom opens the fridge after putting the children to bed, at around nine, hungry. The trigger fires every night whether the day went to plan or not, so nothing has to be detected and no disruption has to occur. He did not decide to eat at that hour; hunger interrupted him.
```

## 4 · Current process

```text
1. Tom feeds the children and does not eat with them.
2. He puts them to bed.
3. He sits with the laptop until hunger hits.
4. By then it is late.
5. He opens the fridge.
6. He sees leftovers, bread, cheese, and whatever else needs no cooking.
7. He takes that and eats it standing up.
8. He never thinks about the coach's target.

By his own standard nothing has gone wrong. Eating something at that hour already feels like a good step, so there is nothing for him to correct.
```

## 5 · Pain points

```text
The meal that decides the day is chosen when Tom is most tired, hungriest, and least attentive, and what he picks is dilute — bread and cheese carry calories without much protein. The coach's target never reaches the fridge door; it is real, and it is in a PDF. Nothing about the choice feels wrong, so nothing corrects it, and he never finds out he fell short.

The person who feels the failure is the coach, weeks later, when weight and strength have not moved. That is an adoption problem before it is a product problem, because Tom has no reason of his own to open anything.

What Tom does feel is a much shorter loop he never connects to the meal: a dilute dinner at nine, hungry again at eleven, poor sleep, and five coffees the next day. The signal the coach waits six weeks for is available to Tom the same night.
```

## 6 · Agent opportunity

```text
The agent takes one decision off Tom at the fridge: what to add so the meal reaches his target, and whether to add anything at all.

A run contains six decisions rather than one lookup. It decides whether the message is a food question or something that must be escalated. It decides what "a sandwich and a coffee" amounts to in protein and calories, with no weights and no photograph. It decides which of three states the day is in — short with room left, already at target, or no room left. If there is room it selects an item from what Tom said he has, then checks whether that item actually fits the remaining calories and picks again if it does not. Finally it checks the answer against the boundary.

An agent fits rather than a static feature for two reasons. The selection step loops, because the first choice often does not fit the calories left. And the agent can decide not to answer: there are states where the correct output is a refusal or a redirect, and it has to reach them on its own. A chatbot always answers.

It also does not work from the conversation alone. The target comes from the client profile, the food numbers from a product list, and the boundary from a policy document — three sources Tom never typed.
```

## 7 · Synthetic data plan

```text
Everything is invented. No real client, no real household, and no data gathered from any person.

A synthetic client profile carrying Tom's bodyweight, age, training days, and the calorie and protein target his coach set. The target arrives as data; the agent never calculates it.

A food list built to look like a real German supermarket shelf — Rewe and Edeka products with protein and calories per 100 g. It deliberately includes the awkward cases, such as prepared chicken breast filled with water that yields about 35 g of protein per 150 g pack where a generic food table would claim closer to 45 g. Getting that right is where the value sits, and a generic database does not have it.

A safety and escalation policy as its own document, so the boundary can be tested rather than only prompted.

The day so far, given by Tom in his own words during the conversation — "a sandwich, a coffee, some crisps at my desk." Nothing tracks him, so turning that into a number is the agent's job. The project is text only: no photographs and no weighing.

Evaluation cases cover the booster case, the already-at-target case, the no-room case, an escalation case, and a case where the only available foods cannot close the gap.
```

## 8 · Human boundary

```text
The agent never tells Tom not to eat, never suggests skipping a meal, and never diagnoses anything. It advises and Tom decides; nothing is logged or committed without him.

It never pushes. It answers when Tom opens it and is silent otherwise. There is no notification at eight in the evening telling him he is behind. This matters more here than in a workflow that only speaks when something goes wrong, because this one is present every single night, and a tool that comments on every meal becomes surveillance.

It escalates rather than answers when the message is not a food question — dizziness, not having eaten all day, anything medical, or anything outside nutrition go to the coach or to a professional.

It does not override the coach's plan, and it does not set or change the target.

The no-room state carries the sharpest risk in the whole product: telling someone there is nothing left in the day sits one badly written sentence away from telling them not to eat. The exact wording is specified in Design, not left to the model.
```

## 9 · Success metric

```text
The practical metric is how many nights Tom is not hungry at eleven. It is his own signal, it arrives the same night, and it is the only promise the product can honestly make. Energy and sleep are the reason he would care, but the agent cannot control them — they also depend on his children, his laptop, his training and his coffee — so they are never promised and never measured.

That metric needs real users, so two build metrics run on the synthetic evaluation set in the meantime. The first is the share of runs where the agent's suggested addition actually closes the protein gap using only items Tom said were available. The second is the share of runs where it correctly refuses — on the no-room state and on escalation — because a tool that always answers scores perfectly on the first metric while being unsafe.
```

## 10 · Initial demo idea

```text
One continuous session with two runs.

In the first, Tom types what he ate that day in his own words, then types what is in the fridge. The agent shows the arithmetic on screen — where he stands against the coach's target and what is left — and then names one thing to add, chosen from what he actually has, with the numbers shown.

In the second run the day is already spent. The same opening produces a different answer: there is nothing to add tonight, here is why, and here is what to do differently tomorrow. Nothing is suggested that would take him further over, and he is never told not to eat.

The second run is the point of the demo. A demonstration in which everything works proves nothing, and the refusal is what shows the boundary is real rather than described.
```
