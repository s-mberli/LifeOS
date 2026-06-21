# Unified Agent Memory Architecture for LifeOS

## Problem
LifeOS agents suffer from memory fragmentation: some store context in prompts, others in vector databases, and others in external tools like Notion or Obsidian. There is no consistent memory model, leading to agents that forget user preferences, repeat work, or fail to build on past interactions. As agent harnesses become the primary runtime, memory management is now a first-class concern.

## Proposed Solution
Design a unified agent memory architecture based on insights from the State of Memory in Agent Harness report:
- **Tiered memory system**: 
  - *Working memory*: in-context, short-lived (current session).
  - *Episodic memory*: vector-stored past interactions, retrievable by semantic similarity.
  - *Semantic memory*: structured knowledge graph of user preferences, relationships, and facts.
  - *Procedural memory*: learned workflows and tool usage patterns.
- **Memory lifecycle policies**: auto-expire, compress, or promote memories based on usage and relevance.
- **Cross-agent memory sharing**: allow authorized agents to access shared memories (with privacy controls).
- **Memory provenance**: track where each memory came from and when it was last validated.

Implement this as a LifeOS Memory Service with APIs for agents to store, retrieve, and forget memories.

## Source
https://x.com/mem0ai/status/2061822612398014782?utm_source=tldrai

## Status
✅ Implemented

## Effort
Large