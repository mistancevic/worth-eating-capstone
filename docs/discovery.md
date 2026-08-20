# Discovery

Run with the Discovery Companion v0.2, in `discovery-companion/`.

## The start prompt

Verbatim from `STUDENT_START_PROMPT.md`:

```text
I am starting the Discovery phase of my Agentic AI Capstone.

Read START_HERE.md, AGENTS.md, and 01_DISCOVERY.md.

Help me choose my own capstone project. Do not recommend Northstar Home as my project. Northstar Home is only an example.

Ask me one question at a time. Grill me until I have a safe, specific, demoable agentic workflow.

Then help me write self-contained Discovery PRD answers for:
1. User
2. Workflow
3. Trigger
4. Current process
5. Pain points
6. Agent opportunity
7. Synthetic data plan
8. Human boundary
9. Success metric
10. Initial demo idea

After the Discovery PRD answers are complete, stop and tell me not to move to Design yet.
```

## How this runs

From `AGENTS.md`. One question at a time. After each answer: assess it briefly,
say how to improve it, ask the next one. Grill on vague users, vague workflows,
unsafe data, generic chatbot ideas, no visible demo, too much autonomy, no human
boundary, no success metric.

Stop when the ten PRD answers are done. Do not touch Design.

## Three lists, and they are not the same

**The interview** — `01_DISCOVERY.md` Step 4. What gets asked.

1. Who is the specific user?
2. What event starts the workflow?
3. What does the user do today?
4. Where does the workflow slow down or fail?
5. What decision should the agent help with?
6. What should the agent not be allowed to do?
7. What data can you safely use?
8. What output will the demo show?
9. What metric would show value?
10. What would make this clearly agentic?

**The Grill** — `PROJECT_IDEA_GRILL.md`. A pressure test, plus a Go / No-Go
filter. Used to break the idea, not to build it.

**The PRD fields** — what gets written at the end. Ten self-contained answers,
no link-outs.

---

# Answers

## 1 · Who is the specific user?

*Open. Waiting on the workflow question first.*
