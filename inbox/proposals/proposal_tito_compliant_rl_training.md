# TITO-Compliant RL Training Loop for Tool-Using Agents

## Problem

When training LifeOS agents with reinforcement learning (RL) that involve mid-rollout tool calls, the **Token-In, Token-Out (TITO) invariant** is frequently violated. Parsing a model response to detect tool calls, re-tokenizing the updated conversation, and feeding it back into the next turn can silently produce token sequences the model never sampled. This causes gradient misalignment, loss spikes, and training instability — making it impossible to reliably train agents that use tools.

## Proposed Solution

Adopt a TITO-compliant RL training architecture:

1. **Canonical Tokenization Contract**: Enforce that any tool-call parsing and re-serialization round-trip must produce the exact same token IDs. Implement a validation check in the training loop that aborts or flags a rollout if token IDs change after re-tokenization.
2. **Token-Level Rollout Management**: Instead of re-tokenizing the full conversation at each turn, maintain a growing token sequence and append only new tokens (model outputs + tool results encoded in the model's own tokenization scheme).
3. **Tool Result Encoding Standard**: Define a canonical format for encoding tool results (e.g., JSON wrapped in specific delimiters) that is guaranteed to be tokenization-stable across the model's tokenizer.
4. **Gradient Safety Checks**: Add runtime assertions that verify gradient tokens correspond to positions the model actually sampled during the forward pass.
5. **Training Observability Dashboard**: Log TITO invariant violations, loss spikes, and rollout divergence metrics to a monitoring dashboard for rapid debugging.

## Source
https://qgallouedec-tito.hf.space/?utm_source=tldrai

## Status
Proposed

## Effort
Large