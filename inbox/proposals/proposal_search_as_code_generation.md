# Search-as-Code-Generation for Adaptive Agent Retrieval

## Problem

Traditional search pipelines return static results for a query, but LifeOS agents perform tasks that require dynamic, task-specific retrieval strategies. A single complex task may require hundreds or thousands of retrieval operations with different filters, sources, and strategies. Hardcoding retrieval logic into agent prompts is brittle and doesn't adapt to the task at hand.

## Proposed Solution

Implement a **Search-as-Code-Generation** paradigm within LifeOS:

1. **Retrieval Code Generation**: Instead of static search tool calls, allow agents to generate executable retrieval code (e.g., Python functions, SQL queries, API call chains) that define custom retrieval strategies tailored to the specific task.
2. **Sandboxed Execution Environment**: Provide a secure sandbox where generated retrieval code can be executed against search indices, databases, and external APIs without risking the host system.
3. **Retrieval Strategy Library**: Maintain a library of reusable retrieval patterns (multi-hop search, filtered retrieval, temporal search) that agents can reference and compose.
4. **Cost and Latency Budgets**: Enforce per-task retrieval budgets (max API calls, max latency) to prevent runaway retrieval loops.
5. **Evaluation Integration**: Feed retrieval outcomes into the Agent Judge framework to evaluate whether the generated retrieval strategy actually surfaced the right information for the task.

## Source
https://research.perplexity.ai/articles/rethinking-search-as-code-generation?utm_source=tldrai

## Status
Proposed

## Effort
Medium