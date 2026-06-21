---
actionability: high
attached_experts: []
channel_name: ''
created_at: '2026-06-05T08:53:07.712459+10:00'
domain: unknown
expert_status: unattached
primary_mode: router
privacy: public
review_status: new
secondary_modes: []
source_type: article
source_url: https://tldr.tech/devops/2026-05-22
status: processed
suggested_experts: []
tags: []
title: Secure AI 🥷, AWS CLI Creator ☁️, Policy For Agents 📜
transcript_path: ''
type: insight_note
updated_at: '2026-06-05T08:53:07.712459+10:00'
---

# Secure AI 🥷, AWS CLI Creator ☁️, Policy For Agents 📜

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
https://tldr.tech/devops/2026-05-22

Congratulations: you're responsible for building agents and keeping them running… (Sponsor) …and traditional engineering practices don't work on agentic systems. You can't just write unit tests and call it a day when the same input can produce different outputs every time. In  this ungated guide , New Relic lays out how to transition from deterministic software to probabilistic agents. It explains the  5 core pillars of an agent , quantifies the cost of poor visibility, and helps you identify the difference between a technical issue and a logical failure.  Understand the core architecture of agentic engineering and how to treat agents as manageable systems.  Get the guide

Building Self-Extending CLI Tools with Strands Agent (9 minute read) CLI Creator is an open-source tool that uses Amazon Bedrock and the Strands Agents SDK to automatically generate command-line interface tools from natural language descriptions, allowing users to create and iteratively refine new commands in minutes without manual coding. The tool uses Claude Opus 4.6 on Amazon Bedrock with self-correcting post-conditions to validate generated code and integrates with Anthropic's Model Context Protocol to automatically discover relevant API servers, while maintaining full version control through git for all generated tools.

Now in Public Preview: Store Terraform State in Pulumi Cloud (5 minute read) Pulumi Cloud can now act as a Terraform state backend, enabling teams to store Terraform state alongside Pulumi stacks while continuing to use Terraform or OpenTofu. This unlocks unified visibility, RBAC, encrypted state, audit policies, and AI-driven infrastructure insights via Pulumi Neo across mixed IaC environments, including AWS GovCloud and other partitions.

How We Built DigitalOcean Inference Router (12 minute read) Inference Router is an infrastructure-level tool from DigitalOcean that automatically routes AI requests to the most appropriate model based on task requirements, helping developers cut costs by avoiding unnecessary use of expensive frontier models for simple tasks. The system is powered by Plano, an open-source AI proxy using a 30B Mixture-of-Experts routing model that outperforms GPT-5.1 and Claude Sonnet 4.5 on routing accuracy while resolving intent in roughly 200ms.

What kubectl debug doesn't tell you: The silent evidence gap (5 minute read) Kubernetes doesn't retain debug session data like exit codes or duration after a pod's state changes, creating potential gaps in incident response and compliance tracking since ephemeral containers lack the "lastState" field that regular containers use to preserve termination records. A CNCF community member demonstrated this API design limitation affects Kubernetes 1.25+ clusters and outlined workarounds including real-time capture tools and external logging, while suggesting that SIG Node or SIG Instrumentation could address this as kubectl debug becomes standard for troubleshooting.

Twelve Ways to Be Wrong About AI-Assisted Coding (8 minute read) Measuring AI coding productivity is easy to get wrong: lines of code, adoption rates, ticket counts, self-reported productivity, and toy-task speedups often measure activity or novelty rather than real long-term value. Better evaluation needs control groups, system-level metrics, long-term observation, and accounting for hidden costs like review burden, security issues, technical debt, and increased maintenance.

GitOps with Octopus and Argo CD (11 minute read) Octopus Deploy complements Argo CD by adding enterprise-focused GitOps capabilities like standardized manifest management, approvals, auditing, environment promotion, rollback visibility, and compliance workflows without replacing Argo CD's Kubernetes synchronization engine. Together, they provide scalable GitOps operations with centralized observability, secure deployment governance, and consistent release management across teams and environments.

From latency to instant: Modernizing GitHub Issues navigation performance (15 minute read) GitHub redesigned Issues navigation around a local-first architecture using IndexedDB caching, preheating, in-memory layers, and service workers to reduce perceived latency and make repeated issue views feel instant. The rollout dramatically improved navigation speeds, with many React paths loading under 200 ms, while ongoing work targets remaining hard navigation bottlenecks tied to JavaScript boot and server rendering.

Is your mobile release tooling keeping up with AI? (Sponsor) AI drives up code volume, shifting build vs. buy math for mobile release tooling. Hear how engineers from Monzo, Spotify, Etsy, and Tuist are recalculating. May 28, 1pm ET.  Save your spot.

Announcing etcd 3.7.0-beta.0 (3 minute read) etcd v3.7.0-beta.0 introduces RangeStream, which allows applications to receive large query results in chunks rather than waiting for complete datasets, reducing latency and memory usage issues.

Securing AI in the cloud starts at runtime (2 minute read) Runtime security provides the highest fidelity cloud defense data by capturing how workloads actually behave, helping teams identify active risks, unused permissions, and sensitive interactions beyond static posture analysis.

Introducing Prempti: Policy and visibility for AI coding agents (4 minute read) Prempti is an experimental security tool that monitors and controls AI coding agents like Claude Code by intercepting their file reads, shell commands, and other actions before execution using policy-based rules.

### Fetched Web Text
Congratulations: you're responsible for building agents and keeping them running… (Sponsor) …and traditional engineering practices don't work on agentic systems. You can't just write unit tests and call it a day when the same input can produce different outputs every time. In  this ungated guide , New Relic lays out how to transition from deterministic software to probabilistic agents. It explains the  5 core pillars of an agent , quantifies the cost of poor visibility, and helps you identify the difference between a technical issue and a logical failure.  Understand the core architecture of agentic engineering and how to treat agents as manageable systems.  Get the guide

Building Self-Extending CLI Tools with Strands Agent (9 minute read) CLI Creator is an open-source tool that uses Amazon Bedrock and the Strands Agents SDK to automatically generate command-line interface tools from natural language descriptions, allowing users to create and iteratively refine new commands in minutes without manual coding. The tool uses Claude Opus 4.6 on Amazon Bedrock with self-correcting post-conditions to validate generated code and integrates with Anthropic's Model Context Protocol to automatically discover relevant API servers, while maintaining full version control through git for all generated tools.

Now in Public Preview: Store Terraform State in Pulumi Cloud (5 minute read) Pulumi Cloud can now act as a Terraform state backend, enabling teams to store Terraform state alongside Pulumi stacks while continuing to use Terraform or OpenTofu. This unlocks unified visibility, RBAC, encrypted state, audit policies, and AI-driven infrastructure insights via Pulumi Neo across mixed IaC environments, including AWS GovCloud and other partitions.

How We Built DigitalOcean Inference Router (12 minute read) Inference Router is an infrastructure-level tool from DigitalOcean that automatically routes AI requests to the most appropriate model based on task requirements, helping developers cut costs by avoiding unnecessary use of expensive frontier models for simple tasks. The system is powered by Plano, an open-source AI proxy using a 30B Mixture-of-Experts routing model that outperforms GPT-5.1 and Claude Sonnet 4.5 on routing accuracy while resolving intent in roughly 200ms.

What kubectl debug doesn't tell you: The silent evidence gap (5 minute read) Kubernetes doesn't retain debug session data like exit codes or duration after a pod's state changes, creating potential gaps in incident response and compliance tracking since ephemeral containers lack the "lastState" field that regular containers use to preserve termination records. A CNCF community member demonstrated this API design limitation affects Kubernetes 1.25+ clusters and outlined workarounds including real-time capture tools and external logging, while suggesting that SIG Node or SIG Instrumentation could address this as kubectl debug becomes standard for troubleshooting.

Twelve Ways to Be Wrong About AI-Assisted Coding (8 minute read) Measuring AI coding productivity is easy to get wrong: lines of code, adoption rates, ticket counts, self-reported productivity, and toy-task speedups often measure activity or novelty rather than real long-term value. Better evaluation needs control groups, system-level metrics, long-term observation, and accounting for hidden costs like review burden, security issues, technical debt, and increased maintenance.

GitOps with Octopus and Argo CD (11 minute read) Octopus Deploy complements Argo CD by adding enterprise-focused GitOps capabilities like standardized manifest management, approvals, auditing, environment promotion, rollback visibility, and compliance workflows without replacing Argo CD's Kubernetes synchronization engine. Together, they provide scalable GitOps operations with centralized observability, secure deployment governance, and consistent release management across teams and environments.

From latency to instant: Modernizing GitHub Issues navigation performance (15 minute read) GitHub redesigned Issues navigation around a local-first architecture using IndexedDB caching, preheating, in-memory layers, and service workers to reduce perceived latency and make repeated issue views feel instant. The rollout dramatically improved navigation speeds, with many React paths loading under 200 ms, while ongoing work targets remaining hard navigation bottlenecks tied to JavaScript boot and server rendering.

Is your mobile release tooling keeping up with AI? (Sponsor) AI drives up code volume, shifting build vs. buy math for mobile release tooling. Hear how engineers from Monzo, Spotify, Etsy, and Tuist are recalculating. May 28, 1pm ET.  Save your spot.

Announcing etcd 3.7.0-beta.0 (3 minute read) etcd v3.7.0-beta.0 introduces RangeStream, which allows applications to receive large query results in chunks rather than waiting for complete datasets, reducing latency and memory usage issues.

Securing AI in the cloud starts at runtime (2 minute read) Runtime security provides the highest fidelity cloud defense data by capturing how workloads actually behave, helping teams identify active risks, unused permissions, and sensitive interactions beyond static posture analysis.

Introducing Prempti: Policy and visibility for AI coding agents (4 minute read) Prempti is an experimental security tool that monitors and controls AI coding agents like Claude Code by intercepting their file reads, shell commands, and other actions before execution using policy-based rules.

### Source URL
https://tldr.tech/devops/2026-05-22
