# Long-Context Evaluation Harness for LifeOS Agents

## Problem
LifeOS agents increasingly perform long-horizon tasks (e.g., planning a week of meetings, drafting a multi-section report) that involve dozens of tool calls and stateful changes. Traditional LLM judges fail on these trajectories—they can’t fit the full context, and they can’t verify stateful changes against source-of-truth systems (e.g., did the agent actually book the meeting in Google Calendar?).

## Proposed Solution
Build a specialized long-context evaluation harness based on Judgment Labs’ Agent Judge approach:
- **Trajectory chunking**: split long agent trajectories into verifiable segments.
- **Source-of-truth verification**: for each segment, check actual system state (CRM, calendar, file system) rather than relying solely on LLM judgment.
- **Hierarchical scoring**: evaluate sub-tasks independently, then aggregate into an overall score.
- **Rubric-based assessment**: define clear, task-specific rubrics that the judge uses for each segment.
- **Human-in-the-loop validation**: periodically sample and verify judge outputs against human labels.

This harness would be used in LifeOS’s CI/CD pipeline to evaluate agent performance on complex, real-world tasks before deployment.

## Source
https://www.judgmentlabs.ai/blogs/agent-judge-solving-long-context-evaluations?utm_source=tldrai

## Status
Proposed

## Effort
Medium