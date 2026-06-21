# Self-Repairing Agent Harness

## Problem
Currently, agent executions crash or return raw error messages when a tool call fails or the LLM hallucinates an invalid schema.

## Proposed Solution
Create a new dedicated module `src/core/agent_harness.py` that implements an `execute_with_repair` decorator. This harness catches agent failures (JSON parsing errors, timeouts) and applies known repair strategies.

The harness operates in two modes:
1. `mode="background"`: Used by unattended scripts like `scripts/weekly_hermes_run.py`. Blocks with exponential backoffs and schema re-prompts (up to 3 retries) to guarantee success.
2. `mode="ui"`: Used by interactive foreground apps like `apps/streamlit-chat/`. Fails fast (max 1 quick retry), bubbling the error to the UI.

Repair logs are stored in the `agent_repair_logs` SQLite table.

## Source
N/A

## Status
✅ Implemented

## Effort
Medium
