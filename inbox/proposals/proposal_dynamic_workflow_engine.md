# Dynamic Workflow Engine for LifeOS Agents

## Problem
Most agent workflows in LifeOS are statically defined—predetermined sequences of tool calls and decisions. However, real user tasks are fluid and context-dependent. A rigid workflow fails when unexpected inputs, tool failures, or shifting user intent occur mid-execution. This leads to brittle agents that require constant manual updates.

## Proposed Solution
Adopt a dynamic workflow engine similar to Claude Code’s new dynamic workflows. Instead of hardcoding execution paths, define workflows as reactive graphs that reconfigure at runtime based on intermediate outcomes. Key features:
- **Conditional branching** based on tool output semantics (not just success/failure).
- **On-the-fly subworkflow injection**: if a task requires research, dynamically spawn a research sub-agent.
- **User-in-the-loop checkpoints**: pause and request clarification when confidence is low.
- **Workflow versioning**: track which dynamic path was taken for auditability.

This engine would be embedded in LifeOS’s agent runtime, allowing agents to adapt their plan without restarting or losing context.

## Source
https://claude.com/blog/introducing-dynamic-workflows-in-claude-code?utm_source=tldrai

## Status
Proposed

## Effort
Medium