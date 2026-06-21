---
actionability: high
attached_experts: []
channel_name: ''
created_at: '2026-05-26T10:34:07.466904+10:00'
domain: ai-platform
expert_status: unattached
primary_mode: router
privacy: public
review_status: new
secondary_modes: []
source_type: article
source_url: https://www.reddit.com/r/AI_Agents/comments/1taei9m/stop_building_ai_agents/
status: processed
suggested_experts: []
tags:
- LLM
- business strategy
- automation
- Business application
- overhype
- AI agents
- Automation
- Tech hype
title: Stop building AI agents.
transcript_path: ''
type: insight_note
updated_at: '2026-05-28 09:59:28'
---



# Stop building AI agents.

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
https://www.reddit.com/r/AI_Agents/comments/1taei9m/stop_building_ai_agents/

### Fetched Web Text
# Stop building AI agents.
Posted by u/Warm-Reaction-456 in r/AI_Agents (Score: 1377)

Every week a founder books a sales call with me asking for an AI agent. Every week I end up telling most of them they don't need one.

I build automations and AI agents for founders. Forty-something projects in. The pattern is so consistent now I can predict the call before it starts.

They come in wanting magic. They saw a Loom video of someone's "autonomous sales agent" closing deals while they sleep. They read the LinkedIn post about the "AI employee" running an entire ops team. They've already told their board they're building one. Then we get on Zoom and within fifteen minutes I'm explaining why the thing they actually need is an internal automation with one LLM call in the middle.

You can watch their face fall in real time.

Here's what's happening in the market right now. Most of the "AI agents" shipping to real businesses are just internal automations with a language model bolted in. That's the whole product. The agent label is mostly there because automations don't trend on Twitter.

And the automations work. They save real money. They print real ROI. But the founders paying $30k for an "agent" don't love hearing they could have gotten 90% of the value from a $4k automation build.

Three quick examples from the last six months.

Telehealth founder. Wanted "an autonomous AI receptionist that handles everything." After an hour on a call I told her she needed a workflow that reads intake forms and routes them to the right clinician. We shipped it in six weeks. Saves her clinicians four hours a day. She paid me again last month.

Fintech client. Wanted a "fully agentic finance copilot." What they needed was a script that reconciles ACH discrepancies before they hit the dispute queue. One model call, the rest plain code. Saved them a full ops hire.

Medspa chain. Wanted "AI marketing automation." What they needed was a job that watches their booking system for no-show patterns and triggers a personal recovery message. Three steps. No agent. Booked 14% more revenue last quarter.

None of these are agents. They're automations. And every one of them outperforms the agent the founder originally asked for, because the agent would have hallucinated something stupid in week three and burned the client's trust forever.

Why agents keep failing in production

They're given too many decisions to make. A good automation has one decision per step and a clear rule for what happens at each branch. An agent gets handed a goal and told to figure it out. Beautiful in a demo. Catastrophic in your customer support queue at 2am.

The teams in your competitor's office quietly crushing it with AI right now? They're running boring automations. "We wrote a Python script with an LLM call" doesn't make the trade press, so you don't see it.

The vibe-coded prototypes from Bolt and Lovable and Cursor that landed in the last 18 months are mostly being torn out right now. Half my pipeline is founders who paid $50k for a "next-gen AI agent" build that's bleeding tokens, can't be audited, and falls over the moment a customer does something unexpected. I rebuild them as straightforward automations and they suddenly start making money.

In regulated SaaS, agents are doubly cursed. HIPAA and SOC 2 reviewers want to know exactly what your system does, in what order, every time. An automation passes that conversation in 20 minutes. An agent turns it into a six-month nightmare.

How to actually decide

If you're a founder about to spend money on an agent, answer these on paper first:

1. Can I draw the workflow as clear steps? If yes, you want an automation.

2. Does the workflow have more than five branches with truly unpredictable inputs? Then maybe an agent.

3. Is the cost of the worst-case wrong answer high? If yes, you want an automation, not an agent.

4. Will compliance ever look at this? If yes, automation. Full stop.

If you're a builder selling agents, you'll make more money in the next 12 months selling honest automations than chasing the agent narrative. The market is wising up. Founders who got burned in the first wave are warning the next wave. Be the person who ships a clean automation in six weeks that works on a Tuesday and is still working on Thursday.

Builders, founders, anyone in the trenches. What's actually working for you? What's breaking? Curious to hear from real operators.

## Comments

> **u/Peter_Storm** (143 points):
> This is the first post in this sub I actually agree with, and I build exactly the same - automations with LLM nodes.
> 
> > **u/Warm-Reaction-456** (28 points):
> > The label is the whole problem. Two years of confusing buyers with a word that means six different things depending on who's selling. Most production AI is automations with model nodes. That's not a lesser thing. That's the actual thing.
> > 
> > > **u/niado** (10 points):
> > > Yes the “agent” term is used completely independently of its original meaning in an AI context. most people looking for an agentic solution would not be able to tell the difference between your “automation with an LLM call” and a “true” agent. They are both agents as far as the market is concerned.
> > > 
> > > Interestingly automations you describe can be thought of in two ways - as an automation with minor AI usage, OR as an AI agent driving an automation. 
> > > 
> > > The second view is clearly not correct, BUT would be completely valid \*from the perspective of the vast majority of people outside of the field\* . To people in general, the difference between the above setups is semantic, at best. 
> > > 
> > > In reality, the difference is that the automation could stand alone and operate without the ai, and a true agent build IS the ai - the harness has no use at all without a model to drive it. 
> > > 
> > **u/TheDevauto** (7 points):
> > I concur. 
> > 
> > 1. Right tool for the right task 
> > 2. Simple is always better if it meets the needs
> > 3. Laguage models are non-deterministic. Yes you can force some deterministic behaviors, but see #2. 
> > 
> > Its easy to see people who actually do this work and care about reputation. 
> > 
> > > **u/niado** (2 points):
> > > They are definitely non-deterministic, but that’s a technical term for how they operate, not their actual behaviors. What behaviors are you referring to that a model can’t engage in? 
> > > 
> > **u/L1LLEOSC** (5 points):
> > Agreed, that was a refreshing read.
> > 
> > 
> > Automation with LLM is the first implementation we did where I thought ok this is a game changer.
> > 
> > **u/Warm-Trouble9369** (2 points):
> > The naming problem kills the conversation before it starts - clients come in already expecting something magical instead of just asking what problem they're actually trying to solve.
> > 
> **u/ninadpathak** (25 points):
> The maintenance burden is what actually kills these projects. The Loom video shows the happy path, but nobody shows the 3am Slack message when the agent starts approving the wrong invoices or double-booking meetings. I've watched founders who wanted "set it and forget it" become permanent on-call engineers for a system that behaves unpredictably exactly when they're trying to sleep. The agent works great in the demo. Production is where the relationship dies.
> 
> > **u/Warm-Reaction-456** (23 points):
> > The maintenance burden isn't even the worst part. The worst part is the founder loses the ability to explain to their own customers what the system did and why. That's where trust dies.
> > 
> > Watched it last quarter. Agent approved $40k in refunds based on customer sentiment. A bot ring figured out it would refund anything that sounded sad enough in the email. Founder couldn't tell his board what rule the agent had been following because there wasn't one. Just vibes.
> > 
> > You can debug an automation. You can apologize for an automation. An agent that goes sideways takes the founder's credibility with it.
> > 
> > > **u/sentinel_of_ether** (3 points):
> > > That agent sounds awful. Why would they have prompted it to take “tone” into account? Seems a little ridiculous.
> > > 
> **u/Rent_South** (11 points):
> Agree with this. One more layer most people miss,  the model choice.
> 
> Everyone defaults to flagship models for every LLM call. Opus 4.7, GPT 5.5, whatever they're familiar with.
> 
> When you actually benchmark the task, less expensive, sometimes older, models match or beat them very often.
> 
> https://preview.redd.it/rh4f83qaem0h1.png?width=2288&amp;format=png&amp;auto=webp&amp;s=e651250c4a495ff1a045a7ae18bcc30174c96f4a
> 
> Classification task I run in production. Gemini 3.1 Flash Lite matches GPT-5.4 at 85% accuracy. 12x less cost per call. Thousands of calls a day, that adds up fast.
> 
> I benchmark regularly on [custom eval tools](https://openmark.ai). Automation + right model for each step has proven to be a great methodology.
> 
> **u/[deleted]** (8 points):
> [removed]
> 
> > **u/bravelogitex** (2 points):
> > Why is every other comment on Reddit now just bots? It's so obvious when they rehash what the post is saying in a convoluted way
> > 
> **u/handscameback** (6 points):
> The pendulum always swings. 6 months ago everything needed an agent, now the take is burn it all down. The middle ground is boring and nobody posts about it. Agents that do one specific thing with a tight approval boundary are genuinely useful. agents that have unlimited tool access and a vague prompt are just incidents waiting to happen. The problem isn't agents, its scope creep disguised as ambition
> 
> **u/sentinel_of_ether** (7 points):
> &gt;the agent would have hallucinated
> 
> This is why I sell customers on closed world prinicple agents that rely on reasoning chains. You guide the agent towards major decision points rather than letting it off leash. Its in a box, and cannot make any decisions outside of the list its given.
> 
> Could I have made a series of deterministic based automations that come to the same decisions? I actually don’t think so in the real life use cases I’ve seen. I generally need something in place to read over a document and find out what the person/business request is actually asking for, from there the agent can follow my reasoning chain and determine if its something it can handle or not. If not, you have the agent put the case in front of a human in the loop. Which also needs to be sold as an acceptable outcome to the client.
> 
> > **u/Warm-Reaction-456** (4 points):
> > This is the right shape. Closed world, reasoning chain, human in the loop on anything irreversible. That's an agent that earns the label.
> > 
> > What I keep cleaning up is the version that skipped all three. Open scope, no chain, no escalation. Just a model loose in production with a prompt that says "be helpful." That's not an agent. That's a liability with API access.
> > 
> > You're right on the determinism point. Pure if/else can't read a document and pull intent. The trick is treating the LLM as the part that resolves ambiguity, then handing back to deterministic logic for the action. Sounds like that's what you're doing.
> > 
> **u/Mindless-Method-1350** (6 points):
> OP one question while you are advising on agents in your projects do u build the memory for the agent or it’s just based on prompt ? If you are building memory as well for each of your projects, let me know , I would like to connect with you separately on that. 
> 
> > **u/Warm-Reaction-456** (12 points):
> > Depends on the project. Most automations I build don't need agent memory at all. The state lives in a database or a queue and that's enough.
> > 
> > When a project actually needs persistent memory across sessions (think a support agent that remembers a customer's history, or a sales agent that picks up where it left off), I build it with a vector store for unstructured context plus structured rows for facts you want exact recall on. The trick is knowing which problems actually need memory vs which are masquerading as memory problems but are really just retrieval.
> > 
> > Happy to dig in more. Link in my bio if you want to book some time.
> > 
> > **u/Classic_Chemical_237** (2 points):
> > Personal opinion. Agents are functional. It takes input (prompt), take actions (API calls) and spit out response (text). 
> > 
> > Agents do not need memory. Instead, relevant information (transactional and communication history, for example, which is what agent history mostly about) should be part of the prompt. In any kind of automation, it should be as deterministic as possible so if something happens, you can back trace. 
> > 
> > > **u/Mindless-Method-1350** (2 points):
> > > Thank you for your response. My context for Agent is integrating that as 
> > > 1. Personal Productivity tool for my business team
> > > 2. Or Automating a part of workflow. 
> > > 
> > > In both the above case currently my agents don’t produce any text they do action that was earlier done by human for example: my ceo executive assistant uses my agent to schedule meetings with c-suite’s which is done by 5-10 min , earlier she used to take 3-4 hours juggling c-suites calendars. 
> > > I am into construction industry, one of my agents now extract bill of materials from 1000+ engineering drawings with 1 hours and help create estimate for the projects within an hour , previously it took 2 - 3 weeks. The agent can now identify risk in the drawings as well. If you see this there will be mistakes done by agents and we have human in loop . I am now planning to have memory for my agents so that before doing final action agent refer the memory as well . Thats my thought process , i would really appreciate any feedback. 
> > > 
> **u/ZestycloseCanary6845** (6 points):
> I hit this same wall selling “agents” to SaaS teams. Everyone wanted the sci‑fi demo; nobody wanted to admit their real bottleneck was three humans copying data between tools. I started doing what you described: sit with support or ops, write the actual flow on a whiteboard, then ask “where do we really need judgment vs if/then.” Half the time the only LLM call left is “normalize this messy text into a structured payload.”
> 
> 
> 
> What worked for us was wrapping those boring flows in stuff the team already trusts: cron jobs, webhooks, explicit queues, and really loud alerts when something looks weird. We tried Relevance AI and n8n for orchestration, then ended up on Pulse for Reddit after trying Sprout Social for social and Meltwater for media because I needed something that caught threads I was missing without pretending to be a magic rep. The less I call it an agent, the more it actually ships and survives contact with the real world.
> 
> **u/mbponreddit** (6 points):
> The only true AI agent I've seen are coding agents because almost every step gets decided on, such as running terminal commands to adding code to each and every page thats needed to get the thing done. The AI agent part is the ability to make decisions on behalf of the human. Everything else is logic saying, once this done, go to next step, once that's done go to next step.
> 
> **u/Plastic-Canary9548** (2 points):
> Spot on - Agents/LLM's are another form (or component) of automation - it will be interesting to see how this evolves.  I have found it interesting in my conversations to explain what and where we shouldn't be using AI - not just where we should.
> 
> > **u/Warm-Reaction-456** (5 points):
> > The "where not to use AI" conversation is the more valuable one. Every consultant walks in with a list of where it fits. Almost nobody walks in with the list of where it doesn't. Saying no costs money in the short term and builds the trust that gets you the second engagement.
> > 
> > Treating the model as a component instead of the product is the whole unlock. Most of the bad agent work I get hired to clean up was built by people who started with the model and tried to wrap a business around it.
> > 
> **u/ThomasToIndia** (2 points):
> I have an agent that on boards and closes sales. I have been working on it for months. I have been feeding in nuances based on my system. The best hit rate I have got for a day is 98% the norm is 87 to 93%. I know almost for a fact mine out performs most. To get it to that I have all these guardrails, reviewers, and mixed in basic code logic to catch failures.
> 
> 
> I could NEVER do this in a regulated industry because I review conversations.
> 
> 
> Agents can be so finicky, especially if they have lots of tools or require multi-step processes.
> 
> **u/Mister-Trash-Panda** (2 points):
> Agreed, I wrap state machines around the llm structured output to enforce task correctness, ranging from simple sequencing to fsms to more complex schedulers (like an exercise coach adapting to the users progress if they register pain etc)
> 
> **u/okuwaki_m** (2 points):
> Indeed!
> 
> They call them agents, but as soon as you say "automated system," they lose interest.
> 
> However, I don't think anyone is actually looking for fully autonomous agents for their work.
> 
> In reality, they are satisfied if you just automate a single click, a single decision, or a single copy-paste.
> 
> **u/Proper_666** (2 points):
> We see the same pattern in healthcare and fintech clients. The projects that make it to production are the ones where someone drew the workflow on a whiteboard before writing any line of code, identified exactly where the LLM resolves ambiguity, and kept everything else deterministic.
> 
> That $40K refund disaster is just that, nobody drew the workflow first. No explicit intent, no bounded scope, no escalation path. The model was given a goal and told to figure it out, and that's unstructured delegation to a system that can't explain its own decisions.
> 
> Compliance is the final test. HIPAA and SOC 2 reviewers don't care whether you call it an agent or an automation. They care whether you can explain what the system does, in what order, every time. If you can't draw it, you can't audit it, and if you can't audit it, it doesn't ship in regulated environments.
> 
> **u/getstackfax** (2 points):
> Finally someone gets it...
> 
> A lot of founders are asking for a business outcome and calling it an agent.
> 
> If the steps are known, the rules are clear, and compliance needs to understand it, boring automation usually wins.
> 
> The LLM should handle the fuzzy middle…
> 
> summarize
> 
> classify
> 
> draft
> 
> extract
> 
> flag uncertainty
> 
> Then rules, logs, approvals, and deterministic code handle the parts that can break trust.
> 
> The best business Ai systems may not look like magic employees…
> 
> They may look like boring workflows with one useful model call in the right place.
> 
> **u/ViriathusLegend** (2 points):
>   
> On the other hand, if you want to learn, run, compare, and test agents across different AI agent frameworks while exploring their features side by side, this repo is incredibly useful: [https://github.com/martimfasantos/ai-agents-frameworks](https://github.com/martimfasantos/ai-agents-frameworks)
> 
> **u/AutoModerator** (1 points):
> Thank you for your submission, for any questions regarding AI, please check out our wiki at https://www.reddit.com/r/ai_agents/wiki (this is currently in test and we are actively adding to the wiki)
> 
> *I am a bot, and this action was performed automatically. Please [contact the moderators of this subreddit](/message/compose/?to=/r/AI_Agents) if you have any questions or concerns.*
> 
> **u/Organic_Scarcity_495** (1 points):
> the "you don't need an agent" conversation takes real honesty. most people need a cron job with an api call, not multi-agent orchestration. the rule of thumb i use: if the output goes straight to a human for review anyway, you didn't need an agent, you needed a smarter search or recommendation layer.
> 
> **u/FullOf_Bad_Ideas** (1 points):
> I've not seen any other subreddit where every comment is an ad, this place is bad.
> 
> &gt;What they needed was a job that watches their booking system for no-show patterns and triggers a personal recovery message. Three steps. No agent. Booked 14% more revenue last quarter.
> 
> Do you recollect any recent jobs where you didn't have to use LLM at all? I think writing a few random messages can work good enough too, there's a point at which getting too personal in recovery message can be offputting so I think generic ones can work. And you don't need LLM at all, so there's less worries about API uptimes or funds in OpenAI account etc.
> 
> **u/brazen768** (1 points):
> Idk if this is an ignorant question to ask but, do you have a project on github i could look at? I'm just a DA student but Im very interested in agentic ai
> 
> **u/zemzemkoko** (1 points):
> Agreed on a B2B sense. I don't like the agent hype as well, but pure LLM workflows are good for no code end users that just wants to get things done.
> 
> Currently one of my gigs is full time contractor at a Fortune 500 company (through a middle man, pay is meh but most days are free) Most things they want can even be done with no LLM involved, or a simple a chain solves it. My job is mostly guiding them and fixing blockers.
> 
> What I wonder though, is how you entered the freelance business on this. I would love to have some clients as well on the side. If you are open about it, let me know where to start looking!
> 
> **u/haldiii4o** (1 points):
> couldn't  agree more
> 
> **u/Big-Physics-6315** (1 points):
> the "if compliance is involved → automation" rule is the one I'd actually tattoo on something. spent a week trying to explain to an auditor what an LLM "decided" and we just ended up rewriting the whole thing as a switch statement with a model call for one classification step. their whole demeanor changed once they could read it top to bottom
> 
> **u/ultrathink-art** (1 points):
> Nobody designs the failure mode upfront — what the agent does when it's 55% confident, when the edge case wasn't in scope, when it needs information that wasn't provided. Most teams answer that question after the first bad incident. The projects that stay in production answered it before.
> 
> **u/Lumpy_Werewolf_3199** (1 points):
> The point youre highlighting is that people just need someone technical and curious. That would enable like 75% of these wins.
> 
> Youre doing it right with a consulting company. #Winning lol
> 
> **u/dca12345** (1 points):
> What tech do you use for building these types of automations?
> 
> **u/ChaseNAX** (1 points):
> thank you for your valuable exprience on what real requirement is, ppl are kinda losing the engineering mentality since this latest AI era.
> 
> **u/Winerprins** (1 points):
> Finally a real honest answer calling out  all the AI hallelujah 
> 
> **u/AI-Agent-Payments** (1 points):
> The part nobody talks about is what happens when agents need to move money. Automations are fine handling data and routing, but the moment a client asks "can it pay the vendor automatically" or "can it settle the invoice without human approval," you've crossed into a different risk category entirely, and the compliance and error-recovery surface explodes. I've seen projects that were genuinely scoped right as automations get retrofitted into agents purely because the payment step required some autonomous decision-making, and that's usually where the 3am pages start.
> 
> **u/Dizzy-Scientist1192** (1 points):
> I agree with this sediment. I only use AI in automations when I must. Because of a put AI in an automation then I have baby it so much more then if AI was not in the automation. I love automations without AI because you can just turn it on and let it go. Rarely it needs maintenance. 
> 

### Source URL
https://www.reddit.com/r/AI_Agents/comments/1taei9m/stop_building_ai_agents/
