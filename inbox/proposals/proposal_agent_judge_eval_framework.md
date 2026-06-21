# Agent Judge Evaluation Framework for Long-Horizon Agent Trajectories

## Problem

As LifeOS agents evolve to perform long-horizon, multi-step tasks (e.g., researching leads, updating CRMs, sending emails, booking meetings), traditional LLM-judge evaluation approaches break down. A simple LLM judge cannot fit an entire agent trajectory into its context window, and it cannot verify stateful changes against source-of-truth systems (e.g., Google Calendar, CRM databases). This means we currently lack a reliable way to evaluate whether complex agent runs actually achieved their intended outcomes.

## Proposed Solution

Implement an **Agent Judge** evaluation system inspired by Judgment Labs' approach:

1. **Trajectory-Aware Judges**: Instead of passing the full trajectory to a single LLM judge, decompose evaluation into sub-judges that each assess a specific segment or tool-call outcome against a ground-truth source system.
2. **Stateful Verification Layer**: Build a verification module that compares agent-side state changes (e.g., "meeting booked") against the actual state in external systems (Google Calendar API, CRM API) to produce binary or graded correctness signals.
3. **Rubric-Driven Scoring**: Define structured rubrics per task type (sales outreach, code generation, scheduling) that combine trajectory-segment scores into an overall quality score.
4. **Continuous Eval Pipeline**: Run the Agent Judge on every production agent run (sampled) and store scores in a metrics dashboard to track quality drift over time.
5. **Feedback Loop**: Feed judge scores back into the agent governance framework to trigger retraining, prompt revision, or human review when scores drop below threshold.

## Source
https://www.judgmentlabs.ai/blogs/agent-judge-solving-long-context-evaluations?utm_source=tldrai

## Status
Proposed

## Effort
Large