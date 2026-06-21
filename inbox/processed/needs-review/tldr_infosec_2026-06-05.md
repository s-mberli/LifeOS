---
actionability: high
attached_experts: []
channel_name: ''
created_at: '2026-06-07T12:43:49.521105+10:00'
domain: unknown
expert_status: unattached
primary_mode: router
privacy: public
review_status: new
secondary_modes: []
source_type: article
source_url: https://tldr.tech/infosec/2026-06-05
status: processed
suggested_experts: []
tags:
- infosec
- supply-chain-attack
- ai-security
- ci-cd-security
- data-breach
- vulnerability-research
- ai-agents
- identity-access-management
- redis
- zapier
title: Zapier Hijack Chain ⚡, DentaQuest Data Leak 🦷, AI Finds Redis Bug 🛢
transcript_path: ''
type: insight_note
updated_at: '2026-06-07T12:43:49.521105+10:00'
---

# Zapier Hijack Chain ⚡, DentaQuest Data Leak 🦷, AI Finds Redis Bug 🛢

## Summary
This TL;DR InfoSec digest (2026-06-05) delivers a high-density snapshot of the week's most critical security incidents, research breakthroughs, and tooling developments. The resource paints a landscape where supply chain attacks, AI-assisted vulnerability discovery, and identity/access control for AI agents are converging as dominant threat vectors. Major breaches at DentaQuest (2.6M health records), Columbia University (1.8M SSNs), and Ultrahuman underscore systemic failures in legacy data retention and internal analytics isolation. Law enforcement's 'Disruption Week' dismantled 1.4M+ scam accounts tied to human-trafficking compounds, highlighting the intersection of cybercrime and physical exploitation. On the offensive research side, the 'Zapocalypse' attack chain against Zapier demonstrates how CI/CD pipelines with overly permissive IAM roles and unisolated build environments can be escalated from sandbox escape to full supply chain compromise — leaking NPM publish tokens across 1,111 ECR repos. AI's role in security is dual-edged: open-weight models (Gemma, GPT-OSS) successfully identified a 17-year-old FreeBSD RCE and a Redis use-after-free (CVE-2026-23479), but only when paired with structured harnesses (IronCurtain) and reachability filtering to suppress false positives. Meanwhile, attackers are weaponizing AI features themselves — LLMShare abuses ChatGPT's rendering to serve phishing pages, and SafeBreach's 'Fake Context Alignment' hijacked Gemini via poisoned notifications. The emerging defensive toolkit includes DockSec (OWASP's AI-powered container scanner), KQLab for SOC query management, and Willow — an identity layer purpose-built for enterprise AI agents enforcing least-privilege. The overarching worldview is that security is shifting from perimeter defense to identity-centric, AI-augmented, supply-chain-aware architectures where legacy data hygiene and CI/CD hardening are non-negotiable.

## Key Ideas
- Zapier CI/CD Supply Chain Attack ('Zapocalypse'): Attackers exploited Zapier's Python sandbox with `os.system` access, recovered orphaned STS tokens from Lambda heap memory, pulled container images via raw ECR API across 1,111 repos to evade Docker monitoring, and leaked high-privilege NPM publish tokens via build-time environment variables. Defenders must validate IAM permissions rigorously, isolate untrusted code execution, use BuildKit secrets instead of ARG/ENV for sensitive values, scope and rotate CI tokens, pin dependencies with `npm ci`, and monitor egress to private registries.
- AI-Assisted Vulnerability Research with Reachability Filtering: Open-weight models (Gemma, GPT-OSS) reproduced a 17-year-old FreeBSD RCE and found CVE-2026-23479 (Redis use-after-free, 7.7 High, present since 7.2.0). Broad scans produce excessive false positives, but adding a reachability filtering stage — focusing analysis on attacker-controllable code paths — reduces noise to a human-reviewable shortlist. Harness selection matters: Opus 4.7 and GLM-5.1 excelled with Claude Code harness for crackaddr variants; IronCurtain harness improved results for other models. Post-training quality significantly impacts bug-finding efficacy.
- Redis CVE-2026-23479 — Use-After-Free to Full RCE: Authenticated attackers can chain a Lua heap leak, forced eviction, and GOT overwrite of `strcasecmp()` with `system()` for full server code execution. Present since Redis 7.2.0. Remediation: upgrade to 7.2.14, 7.4.9, 8.2.6, 8.4.3, or 8.6.3; restrict `CONFIG`, `@scripting`, and stream commands on self-managed deployments.
- Identity & Access Layer for AI Agents (Willow): A new category of security tool emerging to centralize and enforce least-privilege access for enterprise AI agents (Claude, Gemini, ChatGPT). Willow provides unified access control, auditing of unauthorized AI use, and policy enforcement — addressing the growing risk of agents operating with excessive permissions across SaaS tools.
- LLMShare Malvertising via ChatGPT Rendering: Attackers abuse ChatGPT's rendering feature to display fake service disruption pages that redirect users to phishing sites delivering infostealers disguised as desktop app downloads. This represents a new class of AI-feature-abuse where the trust surface of an AI product is weaponized for social engineering.
- Gemini Voice Assistant Hijacking via Fake Context Alignment: SafeBreach demonstrated injection of hidden instructions through WhatsApp/Slack/SMS notifications to silently control Google Home devices, launch Zoom calls, and poison the assistant's memory. Patched by Google November 2025. Highlights the risk of AI assistants processing untrusted notification content as operational context.
- Legacy Data Retention as Breach Amplifier: Both Columbia University (1.8M SSNs, including non-affiliates) and DentaQuest (2.6M health records) breaches were exacerbated by decades-old data retained in legacy systems that were missed during modernization/SSN-removal efforts. Data minimization and lifecycle management are critical — not just encryption.
- Personal Security Stack Blueprint: A privacy journalist's real-world setup: YubiKeys (phishing-resistant MFA), dual password managers (1Password + Bitwarden for redundancy), Authy TOTP, Mullvad VPN, uBlock Origin, Google Advanced Protection, Apple Lockdown Mode, Signal, credit freezes, and HaveIBeenPwned monitoring. Guided by a 'vibes first' heuristic — treating urgency as a red flag for social engineering.

## Why this matters for Markus
- AI Platform & Agent Architecture: The Zapier attack chain is a masterclass in CI/CD supply chain exploitation — directly relevant as Markus builds AI agent workflows and platforms. Any agent orchestration system that executes untrusted code, manages IAM roles, or handles secrets via environment variables is a potential target. The defensive patterns (BuildKit secrets, scoped CI tokens, dependency pinning, egress monitoring) should be baked into Markus's ai-platform architecture from day one.
- AI Security & Agent Identity: Willow's emergence as an identity layer for AI agents signals a new security category Markus should track closely. As he builds agent systems, implementing least-privilege access control and audit trails for agent tool usage will be a competitive differentiator and a trust requirement for enterprise clients.
- AI-Assisted Code Security: The research showing open-weight models can find real vulnerabilities (FreeBSD RCE, Redis UAF) with proper harnessing and reachability filtering is directly applicable. Markus could integrate AI-assisted security scanning into his development workflow — using models like GPT-OSS locally with structured security harnesses to audit his own codebases.
- Content & Thought Leadership: The convergence of AI, supply chain attacks, and identity creates rich content angles for Flow Temple's audience and Markus's career brand. A breakdown of the Zapier attack chain or 'how AI found a 2-year-old Redis bug' would perform well on LinkedIn and position Markus at the intersection of AI and security.
- Personal Security Posture: Given Markus's multi-project workload across AI, wellness, and career domains, the personal security stack blueprint is actionable. Implementing YubiKeys, credit freezes, and HaveIBeenPwned monitoring protects the digital infrastructure underlying all his ventures.

## Related Modes
- ai-platform
- career
- life-kompass

## Next Action
- [ ] Audit your AI platform's CI/CD pipeline and agent orchestration architecture against the Zapier attack chain: (1) Review all IAM roles for overly permissive ECR/Lambda permissions — scope them to least-privilege. (2) Replace any ARG/ENV-based secret injection in Docker builds with BuildKit secrets. (3) Pin all dependencies with `npm ci` and rotate any long-lived CI tokens. (4) Implement egress monitoring to detect unexpected calls to private registries. (5) Evaluate integrating an AI-assisted security scanning step using a local open-weight model (e.g., GPT-OSS) with a security-focused harness into your build pipeline.

## Long Resource Processing
- chunks processed: 4
- method: chunked map-reduce summary

## AI Generation Data
- Provider: openrouter
- Model: openrouter/owl-alpha

## Source Reliability
high

## Detailed Chunk Summaries

Chunk 1 Summary:
Here are the key points from this section of the resource:

- **DentaQuest Data Breach**: The ShinyHunters ransomware gang leaked 234GB of data from dental benefits provider DentaQuest, affecting 2.6 million accounts. Exposed data includes emails, names, phone numbers, government IDs, health insurance info, DOB, and gender. Have I Been Pwned confirmed the breach, noting ~66% of accounts were already in their database.

- **Cybercrime Crackdown ("Disruption Week")**: Law enforcement and tech companies disrupted over 1.4 million scam accounts tied to compounds in Cambodia, Laos, and Burma, where trafficked workers were forced into crypto fraud. Resulted in 63 arrests and $3.8M in frozen cryptocurrency.

- **Ultrahuman Data Breach**: Health-tech wearables company Ultrahuman suffered a breach via an internal analytics system, exposing contact/account details, order history, and transaction history — but no financial or wellness data.

- **AI-Assisted Vulnerability Research**: Anthropic's Mythos highlighted a 17-year-old FreeBSD RCE, which was reproduced using local open-weight models (Gemma, GPT-OSS). A reachability filtering stage helped reduce false positives, making AI-assisted bug finding more practical for analysts.

- **LLMShare Malvertising Campaign**: Attackers are abusing ChatGPT's rendering feature to create fake service disruption pages that redirect users to phishing sites delivering infostealers disguised as desktop app downloads.

- **Zapier Attack Chain ("Zapocalypse")**: Researchers demonstrated a chain exploiting Zapier's Python sandbox — recovering orphaned STS tokens from Lambda heap, pulling container images via raw ECR API, and leaking high-privilege NPM publish tokens. Defenders should validate IAM permissions, isolate untrusted code, use BuildKit secrets, and rotate CI tokens.

- **DockSec (OWASP)**: An AI-powered Docker container for context-aware security analysis using industry-standard scanners.

- **KQLab**: A self-hosted KQL query management platform for SOC teams.

- **Willow**: An identity and access layer for enterprise AI agents, centralizing access to tools like Claude, Gemini, and ChatGPT with least-privilege enforcement and unauthorized AI use auditing.

- **Columbia University SSN Breach**: A 2025 breach exposed 1.8 million SSNs, including people with no connection to the university, due to decades-old recruitment data in a legacy database missed during SSN removal efforts. Faces class action and regulatory scrutiny.

- **Personal Privacy/Security Stack**: A journalist shares her setup: YubiKeys, 1Password + Bitwarden, Authy TOTP, Mullvad VPN, uBlock Origin, Google Advanced Protection, Apple Lockdown Mode, Signal, credit freezes, and HaveIBeenPwned monitoring — guided by a "vibes first" rule treating urgency as a red flag.

- **Open-Weight Model Bug Finding**: Testing showed Opus 4.7 and GLM-5.1 consistently found the crackaddr vulnerability using the Claude Code harness, while other models performed better with the security-focused IronCurtain harness. Post-training quality significantly impacts results.

- **Hola Browser Supply Chain Compromise**: Hola Browser's Windows build was compromised to deliver an unsigned Monero cryptominer that installs as an auto-starting service.

- **Gemini Voice Assistant Hijacking**: SafeBreach's "Fake Context Alignment" attack injected hidden instructions via WhatsApp/Slack/SMS notifications to silently control Google Home devices, launch Zoom calls, and poison the assistant's memory. Patched by Google in November 2025.

- **Redis Bug Found by AI (CVE-2026-23479)**: A use-after-free vulnerability in Redis (present since 7.2.0, rated 7.7 High) allows authenticated attackers to achieve full code execution via Lua heap leak, forced eviction, and GOT overwrite. Self-managed deployments should upgrade to patched versions or restrict CONFIG, @scripting, and stream commands.

---

Chunk 2 Summary:
Here is a concise summary of the key points from Part 2/4:

**Major Data Breaches**
*   **DentaQuest:** The ShinyHunters ransomware gang leaked 234GB of data, affecting 2.6 million accounts. Exposed information includes government-issued IDs, health insurance details, and SSNs.
*   **Ultrahuman:** A breach of an internal analytics system exposed user contact details, order history, and transaction data, though the company claims financial and wellness data remained secure.
*   **Columbia University:** A legacy database breach exposed 1.8 million SSNs, including data from individuals who never attended the school, leading to a proposed class action.

**Cybercrime & Law Enforcement**
*   **Disruption Week:** A joint operation by law enforcement and tech firms dismantled 1.4 million scam accounts and froze $3.8M in crypto, targeting human-trafficking-linked compounds in Southeast Asia.
*   **LLMShare Malvertising:** Attackers are using ChatGPT’s rendering features to create fake service disruption pages that redirect users to phishing sites to install infostealers.
*   **Hola Browser:** A supply chain compromise resulted in a Windows build delivering a hidden Monero cryptominer.

**AI & Security Research**
*   **Redis Bug (CVE-2026-23479):** An AI tool discovered a two-year-old use-after-free vulnerability in Redis that allows authenticated attackers to achieve full server code execution.
*   **Open-Weight Models:** Research shows that while models like Gemma and GPT-OSS can identify specific vulnerabilities (like the FreeBSD RCE), they require structured "harnesses" and reachability stages to filter out false positives.
*   **Gemini Hijack:** A "Fake Context Alignment" attack allowed hackers to hijack Google Home devices via hidden instructions in messaging notifications (WhatsApp/SMS).

**Tools & Launches**
*   **DockSec:** An OWASP project providing a Docker container for AI-driven security analysis.
*   **Willow:** A new identity and access layer designed to manage and audit enterprise AI agents.

---

Chunk 3 Summary:
**Key Points from Part 3/4 of the Resource:**

1. **AI-Assisted Vulnerability Discovery**:  
   - Open-weight models (Gemma, GPT-OSS) identified a real stack overflow in FreeBSD’s `sys/rpc` subsystem, but broad scans produced many false positives.  
   - Adding a **reachability filtering stage**—focusing on attacker-controlled paths—effectively reduced noise to a manageable shortlist for human review.

2. **LLMShare Malvertising Campaign**:  
   - Attackers abuse **ChatGPT’s rendering feature** to display fake service disruption alerts, tricking users into downloading malware via phishing pages that mimic legitimate app installers—delivering infostealers.

3. **Zapier “Zapocalypse” Attack Chain**:  
   - Exploited Zapier’s Python sandbox (`os.system` access), leaked AWS STS tokens from Lambda memory, and abused ECR permissions across 1,111 repos using raw API calls to evade Docker monitoring.  
   - High-privilege **NPM publish tokens** leaked via build-time environment variables enabled account takeovers.  
   - **Defensive recommendations**: Validate IAM roles, isolate untrusted code, use BuildKit secrets, rotate CI tokens, pin dependencies, and monitor egress.

4. **New Security Tools**:  
   - **DockSec** (OWASP): AI-powered Docker container for context-aware security scanning.  
   - **KQLab**: Self-hosted platform for managing KQL queries in SOC environments.  
   - **Willow**: Identity and access layer for enterprise AI agents, enforcing least-privilege and auditing unauthorized AI usage.

5. **Data Breaches & Privacy Incidents**:  
   - **Columbia University breach** exposed 1.8M SSNs—including non-affiliated individuals—due to legacy data retention; led to class-action lawsuits.  
   - **DentaQuest breach**: ShinyHunters leaked 234GB (2.6M records) of sensitive health and personal data after ransom refusal.  
   - **Ultrahuman breach**: Internal analytics system compromised; exposed contact, order, and transaction data—but not financial or wellness info.

6. **AI Model Performance in Security Testing**:  
   - Harness and post-training significantly impact open-weight models’ bug-finding efficacy.  
   - **Opus 4.7 and GLM-5.1** performed best in finding `crackaddr` variants; **IronCurtain harness** improved results for other models.

7. **Supply Chain & Assistant Exploits**:  
   - **Hola Browser** compromised to deliver a hidden Monero cryptominer via unsigned service (`hola_monitor_svc`).  
   - **Gemini Voice Assistant hijacked** via malicious notifications (WhatsApp/SMS/Slack) using “Fake Context Alignment” to silently execute commands—patched by Google in late 2025.

8. **Redis Vulnerability (CVE-2026-23479)**:  
   - Use-after-free bug in `unblockClientKey()` (since Redis 7.2.0, severity: High). Allows authenticated attackers to achieve **full code execution** via Lua heap leak + GOT overwrite.  
   - **Mitigation**: Upgrade to patched versions or restrict dangerous commands (`CONFIG`, `@scripting`, streams).

9. **Global Cybercrime Takedown**:  
   - “Disruption Week” dismantled **1.4M+ scam accounts** linked to forced-labor compounds in Southeast Asia; 63 arrests and $3.8M in crypto frozen.

10. **Personal Privacy Practices**:  
    - Journalist shares real-world stack: YubiKeys, dual password managers (1Password + Bitwarden), Authy TOTP, Mullvad VPN, uBlock Origin, Apple Lockdown Mode, Signal, credit freezes, and exposure monitoring via HaveIBeenPwned—prioritizing usability without compromising core security.

---

Chunk 4 Summary:
## Summary of Part 4/4: Zapier Hijack Chain, DentaQuest Data Leak, AI Finds Redis Bug

### Key Security Incidents & Vulnerabilities

**Zapier CI/CD Supply Chain Attack**
- Attackers exploited insecure CI/CD pipelines by injecting malicious packages via ARG/ENV, enabling account takeover.
- **Defensive recommendations:** Validate IAM permissions, isolate untrusted code, use BuildKit secrets, scope/rotate CI NPM tokens, pin dependencies with `npm ci`, and monitor egress to private ECR/NPM.

**DentaQuest Data Leak**
- *(Details covered in earlier parts; this section focuses on other items.)*

**Redis Use-After-Free Vulnerability (CVE-2026-23479)**
- A 2-year-old bug in `unblockClientOnKey()`, present since Redis 7.2.0 (rated 7.7 High).
- Authenticated attackers can chain a Lua heap leak, forced eviction, and GOT overwrite of `strcasecmp()` with `system()` for full code execution.
- **Remediation:** Upgrade to 7.2.14, 7.4.9, 8.2.6, 8.4.3, or 8.6.3; restrict `CONFIG`, `@scripting`, and stream commands.

**Hola Browser Supply Chain Compromise**
- Windows build compromised to deliver an unsigned Monero miner (`me.exe`) that adds Defender exclusions and runs as an auto-starting service.

**Gemini Voice Assistant Hijacking**
- SafeBreach's "Fake Context Alignment" attack injected hidden instructions via WhatsApp/Slack/SMS notifications, controlling Google Home devices and poisoning memory. Patched mid-November 2025.

### Notable Tools & Projects
- **DockSec** (OWASP): AI-powered Docker container security analysis.
- **KQLab**: Self-hosted KQL query management for SOC teams.
- **Willow**: Identity/access layer for enterprise AI agents enforcing least-privilege policies.

### Additional Highlights
- **Columbia University breach** exposed 1.8M SSNs, including non-affiliated individuals, due to legacy database oversight.
- **Open-weight AI models** show improved bug-finding with specialized harnesses (IronCurtain) and post-training.
- **Personal security stack** detailed by a privacy journalist emphasizing physical security keys, VPNs, and exposure monitoring.

## Original Content
### Raw User Input
https://tldr.tech/infosec/2026-06-05

# TLDR InfoSec — 2026-06-05
Source: https://tldr.tech/infosec/2026-06-05

## Articles

### DentaQuest Data Breach Exposed Info of 2.6M Accounts
- **URL:** https://www.bleepingcomputer.com/news/security/dentaquest-data-breach-exposed-info-of-26-million-accounts/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-05
- **Read time:** 2 minute read
- **TLDR Summary:** The ShinyHunters ransomware gang claimed to have stolen and then leaked 234GB of data from the dental benefits provider DentaQuest after they refused to pay a ransom. The breached data includes email addresses, full names, phone numbers, government-issued IDs, health insurance information, dates of birth, and gender. Have I Been Pwned confirmed the breach and stated that it includes 2.6M records, though roughly 66% of the accounts already existed in their database.

### Over 1.4 Million Accounts Disrupted in Cybercrime Crackdown
- **URL:** https://www.securityweek.com/over-1-4-million-accounts-disrupted-in-cybercrime-crackdown/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-05
- **Read time:** 2 minute read
- **TLDR Summary:** Law enforcement and major tech firms ran "Disruption Week," taking down more than 1.4 million scam accounts, pages, Microsoft accounts, and Starlink kits tied to compounds in Cambodia, Laos, and Burma. Workers were trafficked into these sites and forced into scam operations, including crypto investment fraud, leading to 63 arrests and freezing of over 3.8 million dollars in cryptocurrency.

### Ultrahuman Data Breach Exposes User Info via Internal Tool
- **URL:** https://cybernews.com/security/ultrahuman-data-breach-exposes-users/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-05
- **Read time:** 2 minute read
- **TLDR Summary:** Health-tech wearables company Ultrahuman informed customers of a data breach affecting its systems. The company stated that the attackers breached an internal analytics system. The breached data includes contact and account details, order history, and transaction history, but the company stated that it does not contain any financial or wellness data.

### System Over Model, Tested: Reproducing Mythos's FreeBSD Find on Local Open-Weight Models
- **URL:** https://clearbluejar.github.io/posts/system-over-model-tested-mythos-freebsd-local-openweight/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-05
- **Read time:** 15 minute read
- **TLDR Summary:** Anthropic's Mythos preview highlighted a 17-year-old FreeBSD RCE. AISLE then reproduced it cheaply with a structured nano-analyzer pipeline and pushed that test onto local open-weight models using Gemma and GPT-OSS across the full FreeBSD sys/rpc subsystem. Both models can identify the stack overflow in the vulnerable file alone, but broader scans drown it out with false positives and inconsistent triage votes. A simple extra reachability stage filters findings based on attacker-controlled paths and preserves the real CVE, turning noisy output into a shortlist that a single analyst can review.

### LLMShare: How Attackers Are Turning AI Chatbot Pages Into Malware Delivery Platforms
- **URL:** https://pushsecurity.com/blog/llmshare-malvertising-campaign/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-05
- **Read time:** 9 minute read
- **TLDR Summary:** Push Security detected a new malvertising campaign that builds on previous campaigns, which used shared ChatGPT conversations to mimic Apple Support information and trick users into downloading malware. The new campaigns that Push detected utilize ChatGPT's rendering feature to present a page that claims to show a service disruption and prompts users to click a button to download the desktop application. The malicious page then redirects the user to a phishing page that mimics the desktop application download page, leading the user to install an infostealer.

### Zapocalypse: The Attack Chain That Could Have Hijacked Zapier
- **URL:** https://www.token.security/blog/zapocalypse-the-attack-chain-that-could-have-hijacked-zapier?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-05
- **Read time:** 7 minute read
- **TLDR Summary:** Token security involved chaining known primitives, from Zapier's Python sandbox: os.system ran freely, regex scraping recovered orphaned STS tokens from Lambda heap, belonging to allow_nothing_role with permissions for ECR and other actions across 1,111 private repos. Due to GetAuthorizationToken denial, images were pulled via raw ECR API calls, avoiding Docker monitoring. High-privilege NPM publish tokens leaked via build-time ARG/ENV, enabling account takeover. Defenders should validate IAM permissions, isolate untrusted code, use BuildKit secrets, scope and rotate CI NPM tokens, pin dependencies with npm ci, and monitor egress to private ECR or NPM.

### DockSec (GitHub Repo)
- **URL:** https://github.com/OWASP/DockSec?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-05
- **Read time:** Unknown
- **TLDR Summary:** DockSec is an OWASP incubator project that provides a Docker container that uses AI to deliver context-aware security analysis with industry-standard scanners.

### KQLab (GitHub Repo)
- **URL:** https://github.com/vinsk0h/KQLab?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-05
- **Read time:** Unknown
- **TLDR Summary:** KQLab is a self-hosted KQL query management platform for SOC teams.

### Willow (Product Launch)
- **URL:** https://withwillow.ai/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-05
- **Read time:** Unknown
- **TLDR Summary:** Willow provides an identity and access layer for enterprise AI agents and systems. It centralizes access to tools such as Claude, Gemini, ChatGPT, and custom models, enforces least‑privilege policies, and discovers and audits unauthorized AI use across corporate networks.

### My SSN was exposed in a breach at Columbia—a school I have no connection with
- **URL:** https://arstechnica.com/tech-policy/2026/06/my-ssn-was-exposed-in-a-breach-at-columbia-a-school-i-have-no-connection-with/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-05
- **Read time:** 4 minute read
- **TLDR Summary:** Columbia's 2025 breach exposed 1.8 million SSNs, including people who never applied to or studied at the university, because decades-old recruitment and testing data stayed in a legacy database. Columbia missed that database during SSN removal efforts, then took months to answer basic questions from affected people, and now faces a proposed class action and regulatory scrutiny over long-term SSN hoarding.

### What My Privacy and Security Stack Actually Looks Like
- **URL:** https://blog.yaelwrites.com/what-my-privacy-and-security-stack-actually-looks-like/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-05
- **Read time:** 6 minute read
- **TLDR Summary:** A privacy-focused journalist documents the practices she personally uses rather than recommends, anchored by a "vibes first" rule that treats a sense of pressure or urgency as a red flag and verifies via a separate channel, plus operational habits like meeting new contacts in public, using a PO Box, scrubbing her address with EasyOptOuts, and delaying event posts. The technical stack favors physical security keys (three YubiKeys with backups) over passkeys, two password managers (1Password and Bitwarden), Authy for TOTP with email MFA preferred over SMS, full-disk encryption, Mullvad VPN, Privacy Badger plus uBlock Origin, Google Advanced Protection, Apple Lockdown Mode, Google Fi for SIM-swap resistance, and iCloud Hide My Email aliases. She also avoids biometrics and AI-based browsers in her specific threat model, freezes her credit, uses Signal with disappearing messages, and monitors exposure via HaveIBeenPwned, framing the whole setup as a way to reduce unnecessary exposure without making life unworkable.

### How Harnesses and Post-Training Close the Open-Weight Bug Finding Gap
- **URL:** https://vincenzoiozzo.com/blog/oss-models-vuln-research?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-05
- **Read time:** 6 minute read
- **TLDR Summary:** The author tested several open-weight models and Opus 4.7's ability to find the crackaddr vulnerability in four different variants. When using the Claude Code harness, only Opus 4.7 and GLM-5.1 consistently found all variants. However, other models performed better with the IronCurtain harness, which is specifically designed for security testing. GLM-5.1 performing significantly better than GLM-5 also speaks to the importance of post-training.

### Hola Browser for Windows compromised to deliver cryptominer
- **URL:** https://www.bleepingcomputer.com/news/security/hola-browser-for-windows-compromised-to-deliver-cryptominer/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-05
- **Read time:** 2 minute read
- **TLDR Summary:** A supply chain compromise of Hola Browser's Windows build planted an undeclared, unsigned Monero miner (me.exe) that adds a Windows Defender exclusion, copies itself to Program Files as HolaMonitorService.exe, and runs as an auto-starting service named hola_monitor_svc when the machine is idle.

### Gemini Voice Assistant Hijacked via Messaging Notifications
- **URL:** https://www.securityweek.com/gemini-voice-assistant-hijacked-via-messaging-notifications/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-05
- **Read time:** 2 minute read
- **TLDR Summary:** SafeBreach's Fake Context Alignment attack abused WhatsApp, Slack, and SMS notifications to silently inject hidden instructions that Gemini processes but never reads aloud, letting attackers control Google Home devices, launch Zoom calls, spoof trusted contacts, and poison the assistant's long-term memory before Google patched it in mid-November 2025 with classifier improvements.

### An AI Security Tool Dug Up a 2-Year-Old Redis Bug That Lets Attackers Take Over Servers
- **URL:** https://www.cyberkendra.com/2026/06/an-ai-security-tool-dug-up-2-year-old.html?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-05
- **Read time:** 2 minute read
- **TLDR Summary:** CVE-2026-23479, a use-after-free in unblockClientOnKey() present in every Redis stable release since 7.2.0 and rated 7.7 (High), lets authenticated attackers chain a Lua heap leak, forced eviction, and GOT overwrite of strcasecmp() with system() to gain full code execution as the Redis daemon, so self-managed deployments should upgrade to 7.2.14, 7.4.9, 8.2.6, 8.4.3, or 8.6.3 or restrict CONFIG, @scripting, and stream commands until they can.

## Full Text

[DentaQuest Data Breach Exposed Info of 2.6M Accounts (2 minute read)](https://www.bleepingcomputer.com/news/security/dentaquest-data-breach-exposed-info-of-26-million-accounts/?utm_source=tldrinfosec) The ShinyHunters ransomware gang claimed to have stolen and then leaked 234GB of data from the dental benefits provider DentaQuest after they refused to pay a ransom. The breached data includes email addresses, full names, phone numbers, government-issued IDs, health insurance information, dates of birth, and gender. Have I Been Pwned confirmed the breach and stated that it includes 2.6M records, though roughly 66% of the accounts already existed in their database.

[Over 1.4 Million Accounts Disrupted in Cybercrime Crackdown (2 minute read)](https://www.securityweek.com/over-1-4-million-accounts-disrupted-in-cybercrime-crackdown/?utm_source=tldrinfosec) Law enforcement and major tech firms ran "Disruption Week," taking down more than 1.4 million scam accounts, pages, Microsoft accounts, and Starlink kits tied to compounds in Cambodia, Laos, and Burma. Workers were trafficked into these sites and forced into scam operations, including crypto investment fraud, leading to 63 arrests and freezing of over 3.8 million dollars in cryptocurrency.

[Ultrahuman Data Breach Exposes User Info via Internal Tool (2 minute read)](https://cybernews.com/security/ultrahuman-data-breach-exposes-users/?utm_source=tldrinfosec) Health-tech wearables company Ultrahuman informed customers of a data breach affecting its systems. The company stated that the attackers breached an internal analytics system. The breached data includes contact and account details, order history, and transaction history, but the company stated that it does not contain any financial or wellness data.

[System Over Model, Tested: Reproducing Mythos's FreeBSD Find on Local Open-Weight Models (15 minute read)](https://clearbluejar.github.io/posts/system-over-model-tested-mythos-freebsd-local-openweight/?utm_source=tldrinfosec) Anthropic's Mythos preview highlighted a 17-year-old FreeBSD RCE. AISLE then reproduced it cheaply with a structured nano-analyzer pipeline and pushed that test onto local open-weight models using Gemma and GPT-OSS across the full FreeBSD sys/rpc subsystem. Both models can identify the stack overflow in the vulnerable file alone, but broader scans drown it out with false positives and inconsistent triage votes. A simple extra reachability stage filters findings based on attacker-controlled paths and preserves the real CVE, turning noisy output into a shortlist that a single analyst can review.

[LLMShare: How Attackers Are Turning AI Chatbot Pages Into Malware Delivery Platforms (9 minute read)](https://pushsecurity.com/blog/llmshare-malvertising-campaign/?utm_source=tldrinfosec) Push Security detected a new malvertising campaign that builds on previous campaigns, which used shared ChatGPT conversations to mimic Apple Support information and trick users into downloading malware. The new campaigns that Push detected utilize ChatGPT's rendering feature to present a page that claims to show a service disruption and prompts users to click a button to download the desktop application. The malicious page then redirects the user to a phishing page that mimics the desktop application download page, leading the user to install an infostealer.

[Zapocalypse: The Attack Chain That Could Have Hijacked Zapier (7 minute read)](https://www.token.security/blog/zapocalypse-the-attack-chain-that-could-have-hijacked-zapier?utm_source=tldrinfosec) Token security involved chaining known primitives, from Zapier's Python sandbox: os.system ran freely, regex scraping recovered orphaned STS tokens from Lambda heap, belonging to allow_nothing_role with permissions for ECR and other actions across 1,111 private repos. Due to GetAuthorizationToken denial, images were pulled via raw ECR API calls, avoiding Docker monitoring. High-privilege NPM publish tokens leaked via build-time ARG/ENV, enabling account takeover. Defenders should validate IAM permissions, isolate untrusted code, use BuildKit secrets, scope and rotate CI NPM tokens, pin dependencies with npm ci, and monitor egress to private ECR or NPM.

[DockSec (GitHub Repo)](https://github.com/OWASP/DockSec?utm_source=tldrinfosec) DockSec is an OWASP incubator project that provides a Docker container that uses AI to deliver context-aware security analysis with industry-standard scanners.

[KQLab (GitHub Repo)](https://github.com/vinsk0h/KQLab?utm_source=tldrinfosec) KQLab is a self-hosted KQL query management platform for SOC teams.

[Willow (Product Launch)](https://withwillow.ai/?utm_source=tldrinfosec) Willow provides an identity and access layer for enterprise AI agents and systems. It centralizes access to tools such as Claude, Gemini, ChatGPT, and custom models, enforces least‑privilege policies, and discovers and audits unauthorized AI use across corporate networks.

[My SSN was exposed in a breach at Columbia—a school I have no connection with (4 minute read)](https://arstechnica.com/tech-policy/2026/06/my-ssn-was-exposed-in-a-breach-at-columbia-a-school-i-have-no-connection-with/?utm_source=tldrinfosec) Columbia's 2025 breach exposed 1.8 million SSNs, including people who never applied to or studied at the university, because decades-old recruitment and testing data stayed in a legacy database. Columbia missed that database during SSN removal efforts, then took months to answer basic questions from affected people, and now faces a proposed class action and regulatory scrutiny over long-term SSN hoarding.

[What My Privacy and Security Stack Actually Looks Like (6 minute read)](https://blog.yaelwrites.com/what-my-privacy-and-security-stack-actually-looks-like/?utm_source=tldrinfosec) A privacy-focused journalist documents the practices she personally uses rather than recommends, anchored by a "vibes first" rule that treats a sense of pressure or urgency as a red flag and verifies via a separate channel, plus operational habits like meeting new contacts in public, using a PO Box, scrubbing her address with EasyOptOuts, and delaying event posts. The technical stack favors physical security keys (three YubiKeys with backups) over passkeys, two password managers (1Password and Bitwarden), Authy for TOTP with email MFA preferred over SMS, full-disk encryption, Mullvad VPN, Privacy Badger plus uBlock Origin, Google Advanced Protection, Apple Lockdown Mode, Google Fi for SIM-swap resistance, and iCloud Hide My Email aliases. She also avoids biometrics and AI-based browsers in her specific threat model, freezes her credit, uses Signal with disappearing messages, and monitors exposure via HaveIBeenPwned, framing the whole setup as a way to reduce unnecessary exposure without making life unworkable.

[How Harnesses and Post-Training Close the Open-Weight Bug Finding Gap (6 minute read)](https://vincenzoiozzo.com/blog/oss-models-vuln-research?utm_source=tldrinfosec) The author tested several open-weight models and Opus 4.7's ability to find the crackaddr vulnerability in four different variants. When using the Claude Code harness, only Opus 4.7 and GLM-5.1 consistently found all variants. However, other models performed better with the IronCurtain harness, which is specifically designed for security testing. GLM-5.1 performing significantly better than GLM-5 also speaks to the importance of post-training.

[Hola Browser for Windows compromised to deliver cryptominer (2 minute read)](https://www.bleepingcomputer.com/news/security/hola-browser-for-windows-compromised-to-deliver-cryptominer/?utm_source=tldrinfosec) A supply chain compromise of Hola Browser's Windows build planted an undeclared, unsigned Monero miner (me.exe) that adds a Windows Defender exclusion, copies itself to Program Files as HolaMonitorService.exe, and runs as an auto-starting service named hola_monitor_svc when the machine is idle.

[Gemini Voice Assistant Hijacked via Messaging Notifications (2 minute read)](https://www.securityweek.com/gemini-voice-assistant-hijacked-via-messaging-notifications/?utm_source=tldrinfosec) SafeBreach's Fake Context Alignment attack abused WhatsApp, Slack, and SMS notifications to silently inject hidden instructions that Gemini processes but never reads aloud, letting attackers control Google Home devices, launch Zoom calls, spoof trusted contacts, and poison the assistant's long-term memory before Google patched it in mid-November 2025 with classifier improvements.

[An AI Security Tool Dug Up a 2-Year-Old Redis Bug That Lets Attackers Take Over Servers (2 minute read)](https://www.cyberkendra.com/2026/06/an-ai-security-tool-dug-up-2-year-old.html?utm_source=tldrinfosec) CVE-2026-23479, a use-after-free in unblockClientOnKey() present in every Redis stable release since 7.2.0 and rated 7.7 (High), lets authenticated attackers chain a Lua heap leak, forced eviction, and GOT overwrite of strcasecmp() with system() to gain full code execution as the Redis daemon, so self-managed deployments should upgrade to 7.2.14, 7.4.9, 8.2.6, 8.4.3, or 8.6.3 or restrict CONFIG, @scripting, and stream commands until they can.

### Fetched Web Text
[DentaQuest Data Breach Exposed Info of 2.6M Accounts (2 minute read)](https://www.bleepingcomputer.com/news/security/dentaquest-data-breach-exposed-info-of-26-million-accounts/?utm_source=tldrinfosec) The ShinyHunters ransomware gang claimed to have stolen and then leaked 234GB of data from the dental benefits provider DentaQuest after they refused to pay a ransom. The breached data includes email addresses, full names, phone numbers, government-issued IDs, health insurance information, dates of birth, and gender. Have I Been Pwned confirmed the breach and stated that it includes 2.6M records, though roughly 66% of the accounts already existed in their database.

[Over 1.4 Million Accounts Disrupted in Cybercrime Crackdown (2 minute read)](https://www.securityweek.com/over-1-4-million-accounts-disrupted-in-cybercrime-crackdown/?utm_source=tldrinfosec) Law enforcement and major tech firms ran "Disruption Week," taking down more than 1.4 million scam accounts, pages, Microsoft accounts, and Starlink kits tied to compounds in Cambodia, Laos, and Burma. Workers were trafficked into these sites and forced into scam operations, including crypto investment fraud, leading to 63 arrests and freezing of over 3.8 million dollars in cryptocurrency.

[Ultrahuman Data Breach Exposes User Info via Internal Tool (2 minute read)](https://cybernews.com/security/ultrahuman-data-breach-exposes-users/?utm_source=tldrinfosec) Health-tech wearables company Ultrahuman informed customers of a data breach affecting its systems. The company stated that the attackers breached an internal analytics system. The breached data includes contact and account details, order history, and transaction history, but the company stated that it does not contain any financial or wellness data.

[System Over Model, Tested: Reproducing Mythos's FreeBSD Find on Local Open-Weight Models (15 minute read)](https://clearbluejar.github.io/posts/system-over-model-tested-mythos-freebsd-local-openweight/?utm_source=tldrinfosec) Anthropic's Mythos preview highlighted a 17-year-old FreeBSD RCE. AISLE then reproduced it cheaply with a structured nano-analyzer pipeline and pushed that test onto local open-weight models using Gemma and GPT-OSS across the full FreeBSD sys/rpc subsystem. Both models can identify the stack overflow in the vulnerable file alone, but broader scans drown it out with false positives and inconsistent triage votes. A simple extra reachability stage filters findings based on attacker-controlled paths and preserves the real CVE, turning noisy output into a shortlist that a single analyst can review.

[LLMShare: How Attackers Are Turning AI Chatbot Pages Into Malware Delivery Platforms (9 minute read)](https://pushsecurity.com/blog/llmshare-malvertising-campaign/?utm_source=tldrinfosec) Push Security detected a new malvertising campaign that builds on previous campaigns, which used shared ChatGPT conversations to mimic Apple Support information and trick users into downloading malware. The new campaigns that Push detected utilize ChatGPT's rendering feature to present a page that claims to show a service disruption and prompts users to click a button to download the desktop application. The malicious page then redirects the user to a phishing page that mimics the desktop application download page, leading the user to install an infostealer.

[Zapocalypse: The Attack Chain That Could Have Hijacked Zapier (7 minute read)](https://www.token.security/blog/zapocalypse-the-attack-chain-that-could-have-hijacked-zapier?utm_source=tldrinfosec) Token security involved chaining known primitives, from Zapier's Python sandbox: os.system ran freely, regex scraping recovered orphaned STS tokens from Lambda heap, belonging to allow_nothing_role with permissions for ECR and other actions across 1,111 private repos. Due to GetAuthorizationToken denial, images were pulled via raw ECR API calls, avoiding Docker monitoring. High-privilege NPM publish tokens leaked via build-time ARG/ENV, enabling account takeover. Defenders should validate IAM permissions, isolate untrusted code, use BuildKit secrets, scope and rotate CI NPM tokens, pin dependencies with npm ci, and monitor egress to private ECR or NPM.

[DockSec (GitHub Repo)](https://github.com/OWASP/DockSec?utm_source=tldrinfosec) DockSec is an OWASP incubator project that provides a Docker container that uses AI to deliver context-aware security analysis with industry-standard scanners.

[KQLab (GitHub Repo)](https://github.com/vinsk0h/KQLab?utm_source=tldrinfosec) KQLab is a self-hosted KQL query management platform for SOC teams.

[Willow (Product Launch)](https://withwillow.ai/?utm_source=tldrinfosec) Willow provides an identity and access layer for enterprise AI agents and systems. It centralizes access to tools such as Claude, Gemini, ChatGPT, and custom models, enforces least‑privilege policies, and discovers and audits unauthorized AI use across corporate networks.

[My SSN was exposed in a breach at Columbia—a school I have no connection with (4 minute read)](https://arstechnica.com/tech-policy/2026/06/my-ssn-was-exposed-in-a-breach-at-columbia-a-school-i-have-no-connection-with/?utm_source=tldrinfosec) Columbia's 2025 breach exposed 1.8 million SSNs, including people who never applied to or studied at the university, because decades-old recruitment and testing data stayed in a legacy database. Columbia missed that database during SSN removal efforts, then took months to answer basic questions from affected people, and now faces a proposed class action and regulatory scrutiny over long-term SSN hoarding.

[What My Privacy and Security Stack Actually Looks Like (6 minute read)](https://blog.yaelwrites.com/what-my-privacy-and-security-stack-actually-looks-like/?utm_source=tldrinfosec) A privacy-focused journalist documents the practices she personally uses rather than recommends, anchored by a "vibes first" rule that treats a sense of pressure or urgency as a red flag and verifies via a separate channel, plus operational habits like meeting new contacts in public, using a PO Box, scrubbing her address with EasyOptOuts, and delaying event posts. The technical stack favors physical security keys (three YubiKeys with backups) over passkeys, two password managers (1Password and Bitwarden), Authy for TOTP with email MFA preferred over SMS, full-disk encryption, Mullvad VPN, Privacy Badger plus uBlock Origin, Google Advanced Protection, Apple Lockdown Mode, Google Fi for SIM-swap resistance, and iCloud Hide My Email aliases. She also avoids biometrics and AI-based browsers in her specific threat model, freezes her credit, uses Signal with disappearing messages, and monitors exposure via HaveIBeenPwned, framing the whole setup as a way to reduce unnecessary exposure without making life unworkable.

[How Harnesses and Post-Training Close the Open-Weight Bug Finding Gap (6 minute read)](https://vincenzoiozzo.com/blog/oss-models-vuln-research?utm_source=tldrinfosec) The author tested several open-weight models and Opus 4.7's ability to find the crackaddr vulnerability in four different variants. When using the Claude Code harness, only Opus 4.7 and GLM-5.1 consistently found all variants. However, other models performed better with the IronCurtain harness, which is specifically designed for security testing. GLM-5.1 performing significantly better than GLM-5 also speaks to the importance of post-training.

[Hola Browser for Windows compromised to deliver cryptominer (2 minute read)](https://www.bleepingcomputer.com/news/security/hola-browser-for-windows-compromised-to-deliver-cryptominer/?utm_source=tldrinfosec) A supply chain compromise of Hola Browser's Windows build planted an undeclared, unsigned Monero miner (me.exe) that adds a Windows Defender exclusion, copies itself to Program Files as HolaMonitorService.exe, and runs as an auto-starting service named hola_monitor_svc when the machine is idle.

[Gemini Voice Assistant Hijacked via Messaging Notifications (2 minute read)](https://www.securityweek.com/gemini-voice-assistant-hijacked-via-messaging-notifications/?utm_source=tldrinfosec) SafeBreach's Fake Context Alignment attack abused WhatsApp, Slack, and SMS notifications to silently inject hidden instructions that Gemini processes but never reads aloud, letting attackers control Google Home devices, launch Zoom calls, spoof trusted contacts, and poison the assistant's long-term memory before Google patched it in mid-November 2025 with classifier improvements.

[An AI Security Tool Dug Up a 2-Year-Old Redis Bug That Lets Attackers Take Over Servers (2 minute read)](https://www.cyberkendra.com/2026/06/an-ai-security-tool-dug-up-2-year-old.html?utm_source=tldrinfosec) CVE-2026-23479, a use-after-free in unblockClientOnKey() present in every Redis stable release since 7.2.0 and rated 7.7 (High), lets authenticated attackers chain a Lua heap leak, forced eviction, and GOT overwrite of strcasecmp() with system() to gain full code execution as the Redis daemon, so self-managed deployments should upgrade to 7.2.14, 7.4.9, 8.2.6, 8.4.3, or 8.6.3 or restrict CONFIG, @scripting, and stream commands until they can.

### Source URL
https://tldr.tech/infosec/2026-06-05
