---
actionability: high
attached_experts: []
channel_name: ''
created_at: '2026-06-05T08:51:51.526749+10:00'
domain: unknown
expert_status: unattached
primary_mode: router
privacy: public
review_status: new
secondary_modes: []
source_type: article
source_url: https://tldr.tech/devops/2026-06-03
status: processed
suggested_experts: []
tags: []
title: GPT-5.5 on Bedrock ☁️, Agent Security 🥷, LLM Cost Routing ⚡
transcript_path: ''
type: insight_note
updated_at: '2026-06-05T08:51:51.526749+10:00'
---

# GPT-5.5 on Bedrock ☁️, Agent Security 🥷, LLM Cost Routing ⚡

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
https://tldr.tech/devops/2026-06-03

Get started with OpenAI GPT-5.5, GPT-5.4 models, and Codex on Amazon Bedrock (3 minute read) Amazon Web Services launched OpenAI's GPT-5.5 and GPT-5.4 models, along with the Codex coding agent, on its Bedrock platform, offering pay-per-token pricing without per-developer seat licenses. GPT-5.5 is available in US East (Ohio) for demanding workloads while GPT-5.4 is available in two US regions for better price-performance, with Codex—used by over 4 million developers weekly—integrated into popular IDEs like VS Code and JetBrains.

DigitalOcean Serverless Inference: A Deep Dive (9 minute read) DigitalOcean launched Serverless Inference, a fully managed API platform offering access to over 30 foundation models across text, code, vision, image, video, and speech generation through a single API key with pay-per-token pricing and no minimum commitments. The OpenAI-compatible service includes advanced features like an Inference Router for automatic multi-model selection, prompt caching, built-in tools for knowledge retrieval and web search, and integrates directly with DigitalOcean's existing infrastructure including databases, object storage, and VPCs under unified billing.

Building an Enterprise-Grade SQL Platform on Kubernetes using Crossplane and Azure PostgreSQL (7 minute read) A Kubernetes-native enterprise SQL platform uses Crossplane to provision and manage Azure PostgreSQL Flexible Server with declarative APIs, implementing multi-region active–passive architecture with private networking, DNS abstraction, and automated infrastructure composition. It enables HA via zone-redundant primary deployment and DR via cross-region asynchronous replicas with manual promotion while maintaining security through private endpoints and Azure AD authentication.

The Inference Tax: How Prefix-Aware Routing Eliminates the Hidden Cost of LLMs at Scale (13 minute read) DigitalOcean partnered with Inferact to slash AI inference costs by up to 4x through prefix-aware routing and caching in vLLM, recovering up to 340 GPU-hours daily at 10 million requests by eliminating redundant computation of shared prompt prefixes. The optimization, built for DigitalOcean's Dedicated Inference platform, will roll out to all Serverless Inference customers in the coming weeks, leveraging AMD Instinct MI325X GPUs' 192GB HBM3 and NVIDIA H200's 141GB HBM3e to maintain substantially larger KV cache capacity and boost cache hit rates from ~25% to 75%+.

How we reduced core unit boot time from hours to minutes (8 minute read) Cloudflare slashed server boot times from four hours down to three minutes across nearly 2,000 core servers after a routine firmware update caused machines to waste roughly 20 minutes probing each failed network boot interface before finding the correct one. The fix involved reprogramming the boot sequence to declare the correct network interface upfront, though implementation required workarounds for lazy-loaded UEFI data structures, vendor-specific naming inconsistencies, and immutable firmware settings that initially blocked configuration changes.

Reliability Engineering for Air-Gapped Systems (5 minute read) SLIs and SLOs in air-gapped, high-security systems require shifting observability to on-prem operators through dashboards, alerts, runbooks, and status pages, since developers lack runtime access. Reliability is achieved via structured self-service tooling, error codification, and ownership transfer to reduce detection and resolution time under strict isolation constraints.

Prompt → Secure Infrastructure: The Claude Code DevSecOps Shift on AWS (10 minute read) Claude Code Security and Agent Teams are positioned as a continuous AWS-aware security layer for Terraform environments, using multi-agent parallel audits, IaC graph reasoning, and AWS MCP integration to detect IAM, network, and secrets drift before production. The workflow emphasizes PR-based auto-fixes, cross-region audits, and scheduled compliance checks to replace slow manual security reviews with ongoing automated enforcement.

Coding Agent Horror Stories: The rm -rf ~/ Incident (11 minute read) A Reddit user's entire Mac home directory was wiped out in December 2025 when Claude Code executed a cleanup command that included a trailing "~/".

Malicious Checkmarx Artifacts Found in Official KICS Docker Repository and Code Extensions (11 minute read) Attackers compromised Checkmarx KICS Docker images and VS Code extensions, replacing tags with trojanized binaries and mcpAddon.js that exfiltrated cloud, GitHub, and developer credentials via GitHub repos, Actions workflows, and npm republishing, indicating a multi-stage supply chain attack.

The On-Call Problem AI Can Actually Solve (3 minute read) The on-call 3 AM challenge is fundamentally a knowledge management problem, where engineers often lack sufficient system context due to remote work and incomplete exposure.

### Fetched Web Text
Get started with OpenAI GPT-5.5, GPT-5.4 models, and Codex on Amazon Bedrock (3 minute read) Amazon Web Services launched OpenAI's GPT-5.5 and GPT-5.4 models, along with the Codex coding agent, on its Bedrock platform, offering pay-per-token pricing without per-developer seat licenses. GPT-5.5 is available in US East (Ohio) for demanding workloads while GPT-5.4 is available in two US regions for better price-performance, with Codex—used by over 4 million developers weekly—integrated into popular IDEs like VS Code and JetBrains.

DigitalOcean Serverless Inference: A Deep Dive (9 minute read) DigitalOcean launched Serverless Inference, a fully managed API platform offering access to over 30 foundation models across text, code, vision, image, video, and speech generation through a single API key with pay-per-token pricing and no minimum commitments. The OpenAI-compatible service includes advanced features like an Inference Router for automatic multi-model selection, prompt caching, built-in tools for knowledge retrieval and web search, and integrates directly with DigitalOcean's existing infrastructure including databases, object storage, and VPCs under unified billing.

Building an Enterprise-Grade SQL Platform on Kubernetes using Crossplane and Azure PostgreSQL (7 minute read) A Kubernetes-native enterprise SQL platform uses Crossplane to provision and manage Azure PostgreSQL Flexible Server with declarative APIs, implementing multi-region active–passive architecture with private networking, DNS abstraction, and automated infrastructure composition. It enables HA via zone-redundant primary deployment and DR via cross-region asynchronous replicas with manual promotion while maintaining security through private endpoints and Azure AD authentication.

The Inference Tax: How Prefix-Aware Routing Eliminates the Hidden Cost of LLMs at Scale (13 minute read) DigitalOcean partnered with Inferact to slash AI inference costs by up to 4x through prefix-aware routing and caching in vLLM, recovering up to 340 GPU-hours daily at 10 million requests by eliminating redundant computation of shared prompt prefixes. The optimization, built for DigitalOcean's Dedicated Inference platform, will roll out to all Serverless Inference customers in the coming weeks, leveraging AMD Instinct MI325X GPUs' 192GB HBM3 and NVIDIA H200's 141GB HBM3e to maintain substantially larger KV cache capacity and boost cache hit rates from ~25% to 75%+.

How we reduced core unit boot time from hours to minutes (8 minute read) Cloudflare slashed server boot times from four hours down to three minutes across nearly 2,000 core servers after a routine firmware update caused machines to waste roughly 20 minutes probing each failed network boot interface before finding the correct one. The fix involved reprogramming the boot sequence to declare the correct network interface upfront, though implementation required workarounds for lazy-loaded UEFI data structures, vendor-specific naming inconsistencies, and immutable firmware settings that initially blocked configuration changes.

Reliability Engineering for Air-Gapped Systems (5 minute read) SLIs and SLOs in air-gapped, high-security systems require shifting observability to on-prem operators through dashboards, alerts, runbooks, and status pages, since developers lack runtime access. Reliability is achieved via structured self-service tooling, error codification, and ownership transfer to reduce detection and resolution time under strict isolation constraints.

Prompt → Secure Infrastructure: The Claude Code DevSecOps Shift on AWS (10 minute read) Claude Code Security and Agent Teams are positioned as a continuous AWS-aware security layer for Terraform environments, using multi-agent parallel audits, IaC graph reasoning, and AWS MCP integration to detect IAM, network, and secrets drift before production. The workflow emphasizes PR-based auto-fixes, cross-region audits, and scheduled compliance checks to replace slow manual security reviews with ongoing automated enforcement.

Coding Agent Horror Stories: The rm -rf ~/ Incident (11 minute read) A Reddit user's entire Mac home directory was wiped out in December 2025 when Claude Code executed a cleanup command that included a trailing "~/".

Malicious Checkmarx Artifacts Found in Official KICS Docker Repository and Code Extensions (11 minute read) Attackers compromised Checkmarx KICS Docker images and VS Code extensions, replacing tags with trojanized binaries and mcpAddon.js that exfiltrated cloud, GitHub, and developer credentials via GitHub repos, Actions workflows, and npm republishing, indicating a multi-stage supply chain attack.

The On-Call Problem AI Can Actually Solve (3 minute read) The on-call 3 AM challenge is fundamentally a knowledge management problem, where engineers often lack sufficient system context due to remote work and incomplete exposure.

### Source URL
https://tldr.tech/devops/2026-06-03
