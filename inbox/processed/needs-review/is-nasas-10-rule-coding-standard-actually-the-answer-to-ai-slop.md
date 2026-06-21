---
actionability: high
attached_experts: []
channel_name: ''
created_at: '2026-05-25T21:52:00.044248+10:00'
domain: ai-platform
expert_status: unattached
primary_mode: router
privacy: public
review_status: new
secondary_modes: []
source_type: article
source_url: https://www.reddit.com/r/AI_Agents/comments/1t59duo/is_nasas_10rule_coding_standard_actually_the/
status: processed
suggested_experts: []
tags:
- coding standards
- AI code quality
- LLM pipelines
- debugging
- software engineering
title: Is NASA’s 10-rule coding standard actually the answer to AI slop?
transcript_path: ''
type: insight_note
updated_at: '2026-05-28 09:58:15'
---


# Is NASA’s 10-rule coding standard actually the answer to AI slop?

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
https://www.reddit.com/r/AI_Agents/comments/1t59duo/is_nasas_10rule_coding_standard_actually_the/

### Fetched Web Text
# Is NASA’s 10-rule coding standard actually the answer to AI slop?
Posted by u/Dependent_Payment789 in r/AI_Agents (Score: 499)

So I work as an AI engineer, mostly building LLM pipelines and that kind of stuff. And lately I’ve been genuinely unsettled by the quality of code that comes out of these models.

Not because it’s broken. That would almost be easier to deal with. It’s because it works — and its completely unreadable.

Like you ask Claude or GPT to build you a data pipeline and you get back 500 lines, zero assertions, a function called process\_data() that somehow does 11 different things, and no error handling anywhere. Runs fine in testing. Ships. And then 2 months later you have to debug it and you’re basically doing archaeology.

Anyway. I was going down a rabbit hole last week and stumbled back onto this old paper — NASA’s “Power of Ten” by Gerard Holzmann. Written in 2006 for safety-critical C code. Spacecraft stuff. And I couldn’t stop thinking about how relevant it still is.

The rules that stuck with me:  
	\- No function longer than \~60 lines (one page, one purpose)  
	\- Minimum 2 assertions per function  
	\- Always check return values — AI skips this constantly  
	\- Zero compiler warnings from day one  
	\- No recursion, bounded loops only

The whole philosophy is basically: code should be mechanically verifiable, not just functional. A tool or a tired human at 11pm should be able to prove it’s safe.

And idk, I feel like that’s exactly what AI-generated code needs? We’ve completely changed how code gets written but haven’t really updated how we review it.

Obviously some of the rules are very C-specific and don’t translate to python or modern stacks directly. The no dynamic memory allocation one is basically impossible if you’re doing anything in ML. But the spirit of it holds.

My unpopular opinion: if an AI wrote it and you can’t verify it, you don’t actually own that code. You’re just hosting it and hoping.

Has anyone actually tried enforcing stricter coding standards specifically for LLM-generated code at their job? Curious if its made any difference or if management just sees it as slowing things down.

## Comments

> **u/ProgressSensitive826** (37 points):
> The NASA rules are a good lint but the deeper problem is LLMs don't know what they don't know about your codebase. They write process_data() doing 11 things because from training data, that's what a function named process_data typically does in a one-off script. The rules that matter most for AI-generated code aren't line count — they're assertion density and function contract documentation. Force the model to declare preconditions and postconditions as comments before writing the body, and the 500-line monster collapses into 5 functions because the model has to reason about what each piece guarantees. Linting output fights symptoms. Constraining the generation process is more effective.
> 
> > **u/arun4567** (5 points):
> > Would having these coding standards in co-pilot instructions or in a review agent help?
> > 
> > > **u/Fidel___Castro** (1 points):
> > > you have to assert it deterministically! so make a script that checks for pre and post conditions on every function, run it as part of every merge CI. The instructions file is then just to make agents run the script, but even if it's ignored, the CI catches it.
> > > 
> > > 
> > > The goal is to make agents unable to merge without meeting your deterministic standards
> > > 
> **u/dasookwat** (53 points):
> Dude, this:   
> 
> 
> &gt;"Not because it’s broken. That would almost be easier to deal with. It’s because it works — and its completely unreadable. Like you ask Claude or GPT to build you a data pipeline and you get back 500 lines, zero assertions, a function called process\_data() that somehow does 11 different things, and no error handling anywhere. Runs fine in testing. Ships. And then 2 months later you have to debug it and you’re basically doing archaeology."  
> 
> reads like an AI post.  go on youtube, and listen to any of those ai generated stories, and it has a different subject, but the same format.  
> 
> That being said:  yes, that's how i work with AI in the first place: i've set guardrails. files have a limited size, functions as well, i let a seperate ai based on the descriptions in the documentation or // sections write unit tests. I not only do this for readability, but also because it saves me a lot of money on tokens.  Letting an llm  ingest a single monolotihic monstrosity takes a lot of tokens. If i can reduce that by using specific functions/classes and relational files with documentation for each section, that improves my life.  
> 
> 
> > **u/One_Club_9555** (17 points):
> > It reads like an AI post because it is.
> > 
> > Read the shorter paragraphs out loud. There’s a telltale sing-song to them.
> > 
> > The use of colons to create pseudo-headers where they are unnecessary.
> > 
> > The “code should be X, not just Y”… “We’ve… changed how X, but haven’t Y”
> > 
> > —-
> > 
> > Then again, just because it’s AI-formatted doesn’t mean that it was AI-written (slop). It may have some value here and there
> > 
> > **u/real_bro** (19 points):
> > I definitely detected the AI authorship here. Multiple places. 
> > 
> > > **u/FireHotTakes** (12 points):
> > > I recently started getting recommended posts from this sub, and almost all of them sound ai generated.
> > > 
> > > I actually checked the sub description to see if the whole purpose of the sub was to post AI generated content about AI.
> > > 
> > **u/Lotus_Domino_Guy** (5 points):
> > Not because its so obviously AI, not because I disagree with the point, but because of the sentence structure.
> > 
> > > **u/Dependent_Payment789** (2 points):
> > > Yepz, Used Claude to structure my thoughts.
> > > 
> > **u/Irythros** (2 points):
> > It's because it is an AI post.  
> > 
> > All of the em dashes, the markdown format, the same sentence structure and expanded points that are irrelevant that no human would actually add, "its not x, its y"
> > 
> > User has also hidden their posts.
> > 
> > It's just a straight up bot account.
> > 
> > > **u/Dependent_Payment789** (4 points):
> > > Bro, I aint a bot. See everyone uses LLMs now, I actually love using them, I had always struggled to find right words and put structure to my thoughts. And LLMs do that for me. Whats the harm ? I have accepted that these things are better than any human in terms of vocabulary or grammar or forming the right sentences with a correct tone.
> > > 
> > **u/MildlySelassie** (2 points):
> > Why would anyone expect a sub about AI agents not to be mostly AI posts?
> > 
> > **u/No-Entry9939** (1 points):
> > Do you have like an agent skill you can share? At least, to see how you do it... 
> > 
> **u/Embarrassed_Status73** (5 points):
> Or ask the AI to make it MISRA compliant (or any other coding standard) they are surprisingly good at enforcing rules when you start a new context
> 
> **u/happy_hawking** (6 points):
> &gt; If an AI wrote it and you can’t verify it, you don’t actually own that code. You’re just hosting it and hoping.
> 
> Great way to put it.
> 
> > **u/konm123** (2 points):
> > I have a saying I have used for a decade now "If you can not verify it, it does not work" and similarly "Until you have verified it, it does not work". This implies you can not make assumptions until you have confirmed the assumptions. The difference of the two sentences is that first one implies you foremost must know what you even expect to get as an outcome.
> > 
> > **u/mikkolukas** (2 points):
> > Same goes for the context of what OP have written here 😄
> > 
> > > **u/happy_hawking** (1 points):
> > > I'm not against using AI for coding or writing texts as long as you understand the output.
> > > 
> > > &gt; If an AI wrote it and you can’t verify it
> > > 
> > > The "and" is key. If AI wrote it and you CAN verify it, it's fine. AI is just a tool. But as opposed to a compiler, which can be formally verified and thus creates trustworthy output, you have to verify AI output every time manually.
> > > 
> **u/Live-Bag-1775** (3 points):
> NASA’s “Power of Ten” feels more relevant now than when it was written. The biggest problem with AI-generated code isn’t that it fails immediately — it’s that it creates maintenance debt disguised as productivity. Strict constraints like small functions, assertions, and mandatory error handling force code into shapes humans can still reason about later. In a world of AI slop, verifiability is becoming more important than cleverness.
> 
> > **u/DurianDiscriminat3r** (5 points):
> > You're absolutely right. The best way to use AI is to summarize AI posts and add nothing of value. It's not you — it's me. Now summarize my slop.
> > 
> > > **u/Live-Bag-1775** (1 points):
> > > Thanks bro
> > > 
> **u/FaceDeer** (2 points):
> There are programming languages that allow for *provably correct* programming. You can specify preconditions and postconditions for a chunk of code and know with mathematical rigor that they must always be satisfied when the code is run. This approach doesn't get used much in real world programming though, because it's tedious and requires a fairly rigorous and specialized mindset. You mostly see it in cryptocurrency circles where smart contracts are small and dangerous to get wrong.
> 
> LLMs don't care about tedium, and they can be trained to have whatever mindset we want them to have. I'm thinking that this is going to be where AI generated code eventually heads.
> 
> **u/ToneJumpy1092** (2 points):
> We started enforcing a lightweight version of this at the prompt level, basically instructing the model to keep functions under 40 lines, add assertions at entry and exit points, and check every return value explicitly. The output got dramatically easier to review. Your unpopular opinion is correct by the way.
> 
> **u/Fidel___Castro** (2 points):
> I'm building python repos with LLMs as it's what they know best - the key is setting up contracts and enforcing verification.
> 
> 
> Not only do the plans need to include a strict acceptance criteria (like "x should display y") but it needs to be proved that the acceptance was met as a precommit hook. 
> 
> 
> You can't give agents the entire database, but you can set up so many bumper side-rails that they have no choice but to go in the direction you specify.
> 
> **u/andlewis** (2 points):
> Like you mentioned these guidelines have been in place longer than vibe coding has existed. That means that there are deterministic tools that offload this stuff. We’ve doubled down on strictness in linting and testing for our AI-generated code. We’ve implemented tools like Knip and Madge, added CodeQL scanning, and security scans. We’ve got a process that does LLM powered code reviews and fixes issues, and another process that scans the code reviews for common problems and recommends new linting rules or tools to prevent those issues from even getting to the code review. We’re also in the process of building a self-healing workflow where an agent scans our logs and telemetry regularly and identifies bugs and automatically submits PRs, or if it’s a design flaw or non-obvious it creates tickets for humans to review. All these things work together but none of them solves the problem in isolation. And that’s just a brief summary, I expect we’ll do more in the future.
> 
> Your AI-generated code will be as strong as the guardrails you place around it.
> 
> **u/Decoupler** (2 points):
> We typically give our agents strict coding guidelines/standards.  We use Clean Coding standards written by Robert C. Martin (which is basically an expanded version of the NASA 10 rule coding standard) and SOLID principals.  They don’t always get I right but guardrails and guides are absolutely needed.
> 
> **u/b1231227** (3 points):
> If you could actually write code, you'd know that this is utter nonsense.
> 
> > **u/Ptp_9** (1 points):
> > How come?
> > 
> > **u/Gimly** (1 points):
> > No, it's mostly common sense, the only issue I have with those rules (and clean code, and other set of rules) is that it's dealing in absolutes, and rules are made to be broken when they makes sense should be the first and only absolute rule that should be.
> > 
> **u/AutoModerator** (1 points):
> Thank you for your submission, for any questions regarding AI, please check out our wiki at https://www.reddit.com/r/ai_agents/wiki (this is currently in test and we are actively adding to the wiki)
> 
> *I am a bot, and this action was performed automatically. Please [contact the moderators of this subreddit](/message/compose/?to=/r/AI_Agents) if you have any questions or concerns.*
> 
> **u/sunychoudhary** (1 points):
> Makes sense. Agent systems already have enough unpredictability from the model layer. Adding overly complex code on top just compounds it.
> 
> **u/florentin** (1 points):
> For Python code, ask the coding agent to check your code with complexipy
> 
> **u/lionmeetsviking** (1 points):
> In my main project, every agent session needs to end by running a readiness check script. All this is purely heuristic. 
> 
> This readiness check includes:
> - analysis of blast radius and based on that it checks that tests are in place and runs the tests
> - running policy gates that include things like file length, adherence to module boundaries, adherence to module pattern (for example: no direct data access in routers) function length, exception handling standards and many other things
> - if FE code is touched, build and lint are required. And I have very strict linting rules that make sure there are no inline styling, only library components are used, all strings are translatable etc. 
> - coverage of documentation and adherence to documentation standards
> 
> Yes, it makes every agent session take more time, but improves the quality considerably. I can implement fairly big features almost one-shotting and trust it works in the end. Even though it takes some time, it doesn’t actually spend that many tokens. My readiness check script is much less verbose than standard pytest. 
> 
> **u/ultrathink-art** (1 points):
> NASA's rules fix a human-review problem. LLM code slop is a different failure mode — the model optimizes for task completion and has no incentive to write for a future reader it'll never see.
> 
> What's worked better in practice: scope tasks to produce verifiable intermediate outputs rather than complete features. If the natural output is process_data() doing 11 things, that's a scoping bug, not a style guide problem.
> 
> **u/Creative-Alfalfa-317** (1 points):
> It literally makes sense
> 
> **u/tes_kitty** (1 points):
> &gt; Like you ask Claude or GPT to build you a data pipeline and you get back 500 lines, zero assertions, a function called process_data() that somehow does 11 different things, and no error handling anywhere. Runs fine in testing. Ships. And then 2 months later you have to debug it and you’re basically doing archaeology. 
> 
> So, it's a tech debt generator on speed?
> 
> **u/yawars20** (1 points):
> The NASA “Power of Ten” rules are a strong reminder that verifiability and structure matter, especially when AI is generating code. AI agents can produce functional pipelines that are unreadable and unmaintainable, which is exactly the problem Holzmann’s rules aim to solve: keep functions short, assert behavior, check everything, and avoid hidden complexity. In a way, AgentX on 1024EX demonstrates a similar philosophy applied to trading. You describe your goal in natural language, and the agent executes autonomously but it also evaluates and explains its decisions. You don’t just hope it works; there’s a framework for accountability. Translating that to coding, you’d want AI-generated code to have the same guarantees: measurable, auditable, and verifiable behavior rather than just “it runs.” The lesson is that autonomy without structured guardrails is fragile. Whether it’s rockets, trading, or pipelines, the principle holds: AI can execute, but we need systems in place to make sure what it does is reliable and understandable.
> 
> **u/lhx555** (1 points):
> How about using linters? Like giving a linter config file to your coding agent and making linter tests a part of your CI/ CD?
> 
> **u/getstackfax** (1 points):
> NASA rules are useful but.... less as a literal checklist and more as a forcing function.
> 
> The real problem with AI-generated code is not only “does it run?”
> 
> It is:
> 
> can a tired human or another tool verify what this is supposed to do later?
> 
> For AI code, the rules I care about most are...
> 
> \- small functions with one job
> 
> \- explicit inputs/outputs
> 
> \- preconditions and postconditions
> 
> \- assertions around assumptions
> 
> \- checked errors / return values
> 
> \- tests before broad refactors
> 
> \- zero ignored warnings
> 
> \- no giant “process\_data()” mystery boxes
> 
> The 60-line rule is not magic, but it prevents the model from hiding five decisions inside one function.
> 
> The assertion/contract part is probably the real win.
> 
> If the model has to write what each function expects, guarantees, and can fail on before writing the body, the code usually becomes easier to review.
> 
> NASA-style discipline is not the whole answer to AI slop.
> 
> But “mechanically reviewable code” is exactly the right direction.
> 
> **u/AI_Conductor** (1 points):
> NASAs 10 rules are a useful starting point but they are aimed at a different failure mode than AI slop. The Power of 10 was written to constrain how a deterministic program reasons about its own resources - bounded loops, no recursion, statically allocated memory - because the failure cost of the Mars rover overrunning a buffer is unrecoverable. AI-generated code mostly fails at a higher layer: unclear intent, drift between what was asked and what was built, code that looks plausible but solves the wrong problem.
> 
> The rules that actually catch AI slop are the ones the AI itself does not enforce: a clear, testable definition of done before you generate; an explicit contract for what the function takes and returns; an evaluation harness that proves the change behaves before it merges. NASAs rules harden the inside of a function. The slop problem lives at the boundary - did we build the right function at all.
> 
> Where I do think the spirit of the 10 rules transfers cleanly is the no-cleverness norm. AI is most useful when the surrounding code style is boring, predictable, and easy for the next reviewer (human or model) to scan. Clever code is where AI hallucinations hide longest.
> 
> > **u/D_Mac8134** (1 points):
> > One of the best bits of advice early in my career, in a class taught by a late career industry developer, was “be smart, don’t be clever.  Clever bites someone in the ass in 6 months - probably you”
> > 
> > Doesn’t matter if it’s AI or human, clever code is problematic
> > 
> **u/elchemy** (1 points):
> [https://www.youtube.com/watch?v=0fKBhvDjuy0](https://www.youtube.com/watch?v=0fKBhvDjuy0) reminds me of this - NASA powers of 10
> 
> **u/gannu1991** (1 points):
> Holzmann came up in a review I did for a healthtech a few weeks ago. Same exact thing you're describing. process\_data() style functions, no assertions, half the return values ignored. Worked fine. Until it didn't and the on-call had to figure out what the AI meant six months ago.
> 
> We pulled maybe four of the ten rules. 40 line function cap (Python compresses, 60 is too generous). Assertions on inputs and outputs. Every external call handles the failure path explicitly, no bare try/except passes. That's basically it.
> 
> Honestly the rules mattered less than where we put them. Stuck them in a [CLAUDE.md](http://CLAUDE.md) at the repo root with good and bad examples and a pre-commit hook that runs Claude as a reviewer against the same doc. Slop dropped a lot. Not overnight but close. And it wasn't the model getting better, it was just having a tighter spec to write against.
> 
> Your last line is the whole thing tbh. Hosting and hoping. That's most teams right now. Management never wants stricter standards until prod breaks and nobody can read what shipped.
> 
> One thing I keep coming back to though, the constraints aren't slowing AI down. Unconstrained generation is what produced the slop in the first place. Give it a shape to hit and it hits it.
> 
> **u/Nnaz123** (1 points):
> Ai slop
> 
> **u/newhunter18** (1 points):
> There are a lot of things to complain about AI generated code, but this set of complaints is just outdated.
> 
> Ask Claude to build you a data pipeline. It's not going to be unreadable anymore. And if you ask for tests, it's going to build tests. Probably will anyway.
> 
> This is just lazy complaining.
> 
> **u/mufasis** (1 points):
> Have you written an md file in your workflow for this?
> 
> **u/Foreign-Chocolate86** (1 points):
> I’ve got a pretty good Test-Driven-Development workflow going. For every feature or functionality addition it has to write a bunch of failing unit tests based on the requirements spec before developing. For each implementation phase it runs the entire test suite at least once to ensure no regressions. 
> 
> **u/willaimsing** (1 points):
> this comparison gets weirder the more you think about it. NASAs rules were written for jpl flight code where a recursion or unbounded loop kills a $2B mission. its like 90% about preventing memory faults in realtime embedded.
> 
> most ai slop i see is glue code in python/ts, totally different failure modes. unbounded recursion isnt the bug, hallucinated apis and wrong data shapes are. the rules dont even point at that.
> 
> what actually catches it is dumb stuff like running the code, reading the diff, making the agent justify non-trivial changes. tested with ~200 PRs from claude code over 3 months and the eval-after-write loop catches more than any style rule could.
> 
> NASA-style discipline matters where memory faults kill people. for the rest of us its prolly cargo-culting. could be wrong tho
> 
> **u/viitorfermier** (1 points):
> And yet their failure rate is over 60%
> 

### Source URL
https://www.reddit.com/r/AI_Agents/comments/1t59duo/is_nasas_10rule_coding_standard_actually_the/
