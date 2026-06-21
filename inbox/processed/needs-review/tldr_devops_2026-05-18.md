---
actionability: high
attached_experts: []
channel_name: ''
created_at: '2026-06-05T08:53:48.570252+10:00'
domain: unknown
expert_status: unattached
primary_mode: router
privacy: public
review_status: new
secondary_modes: []
source_type: article
source_url: https://tldr.tech/devops/2026-05-18
status: processed
suggested_experts: []
tags: []
title: Bun’s Rust Rewrite 🦀, Remote Cache CDC 📦, AWS Security Agent 🥷
transcript_path: ''
type: insight_note
updated_at: '2026-06-05T08:53:48.570252+10:00'
---

# Bun’s Rust Rewrite 🦀, Remote Cache CDC 📦, AWS Security Agent 🥷

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
https://tldr.tech/devops/2026-05-18

Why dev teams outgrow their first CI (Sponsor) Most engineering teams start on GitHub Actions or Jenkins. Then the monorepo gets real, agents 5-10-50x the commit volume... and a flaky test sparks a Friday-afternoon outage. Shopify, Pinterest, Block, Airbnb, OpenAI and Canva all run their CI on Buildkite. We're built for the teams that need control over what runs where. Try the lot for 30 days, zero commitment, no credit card. There's a real engineer named Ola on standby if you get stuck. See what's included →

incident.io launches PagerDuty Rescue Program (7 minute read) incident.io launched a PagerDuty Rescue Program offering contract buyouts, AI-assisted migrations, and a 99.99% uptime SLA to help companies replace PagerDuty with its AI-driven incident management platform.

Amazon Bedrock introduces new advanced prompt optimization and migration tool (3 minute read) AWS Bedrock Advanced Prompt Optimization is a new tool that lets developers optimize and compare prompts across up to 5 models simultaneously using a metric-driven feedback loop with support for multimodal inputs, including images and PDFs. The service is now available in 14 regions worldwide. It charges users based on standard Bedrock model-inference token rates consumed during the optimization process.

Gradual deployments in Amazon ECS with linear and canary strategies (5 minute read) Amazon ECS now supports linear and canary deployment strategies using weighted target groups, CloudWatch alarms, and deployment circuit breakers to enable gradual traffic shifting with automated rollback on failures. Linear deployments shift traffic in fixed increments with bake times, while canary deployments test small traffic slices first, improving deployment safety, observability, and control across microservices.

Cloud native application challenges: installing the walking skeleton (6 minute read) Managing Kubernetes at scale creates YAML configuration sprawl, cluster drift, and compliance challenges across multicloud environments. GitOps centralizes declarative configurations in Git repositories, enabling automated reconciliation, policy enforcement, and consistent cluster management without manual intervention.

My Thoughts on Bun's Rust Rewrite (5 minute read) Bun's Rust rewrite may reduce memory-safety issues, but the bigger concern is maintainability: a large AI-generated port with little human review can pass tests while still hiding untested invariants, edge cases, and future debugging traps. This is not a simple “Zig failed, Rust wins” story, but a bet on whether AI-translated, insufficiently understood production code can be safely maintained over time.

Remote Cache CDC: Reusing Bytes (15 minute read) BuildBuddy is using content-defined chunking in its remote cache so large build outputs can reuse unchanged byte chunks instead of re-uploading or re-downloading entire files after small code changes. Early results show major savings for Bazel builds—about 40% less uploaded data in a benchmark and hundreds of TiB of duplicate chunk uploads skipped in production—with support available via Bazel's experimental remote cache chunking flag.

Create Custom MCP Catalogs and Profiles (8 minute read) Docker's Custom Catalogs and Profiles for managing Model Context Protocol (MCP) servers allows organizations to curate approved collections of AI tools and distribute them as portable OCI artifacts while enabling developers to create reusable, named configurations of MCP servers for different workflows. The feature, available in Docker Desktop 4.56 and 4.63, lets teams push catalogs to container registries like Docker Hub and share server setups across projects without vendor lock-in.

AWS Security Agent now supports full repository code reviews (2 minute read) AWS launched full repository code review for AWS Security Agent, enabling AI-driven analysis of entire codebases to detect architectural and data flow vulnerabilities that traditional static analysis tools often miss.

Kubernetes v1.36: New Metric for Route Sync in the Cloud Controller Manager (2 minute read) Kubernetes v1.36 added a new alpha metric called `route_controller_route_sync_total` to help operators measure the impact of the watch-based route reconciliation feature introduced in v1.35.

### Fetched Web Text
Why dev teams outgrow their first CI (Sponsor) Most engineering teams start on GitHub Actions or Jenkins. Then the monorepo gets real, agents 5-10-50x the commit volume... and a flaky test sparks a Friday-afternoon outage. Shopify, Pinterest, Block, Airbnb, OpenAI and Canva all run their CI on Buildkite. We're built for the teams that need control over what runs where. Try the lot for 30 days, zero commitment, no credit card. There's a real engineer named Ola on standby if you get stuck. See what's included →

incident.io launches PagerDuty Rescue Program (7 minute read) incident.io launched a PagerDuty Rescue Program offering contract buyouts, AI-assisted migrations, and a 99.99% uptime SLA to help companies replace PagerDuty with its AI-driven incident management platform.

Amazon Bedrock introduces new advanced prompt optimization and migration tool (3 minute read) AWS Bedrock Advanced Prompt Optimization is a new tool that lets developers optimize and compare prompts across up to 5 models simultaneously using a metric-driven feedback loop with support for multimodal inputs, including images and PDFs. The service is now available in 14 regions worldwide. It charges users based on standard Bedrock model-inference token rates consumed during the optimization process.

Gradual deployments in Amazon ECS with linear and canary strategies (5 minute read) Amazon ECS now supports linear and canary deployment strategies using weighted target groups, CloudWatch alarms, and deployment circuit breakers to enable gradual traffic shifting with automated rollback on failures. Linear deployments shift traffic in fixed increments with bake times, while canary deployments test small traffic slices first, improving deployment safety, observability, and control across microservices.

Cloud native application challenges: installing the walking skeleton (6 minute read) Managing Kubernetes at scale creates YAML configuration sprawl, cluster drift, and compliance challenges across multicloud environments. GitOps centralizes declarative configurations in Git repositories, enabling automated reconciliation, policy enforcement, and consistent cluster management without manual intervention.

My Thoughts on Bun's Rust Rewrite (5 minute read) Bun's Rust rewrite may reduce memory-safety issues, but the bigger concern is maintainability: a large AI-generated port with little human review can pass tests while still hiding untested invariants, edge cases, and future debugging traps. This is not a simple “Zig failed, Rust wins” story, but a bet on whether AI-translated, insufficiently understood production code can be safely maintained over time.

Remote Cache CDC: Reusing Bytes (15 minute read) BuildBuddy is using content-defined chunking in its remote cache so large build outputs can reuse unchanged byte chunks instead of re-uploading or re-downloading entire files after small code changes. Early results show major savings for Bazel builds—about 40% less uploaded data in a benchmark and hundreds of TiB of duplicate chunk uploads skipped in production—with support available via Bazel's experimental remote cache chunking flag.

Create Custom MCP Catalogs and Profiles (8 minute read) Docker's Custom Catalogs and Profiles for managing Model Context Protocol (MCP) servers allows organizations to curate approved collections of AI tools and distribute them as portable OCI artifacts while enabling developers to create reusable, named configurations of MCP servers for different workflows. The feature, available in Docker Desktop 4.56 and 4.63, lets teams push catalogs to container registries like Docker Hub and share server setups across projects without vendor lock-in.

AWS Security Agent now supports full repository code reviews (2 minute read) AWS launched full repository code review for AWS Security Agent, enabling AI-driven analysis of entire codebases to detect architectural and data flow vulnerabilities that traditional static analysis tools often miss.

Kubernetes v1.36: New Metric for Route Sync in the Cloud Controller Manager (2 minute read) Kubernetes v1.36 added a new alpha metric called `route_controller_route_sync_total` to help operators measure the impact of the watch-based route reconciliation feature introduced in v1.35.

### Source URL
https://tldr.tech/devops/2026-05-18
