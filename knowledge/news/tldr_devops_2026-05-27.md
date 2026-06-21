# TLDR DevOps — 2026-05-27

Source: https://tldr.tech/devops/2026-05-27

Build to ship with NVIDIA at Microsoft Build, online & on-site (Sponsor) Unlock developer-first, hands-on experiences with NVIDIA agentic solutions on Azure at Microsoft Build, happening in San Francisco and online June 2–3. From hands-on labs and demos to speaking sessions and interactive events, Microsoft Build offers developers a unique opportunity to go deep on real code, real systems, and real workflows. Virtual passes are still available—sign up now.

Introducing Nova, Dropbox's internal platform for coding agents (7 minute read) Nova is an internal cloud platform within Dropbox for running coding agents across its engineering workflows. It lets engineers run multiple coding sessions in parallel, execute agents inside isolated environments pinned to specific repository commits, validate proposed changes with Bazel-backed build and test commands, and continue sessions when validation fails.

Staged publishing and new install-time controls for npm (2 minute read) GitHub introduced staged publishing and install-time controls for npm packages, giving maintainers safer ways to roll out package releases and giving consumers more control over what gets installed. The changes are a direct response to the growing risk of compromised packages and maintainer accounts, making npm supply-chain defense more operational instead of relying only on fast takedowns after a bad release spreads.

Agent Memory: An Anatomy (9 minute read) Agent memory systems are better understood as a pipeline of extraction, storage, and retrieval rather than a single magical “memory” feature. Agent libraries compress conversations into facts, store them in vectors/tables/graphs, retrieve them later, and struggle with contradictions, stale context, procedural memory, and future intentions.

Migrating Azure DevOps to GitHub Enterprise: The ROI Case (7 minute read) Delaying migration from Azure DevOps to GitHub Enterprise creates a compounding productivity gap due to Copilot agents and autonomous workflows, while costs include pipelines, work items, and RBAC redesign but can be mitigated via a hybrid strategy and phased adoption.

CI/CD security: How to secure your GitHub ecosystem (9 minute read) Applying threat modeling to GitHub environments highlights risks like unauthorized access, malicious CI code execution, and data exfiltration, while historical supply chain attacks demonstrate the need for detection tools, dependency scanning, and monitoring to secure CI CD workflows and prevent compromise.

Project Glasswing: what Mythos showed us (9 minute read) Anthropic's Project Glasswing gives select organizations access to Claude Mythos Preview, a restricted cybersecurity model designed to find and help fix vulnerabilities in critical software. Cloudflare's analysis of Mythos highlights how AI security agents can chain low-severity issues into more serious exploits, generate proof-of-concept code, and change the economics of vulnerability discovery.

5 Incident Response Principles for CTOs (5 minute read) Operational resilience requires accepting incidents as inevitable, building systems and observability for fast detection and recovery, and pairing technical design with prepared teams operating in psychologically safe, blameless cultures. Mature organizations focus on learning from incidents and leadership that reinforces continuous improvement.

AWS Control Tower Proactive Controls for Terraform: A Proof of Concept (16 minute read) AWS Control Tower proactive controls are CloudFormation Hooks that evaluate resources at creation time via the Cloud Control API, but they are not natively compatible with Terraform workflows. An experiment explores whether Terraform's Cloud Control provider can trigger these controls to bridge the gap.

Terraform Your AWS AgentCore (6 minute read) An AWS Bedrock AgentCore deployment built with Terraform demonstrates how to orchestrate multiple agent runtimes, gateways, IAM roles, memory, and policy enforcement in a single dependency graph, while working around current provider gaps using CLI-driven null_resource workarounds.

5 Ways to Run Your Containerized App on AWS in 2026 (3 minute read) AWS now offers five primary ways to run containers.