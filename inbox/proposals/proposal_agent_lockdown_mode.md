# Agent Lockdown Mode for High-Security Tasks

## Problem
LifeOS agents interact with external services, APIs, and the open web. This creates a prompt injection and data exfiltration surface: a malicious payload embedded in fetched content could instruct the agent to leak sensitive user data or perform unauthorized actions. OpenAI's Lockdown Mode demonstrates a practical pattern for mitigating this risk by restricting outbound capabilities.

## Proposed Solution
Implement a **Lockdown Mode** for LifeOS agents that can be toggled per-task or per-user:
- When enabled, the agent's outbound network requests are blocked or heavily restricted (no external API calls, no web fetch).
- Tool access is limited to a read-only, local-only subset (e.g., local file search, internal knowledge base).
- The agent operates in a "walled garden" where it can reason and generate output but cannot transmit data externally.
- Provide a clear UX indicator when Lockdown Mode is active, and allow users to selectively whitelist trusted domains or tools.
- This mode should be the default for agents handling sensitive personal data (financial, health, identity).

## Source
https://help.openai.com/en/articles/20001061-lockdown-mode

## Status
Proposed

## Effort
Medium