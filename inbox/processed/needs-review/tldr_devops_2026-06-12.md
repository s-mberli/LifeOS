---
actionability: high
attached_experts: []
channel_name: ''
created_at: '2026-06-13T10:08:46.790576+10:00'
domain: unknown
expert_status: unattached
primary_mode: router
privacy: public
review_status: new
secondary_modes: []
source_type: article
source_url: https://tldr.tech/devops/2026-06-12
status: processed
suggested_experts: []
tags:
- terraform
- policy-as-code
- ai-agents
- kubernetes
- formal-verification
- aws
- bedrock
- datadog
- metrics
- edge-computing
title: Terraform Auto-Apply 🪐, Fable on AWS ☁️, Infinite Cardinality Metrics 📏
transcript_path: ''
type: insight_note
updated_at: '2026-06-13T10:08:46.790576+10:00'
---

# Terraform Auto-Apply 🪐, Fable on AWS ☁️, Infinite Cardinality Metrics 📏

## Summary
This TLDR DevOps newsletter (2026-06-12) covers a dense set of infrastructure, AI agent, and formal verification trends converging around one central theme: making automated systems safe enough to run without human gatekeeping at every step. The newsletter argues—implicitly through its curation—that the bottleneck in modern DevOps is no longer provisioning or deployment speed, but trust. Trust that AI-generated code won't introduce subtle bugs, trust that auto-applied infrastructure changes won't blow up production, trust that multi-tenant agent runtimes can't leak data, and trust that observability costs won't explode as tagging grows.

The most architecturally significant items are: (1) Safe Terraform auto-apply via deterministic policy-as-code (conftest/Rego), which replaces rushed human review or non-deterministic AI judgment with machine-checkable rules—restricting to creates-only, limiting blast radius, restricting resource types, or gating production changes. (2) Agent Substrate (Solo.io + Google), an open-source Kubernetes runtime for sandboxed AI agents with scale-to-zero, 50–200ms resume times, and per-pod multi-tenant isolation—essentially treating AI agents as first-class workloads with the same isolation guarantees as VMs. (3) AWS Nitro Isolation Engine, the first formally verified cloud hypervisor, using Rust + Isabelle/HOL with 330k+ lines of machine-checked proofs covering confidentiality, integrity, functional correctness, runtime safety, and memory safety—now always-on for Graviton5 users. (4) Jane Street building a formal methods team specifically because AI agents produce fast but overly complex code with subtle bugs—formal methods serve dual purpose as verification for humans and feedback to improve agent output.

The newsletter also covers: Datadog's infinite cardinality pricing (charge by metric name, not time series, enabling unlimited tagging dimensions), Discord's voice migration to Cloudflare's edge (80%+ traffic, 300+ cities, solving ISP peering and Rust event-loop starvation), Zed's DeltaDB (version control linking code changes to conversations with multi-agent editing support), Claude Fable 5 on Bedrock (auto-routing sensitive prompts to Opus 4.8), and the evolution of static type systems making them genuinely practical through nullability, union types, and inference.

## Key Ideas
- Safe Terraform Auto-Apply via Policy-as-Code: Replace human review gates with deterministic conftest/Rego policies that auto-apply only when plans pass machine-checkable rules. Practical rules include: allow only creates (no destroys), limit blast radius (max N resources), restrict to approved resource types, require human review for production namespaces. This is the infrastructure equivalent of CI/CD gates but applied at the plan-approval stage—critical as AI agents increasingly generate Terraform and human review becomes the bottleneck.
- Agent Substrate / kagent (Solo.io + Google): Open-source Kubernetes-native runtime for sandboxed AI agents. Key properties: scale-to-zero (pay nothing when idle), suspend/resume in 50–200ms (faster than cold-start containers), multi-agent pod packing with per-pod tenant isolation. Solo.io merged their own sandboxing stack (Bubblewrap, Landlock, seccomp, Firecracker microVMs) with Google's overlapping project. This is the infrastructure layer for running AI agents as production workloads—not just dev experiments.
- Formal Methods as AI Code Verification: Jane Street is building a formal methods team specifically because AI-generated code is fast but introduces subtle, complex bugs that humans miss in review. Formal methods serve a dual purpose: (a) verification oracle for human reviewers, (b) structured feedback signal to improve agent output quality over time. This represents a shift from 'move fast and fix in prod' to 'prove correctness before merge'—especially critical for financial systems.
- AWS Nitro Isolation Engine — First Formally Verified Cloud Hypervisor: Rust-based separation kernel verified with Isabelle/HOL, μRust, Separation Logic. 330,000+ lines of machine-checked proofs covering confidentiality, integrity, functional correctness, runtime safety, memory safety. Always-on for Graviton5 (M9g/M9gd) users. This means every Graviton5 instance runs on a hypervisor with mathematical proofs of isolation—not just best-effort security.
- Datadog Infinite Cardinality Metrics: Pricing model shift from charging per unique time series (tag combination explosion = cost explosion) to charging per metric name. Enables unlimited tagging dimensions without exponential cost growth. This removes the artificial constraint that has limited observability granularity for years—teams can now tag by any dimension (agent ID, workflow, tenant, experiment) without cost anxiety.
- DeltaDB (Zed): Version control system that records every operation between commits (not just diffs), linking code changes to the conversations that produced them. Supports conflict-free replicated worktrees for multi-user/multi-agent editing. Traces any line of code back to its origin conversation. This is version control designed for the AI agent era—where code is produced by agents in conversation, not by humans typing files.
- Discord Voice Migration to Cloudflare Edge: 80%+ of voice/video traffic moved to 300+ city edge network. 70% of regions saw quality improvements (Frankfurt: 34% lower ping, 42% less packet loss). Key engineering challenges solved: ISP peering bottlenecks, NIC queue contention (halved server density), Rust event-loop starvation + CPU scheduling conflicts causing latency spikes. Demonstrates that edge migration at scale requires solving systems-level problems, not just DNS changes.
- Claude Fable 5 on AWS Bedrock: Anthropic's new model with built-in safety routing—sensitive prompts (cybersecurity, biology, chemistry, health) automatically escalated to Opus 4.8. Requires explicit opt-in to 30-day data retention and human review. Relevant for teams building AI agents on AWS who need model-tier routing based on content sensitivity.

## Why this matters for the user
- AI Brain & Projects (ai-platform): Agent Substrate is directly relevant as a reference architecture for running sandboxed AI agents on Kubernetes with scale-to-zero and tenant isolation—this could inform your agent platform architecture decisions. DeltaDB's conversation-to-code lineage model is relevant for tracking which agent conversations produced which code changes in your portfolio projects. The formal methods trend (Jane Street, AWS Nitro) signals that AI-generated code verification is becoming a first-class concern—your agent workflows should plan for deterministic verification gates, not just human review.
- AI Brain & Projects (ai-platform): Safe Terraform auto-apply via conftest/Rego is a concrete pattern you can adopt for your own infrastructure—if you're building agent-driven infrastructure, deterministic policy gates are the only safe path to auto-apply. The Datadog infinite cardinality pricing model is relevant if your agent platform generates high-cardinality metrics (per-agent, per-workflow, per-tenant)—this removes a cost barrier to granular observability.
- Flow Temple (flow-temple): The Discord edge migration case study is a useful reference for understanding how to architect low-latency systems at scale—relevant if you're building any real-time features (e.g., live sound healing sessions, real-time biometric feedback). The formal verification trend (Nitro, Jane Street) connects to the wellness domain's need for trust and safety—if you integrate AI into wellness recommendations, formal verification of safety constraints becomes critical.
- Life Kompass (life-kompass): The overarching theme of this newsletter—replacing human bottleneck gates with deterministic automated checks—is a useful mental model for your own productivity systems. The pattern of 'deterministic policy > human judgment at scale' applies to daily routines, content pipelines, and decision frameworks. The static typing evolution insight (types becoming genuinely useful, not just verbose) is a reminder that infrastructure investments in correctness pay compound returns.

## Related Modes
- ai-platform
- life-kompass

## Next Action
- [ ] 1. Read the Agent Substrate / kagent GitHub repo (Solo.io + Google) and evaluate whether its sandboxed agent runtime model could inform your ai-platform architecture—specifically the scale-to-zero + tenant isolation pattern. 2. Set up a conftest/Rego policy for one of your Terraform repos as a test: write a rule that auto-approves plans containing only 'create' operations on non-production resources, and blocks anything else. This gives you hands-on experience with the safe auto-apply pattern. 3. Review your current Datadog (or equivalent) metric tagging strategy—identify one high-cardinality dimension you've been avoiding due to cost, and evaluate whether infinite cardinality pricing (or a self-hosted alternative) unlocks it.

## Long Resource Processing
- chunks processed: 3
- method: chunked map-reduce summary

## AI Generation Data
- Provider: openrouter
- Model: openrouter/owl-alpha

## Source Reliability
high

## Detailed Chunk Summaries

Chunk 1 Summary:
Here are the key points from this section of the TLDR DevOps newsletter (2026-06-12):

- **Agent Substrate (Solo.io + Google):** Open-source project for running sandboxed AI agents on Kubernetes with scale-to-zero, fast resume (50–200ms), and multi-tenant isolation per pod.

- **Claude Fable 5 on AWS:** Anthropic’s new model available on Amazon Bedrock; routes sensitive prompts to Opus 4.8 and requires opting into 30-day data retention/human review.

- **Formal methods (Jane Street):** Growing importance due to AI-generated code’s complexity and subtle bugs; used for verification and agent feedback.

- **AWS Nitro formal verification:** First formally verified cloud hypervisor using Rust, Isabelle/HOL, and 330k+ lines of machine-checked proofs for isolation guarantees.

- **Safe Terraform auto-apply:** Use conftest/Rego to enforce deterministic policy-as-code checks on Terraform plans instead of relying on human or AI judgment.

- **DeltaDB (Zed):** Version-control system that tracks fine-grained operations between commits, linking code changes to conversations and supporting multi-agent collaboration.

- **Discord voice migration to edge:** Moved >80% of voice/video traffic to Cloudflare’s edge network, improving latency and packet loss; required solving peering, NIC, and Rust event-loop issues.

- **AWS Graviton5 (M9g/M9gd):** New EC2 instances with up to 25% better compute performance vs Graviton4.

- **Infinite Cardinality Metrics (Datadog):** Pricing by metric name instead of unique time series, enabling unlimited tagging dimensions without cost explosion.

- **Static types evolution:** Modern type systems (nullability, union types, inference) have made static typing significantly more practical and valuable.

---

Chunk 2 Summary:
**Key Points Summary (Part 2/3):**

- **Safe Terraform Auto-Apply**: Use policy-as-code (e.g., conftest/Rego) to auto-apply plans only if they pass deterministic checks—like allowing only creates, limiting blast radius, restricting resource types, or requiring human review for production.

- **DeltaDB (Zed)**: A version-control system linking code changes to the conversations that produced them, with stable delta identities and support for multi-user/multi-agent editing.

- **Discord Voice Migration**: Moved >80% of voice/video traffic to Cloudflare’s edge network, improving latency and packet loss; solved challenges like ISP peering, NIC contention, and Rust event-loop issues.

- **AWS Graviton5 Instances**: New M9g/M9gd EC2 instances offer up to 25% better compute performance than Graviton4.

- **Datadog Infinite Cardinality Metrics**: Charges by metric name—not time series—enabling unlimited tagging without cost explosion.

- **Static Typing Evolution**: Modern type systems now include nullability, union types, and inference, making static typing more practical and valuable.

- **Agent Substrate (Solo.io + Google)**: Open-source Kubernetes solution for sandboxed AI agents that scale to zero, suspend/resume quickly, and enforce tenant isolation.

- **Claude Fable 5 on AWS**: Anthropic’s new model available on Bedrock with built-in safeguards (e.g., routing sensitive prompts to Opus 4.8); requires opting into data retention and human review.

- **Formal Methods at Jane Street**: Adopting formal verification to catch subtle bugs in AI-generated code and improve agent output quality.

- **AWS Nitro Isolation Engine**: First formally verified cloud hypervisor, using machine-checked proofs to ensure VM isolation on Graviton5.

---

Chunk 3 Summary:
# Summary: Terraform Auto-Apply, Fable on AWS, Infinite Cardinality Metrics

## Key Points

**Buildkite** — CI/CD platform offering multi-language/cloud pipelines, flaky-test detection with auto-quarantine, test splitting, artifact management, MCP integration, and universal pipeline triggers. 30-day free trial available.

**Agent Substrate / kagent** — Solo.io and Google collaborated on an open-source solution for running sandboxed AI agents on Kubernetes. Features scale-to-zero, suspend/resume in 50–200ms, multi-agent pod packing with tenant isolation. Solo.io merged its own similar tech (Bubblewrap, Landlock, seccomp, Firecracker microVMs) with Google's overlapping project.

**Anthropic Claude Fable 5 on AWS** — Now available on Amazon Bedrock and Claude Platform in US East (N. Virginia) and Europe (Stockholm). State-of-the-art in software engineering and knowledge work. Automatically routes sensitive prompts (cybersecurity, biology, chemistry, health) to Opus 4.8. Requires opting into 30-day data retention and human review.

**Formal Methods & Agentic Coding** — Jane Street is building a formal methods team because AI agents produce fast but overly complex code with subtle bugs. Formal methods serve as both verification for human reviewers and feedback to improve agent output quality.

**AWS Nitro Isolation Engine** — First formally verified cloud hypervisor. Uses a Rust-based separation kernel verified with Isabelle/HOL, μRust, Separation Logic, and 330,000 lines of machine-checked proofs. Always-on for Graviton5 users. Covers confidentiality, integrity, functional correctness, runtime safety, and memory safety.

**Safe Terraform Auto-Apply** — Auto-apply Terraform plans safely using deterministic policy-as-code checks (conftest/Rego) instead of rushed human reviews or non-deterministic AI. Rules can restrict to creates only, limit blast radius, restrict resource types, or gate production changes.

**DeltaDB (Zed)** — Version-control system recording every operation between commits, linking code changes to the conversations that produced them. Supports conflict-free replicated worktrees for multi-user/multi-agent editing and traces any line of code back to its origin.

**Discord Voice Migration to Edge** — Discord moved 80%+ of voice/video traffic to Cloudflare's 300+ city network. 70% of regions saw quality improvements (Frankfurt: 34% lower ping, 42% less packet loss). Challenges included ISP peering bottlenecks, NIC queue contention (halved server density), and latency spikes from Rust event loop starvation + CPU scheduling conflicts.

**Redwood RunMyJobs** — Workload automation platform: 4B SaaS executions/year, 99.95% uptime SLA, no infra costs for agents/databases/VMs. Used by >50% of Fortune 50.

**AWS Graviton5 / M9g & M9gd Instances** — New EC2 instances delivering up to 25% better compute performance than Graviton4.

**Datadog Infinite Cardinality Metrics** — New pricing model charging by metric name rather than unique time series from tag combinations, enabling unlimited dimensions without exponential cost growth.

**Static Types Evolution** — Modern type systems (nullability, union types, type inference) transformed static typing from verbose "paper shovels" into genuinely useful tools.

## Original Content
### Raw User Input
https://tldr.tech/devops/2026-06-12

# TLDR DevOps — 2026-06-12
Source: https://tldr.tech/devops/2026-06-12

## Articles

### Agent Substrate Can Power Agents on Kubernetes with kagent
- **URL:** https://www.solo.io/blog/agent-substrate-powers-kubernetes-agents-with-kagent?utm_source=tldrdevops
- **Via:** TLDR DevOps, 2026-06-12
- **Read time:** 16 minute read
- **TLDR Summary:** Solo.io announced its collaboration with Google on the Agent Substrate project, an open-source solution for running sandboxed AI agents on Kubernetes that can scale to zero, suspend idle agents to storage, and resume them in 50-200ms while packing multiple agent instances into single pods with strict tenant isolation. The company was preparing to open-source its own similar technology—which used Bubblewrap, Landlock, seccomp, and optional Firecracker microVMs—when it discovered Google's overlapping architecture and decided to combine efforts instead.

### Anthropic Claude Fable 5 on AWS: Mythos-class capabilities with built-in safeguards now available
- **URL:** https://aws.amazon.com/blogs/aws/anthropic-claude-fable-5-on-aws-mythos-class-capabilities-with-built-in-safeguards-now-available/?utm_source=tldrdevops
- **Via:** TLDR DevOps, 2026-06-12
- **Read time:** 4 minute read
- **TLDR Summary:** Anthropic's Claude Fable 5 model has launched on Amazon Bedrock and Claude Platform on AWS. Featuring state-of-the-art performance across software engineering and knowledge work while automatically routing potentially harmful prompts about cybersecurity, biology, chemistry, and health to the older Opus 4.8 model, the model is now available in US East (N. Virginia), and Europe (Stockholm) regions, though accessing it requires opting into a 30-day data retention and human review policy through Amazon Bedrock's Data Retention API.

### Formal methods and the future of programming
- **URL:** https://blog.janestreet.com/formal-methods-at-jane-street-index/?utm_source=tldrdevops
- **Via:** TLDR DevOps, 2026-06-12
- **Read time:** 8 minute read
- **TLDR Summary:** Jane Street is building a formal methods team because agentic coding has changed the cost-benefit tradeoff for software verification. AI agents can now generate useful code quickly, but they also tend to produce overly complex code with subtle bugs and missed invariants, making formal methods more attractive as both a verification tool for human reviewers and a feedback mechanism that helps agents produce safer, higher-quality code.

### How formal verification makes AWS Nitro the first formally verified cloud hypervisor
- **URL:** https://www.amazon.science/blog/ec2s-formally-verified-isolation-engine-provides-mathematical-assurance-of-virtual-machine-isolation?utm_source=tldrdevops
- **Via:** TLDR DevOps, 2026-06-12
- **Read time:** 7 minute read
- **TLDR Summary:** The new AWS Nitro Isolation Engine provides mathematically verified isolation between EC2 virtual machines and ships as an always-on feature for Graviton5 users. Its critical isolation logic runs through a small Rust-based separation kernel verified with Isabelle/HOL, μRust, Separation Logic, and 330,000 lines of machine-checked proofs covering confidentiality, integrity, functional correctness, runtime safety, and memory safety.

### Safe Terraform auto-apply with conftest
- **URL:** https://www.bejarano.io/terraform-autoapply/?utm_source=tldrdevops
- **Via:** TLDR DevOps, 2026-06-12
- **Read time:** 4 minute read
- **TLDR Summary:** Terraform plans can be auto-applied safely when they pass deterministic policy-as-code checks instead of relying on rushed human reviews or non-deterministic AI judgment. Exporting Terraform plans as JSON and evaluating them with conftest/Rego lets teams define explicit rules for safe changes, such as allowing only creates, limiting blast radius, restricting resource types, or gating production changes for human review.

### Software Is Made Between Commits
- **URL:** https://zed.dev/blog/introducing-deltadb?utm_source=tldrdevops
- **Via:** TLDR DevOps, 2026-06-12
- **Read time:** 3 minute read
- **TLDR Summary:** DeltaDB is a version-control system that records every operation between commits so code changes and the conversations that produced them stay linked over time. It gives each fine-grained delta a stable identity, supports conflict-free replicated worktrees for multi-user and multi-agent editing, and lets developers trace any line of code back to the agent or teammate conversation that created or changed it.

### How We Moved Discord Voice to the Edge
- **URL:** https://discord.com/blog/how-we-moved-discord-voice-to-the-edge?utm_source=tldrdevops
- **Via:** TLDR DevOps, 2026-06-12
- **Read time:** 12 minute read
- **TLDR Summary:** Discord migrated over 80% of its voice and video traffic from traditional cloud providers to Cloudflare's 300+ city network, resulting in quality improvements across 70% of regions with Frankfurt seeing 34% lower ping and 42% less packet loss. The year-long migration required building custom infrastructure to handle Cloudflare's ephemeral container architecture and solving tricky issues like ISP peering bottlenecks in France, NIC queue contention that initially forced them to halve server density, and mysterious latency spikes in Europe that turned out to be a combination of event loop starvation in their Rust code and CPU scheduling conflicts with network interrupt handling.

### Now available: Amazon EC2 M9g and M9gd instances powered by new AWS Graviton5 processors
- **URL:** https://aws.amazon.com/blogs/aws/now-available-amazon-ec2-m9g-and-m9gd-instances-powered-by-new-aws-graviton5-processors/?utm_source=tldrdevops
- **Via:** TLDR DevOps, 2026-06-12
- **Read time:** 5 minute read
- **TLDR Summary:** Amazon EC2 M9g and M9gd instances, powered by Graviton5 processors, deliver up to 25% better compute performance than Graviton4.

### Infinite Cardinality Metrics: Custom metrics built for modern systems
- **URL:** https://www.datadoghq.com/blog/infinite-cardinality-metrics/?utm_source=tldrdevops
- **Via:** TLDR DevOps, 2026-06-12
- **Read time:** 4 minute read
- **TLDR Summary:** Datadog's Infinite Cardinality Metrics is a new pricing model that charges custom metrics by metric name rather than the number of unique time series created by tag combinations, allowing engineers to add unlimited dimensions without worrying about exponential cost increases.

### Static types and shovels
- **URL:** https://carefully.understood.systems/blog-2026-06-10-static-type-shovel.html?utm_source=tldrdevops
- **Via:** TLDR DevOps, 2026-06-12
- **Read time:** 3 minute read
- **TLDR Summary:** Static typing became more useful as mainstream type systems improved from verbose, low-value “paper shovels” into modern systems with nullability, sum or union types, and type inference.

## Full Text

[You're now building at a scale that deserves a pro-tool. (Sponsor)](https://buildkite.com/pricing?utm_campaign=Primary05152026&amp;utm_source=tldrtech&amp;utm_medium=newsletter_header) Other CI platforms make you compromise on flexibility, speed or scale. Need 1,000 concurrent runners? 10,000? 100,000+? Done. Buildkite runners live on your infra, ours, or both. Parallelize, fan-out and orchestrate to depths a faster runner can't reach. With Buildkite, you get pipelines across any language or cloud, flaky-test detection with auto-quarantine and test splitting, artifact management to cache dependencies and secure your supply chain, and agentic components like first-party MCP and universal pipeline triggers. Try the 30-day all-access trial. No credit card. Real engineer on standby. [Start building →](https://buildkite.com/pricing?utm_campaign=Primary05152026&utm_source=tldrtech&utm_medium=newsletter_cta)

[Agent Substrate Can Power Agents on Kubernetes with kagent (16 minute read)](https://www.solo.io/blog/agent-substrate-powers-kubernetes-agents-with-kagent?utm_source=tldrdevops) Solo.io announced its collaboration with Google on the Agent Substrate project, an open-source solution for running sandboxed AI agents on Kubernetes that can scale to zero, suspend idle agents to storage, and resume them in 50-200ms while packing multiple agent instances into single pods with strict tenant isolation. The company was preparing to open-source its own similar technology—which used Bubblewrap, Landlock, seccomp, and optional Firecracker microVMs—when it discovered Google's overlapping architecture and decided to combine efforts instead.

[Anthropic Claude Fable 5 on AWS: Mythos-class capabilities with built-in safeguards now available (4 minute read)](https://aws.amazon.com/blogs/aws/anthropic-claude-fable-5-on-aws-mythos-class-capabilities-with-built-in-safeguards-now-available/?utm_source=tldrdevops) Anthropic's Claude Fable 5 model has launched on Amazon Bedrock and Claude Platform on AWS. Featuring state-of-the-art performance across software engineering and knowledge work while automatically routing potentially harmful prompts about cybersecurity, biology, chemistry, and health to the older Opus 4.8 model, the model is now available in US East (N. Virginia), and Europe (Stockholm) regions, though accessing it requires opting into a 30-day data retention and human review policy through Amazon Bedrock's Data Retention API.

[Formal methods and the future of programming (8 minute read)](https://blog.janestreet.com/formal-methods-at-jane-street-index/?utm_source=tldrdevops) Jane Street is building a formal methods team because agentic coding has changed the cost-benefit tradeoff for software verification. AI agents can now generate useful code quickly, but they also tend to produce overly complex code with subtle bugs and missed invariants, making formal methods more attractive as both a verification tool for human reviewers and a feedback mechanism that helps agents produce safer, higher-quality code.

[How formal verification makes AWS Nitro the first formally verified cloud hypervisor (7 minute read)](https://www.amazon.science/blog/ec2s-formally-verified-isolation-engine-provides-mathematical-assurance-of-virtual-machine-isolation?utm_source=tldrdevops) The new AWS Nitro Isolation Engine provides mathematically verified isolation between EC2 virtual machines and ships as an always-on feature for Graviton5 users. Its critical isolation logic runs through a small Rust-based separation kernel verified with Isabelle/HOL, μRust, Separation Logic, and 330,000 lines of machine-checked proofs covering confidentiality, integrity, functional correctness, runtime safety, and memory safety.

[Safe Terraform auto-apply with conftest (4 minute read)](https://www.bejarano.io/terraform-autoapply/?utm_source=tldrdevops) Terraform plans can be auto-applied safely when they pass deterministic policy-as-code checks instead of relying on rushed human reviews or non-deterministic AI judgment. Exporting Terraform plans as JSON and evaluating them with conftest/Rego lets teams define explicit rules for safe changes, such as allowing only creates, limiting blast radius, restricting resource types, or gating production changes for human review.

[Software Is Made Between Commits (3 minute read)](https://zed.dev/blog/introducing-deltadb?utm_source=tldrdevops) DeltaDB is a version-control system that records every operation between commits so code changes and the conversations that produced them stay linked over time. It gives each fine-grained delta a stable identity, supports conflict-free replicated worktrees for multi-user and multi-agent editing, and lets developers trace any line of code back to the agent or teammate conversation that created or changed it.

[How We Moved Discord Voice to the Edge (12 minute read)](https://discord.com/blog/how-we-moved-discord-voice-to-the-edge?utm_source=tldrdevops) Discord migrated over 80% of its voice and video traffic from traditional cloud providers to Cloudflare's 300+ city network, resulting in quality improvements across 70% of regions with Frankfurt seeing 34% lower ping and 42% less packet loss. The year-long migration required building custom infrastructure to handle Cloudflare's ephemeral container architecture and solving tricky issues like ISP peering bottlenecks in France, NIC queue contention that initially forced them to halve server density, and mysterious latency spikes in Europe that turned out to be a combination of event loop starvation in their Rust code and CPU scheduling conflicts with network interrupt handling.

[They have 10x the uptime SLA of the nearest workload automation competitor (Sponsor)](https://runmyjobs.redwood.com/lp/redwood-orchestration?utm_source=tldr&amp;utm_medium=listing&amp;utm_campaign=devops_primary) 4 billion SaaS executions per year, 99.95% uptime SLA, and no infra costs for agents, databases, or VMs. No wonder why >50% of the Fortune 50 trust Redwood.  [Get a Demo](https://runmyjobs.redwood.com/lp/redwood-orchestration?utm_source=tldr&utm_medium=listing&utm_campaign=devops_primary)

[Now available: Amazon EC2 M9g and M9gd instances powered by new AWS Graviton5 processors (5 minute read)](https://aws.amazon.com/blogs/aws/now-available-amazon-ec2-m9g-and-m9gd-instances-powered-by-new-aws-graviton5-processors/?utm_source=tldrdevops) Amazon EC2 M9g and M9gd instances, powered by Graviton5 processors, deliver up to 25% better compute performance than Graviton4.

[Infinite Cardinality Metrics: Custom metrics built for modern systems (4 minute read)](https://www.datadoghq.com/blog/infinite-cardinality-metrics/?utm_source=tldrdevops) Datadog's Infinite Cardinality Metrics is a new pricing model that charges custom metrics by metric name rather than the number of unique time series created by tag combinations, allowing engineers to add unlimited dimensions without worrying about exponential cost increases.

[Static types and shovels (3 minute read)](https://carefully.understood.systems/blog-2026-06-10-static-type-shovel.html?utm_source=tldrdevops) Static typing became more useful as mainstream type systems improved from verbose, low-value “paper shovels” into modern systems with nullability, sum or union types, and type inference.

### Fetched Web Text
[You're now building at a scale that deserves a pro-tool. (Sponsor)](https://buildkite.com/pricing?utm_campaign=Primary05152026&amp;utm_source=tldrtech&amp;utm_medium=newsletter_header) Other CI platforms make you compromise on flexibility, speed or scale. Need 1,000 concurrent runners? 10,000? 100,000+? Done. Buildkite runners live on your infra, ours, or both. Parallelize, fan-out and orchestrate to depths a faster runner can't reach. With Buildkite, you get pipelines across any language or cloud, flaky-test detection with auto-quarantine and test splitting, artifact management to cache dependencies and secure your supply chain, and agentic components like first-party MCP and universal pipeline triggers. Try the 30-day all-access trial. No credit card. Real engineer on standby. [Start building →](https://buildkite.com/pricing?utm_campaign=Primary05152026&utm_source=tldrtech&utm_medium=newsletter_cta)

[Agent Substrate Can Power Agents on Kubernetes with kagent (16 minute read)](https://www.solo.io/blog/agent-substrate-powers-kubernetes-agents-with-kagent?utm_source=tldrdevops) Solo.io announced its collaboration with Google on the Agent Substrate project, an open-source solution for running sandboxed AI agents on Kubernetes that can scale to zero, suspend idle agents to storage, and resume them in 50-200ms while packing multiple agent instances into single pods with strict tenant isolation. The company was preparing to open-source its own similar technology—which used Bubblewrap, Landlock, seccomp, and optional Firecracker microVMs—when it discovered Google's overlapping architecture and decided to combine efforts instead.

[Anthropic Claude Fable 5 on AWS: Mythos-class capabilities with built-in safeguards now available (4 minute read)](https://aws.amazon.com/blogs/aws/anthropic-claude-fable-5-on-aws-mythos-class-capabilities-with-built-in-safeguards-now-available/?utm_source=tldrdevops) Anthropic's Claude Fable 5 model has launched on Amazon Bedrock and Claude Platform on AWS. Featuring state-of-the-art performance across software engineering and knowledge work while automatically routing potentially harmful prompts about cybersecurity, biology, chemistry, and health to the older Opus 4.8 model, the model is now available in US East (N. Virginia), and Europe (Stockholm) regions, though accessing it requires opting into a 30-day data retention and human review policy through Amazon Bedrock's Data Retention API.

[Formal methods and the future of programming (8 minute read)](https://blog.janestreet.com/formal-methods-at-jane-street-index/?utm_source=tldrdevops) Jane Street is building a formal methods team because agentic coding has changed the cost-benefit tradeoff for software verification. AI agents can now generate useful code quickly, but they also tend to produce overly complex code with subtle bugs and missed invariants, making formal methods more attractive as both a verification tool for human reviewers and a feedback mechanism that helps agents produce safer, higher-quality code.

[How formal verification makes AWS Nitro the first formally verified cloud hypervisor (7 minute read)](https://www.amazon.science/blog/ec2s-formally-verified-isolation-engine-provides-mathematical-assurance-of-virtual-machine-isolation?utm_source=tldrdevops) The new AWS Nitro Isolation Engine provides mathematically verified isolation between EC2 virtual machines and ships as an always-on feature for Graviton5 users. Its critical isolation logic runs through a small Rust-based separation kernel verified with Isabelle/HOL, μRust, Separation Logic, and 330,000 lines of machine-checked proofs covering confidentiality, integrity, functional correctness, runtime safety, and memory safety.

[Safe Terraform auto-apply with conftest (4 minute read)](https://www.bejarano.io/terraform-autoapply/?utm_source=tldrdevops) Terraform plans can be auto-applied safely when they pass deterministic policy-as-code checks instead of relying on rushed human reviews or non-deterministic AI judgment. Exporting Terraform plans as JSON and evaluating them with conftest/Rego lets teams define explicit rules for safe changes, such as allowing only creates, limiting blast radius, restricting resource types, or gating production changes for human review.

[Software Is Made Between Commits (3 minute read)](https://zed.dev/blog/introducing-deltadb?utm_source=tldrdevops) DeltaDB is a version-control system that records every operation between commits so code changes and the conversations that produced them stay linked over time. It gives each fine-grained delta a stable identity, supports conflict-free replicated worktrees for multi-user and multi-agent editing, and lets developers trace any line of code back to the agent or teammate conversation that created or changed it.

[How We Moved Discord Voice to the Edge (12 minute read)](https://discord.com/blog/how-we-moved-discord-voice-to-the-edge?utm_source=tldrdevops) Discord migrated over 80% of its voice and video traffic from traditional cloud providers to Cloudflare's 300+ city network, resulting in quality improvements across 70% of regions with Frankfurt seeing 34% lower ping and 42% less packet loss. The year-long migration required building custom infrastructure to handle Cloudflare's ephemeral container architecture and solving tricky issues like ISP peering bottlenecks in France, NIC queue contention that initially forced them to halve server density, and mysterious latency spikes in Europe that turned out to be a combination of event loop starvation in their Rust code and CPU scheduling conflicts with network interrupt handling.

[They have 10x the uptime SLA of the nearest workload automation competitor (Sponsor)](https://runmyjobs.redwood.com/lp/redwood-orchestration?utm_source=tldr&amp;utm_medium=listing&amp;utm_campaign=devops_primary) 4 billion SaaS executions per year, 99.95% uptime SLA, and no infra costs for agents, databases, or VMs. No wonder why >50% of the Fortune 50 trust Redwood.  [Get a Demo](https://runmyjobs.redwood.com/lp/redwood-orchestration?utm_source=tldr&utm_medium=listing&utm_campaign=devops_primary)

[Now available: Amazon EC2 M9g and M9gd instances powered by new AWS Graviton5 processors (5 minute read)](https://aws.amazon.com/blogs/aws/now-available-amazon-ec2-m9g-and-m9gd-instances-powered-by-new-aws-graviton5-processors/?utm_source=tldrdevops) Amazon EC2 M9g and M9gd instances, powered by Graviton5 processors, deliver up to 25% better compute performance than Graviton4.

[Infinite Cardinality Metrics: Custom metrics built for modern systems (4 minute read)](https://www.datadoghq.com/blog/infinite-cardinality-metrics/?utm_source=tldrdevops) Datadog's Infinite Cardinality Metrics is a new pricing model that charges custom metrics by metric name rather than the number of unique time series created by tag combinations, allowing engineers to add unlimited dimensions without worrying about exponential cost increases.

[Static types and shovels (3 minute read)](https://carefully.understood.systems/blog-2026-06-10-static-type-shovel.html?utm_source=tldrdevops) Static typing became more useful as mainstream type systems improved from verbose, low-value “paper shovels” into modern systems with nullability, sum or union types, and type inference.

### Source URL
https://tldr.tech/devops/2026-06-12
