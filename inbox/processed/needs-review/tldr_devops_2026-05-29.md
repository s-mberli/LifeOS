---
actionability: high
attached_experts: []
channel_name: ''
created_at: '2026-06-05T08:52:27.409814+10:00'
domain: unknown
expert_status: unattached
primary_mode: router
privacy: public
review_status: new
secondary_modes: []
source_type: article
source_url: https://tldr.tech/devops/2026-05-29
status: processed
suggested_experts: []
tags: []
title: AWS Resilience Hub 🏢, Reliability Metrics at Scale ⚖️, Multi Cloud AI ☁️
transcript_path: ''
type: insight_note
updated_at: '2026-06-05T08:52:27.409814+10:00'
---

# AWS Resilience Hub 🏢, Reliability Metrics at Scale ⚖️, Multi Cloud AI ☁️

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
https://tldr.tech/devops/2026-05-29

Workload automation shouldn't need its own infrastructure team (Sponsor) Redwood is a Gartner SOAP Leader for two years running - and  RunMyJobs  by Redwood is why. ✅ Agentless - no agents, VMs, or databases to deploy or maintain ✅ 99.95% uptime SLA - we manage the infrastructure, you just use it ✅ Trusted by 50% of the Fortune 50 With RunMyJobs, you can: >> Orchestrate applications, data and infrastructure across cloud, on-prem and hybrid - with 83+ native connectors, no agents required >> Build automations faster with  AI embedded across the automation lifecycle  - scripts, documentation, and workflows >> Stay ahead of failures with predictive SLA monitoring and advanced observability Get a demo today and eliminate infrastructure overhead

Introducing the next generation of AWS Resilience Hub for generative AI-based SRE resilience journey (4 minute read) AWS has launched the next generation of Resilience Hub, introducing an organization-wide system that helps Site Reliability Engineers set consistent resilience goals across hundreds of applications using AI-powered failure mode analysis, dependency discovery, and modular policies with targets like 99.95% availability SLOs. The service is now generally available in AWS commercial regions with a new service-based pricing model that includes two free failure mode assessments per month, and it integrates with AWS Organizations to let teams evaluate resilience from a single delegated administrator account.

Announcing Rust 1.96.0 (3 minute read) Rust 1.96.0 stabilizes new core::range types that implement IntoIterator instead of Iterator, allowing range values to be Copy and making them easier to store inside lightweight structs like spans and slice accessors. The release also adds assert_matches! and debug_assert_matches! for pattern-based assertions with better failure output, tightens WebAssembly linking by treating undefined symbols as errors by default, and fixes two Cargo vulnerabilities affecting third-party registries while leaving crates.io users unaffected.

ISO 27001 on AWS: Building Compliance Into the Architecture (7 minute read) An ISO 27001 certification effort at a Terraform-first AWS startup required turning infrastructure, access control, encryption, monitoring, and vulnerability management into code so audit evidence could be generated directly from Git and production systems. Compliance shifted from documentation to embedded engineering practices, with Security Hub metrics and automated pipelines used as measurable proof of control effectiveness.

How ACR Artifact Cache Handles Multi-Arch Images: What Gets Cached and When Webhooks Fire (9 minute read) Azure Container Registry Artifact Cache stores the full manifest list but only the requested architecture manifest, triggering asynchronous copy where subsequent pulls stop proxying to upstream once complete. A single-platform multi-arch pull emits three push webhooks, and the completion push event indicates local caching and storage charge initiation.

The Silent Failure of Reliability Metrics at Scale: Lessons Learned from a Decade of Broken Metrics (8 minute read) Reliability metrics and SLIs gradually lose accuracy as systems evolve, with broadened scopes and shifting semantics causing green dashboards to mask real issues. Improving fidelity requires bounded instrumentation, explicit metrics, and strong correlation to prevent misleading operational confidence.

AI agent at the wheel: How an attacker used LLMs to move from a CVE to an internal database in 4 pivots (7 minute read) The Sysdig Threat Research Team observed what appears to be the first documented AI agent-driven cyberattack on May 10, where an attacker exploited a marimo notebook vulnerability (CVE-2026-39987) and used a large language model to autonomously navigate from initial access through AWS credentials to exfiltrating an entire PostgreSQL database in under two minutes. Four key signatures pointed to real-time AI composition rather than pre-scripted automation: the agent dumped a non-existent "credential" table based on schema assumptions, left a Chinese-language internal monologue comment mid-attack, used distinctively AI-formatted commands with separators and bounded captures, and dynamically chained outputs from one command as inputs to the next—all while spreading requests across multiple Cloudflare Workers IPs to evade detection.

Slack AI: The Path to Multi-Cloud (8 minute read) Slack evolved its AI infrastructure through four phases over three years, migrating from AWS SageMaker to Bedrock and eventually to a multi-cloud architecture spanning AWS and Google Cloud Platform by early 2026 to access best-in-class models while maintaining enterprise security and avoiding vendor lock-in.

Monitor Azure Managed Redis with Datadog (4 minute read) Datadog's Azure Managed Redis integration gives teams agentless visibility into Redis cache activity, efficiency, resource pressure, latency, and availability through automatic metrics, dashboards, and recommended monitors.

Legacy Image Provider to Cloudflare Images: Traffic Estimation and Safe Rollout (5 minute read) Migration to Cloudflare Images preserved legacy URLs by running dual paths and using Cloudflare edge origin overrides with S3 host-header HTTPS while validating image quality, compression, and egress cost, and executing a canary rollout with prefix purging and traffic ramp.

### Fetched Web Text
Workload automation shouldn't need its own infrastructure team (Sponsor) Redwood is a Gartner SOAP Leader for two years running - and  RunMyJobs  by Redwood is why. ✅ Agentless - no agents, VMs, or databases to deploy or maintain ✅ 99.95% uptime SLA - we manage the infrastructure, you just use it ✅ Trusted by 50% of the Fortune 50 With RunMyJobs, you can: >> Orchestrate applications, data and infrastructure across cloud, on-prem and hybrid - with 83+ native connectors, no agents required >> Build automations faster with  AI embedded across the automation lifecycle  - scripts, documentation, and workflows >> Stay ahead of failures with predictive SLA monitoring and advanced observability Get a demo today and eliminate infrastructure overhead

Introducing the next generation of AWS Resilience Hub for generative AI-based SRE resilience journey (4 minute read) AWS has launched the next generation of Resilience Hub, introducing an organization-wide system that helps Site Reliability Engineers set consistent resilience goals across hundreds of applications using AI-powered failure mode analysis, dependency discovery, and modular policies with targets like 99.95% availability SLOs. The service is now generally available in AWS commercial regions with a new service-based pricing model that includes two free failure mode assessments per month, and it integrates with AWS Organizations to let teams evaluate resilience from a single delegated administrator account.

Announcing Rust 1.96.0 (3 minute read) Rust 1.96.0 stabilizes new core::range types that implement IntoIterator instead of Iterator, allowing range values to be Copy and making them easier to store inside lightweight structs like spans and slice accessors. The release also adds assert_matches! and debug_assert_matches! for pattern-based assertions with better failure output, tightens WebAssembly linking by treating undefined symbols as errors by default, and fixes two Cargo vulnerabilities affecting third-party registries while leaving crates.io users unaffected.

ISO 27001 on AWS: Building Compliance Into the Architecture (7 minute read) An ISO 27001 certification effort at a Terraform-first AWS startup required turning infrastructure, access control, encryption, monitoring, and vulnerability management into code so audit evidence could be generated directly from Git and production systems. Compliance shifted from documentation to embedded engineering practices, with Security Hub metrics and automated pipelines used as measurable proof of control effectiveness.

How ACR Artifact Cache Handles Multi-Arch Images: What Gets Cached and When Webhooks Fire (9 minute read) Azure Container Registry Artifact Cache stores the full manifest list but only the requested architecture manifest, triggering asynchronous copy where subsequent pulls stop proxying to upstream once complete. A single-platform multi-arch pull emits three push webhooks, and the completion push event indicates local caching and storage charge initiation.

The Silent Failure of Reliability Metrics at Scale: Lessons Learned from a Decade of Broken Metrics (8 minute read) Reliability metrics and SLIs gradually lose accuracy as systems evolve, with broadened scopes and shifting semantics causing green dashboards to mask real issues. Improving fidelity requires bounded instrumentation, explicit metrics, and strong correlation to prevent misleading operational confidence.

AI agent at the wheel: How an attacker used LLMs to move from a CVE to an internal database in 4 pivots (7 minute read) The Sysdig Threat Research Team observed what appears to be the first documented AI agent-driven cyberattack on May 10, where an attacker exploited a marimo notebook vulnerability (CVE-2026-39987) and used a large language model to autonomously navigate from initial access through AWS credentials to exfiltrating an entire PostgreSQL database in under two minutes. Four key signatures pointed to real-time AI composition rather than pre-scripted automation: the agent dumped a non-existent "credential" table based on schema assumptions, left a Chinese-language internal monologue comment mid-attack, used distinctively AI-formatted commands with separators and bounded captures, and dynamically chained outputs from one command as inputs to the next—all while spreading requests across multiple Cloudflare Workers IPs to evade detection.

Slack AI: The Path to Multi-Cloud (8 minute read) Slack evolved its AI infrastructure through four phases over three years, migrating from AWS SageMaker to Bedrock and eventually to a multi-cloud architecture spanning AWS and Google Cloud Platform by early 2026 to access best-in-class models while maintaining enterprise security and avoiding vendor lock-in.

Monitor Azure Managed Redis with Datadog (4 minute read) Datadog's Azure Managed Redis integration gives teams agentless visibility into Redis cache activity, efficiency, resource pressure, latency, and availability through automatic metrics, dashboards, and recommended monitors.

Legacy Image Provider to Cloudflare Images: Traffic Estimation and Safe Rollout (5 minute read) Migration to Cloudflare Images preserved legacy URLs by running dual paths and using Cloudflare edge origin overrides with S3 host-header HTTPS while validating image quality, compression, and egress cost, and executing a canary rollout with prefix purging and traffic ramp.

### Source URL
https://tldr.tech/devops/2026-05-29
