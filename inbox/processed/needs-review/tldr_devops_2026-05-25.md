---
actionability: high
attached_experts: []
channel_name: ''
created_at: '2026-06-05T08:52:54.812077+10:00'
domain: unknown
expert_status: unattached
primary_mode: router
privacy: public
review_status: new
secondary_modes: []
source_type: article
source_url: https://tldr.tech/devops/2026-05-25
status: processed
suggested_experts: []
tags: []
title: Pulumi Do ☁️, VS Code Attack 🥷, Go to Rust 🦀
transcript_path: ''
type: insight_note
updated_at: '2026-06-05T08:52:54.812077+10:00'
---

# Pulumi Do ☁️, VS Code Attack 🥷, Go to Rust 🦀

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
https://tldr.tech/devops/2026-05-25

How do software leaders ship? With CI that turns scale into speed, reliably. (Sponsor) Buildkite  has run CI for OpenAI, Airbnb, Canva, Uber and Shopify for 7-12 yrs as they grew. Now we also orchestrate for Cursor, Anthropic, Meta, Mistral, xAI, Discord, Reddit, Ramp, Boston Dynamics, Applied Intuition, ASML, Planetscale, Pierre and Bun... ...and the workloads that build vLLM, Bazel and Backstage. Quietly powering software used by 1B+ people daily, since 2013. Parallelize, fan-out and orchestrate at depths a slightly faster runner won't reach as agentic codegen blows up your build queue. Start with our all-access 30-day trial.  Get building →

Introducing Pulumi Do: Direct Resource Operations for Any Cloud (6 minute read) 'pulumi do' is a new command-line tool that lets developers create, read, update, delete, and query cloud resources across thousands of providers with a single terminal command—no project setup, code, or state tracking required. The tool is designed for both humans and AI agents to handle quick, one-off cloud operations, with future plans to integrate credential management through Pulumi ESC and provide an upgrade path to full infrastructure-as-code projects.

GitHub internal repositories exfiltrated via malicious VS Code extension (5 minute read) GitHub confirmed that roughly 3,800 internal repositories were accessed after a developer installed a malicious Visual Studio Code extension, highlighting the growing risk of compromised developer tooling in the software supply chain. GitHub says there is no evidence customer repositories were affected, but the incident reinforces the need for extension governance, credential rotation, endpoint monitoring, and tighter controls around tools that can access source code, terminals, and local secrets.

Request-Based Autoscaling Is Now Generally Available on App Platform (4 minute read) DigitalOcean launched request-based autoscaling for its App Platform, allowing applications to scale automatically based on real-time HTTP traffic metrics like requests per second and P95 response latency rather than waiting for CPU utilization to spike. The feature now works on both shared and dedicated CPU instances, expanding autoscaling capabilities to users who were previously limited to manual scaling on shared plans.

Designing end-to-end ingress request tracing for multi-tenant SaaS platforms (7 minute read) The Cloud Native Computing Foundation published a framework for implementing distributed tracing in multi-tenant SaaS platforms that uses trace IDs to follow customer requests across microservices and span IDs to track individual operations, preventing the common problem where disconnected logs make it nearly impossible to diagnose failures that touch multiple services. The framework emphasizes treating tracing as a core platform capability rather than optional tooling, with specific guardrails like excluding sensitive data by design and ensuring trace failures never block actual customer requests.

Migrating from Go to Rust (26 minute read) Go teams considering Rust need to weigh stronger compile-time guarantees against a steeper learning curve and more explicit ownership model. Rust shifts more correctness checks into the type system, offering stronger null safety, error handling, memory safety, and concurrency guarantees while preserving strong performance and deployment ergonomics. Common Go patterns are mapped to Rust equivalents, with an emphasis on incremental backend migration instead of risky full rewrites.

Add dynamically updating context to logs with Reference Tables and Observability Pipelines (7 minute read) Datadog Observability Pipelines enables centralized log enrichment using dynamic Reference Tables to add real time context, improve threat investigations, and route data efficiently, reducing manual correlation, latency, and costs across security and logging workflows.

Mitigate credential exposure in Windows environments with Boundary and Vault (8 minute read) Organizations face Windows remote access risks from static credentials and broad VPN based network access. Boundary and Vault provide identity based RDP with short lived dynamic AD credentials and credential injection, plus a Terraform based AWS proof of concept setup.

Deploying to Multiple Azure Subscriptions with Terraform Provider Aliases (5 minute read) Using Terraform with provider aliases enables one project to deploy to multiple Microsoft Azure subscriptions by defining multiple azurerm provider instances with different subscription IDs, pinning resources via a provider, managing everything in a single state.

[Live panel] Build vs. buy: mobile release tooling (Sponsor) How mobile engineers handle release processes ranges from in-house scripts to bespoke platforms. Hear how leaders from Monzo, Spotify, Etsy, and Tuist decided to build or buy May 28, 1pm ET.  Save your spot .

Is your SIEM actually ready? A new way to find out (7 minute read) SIEM Readiness introduces a centralized, environment-aware view of SIEM operational health by evaluating log coverage, data quality, pipeline continuity, and retention across key telemetry domains, helping teams identify gaps, validate detection readiness, and ensure data is available for security investigations and compliance.

Accelerating LLM Inference with Prompt Caching for Open‑Source Models on Databricks (2 minute read) Databricks rolled out automatic prompt caching for open-source LLMs including Llama, Mistral, and DBRX models, reducing redundant processing of repeated prompts to cut costs and latency without requiring any customer configuration.

### Fetched Web Text
How do software leaders ship? With CI that turns scale into speed, reliably. (Sponsor) Buildkite  has run CI for OpenAI, Airbnb, Canva, Uber and Shopify for 7-12 yrs as they grew. Now we also orchestrate for Cursor, Anthropic, Meta, Mistral, xAI, Discord, Reddit, Ramp, Boston Dynamics, Applied Intuition, ASML, Planetscale, Pierre and Bun... ...and the workloads that build vLLM, Bazel and Backstage. Quietly powering software used by 1B+ people daily, since 2013. Parallelize, fan-out and orchestrate at depths a slightly faster runner won't reach as agentic codegen blows up your build queue. Start with our all-access 30-day trial.  Get building →

Introducing Pulumi Do: Direct Resource Operations for Any Cloud (6 minute read) 'pulumi do' is a new command-line tool that lets developers create, read, update, delete, and query cloud resources across thousands of providers with a single terminal command—no project setup, code, or state tracking required. The tool is designed for both humans and AI agents to handle quick, one-off cloud operations, with future plans to integrate credential management through Pulumi ESC and provide an upgrade path to full infrastructure-as-code projects.

GitHub internal repositories exfiltrated via malicious VS Code extension (5 minute read) GitHub confirmed that roughly 3,800 internal repositories were accessed after a developer installed a malicious Visual Studio Code extension, highlighting the growing risk of compromised developer tooling in the software supply chain. GitHub says there is no evidence customer repositories were affected, but the incident reinforces the need for extension governance, credential rotation, endpoint monitoring, and tighter controls around tools that can access source code, terminals, and local secrets.

Request-Based Autoscaling Is Now Generally Available on App Platform (4 minute read) DigitalOcean launched request-based autoscaling for its App Platform, allowing applications to scale automatically based on real-time HTTP traffic metrics like requests per second and P95 response latency rather than waiting for CPU utilization to spike. The feature now works on both shared and dedicated CPU instances, expanding autoscaling capabilities to users who were previously limited to manual scaling on shared plans.

Designing end-to-end ingress request tracing for multi-tenant SaaS platforms (7 minute read) The Cloud Native Computing Foundation published a framework for implementing distributed tracing in multi-tenant SaaS platforms that uses trace IDs to follow customer requests across microservices and span IDs to track individual operations, preventing the common problem where disconnected logs make it nearly impossible to diagnose failures that touch multiple services. The framework emphasizes treating tracing as a core platform capability rather than optional tooling, with specific guardrails like excluding sensitive data by design and ensuring trace failures never block actual customer requests.

Migrating from Go to Rust (26 minute read) Go teams considering Rust need to weigh stronger compile-time guarantees against a steeper learning curve and more explicit ownership model. Rust shifts more correctness checks into the type system, offering stronger null safety, error handling, memory safety, and concurrency guarantees while preserving strong performance and deployment ergonomics. Common Go patterns are mapped to Rust equivalents, with an emphasis on incremental backend migration instead of risky full rewrites.

Add dynamically updating context to logs with Reference Tables and Observability Pipelines (7 minute read) Datadog Observability Pipelines enables centralized log enrichment using dynamic Reference Tables to add real time context, improve threat investigations, and route data efficiently, reducing manual correlation, latency, and costs across security and logging workflows.

Mitigate credential exposure in Windows environments with Boundary and Vault (8 minute read) Organizations face Windows remote access risks from static credentials and broad VPN based network access. Boundary and Vault provide identity based RDP with short lived dynamic AD credentials and credential injection, plus a Terraform based AWS proof of concept setup.

Deploying to Multiple Azure Subscriptions with Terraform Provider Aliases (5 minute read) Using Terraform with provider aliases enables one project to deploy to multiple Microsoft Azure subscriptions by defining multiple azurerm provider instances with different subscription IDs, pinning resources via a provider, managing everything in a single state.

[Live panel] Build vs. buy: mobile release tooling (Sponsor) How mobile engineers handle release processes ranges from in-house scripts to bespoke platforms. Hear how leaders from Monzo, Spotify, Etsy, and Tuist decided to build or buy May 28, 1pm ET.  Save your spot .

Is your SIEM actually ready? A new way to find out (7 minute read) SIEM Readiness introduces a centralized, environment-aware view of SIEM operational health by evaluating log coverage, data quality, pipeline continuity, and retention across key telemetry domains, helping teams identify gaps, validate detection readiness, and ensure data is available for security investigations and compliance.

Accelerating LLM Inference with Prompt Caching for Open‑Source Models on Databricks (2 minute read) Databricks rolled out automatic prompt caching for open-source LLMs including Llama, Mistral, and DBRX models, reducing redundant processing of repeated prompts to cut costs and latency without requiring any customer configuration.

### Source URL
https://tldr.tech/devops/2026-05-25
