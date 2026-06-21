---
actionability: high
attached_experts: []
channel_name: ''
created_at: '2026-06-05T08:48:10.955477+10:00'
domain: unknown
expert_status: unattached
primary_mode: router
privacy: public
review_status: new
secondary_modes: []
source_type: article
source_url: https://tldr.tech/infosec/2026-05-21
status: processed
suggested_experts: []
tags: []
title: GitHub Source Breached 🐙, MS RAMPART AI Toolkit 🪟, Discord Calls Now E2EE 💬
transcript_path: ''
type: insight_note
updated_at: '2026-06-05T08:48:10.955477+10:00'
---

# GitHub Source Breached 🐙, MS RAMPART AI Toolkit 🪟, Discord Calls Now E2EE 💬

## Summary
AI summarization succeeded, but JSON parsing failed.

## AI Raw Output
```text
Final synthesis failed.
```

## Key Ideas
- Refer to the AI Raw Output above.

## Why this matters for Markus
- Refer to the AI Raw Output above.

## Related Modes
- router

## AI Generation Data
- Provider: Unknown
- Model: Unknown

## Next Action
- [ ] Review raw AI output and extract action items manually.

## Source Reliability
AI summarization was performed but parsing failed.

## Original Content
### Raw User Input
https://tldr.tech/infosec/2026-05-21

IT leads are overconfident about AI security. Here are the receipts (Sponsor) Security systems have too many AI blind spots to justify the current level of confidence. In their survey of 2,000 IT decision makers,  Delinea found  that most think they're ready for AI, and yet: Non-human identity visibility is minimal Traditional controls haven't  evolved for LLMs or agents Strategic debt is just as widespread as technical debt Download the free report and get the practical steps you need to  harden identity security for the AI era

Exploit Released for New PinTheft Arch Linux root Escalation Flaw (2 minute read) Researchers from V12 uncovered a new local privilege escalation vulnerability in Linux systems. The vulnerability stems from a double free flaw in the Reliable Datagram System (RDS)'s handling of user pages. The RDS kernel module that is required by the vulnerability is only enabled by default on Arch Linux.

How an image could compromise your Mac: understanding an ExifTool vulnerability (CVE-2026-3102) (7 minute read) GReAT discovered CVE-2026-3102 in ExifTool ≤13.49 on macOS where unsanitized date values in the SetMacOSTags function flow into a system() sink, allowing arbitrary command execution via metadata injection when the -n flag is used with -tagsFromFile to copy a crafted DateTimeOriginal tag into FileCreateDate. Attack chain: inject single quotes into DateTimeOriginal using -n flag (which bypasses PrintConvInv validation), then copy via -tagsFromFile to trigger SetMacOSTags with unescaped $val concatenated into /usr/bin/setfile -d 'PAYLOAD' 'FILE' enabling command substitution. Fix in 13.50 replaced string concatenation with list-form system() calls, eliminating manual escaping. Defenders must verify all photo-processing workflows, asset management tools, and bulk image scripts use ExifTool ≥13.50, isolate untrusted file processing on air-gapped machines, and enforce macOS endpoint protection on BYOD and contractor devices.

GitHub Breached — Employee Device Hack Led to Exfiltration of 3,800+ Internal Repos (4 minute read) TeamPCP claims access to around 3,800 internal GitHub repositories after compromising an employee device with a poisoned VS Code extension, leading GitHub to rotate secrets and investigate scope. The same group trojanized Microsoft's durabletask PyPI package to drop a Linux-only infostealer that steals cloud, vault, SSH, and Kubernetes credentials and propagates across AWS and clusters. LAPSUS$ is now co-selling the leaked internal projects, including Actions, Copilot, CodeQL, and Dependabot components, raising concern over source exposure and supply chain abuse.

Score By Collisions, Patch By Panic (9 minute read) Severity should track how many independent researchers and attackers hit the same bug, with collision counts shrinking patch windows from weeks to hours. Vendors need solo researchers to push for shorter disclosure windows and ship patches, not just reports, while bug hunters move up the stack toward logic bugs and deep system understanding. Corporate teams should lock down egress, recycle infrastructure aggressively, sandbox runtimes, and add automated circuit breakers and feature flags to contain zero-days and keep production running under constant incident pressure.

Tracking TamperedChef Clusters via Certificate and Code Reuse (23 minute read) Unit 42 mapped three TamperedChef (aka EvilAI) clusters distributing trojanized productivity apps (PDF editors, calendars, and ZIP tools) that stay dormant for weeks before pulling second-stage stealers, RATs, or proxy malware, identifying over 4,000 samples across 100 variants by pivoting on code-signing certificate reuse, code overlap, and ad-transparency data. Operators function as advertising and logistics specialists rather than malware experts, registering shell corporations for OV/EV certificates (CL-CRI-1089 burned 34 certs costing $10,000+), running 20,000+ malvertisements, and using LLM-generated distribution sites with visually similar pages but distinct DOM structures. Defenders should deploy updated EDR/XDR and enterprise browsers, harden endpoints against untrusted software installs, hunt for persistence via scheduled tasks and registry Run keys, and revoke tokens plus reset browser-stored credentials on any confirmed infection.

Jackalope (GitHub Repo) Jackalope is a customizable, distributed, coverage-guided fuzzer that works in black-box binaries.

Microsoft Open-Sources RAMPART and Clarity to Secure AI Agents During Development (1 minute read) Microsoft has released two open-source tools for testing AI agent security during development: RAMPART (Risk Assessment and Measurement Platform for Agentic Red Teaming), a Pytest-native framework for writing adversarial and benign safety tests covering harm categories like cross-prompt injection and data exfiltration, and Clarity, a "structured sounding board" that pressure-tests design assumptions before code is written. RAMPART builds on Microsoft's PyRIT and connects to an agent through a single adapter, evaluating test outcomes and reporting results. Where PyRIT targets black-box discovery after a system is built, RAMPART runs during development and Clarity captures design intent, turning red-team findings into reusable engineering assets across the agent lifecycle.

Ocean (Product Launch) Ocean is an email security platform that scans every incoming message with a custom language model, checks sender intent against company context, and flags fraud and impersonation.

London's police asked Big Tech for comms data over 700,000 times last year (4 minute read) London's Met made over 700,000 requests for communications metadata in 2025, including data from Proton services, Signal, MVNO LycaMobile, and gig platforms like Uber and Deliveroo. Proton and Signal dispute claims about data handed over, highlighting reliance on metadata and legal channels. Requests targeting LycaMobile and delivery riders intersect with immigration enforcement and source-identification efforts involving journalists and migrants.

Google publishes exploit code threatening millions of Chromium users (2 minute read) Google accidentally exposed proof-of-concept code for a still-unpatched Browser Fetch API bug that can turn Chromium-based browsers into limited bots for proxying traffic, DDoS, and activity monitoring. Any visited site can trigger a persistent service worker, with behavior particularly stealthy on Edge. Chrome, Edge, Brave, Opera, Vivaldi, and Arc are affected. Firefox and Safari are not.

Microsoft disrupts malware code-signing service used by ransomware gangs (3 minute read) Microsoft disrupted Fox Tempest's malware-signing-as-a-service (MSaaS) operation by seizing signspace[.]cloud, revoking 1,000+ code-signing certificates obtained via stolen identities and abused Azure Artifact Signing subscriptions, and taking offline hundreds of attacker-controlled VMs, with cybercriminals paying $5,000–$9,000 per deployment to bypass SmartScreen warnings and evade detection. Vanilla Tempest and affiliates of INC, Qilin, Akira, and Rhysida used signed fake installers (AnyDesk, Teams, PuTTY, and Webex) distributed through SEO poisoning and malvertising to deploy backdoors, infostealers, and ransomware. The shift reflects cybercrime's modularization: specialized high-friction services like code-signing are now commoditized and sold interchangeably, replacing monolithic attack chains and enabling rapid scaling across ransomware campaigns since at least May 2025.

Anthropic Silently Patches Claude Code Sandbox Bypass (2 minute read) Researcher Aonan Guan found a SOCKS5 null-byte injection flaw in Claude Code's network sandbox that let attackers bypass hostname filtering.

Every Voice and Video Call on Discord Is Now End-to-End Encrypted (4 minute read) Discord has finished migrating all one-to-one, group, channel, and Go Live calls to the DAVE end-to-end encryption protocol.

Grafana breach caused by missed token rotation after TanStack attack (1 minute read) Grafana's breach traces to a single GitHub workflow token missed during incident-response rotation after the Shai-Hulud campaign (attributed to TeamPCP) poisoned dozens of TanStack npm packages with credential-stealing code that Grafana's CI/CD consumed on May 1, letting attackers reach private repositories and steal source code plus business contact data, though Grafana confirms no customer production systems were affected and its codebase was not modified.

### Fetched Web Text
IT leads are overconfident about AI security. Here are the receipts (Sponsor) Security systems have too many AI blind spots to justify the current level of confidence. In their survey of 2,000 IT decision makers,  Delinea found  that most think they're ready for AI, and yet: Non-human identity visibility is minimal Traditional controls haven't  evolved for LLMs or agents Strategic debt is just as widespread as technical debt Download the free report and get the practical steps you need to  harden identity security for the AI era

Exploit Released for New PinTheft Arch Linux root Escalation Flaw (2 minute read) Researchers from V12 uncovered a new local privilege escalation vulnerability in Linux systems. The vulnerability stems from a double free flaw in the Reliable Datagram System (RDS)'s handling of user pages. The RDS kernel module that is required by the vulnerability is only enabled by default on Arch Linux.

How an image could compromise your Mac: understanding an ExifTool vulnerability (CVE-2026-3102) (7 minute read) GReAT discovered CVE-2026-3102 in ExifTool ≤13.49 on macOS where unsanitized date values in the SetMacOSTags function flow into a system() sink, allowing arbitrary command execution via metadata injection when the -n flag is used with -tagsFromFile to copy a crafted DateTimeOriginal tag into FileCreateDate. Attack chain: inject single quotes into DateTimeOriginal using -n flag (which bypasses PrintConvInv validation), then copy via -tagsFromFile to trigger SetMacOSTags with unescaped $val concatenated into /usr/bin/setfile -d 'PAYLOAD' 'FILE' enabling command substitution. Fix in 13.50 replaced string concatenation with list-form system() calls, eliminating manual escaping. Defenders must verify all photo-processing workflows, asset management tools, and bulk image scripts use ExifTool ≥13.50, isolate untrusted file processing on air-gapped machines, and enforce macOS endpoint protection on BYOD and contractor devices.

GitHub Breached — Employee Device Hack Led to Exfiltration of 3,800+ Internal Repos (4 minute read) TeamPCP claims access to around 3,800 internal GitHub repositories after compromising an employee device with a poisoned VS Code extension, leading GitHub to rotate secrets and investigate scope. The same group trojanized Microsoft's durabletask PyPI package to drop a Linux-only infostealer that steals cloud, vault, SSH, and Kubernetes credentials and propagates across AWS and clusters. LAPSUS$ is now co-selling the leaked internal projects, including Actions, Copilot, CodeQL, and Dependabot components, raising concern over source exposure and supply chain abuse.

Score By Collisions, Patch By Panic (9 minute read) Severity should track how many independent researchers and attackers hit the same bug, with collision counts shrinking patch windows from weeks to hours. Vendors need solo researchers to push for shorter disclosure windows and ship patches, not just reports, while bug hunters move up the stack toward logic bugs and deep system understanding. Corporate teams should lock down egress, recycle infrastructure aggressively, sandbox runtimes, and add automated circuit breakers and feature flags to contain zero-days and keep production running under constant incident pressure.

Tracking TamperedChef Clusters via Certificate and Code Reuse (23 minute read) Unit 42 mapped three TamperedChef (aka EvilAI) clusters distributing trojanized productivity apps (PDF editors, calendars, and ZIP tools) that stay dormant for weeks before pulling second-stage stealers, RATs, or proxy malware, identifying over 4,000 samples across 100 variants by pivoting on code-signing certificate reuse, code overlap, and ad-transparency data. Operators function as advertising and logistics specialists rather than malware experts, registering shell corporations for OV/EV certificates (CL-CRI-1089 burned 34 certs costing $10,000+), running 20,000+ malvertisements, and using LLM-generated distribution sites with visually similar pages but distinct DOM structures. Defenders should deploy updated EDR/XDR and enterprise browsers, harden endpoints against untrusted software installs, hunt for persistence via scheduled tasks and registry Run keys, and revoke tokens plus reset browser-stored credentials on any confirmed infection.

Jackalope (GitHub Repo) Jackalope is a customizable, distributed, coverage-guided fuzzer that works in black-box binaries.

Microsoft Open-Sources RAMPART and Clarity to Secure AI Agents During Development (1 minute read) Microsoft has released two open-source tools for testing AI agent security during development: RAMPART (Risk Assessment and Measurement Platform for Agentic Red Teaming), a Pytest-native framework for writing adversarial and benign safety tests covering harm categories like cross-prompt injection and data exfiltration, and Clarity, a "structured sounding board" that pressure-tests design assumptions before code is written. RAMPART builds on Microsoft's PyRIT and connects to an agent through a single adapter, evaluating test outcomes and reporting results. Where PyRIT targets black-box discovery after a system is built, RAMPART runs during development and Clarity captures design intent, turning red-team findings into reusable engineering assets across the agent lifecycle.

Ocean (Product Launch) Ocean is an email security platform that scans every incoming message with a custom language model, checks sender intent against company context, and flags fraud and impersonation.

London's police asked Big Tech for comms data over 700,000 times last year (4 minute read) London's Met made over 700,000 requests for communications metadata in 2025, including data from Proton services, Signal, MVNO LycaMobile, and gig platforms like Uber and Deliveroo. Proton and Signal dispute claims about data handed over, highlighting reliance on metadata and legal channels. Requests targeting LycaMobile and delivery riders intersect with immigration enforcement and source-identification efforts involving journalists and migrants.

Google publishes exploit code threatening millions of Chromium users (2 minute read) Google accidentally exposed proof-of-concept code for a still-unpatched Browser Fetch API bug that can turn Chromium-based browsers into limited bots for proxying traffic, DDoS, and activity monitoring. Any visited site can trigger a persistent service worker, with behavior particularly stealthy on Edge. Chrome, Edge, Brave, Opera, Vivaldi, and Arc are affected. Firefox and Safari are not.

Microsoft disrupts malware code-signing service used by ransomware gangs (3 minute read) Microsoft disrupted Fox Tempest's malware-signing-as-a-service (MSaaS) operation by seizing signspace[.]cloud, revoking 1,000+ code-signing certificates obtained via stolen identities and abused Azure Artifact Signing subscriptions, and taking offline hundreds of attacker-controlled VMs, with cybercriminals paying $5,000–$9,000 per deployment to bypass SmartScreen warnings and evade detection. Vanilla Tempest and affiliates of INC, Qilin, Akira, and Rhysida used signed fake installers (AnyDesk, Teams, PuTTY, and Webex) distributed through SEO poisoning and malvertising to deploy backdoors, infostealers, and ransomware. The shift reflects cybercrime's modularization: specialized high-friction services like code-signing are now commoditized and sold interchangeably, replacing monolithic attack chains and enabling rapid scaling across ransomware campaigns since at least May 2025.

Anthropic Silently Patches Claude Code Sandbox Bypass (2 minute read) Researcher Aonan Guan found a SOCKS5 null-byte injection flaw in Claude Code's network sandbox that let attackers bypass hostname filtering.

Every Voice and Video Call on Discord Is Now End-to-End Encrypted (4 minute read) Discord has finished migrating all one-to-one, group, channel, and Go Live calls to the DAVE end-to-end encryption protocol.

Grafana breach caused by missed token rotation after TanStack attack (1 minute read) Grafana's breach traces to a single GitHub workflow token missed during incident-response rotation after the Shai-Hulud campaign (attributed to TeamPCP) poisoned dozens of TanStack npm packages with credential-stealing code that Grafana's CI/CD consumed on May 1, letting attackers reach private repositories and steal source code plus business contact data, though Grafana confirms no customer production systems were affected and its codebase was not modified.

### Source URL
https://tldr.tech/infosec/2026-05-21
