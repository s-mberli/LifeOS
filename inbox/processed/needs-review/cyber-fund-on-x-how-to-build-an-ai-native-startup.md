---
actionability: high
attached_experts: []
channel_name: ''
created_at: '2026-05-28T09:06:19.260971+10:00'
domain: ai-platform
expert_status: unattached
primary_mode: router
privacy: public
review_status: new
secondary_modes: []
source_type: article
source_url: https://x.com/cyberfund/status/2058950286324986294?utm_source=tldrfounders
status: processed
suggested_experts: []
tags:
- founders
- founders guide
- AI startup
- AI-native
- startup building
- business strategy
- entrepreneurship
- startup guide
- AI
title: 'cyber•Fund on X: "How to Build an AI-Native Startup'
transcript_path: ''
type: insight_note
updated_at: '2026-05-28 09:57:15'
---



# cyber•Fund on X: "How to Build an AI-Native Startup

## Summary
**Manual summary needed.**

## Key Ideas
- Manual extraction needed.

## Why this matters for Markus
- Suggested based on routing to unknown.

## Related Modes
- router

## Next Action
- [ ] Review this resource and extract practical action steps.

## Source Reliability
Based on raw user input and metadata.

## Original Content
### Raw User Input
https://x.com/cyberfund/status/2058950286324986294?utm_source=tldrfounders

### Fetched Web Text
Title: cyber•Fund on X: "How to Build an AI-Native Startup" / X

URL Source: https://x.com/cyberfund/status/2058950286324986294

Markdown Content:
## Article

## Conversation

[![Image 1: Square profile picture](https://pbs.twimg.com/profile_images/2056773209765158912/rJ4AdL0w_normal.jpg)](https://x.com/cyberfund)

[![Image 2: Image](https://pbs.twimg.com/media/HJLRo-EXEAAppVJ?format=jpg&name=small)](https://x.com/cyberfund/article/2058950286324986294/media/2058938481447997440)

How to Build an AI-Native Startup

A practical guide for founders going from zero to AI-native: map the work, build the context, write the evals, run the loop.

By Stepan Gershuni,

Read this article on the

blog

It's 9am at two startups in the same market, founded the same month. At company one, the ops lead is still working through old support tickets, the analyst is rebuilding last week's dashboard, and the founder is on a standup about a customer call nobody's been able to resolve. Everyone is scrambling to fix yesterday’s problems and the product is stagnating.

At the second company, all of that happened overnight. Agents triaged the tickets, refreshed the dashboard, surfaced the churn risk buried in the call. The founder has already fixed the problem and is iterating on the product with his team.

Yes, founders will spend their time differently in an AI-native startup, but that’s not the fundamental change. The fundamental change is how fast the company can learn, iterate, and evolve. The second company will outlearn the first every single day. Over weeks, this will compound leverage. Over months and years, only one will succeed.

[![Image 3: Image](https://pbs.twimg.com/media/HJLSHEBXUAEGjuk?format=jpg&name=small)](https://x.com/cyberfund/article/2058950286324986294/media/2058938998442119169)

The company is AI-native when its operating model changes: fewer people coordinate less, agents execute more of the repeat work, and humans focus on direction, taste, relationships, validation, and accountability.

For founders looking to build or rebuild their companies into this new reality, it can seem like a daunting task. But it doesn’t have to be. Building AI-native starts with a few steps that when iterated upon recursively will completely reorganize the way your company operates.

It goes a little something like this:

*   Map the work

*   Build the context system

*   Choose the simplest automation that works for each piece

*   Turn repeated work into skills

*   Write evals that decide whether the work is good

*   Run the company loop on a weekly improvement rhythm.

Step one. Start with the work graph.

List the recurring work the startup ran in the last two weeks: customer-call notes, lead research, outbound drafts, support triage, product QA, onboarding, release notes, investor updates, weekly metrics, bug reproduction, recruiting screens, invoice review, competitor monitoring, all of it. If the work repeats, it is a candidate for encoding. Most founder calendars contain 20 to 40 such items; an early-stage team that lists them honestly will find ten to fifteen they did not realize were already routine.

[![Image 4: Image](https://pbs.twimg.com/media/HJLSZVrXgAA-9w9?format=png&name=small)](https://x.com/cyberfund/article/2058950286324986294/media/2058939312419340288)

Classify every work unit by autonomy level:

L1 is human only: a strategic call, a final hire, a major refund, a legal signature, a board communication.

L2 is AI prepared, human approved: an investor update draft, a contract redline, a pricing-page rewrite, a support macro.

L3 is AI executes, human supervises: inbound triage, meeting-note routing, lead enrichment, test generation.

L4 is autonomous inside clear limits: competitor monitoring, nightly report generation, invoice extraction from known vendors, simple anomaly detection.

The boring workflow usually wins. A weekly strategy memo feels like the prestigious thing to automate. Daily support-tagging — which is unglamorous and repetitive — recovers more hours and gives you cleaner ground truth, because it runs ten times as often. Frequency beats prestige. The first workflow to attack is frequent, measurable, reversible, and tied to a real bottleneck.

Do not automate work that is rare, unclear, high-trust, or unstable. A C.H. Robinson team tried to push email triage at 10,000 messages per day to L4 and reverted to L2 once supervision proved infeasible; the volume hid the cost of every misroute. If the team cannot explain what good output looks like, the workflow is not ready for encoding. If one wrong output can damage a customer relationship, move slowly. If the process changes every week, wait for it to stabilize or keep it as AI-assisted human work.

When you're done with this primary step, you have one page and three workflows to start: one personal (inbox triage, daily brief, investor-update draft), one customer-facing (call synthesis, ticket classification, lead enrichment), one internal (test generation, invoice extraction, the weekly metric narrative). Having too many experiments at the same time dilutes attention and produces twenty half-finished pilots, which is the most common failure mode at this stage.

Context is the AI native startup's operating memory. It's everything the company knows about itself, held where agents can read it. While models are interchangeable and improving every month, context is the part that's actually yours. It’s what separates an agent that works like a cofounder from one that works like a confused temp.

If the team spends more time rewriting agent output than reviewing it, the problem is rarely the prompt or the model. The agent just doesn’t know enough about the company — your customers, your product, your priorities, the decisions you already made and why.

There’s an easy diagnostic you can run weekly to ascertain the state of play: pick one representative task, hand it to a fresh agent with only the workspace context, and ask for three next actions. Two or more strong suggestions means the context layer is carrying weight. Three generic answers means the context is thin and the prompt cannot rescue it.

[![Image 5: Image](https://pbs.twimg.com/media/HJLSnnjWkAA_SwG?format=png&name=small)](https://x.com/cyberfund/article/2058950286324986294/media/2058939557735731200)

Start with one shared Git repository every team member and agent can read. Git wins for a simple reason: it's versioned, diffable, readable by humans and agents alike, and tied to no vendor's runtime. It will outlive every model and harness you run through it. The whole workspace at day seven can be one root with CLAUDE.md, context/company.md, context/product.md, context/customers.md, context/lessons.md, and GTD.md for active work.

A general rule of thumb is to keep it to 40–60 hand-written lines; a tight list of what to avoid beats 400 generated lines of slop. It won't solve every context problem, but it solves enough that agents stop hallucinating basic facts about your own company.

As the startup grows, split the context system by permission boundaries. There are a couple of ways to do this. For example: a shared company repo plus private repos per function (sales, product, engineering, finance, support). Another: private repos per project or customer with a shared root for company-wide context.

At enterprise scale, a private Git server (self-hosted Gitea, GitHub Enterprise, GitLab) gives directory-level or repo-level permissions so agents and humans see only the context they are allowed to see. Block's internal harness Goose reads the same artifact stream the rest of the company sees, scoped by role; the moment scoping drifts, agents start mixing public-conviction language with private-deal context. That’s why boundaries are incredibly important.

Three kinds of data feed the system.

Connectors pull from outside — SaaS tools, APIs, MCP servers, email, calendar, CRM, support, analytics, GitHub, Linear, Stripe, the warehouse, the docs. Every connector needs an identity, scoped permissions, audit logs, and managed credentials, or the sprawl quietly becomes your biggest security hole. An IAM layer like Zitadel carries that identity discipline. How you load the tools matters too: Anthropic's MCP code-execution work shows a filesystem-of-server-folders pattern dropping context use from ~150,000 tokens to ~2,000 versus loading every tool definition upfront — a 98.7% cut in token spend (your accounting team will thank you).

Data the company generates — specs, customer summaries, decisions, lessons, project notes, operating rules. Markdown by default, and one rule that matters more than the rest: keep raw separate from distilled. A call transcript is raw. The decision made on that call, the objection the customer raised, the follow-up owner, the renewal risk — that's distilled, and that's what agents actually query. Keep the decision log append-only, one decision per line, so the reasoning travels with the conclusion. If you conflate raw and distilled, you’ll drown in transcripts while never building the layer that's useful.

Databases and streams, where the source of truth already lives — product data in Postgres, marketing in the warehouse, events in analytics. Don't copy it blindly into markdown. Leave the database as the source of truth, give agents a limited-read user, document the schema in an agent-facing file (data-models/postgres.md), and spell out exactly which queries and writes are allowed. Agents should not be able to delete production data by default. The Replit incident from mid-2025 — a coding agent wiped a production database mid-session — is the standing reminder that a prompt instruction is not a security boundary.

The advanced version is a structured context graph. Before agents query anything, raw artifacts get processed into entities and relationships: people, companies, objections, commitments, feature requests, renewal risks, follow-ups, dates, decisions, source links. Instead of storing transcripts, you extract what's in them and link every call with the same people or project into a chain. Now an agent can answer "what's the renewal risk on Vandelay Industries?" and cite the exact line where the customer said it.

Provenance holds the whole thing together. Every agent summary has to trace back to its source — the transcript, the ticket, the commit, the invoice, the database row. Without it, the company fills with plausible summaries nobody can verify, and the first time a confident answer turns out wrong, trust in the entire agent layer collapses. With it, agents become auditable: a teammate clicks through to the source and settles the disagreement in seconds.

Now that you’ve built the context, it may be tempting to let the machine run wild through every task in the org. Do not do this. Say it with me: Do not turn every workflow into an agent.

The best AI-native systems are a blend of scripts, AI-assisted humans, deterministic workflows, and agents, each doing the work it's actually suited for. Your job as a founder is to reach for the lightest tool that can run the work safely: the fewest moving parts that still clear the quality bar.

Use a script when the step is deterministic — exporting a report, transforming a CSV, running tests, checking links, validating JSON, formatting the weekly metric pack.

Use AI-assisted human work when the output needs judgment before it leaves the company — investor updates, founder emails, pricing copy, contract notes.

Use a workflow when the steps are known in advance — ingest the call, summarize, extract objections, write the CRM note, create the follow-up. Workflow engines (LangGraph, Temporal, Inngest, Prefect) handle the ordering, retries, and observability.

Use an agent when the path can't be pre-specified — investigate a production bug, research a market, work an unusual support case, untangle a messy customer account. Browserbase's bb agent is one Slack-facing generalist that loads a different skill file and scoped permissions for each task; that beats building a separate bot per task, because the bots all drift apart over a long enough timeline.

A harness is the essential, non-negotiable safety layer around the model. A workable first version is six stages:

1.   Preflight — check context and permissions before the agent burns a token.

2.   Plan — decompose the task and expose the proposed steps.

3.   Approve — a human or judge-model gate that catches a bad plan before execution.

4.   Execute — run the work.

5.   Verify — check the output against tests, schema, rubric, or examples.

6.   Log — write what happened to a run file so the next iteration has ground truth.

Guardrails belong in code and config, not in prompts. A prompt that says "do not delete production data" is not a security boundary. The non-negotiables are explicit: cost caps per run and per day, retry caps, a maximum tool-call depth, scoped credentials per agent identity, no production writes without an approval step, no auto-merge on code, and a fleet-wide kill switch. The recursive-spawning incidents through 2025 — agents calling child agents calling child agents — cost teams real money before the harness layer caught up. Caps belong at the runtime, before the model gets a chance to ignore the instruction.

[![Image 6: Image](https://pbs.twimg.com/media/HJLTAQHW8AAageL?format=png&name=small)](https://x.com/cyberfund/article/2058950286324986294/media/2058939980941029376)

Everything up to this point has been setup. Encoding recurring work as skills and grading them with evals is the engine. It’s what turns a company that does the work into one that compounds it a little better every week.

A skill is reusable instructions plus examples for a recurring task. Run it by hand twice, then encode the parts that repeat. Every skill needs a clear shape: scope, inputs, context to load, procedure, output format, examples, escalation rule, owner, and run log.

If the file doesn't say what it accepts, what it returns, when it asks for help, and who maintains it, it's a long prompt, not a skill.

Here’s a skill template founders can adapt:

> Skill: customer-call-synthesis Scope: sales calls after transcript is available Inputs: transcript, account record, product context, open opportunities Load: ICP, pricing, product roadmap, objection taxonomy Steps: extract facts → cluster objections → identify risks → write follow-ups Output: CRM note · customer brief · feature requests · next actions Examples: 3 prior calls with expected notes Escalate: legal or security issue, churn risk, enterprise pricing Owner: revenue lead Logs: runs/<date>/<account>.md Eval: 30 historical calls with expected extraction fields

Start with founder-native skills:

*   Customer-call synthesis — extracts objections, feature requests, risks, commitments, and next actions from raw transcripts.

*   Inbox triage — sorts investor, customer, hiring, and operational messages, and drafts replies for the first three.

*   Investor update — drafts the narrative from metrics and decisions, then cites both.

*   Pricing-page teardown — compares the live page against the latest customer-objection log.

*   Weekly metrics narrative — explains what changed, what broke, and what to inspect.

*   Test generation — turns a spec into tests and a draft PR.

The eval is what makes a skill compound. Once a skill has a usable eval, prompt-tuning becomes optional: a small reflection model proposes changes, the eval ranks them, the best one ships automatically. Without an eval, every iteration is a taste argument between the founder and whoever wrote the last version.

An eval has three layers, and they stack in order.

First, hand-labeled ground truth — a human marks what good output looks like on real examples.

Second, deterministic checks, which cost nothing and return an unambiguous verdict: schema validity, numbers matching the source, links resolving, citations existing, tests passing.

Third, an LLM judge, but only for what the deterministic checks can't reach — writing quality, sentiment, whether the output matches the brief. A small fast model is enough, and it has to be calibrated against the human-marked examples before you trust it on the rest.

Let’s take customer-call synthesis as a case study on how to achieve this. Take thirty past calls and have the revenue lead mark up each — the facts that matter, the objections, the risks, the follow-ups. Some of the checking is deterministic: did it get the names right? Do the dollar figures match the contract? Are the follow-up dates in the right week? What a machine can't check is whether the brief actually sounds like the call, so an LLM judge does that part.

About fifty runs in, you see where it breaks, and it's usually the same two things: it loses track of who's talking when three or more people are on the call, or it merges two different objections into one. Those are what you fix. The problems you imagined before running it usually aren't the ones that show up, and you rewrite the skill against these clusters until it works consistently.

While outbound lead classification works differently, the eval structure is similar. Three hundred old leads, the founder marks each a plain yes or no — fits the ICP or doesn't. The mechanical checks are basic: the company's real, the website loads, the headcount's filled in. An LLM judge against the ICP description handles the rest. With the eval in place, an open-source prompt-evolution loop (GEPA, DSPy) rewrites the classifier prompt against the labels overnight. The founder never reads the final prompt. The eval verdict is the only thing that matters.

Both cases follow the same shape: hand-labeled ground truth first, deterministic checks next, an LLM judge for what remains, and the loop runs against the eval until acceptance crosses the threshold.

Evals mature in five escalating stages:

1.   Spot check one example by hand

2.   Score a handful of cases against a written rubric.

3.   Run that rubric against 20–300 historical cases.

4.   Test on a held-out set the agent never saw

5.   Track the business metric the skill was built to move.

Evals get a skill ready to ship. Staying good is a different question, and you answer it with six numbers tracked every week: acceptance rate, override rate, cost per run, cycle time, review time, and incident count.

Acceptance rate is the one to watch. Below roughly 70% — minor edits still count as accepted — the skill isn't ready to move up an autonomy level to run with less oversight than it has now. When acceptance is low, the instinct is to rewrite the prompt. That's almost never the fix. It's usually one of four moves: load more context at runtime, tighten the skill's scope, add more worked examples to the file, or write a clearer escalation rule for the cases the agent shouldn't have taken on.

The founder goes first.

The fastest way to move a team onto a new way of operating is to show them live, within the context of your company. Show the morning brief that pulled from calendar, inbox, and Slack overnight; the customer synthesis from yesterday's calls; the test PR an agent opened against the spec; the investor-update draft built from the last metric pack.

The goal is calibration: seeing firsthand what the agent layer can and can't do. Jack Dorsey reportedly spent hours every morning through 2025 working directly with these tools before Block reorganized around them. It led to huge efficiency restructuring, and the decisions behind it came from leadership that had used the agents themselves.

Installation begins on day one. Onboarding should end with a useful AI artefact. Every teammate walks out of their first session with output they can ship that day — a cleaned customer brief, a support macro, a test PR, a pricing-page critique. Training that doesn't produce real work gets forgotten by the next week. Ramp's Glass tool went from 20 daily users to around 700 in three months on exactly this rule: every onboarding session ended with the new person adding one skill or one artifact to the shared library.

This means the human role gets bigger, not smaller. People design the system, own the relationships, judge the output, and carry the accountability. The agents handle execution. The teammate who only runs narrow tasks is exposed under this model. The one who can turn judgment into instructions, examples, and evals is worth more than they were before.

Hiring changes too. The bar for opening a role is higher now. Some of what used to need a hire is now a skill, so save new roles for the work that genuinely needs a person. When you do hire, test for the new shape of the job: skip the trivia, hand candidates a project too big to finish by hand in the time given, and watch how they direct agents through it. You're hiring for judgment, taste, and the ability to recover when an agent goes sideways. These are the parts of the work that just got more valuable.

What that looks like in practice: an analyst gets a real report to produce in three hours, sources collected and evidence pulled and a polished brief at the end. An engineer gets a day to clone a real product surface or build an internal tool from a spec, tests included. A growth hire gets a market map and campaign plan across 50 to 100 companies — scraping, clustering, writing, prioritizing. None of it is finishable by hand in the time given. That's the point: you're watching how they work with agents under pressure.

By this point, you’ve pressure tested your automation and your team. Now you go back to the beginning and start again. An AI-native startup improves its operating system every week.

The review should address:

*   what agents did

*   where humans overrode them

*   which evals failed

*   which context was missing

*   which skills need narrowing

*   which workflows to kill

*   which to move up an autonomy level.

Run two loops at once. The inner loop makes existing work better — lower cost per run, shorter cycle time, fewer incidents, less review time per artifact. The outer loop hunts for what's next: new customer segments, product ideas, pricing changes, partnerships, competitor moves, regulatory shifts, churn risk. Background agents feed the outer loop with candidates around the clock; humans decide which ones to chase.

[![Image 7: Image](https://pbs.twimg.com/media/HJLT0NxX0AA9572?format=png&name=small)](https://x.com/cyberfund/article/2058950286324986294/media/2058940873665138688)

The software factory is the biggest piece of the inner loop. Humans write the specs and tests, agents implement against them. Deterministic checks run on their own, humans review before anything merges. Start where the acceptance criteria are clear and the blast radius is small: test generation, dependency upgrades, migrations, internal tools, integration scaffolds, QA scripts, security autofixes.

There are two hard rules: nothing auto-merges, and no agent writes to production. Even Cursor, running autonomous cloud agents at scale, kept a human review gate on merges through early 2026. The gate is what let them scale the rest safely.

The market-learning system is the outer loop. Record the calls, extract objections, cluster feature requests, track competitors, watch usage shift, read the support patterns, study the deals you lost. Turn what you find into hypotheses, then test the strongest ones — customer conversations, landing-page tests, product experiments, fresh queries against the data. The agents propose. You choose. Hand an agent both the proposing and the deciding on strategy and it either settles into bland consensus or hill-climbs whatever metric is easiest to move.

Company-level self-improvement comes down to one skill: whether the team can write evals. Hand-label a few hundred examples good or bad, build the eval, wire it to a prompt-evolution loop. GEPA, DSPy, and frameworks like them do this directly — a small reflection model proposes prompt mutations, the eval ranks them on the labeled set, the winner ships, and it repeats. The founder writes the eval and reads the failure clusters. The founder never writes or reads the evolved prompt.

Agent capability is rarely the thing holding you back. If you can encode what good looks like — binary labels, a scoring rubric, a few business metrics — the loop runs at the scale of the whole company. If you can't, no amount of model capability closes the gap. Coding helps, but it isn't the bottleneck; a subject-matter expert who can reliably mark output good or bad can run the entire loop. The eval is the load-bearing artifact. The company stops compounding the moment the eval stops being written.

None of this needs a genius or a big team. It needs the discipline to map the work, build the context, write the evals, and run the loop every week. Discipline is the moat now. Everyone has the same models; the operating system is the secret sauce.

The Monastery exists to build that operating system with you: twelve weeks of pure focus, $2M, and operators already running the loop working alongside you to embed it into your company from day one.

Enter the Monastery, do the impossible with us.

### Source URL
https://x.com/cyberfund/status/2058950286324986294?utm_source=tldrfounders