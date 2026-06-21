---
actionability: high
attached_experts: []
channel_name: ''
created_at: '2026-06-12T08:30:33.816144+10:00'
domain: unknown
expert_status: unattached
primary_mode: router
privacy: public
review_status: new
secondary_modes: []
source_type: article
source_url: https://tldr.tech/infosec/2026-06-10
status: processed
suggested_experts: []
tags:
- infosec
- supply-chain-attack
- ai-agent-security
- linux-kernel
- pypi-worm
- container-escape
- vpn-zero-day
- anthropic
- claude-mythos
- malicious-skills
title: Linux Kernel 0-Day 🐧, Hades PyPI Worm 🐍, Anthropic Fable 5 🪄
transcript_path: ''
type: insight_note
updated_at: '2026-06-12T08:30:33.816144+10:00'
---

# Linux Kernel 0-Day 🐧, Hades PyPI Worm 🐍, Anthropic Fable 5 🪄

## Summary
The TLDR InfoSec digest for 2026-06-10 paints a stark picture of an escalating, multi-vector threat landscape where supply chain attacks, AI-agent exploitation, and critical infrastructure vulnerabilities converge. At its core, the report underscores that traditional perimeter defenses are increasingly obsolete: attackers now target development ecosystems (PyPI, GitHub), abuse trusted AI agent workflows, and exploit one-character kernel bugs to achieve full system compromise. The Hades PyPI Worm exemplifies this shift—by hijacking 19 legitimate Python packages and leveraging Python’s startup hooks (`hades-setup.pth`) to execute Bun-based payloads at interpreter launch, it bypasses conventional import-time scanning and silently exfiltrates cloud credentials (AWS/GCP/Azure), SSH keys, and tokens to attacker-controlled repos. This attack is particularly insidious because it requires no explicit import—merely launching Python in a contaminated environment triggers execution. Similarly, the Miasma worm demonstrates how AI coding agents themselves become attack vectors: by poisoning config files in 73 Microsoft GitHub repos (primarily Azure), it manipulates agent behavior to harvest credentials during routine development workflows.

On the infrastructure front, the Linux kernel 0-day (CVE-2026-23111)—a one-character nf_tables use-after-free flaw—enables unprivileged local users to gain root and escape containers, with public exploits already available for major distributions. This highlights the fragility of containerized environments when kernel-level bugs exist. Meanwhile, Check Point’s IKEv1 VPN zero-days enable authentication bypass and MITM attacks on legacy deployments, directly linked to Qilin ransomware operations. OpenSSL’s heap use-after-free (CVE-2026-45447) in PKCS#7 verification adds another layer of risk, allowing remote code execution via crafted S/MIME messages—a vector especially dangerous for email-dependent enterprises.

The AI security dimension is equally alarming. Trail of Bits demonstrated that malicious AI agent skills can evade all major scanners (Cisco, Vercel, ClawHub) using obfuscation techniques like 10,000-line padding, embedded .docx payloads, or compiled Python bytecode. This reveals a critical gap in current AI agent trust models. Anthropic’s release of Claude Mythos 5—a model with relaxed safeguards for cyber defenders—signals a strategic shift toward offensive-capable AI tools integrated with platforms like Project Glasswing, while Fable 5 routes sensitive queries through Opus 4.8 with hardened classifiers. These developments reflect an arms race where defensive AI must evolve as rapidly as offensive capabilities. Apple’s Siri-AI integration with Google Gemini via Private Cloud Compute introduces new privacy risks through prompt injection from emails/web and potential data leakage via LLM queries, despite on-device processing claims. The UK’s proposed device-level scanning for child safety, opposed by Signal, further illustrates the tension between security mandates and cryptographic integrity—even on-device scanning undermines end-to-end encryption trust and expands attack surfaces.

## Key Ideas
- Supply Chain Attacks Are Now Developer-Centric: The Hades PyPI Worm and Miasma GitHub worm show that attackers no longer need to breach networks—they poison the tools developers trust. By injecting malicious wheels into 19 PyPI packages and abusing Python startup hooks (`hades-setup.pth`), Hades executes `_index.js` via Bun at interpreter startup without any import statement. This means any environment with matched package versions is compromised. Defenders must treat package manifests as untrusted and implement runtime integrity checks beyond static analysis.
- AI Agents Are the New Attack Surface: Malicious skills bypass all major scanners using obfuscation (padding, docx embedding, bytecode). Miasma worm abuses AI coding agent configs to steal credentials when devs open repos. This demands new trust frameworks for AI agent ecosystems—scanning must evolve beyond signature-based detection to behavioral analysis and sandboxed execution.
- Kernel-Level Vulnerabilities Undermine Container Security: CVE-2026-23111 is a one-character nf_tables bug enabling unprivileged root access and container escape. With public exploits for Debian/Ubuntu/RHEL, this proves that container isolation is only as strong as the host kernel. Immediate patching and restricting unprivileged user namespaces are non-negotiable.
- Legacy Protocols Remain High-Risk: Check Point’s IKEv1 VPN zero-days (auth bypass + MITM) are actively exploited by Qilin ransomware. Organizations still using IKEv1 without machine certificates are exposed. Migration to IKEv2 or modern alternatives is urgent.
- AI Model Releases Reflect Offensive-Defensive Arms Race: Anthropic’s Mythos 5 (relaxed safeguards for cyber defenders) and Fable 5 (sensitive query routing via Opus 4.8) show AI vendors building dual-use capabilities. This creates both opportunities for red teams and risks if such models are repurposed maliciously.

## Why this matters for Markus
- AI Platform Security Implications: As an AI systems builder, Markus must assume that any third-party skill or agent configuration could be malicious. The Trail of Bits findings mean that current skill marketplaces (like ClawHub) cannot be trusted without additional validation layers. This directly impacts how Markus designs agent workflows in his ai-platform—requiring sandboxing, behavioral monitoring, and strict provenance verification for all external skills.
- Supply Chain Risk for Development Environments: If Markus uses Python in any project (likely, given modern AI stacks), the Hades worm scenario is a direct threat. His development environments could be compromised simply by installing a tainted package version. This necessitates pinning dependencies with cryptographic verification, using isolated build environments, and scanning for unexpected startup hooks like `.pth` files.
- Container and Infrastructure Hardening: The Linux kernel 0-day affects all containerized deployments. If Markus runs any services in Docker/Kubernetes (e.g., for Flow Temple or ai-platform), unpatched kernels mean container escape is trivial. This demands automated kernel patching and disabling unprivileged user namespaces in production.
- Opportunity in AI Security Tooling: The gap exposed by malicious AI agent skills creates a market opportunity. Markus could develop or integrate tools that provide runtime behavioral analysis for AI agents, filling the void left by current static scanners. This aligns with his AI systems builder role and could become a portfolio project.

## Related Modes
- ai-platform
- life-kompass

## Next Action
- [ ] Immediately audit all Python environments for the presence of `hades-setup.pth` files or unexpected Bun installations. Cross-reference installed packages against the 19 compromised PyPI packages (including `bramin`, `executor-engine`, `funcdesc`, `coolbox`, `dynamo-release`, `magique`). If any match, rotate all cloud credentials (AWS/GCP/Azure), SSH keys, and GitHub/npm tokens. Then, implement a policy to scan for `.pth` files in all Python environments and restrict unprivileged user namespaces on any Linux hosts running containers.

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
**Key Points from TLDR InfoSec — 2026-06-10 (Part 1/4):**

- **MagicAd Android Malware**: Found in 50+ trojanized games on Xiaomi and other app stores; bypasses OS restrictions to flood devices with ads using persistent background services.
- **Linux Kernel 0-Day (CVE-2026-23111)**: A one-character nf_tables use-after-free flaw allows unprivileged local users to gain root access and escape containers; public exploits exist for Debian, Ubuntu, and RHEL.
- **Check Point VPN Zero-Days**: Critical vulnerabilities in IKEv1-based Mobile Access/SSL VPNs and Spark firewalls allow authentication bypass and man-in-the-middle attacks; linked to Qilin ransomware group.
- **Malicious AI Agent Skills**: Trail of Bits demonstrated four malicious skills that evade security scanners (Cisco, Vercel, ClawHub) via obfuscation techniques like padding or embedding payloads in docx/bytecode.
- **Apple Siri-AI Privacy Risks**: Siri-AI uses Google Gemini with Apple Private Cloud Compute; raises concerns about data leakage via LLM queries, prompt injection, and potential misuse of private context (emails, calendars).
- **Hades PyPI Worm**: Attackers compromised 19 legitimate Python packages, injecting malicious wheels that exploit Python startup hooks to run `_index.js` via Bun at interpreter startup—stealing cloud tokens (AWS/GCP/Azure), GitHub/npm/SSH keys, and exfiltrating to attacker-controlled repos.
- **Miasma Supply Chain Worm**: Infected 73 Microsoft GitHub repos (mainly Azure), disrupting CI/CD workflows; abuses AI coding agents via config files to harvest credentials.
- **OpenSSL High-Severity Flaw (CVE-2026-45447)**: Heap use-after-free in PKCS#7 verification enables remote code execution via crafted S/MIME messages.
- **Microsoft Patch Tuesday**: Fixed ~200 vulnerabilities, nearly 40 critical, across Windows, Azure, Office, Outlook, Exchange, and AI tools.
- **Anthropic Releases**: Launched **Claude Fable 5** (most capable general model) and **Claude Mythos 5** (for cyber defenders with relaxed safeguards); both integrate with Project Glasswing and include hardened classifiers and log retention.
- **Apple Passwords Update**: Now uses Apple Intelligence to auto-fix weak/compromised passwords.
- **Signal vs UK Scanning Plan**: Signal warns UK’s proposed device-level nude image scanning for minors creates surveillance risks, expands attack surface, and breaks end-to-end encryption trust.
- **WhatsApp Blocks Pegasus Campaign**: Thwarted NSO Group spear-phishing attack; filed contempt motion against NSO for violating court injunction.

---

Chunk 2 Summary:
# Summary: TLDR Infosec — Part 2/4

## Key Security Incidents

- **Linux Kernel 0-Day (CVE-2026-23111):** A one-character nf_tables use-after-free bug enables unprivileged local users to gain root and escape containers. Exploits are public for Debian, Ubuntu, and RHEL. Admins should patch immediately and restrict unprivileged user namespaces.

- **Hades PyPI Worm:** Attackers hijacked 19 legitimate Python packages, pushing 37 malicious wheels that exploit Python's startup hook (`hades-setup.pth`) to auto-execute a Bun-based payload at interpreter startup. It stole AWS/GCP/Azure tokens, GitHub/npm/SSH keys, and exfiltrated data to attacker-created GitHub repos. Treat any environment with matched versions as fully compromised.

- **Miasma Supply Chain Worm:** A variant infected 73 Microsoft GitHub repos (mainly Azure), breaking CI/CD workflows. It abuses AI coding agents via config files to harvest credentials when developers open tainted repos.

- **VPN Zero-Day → Qilin Ransomware:** Check Point found a critical auth-bypass vulnerability in IKEv1-based VPN deployments, linked to Qilin ransomware gang activity. A separate IKEv1 cert-validation flaw enables MITM attacks.

- **OpenSSL High-Severity Bug (CVE-2026-45447):** Heap use-after-free in PKCS#7 verification, exploitable for RCE via crafted messages. Found using AI.

- **Microsoft Patch Tuesday:** ~200 vulnerabilities fixed, ~40 critical across Windows, Azure, Office, Exchange, and AI tools.

## Malware & Threats

- **MagicAd Android Malware:** Hidden in 50+ trojanized games on Xiaomi/other app stores; bypasses OS protections to flood devices with ads via persistent background services.

- **Pegasus Spyware Campaign:** WhatsApp blocked a new NSO Group campaign delivered via spear-phishing links (not a platform vulnerability); filed contempt against NSO.

## AI & Agent Security

- **Claude Fable 5 & Mythos 5:** Anthropic released Fable 5 (most capable GA model, routes sensitive queries through Opus 4.8) and Mythos 5 (for cyber defenders with relaxed safeguards, supports Project Glasswing).

- **Agent Skill Distribution Crisis:** Trail of Bits demonstrated that malicious skills can bypass scanners from Cisco, Vercel, and ClawHub using techniques like payload obfuscation (10,000-line padding, embedded .docx, compiled bytecode).

- **Apple Siri-AI Privacy Concerns:** Uses Google Gemini + Private Cloud Compute; risks include data leakage via LLM/search queries, prompt injection from inbox/web, and agent reporting/messaging capabilities.

## Policy & Tools

- **UK Device Scanning Plan:** Government demands client-side scanning to block nude image sharing by minors; Signal warns this breaks privacy trust models and expands attack surface.

- **Apple Passwords:** Now auto-rotates weak/compromised passwords using Apple Intelligence.

- **New Tools:** DriverSentinel (detects malicious/vulnerable drivers via LoLDrivers comparison), A Security (autonomous offensive security platform with continuous attack simulation and auto-remediation).

---

Chunk 3 Summary:
**Key Points from Part 3/4 of 'Linux Kernel 0-Day 🐧, Hades PyPI Worm 🐍, Anthropic Fable 5 🪄':**

- **MagicAd Android Malware**: Found in over 50 trojanized games on Xiaomi and other app stores; uses a task scheduler to persistently display ad banners by restarting background services and messaging built-in apps.

- **Linux Kernel 0-Day (CVE-2026-23111)**: A one-character nf_tables use-after-free flaw allows unprivileged local users to gain root access and escape containers. Public exploits exist for Debian, Ubuntu, and RHEL—admins should patch kernels and restrict unprivileged user namespaces.

- **Check Point VPN Zero-Days**: Critical vulnerabilities in IKEv1-based VPNs/firewalls allow authentication bypass and potential man-in-the-middle attacks. Impacts legacy configurations without machine certificate requirements.

- **AI Agent Skill Security Flaws**: Trail of Bits demonstrated that malicious AI agent skills can bypass scanners (Cisco, Vercel, ClawHub) using techniques like padding with 10,000 lines or embedding payloads in docx/Python bytecode.

- **Apple Siri-AI Privacy Risks**: Siri-AI leverages Google Gemini via Apple Private Cloud Compute, but raises concerns about data leakage through LLM queries, prompt injection from emails/web, and potential misuse of agent access for reporting or data exfiltration.

- **Hades PyPI Worm**: Attackers hijacked 19 legitimate Python packages, injecting malicious wheels that exploit Python startup hooks (`hades-setup.pth`) to run `_index.js` via Bun at interpreter startup—no import needed. Harvested cloud tokens (AWS/GCP/Azure), GitHub/npm/SSH keys, exfiltrated to attacker GitHub repos, and masked traffic using decoy Anthropic API calls. Affected packages include `bramin`, `executor-engine`, `funcdesc`, `coolbox`, `dynamo-release`, and `magique`.

- **Miasma Supply Chain Worm**: Infected 73 Microsoft GitHub repos (mainly Azure), disrupting CI/CD workflows. Compromised PyPI package `durabletask` deployed a modular cloud intrusion framework; worm now abuses AI coding agents via config files to steal credentials.

- **Apple Passwords Update**: Now uses Apple Intelligence to automatically fix weak/compromised passwords, expanding beyond detection to automated rotation.

- **Signal vs UK Scanning Plan**: Signal warns that mandatory device-level scanning for nude images undermines end-to-end privacy, creates surveillance risks, and expands attack surfaces—even if scanning occurs on-device.

- **WhatsApp Blocks Pegasus Campaign**: NSO Group used spear-phishing links (not platform exploits) to deploy Pegasus; WhatsApp removed test accounts/groups and filed contempt charges against NSO for violating a court injunction.

- **OpenSSL & Microsoft Patches**: OpenSSL fixed 18 flaws including a critical heap use-after-free (CVE-2026-45447) in PKCS#7 verification. Microsoft patched ~200 vulnerabilities (40 critical) across Windows, Azure, Office, and AI tools.

- **Anthropic Model Releases**: Launched **Claude Fable 5** (most capable general model) and **Claude Mythos 5** (for cyber defenders with relaxed safeguards). Fable 5 routes sensitive queries through Opus 4.8 with hardened classifiers; Mythos 5 supports Project Glasswing and biology research. Pricing: $10/M input, $50/M output.

---

Chunk 4 Summary:
**Key Points from Part 4/4:**

- **Check Point VPN Zero-Days**: Two critical IKEv1 vulnerabilities allow authentication bypass and man-in-the-middle attacks on legacy VPN/firewall deployments.
  
- **Malicious AI Agent Skills**: Trail of Bits demonstrated that current skill scanners (Cisco, Vercel, ClawHub) can be evaded using prompt injections hidden in docx files, Python bytecode, or padded with thousands of benign lines.

- **Apple Siri-AI Privacy Risks**: Siri-AI leverages Google Gemini via Apple’s private cloud, but risks data leakage through LLM queries, prompt injection from emails/web, and potential misuse of agent access for reporting or data exfiltration.

- **Hades PyPI Worm**: Attackers hijacked 19 legitimate Python packages, injecting malicious wheels that exploit Python startup hooks to run `_index.js` via Bun at interpreter launch—stealing cloud tokens (AWS/GCP/Azure), GitHub/npm/SSH keys, and exfiltrating to attacker-controlled repos. IOCs: `hades-setup.pth`, `_index.js`, unexpected Bun downloads.

- **Miasma Supply Chain Worm**: Compromised 73 Microsoft GitHub repos (mainly Azure), disrupting CI/CD via poisoned Actions; earlier variant targeted PyPI’s `durabletask` package with a modular cloud intrusion framework.

- **Apple Passwords Update**: Now uses Apple Intelligence to auto-fix weak/compromised passwords.

- **Signal vs UK Scanning Plan**: Signal warns device-level scanning for child safety creates surveillance risks, expands attack surface, and breaks end-to-end encryption trust.

- **WhatsApp Blocks Pegasus Campaign**: NSO Group used spear-phishing (not zero-click) to deliver Pegasus; WhatsApp removed malicious accounts and filed contempt charges.

- **OpenSSL & Microsoft Patches**: OpenSSL fixed 18 flaws including a critical RCE (CVE-2026-45447); Microsoft patched ~200 vulnerabilities (40 critical) across Windows, Azure, Office, and AI tools.

## Original Content
### Raw User Input
https://tldr.tech/infosec/2026-06-10

# TLDR InfoSec — 2026-06-10
Source: https://tldr.tech/infosec/2026-06-10

## Articles

### New MagicAd Android Malware Floods Devices With Ads Bypassing Restrictions
- **URL:** https://cybersecuritynews.com/new-magicad-android-malware-flood-device/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-10
- **Read time:** 2 minute read
- **TLDR Summary:** Researchers have uncovered a new Android malware dubbed MagicAd that bypasses OS protections to flood the user's device with ads. The malware was hiding in more than 50 trojanized games on the Xiaomi and other app stores. Once installed, the malware uses a task scheduler to continuously restart its background service to continuously send messages to built-in apps to display the ads as banners.

### One-Character Linux Kernel Flaw Enables Local Root Access, Exploits Now Public
- **URL:** https://thehackernews.com/2026/06/one-character-linux-kernel-flaw-enables.html?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-10
- **Read time:** 3 minute read
- **TLDR Summary:** CVE-2026-23111 is an nf_tables use-after-free bug in the Linux kernel that lets an unprivileged local user gain root and escape containers on common desktop and server setups with user namespaces enabled. Exploits now exist for Debian, Ubuntu, and RHEL, so admins should prioritize kernel updates and consider restricting unprivileged user namespaces until patched.

### Check Point Links VPN Zero-Day Attacks to Qlin Ransomware Gang
- **URL:** https://www.bleepingcomputer.com/news/security/check-point-links-vpn-zero-day-attacks-to-qilin-ransomware-gang/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-10
- **Read time:** 2 minute read
- **TLDR Summary:** Check Point discovered a new critical vulnerability that allows remote attackers to bypass authentication on targeted Mobile Access/SSL VPNs, Remote Access VPNs, or Spark firewalls to establish a VPN connection. The vulnerability only impacts deployments configured to use IKEv1 key exchange, with security gateways that accept legacy Remote Access clients, and don't require a machine certificate for connections. While working on this vulnerability, Check Point uncovered another vulnerability in the IKEv1 certificate validation implementation, which could allow attackers to launch man-in-the-middle attacks.

### The Sorry State of Skill Distribution
- **URL:** https://blog.trailofbits.com/2026/06/03/the-sorry-state-of-skill-distribution/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-10
- **Read time:** 5 minute read
- **TLDR Summary:** In an effort to better understand the state of agent skills, Trail of Bits crafted four malicious skills that could bypass the skill security scanners used by Cisco's skill-scanner, Vercel's skills.sh marketplace, and ClawHub. ClawHub's scanner could be defeated by inserting 10,000 new lines between a benign preamble and the prompt injection. The other scanners could be defeated by embedding a malicious payload as a docx or as compiled Python byte code.

### Apple's Siri-AI, or more shouting into the void about “private” agents
- **URL:** https://blog.cryptographyengineering.com/2026/06/09/apples-siri-ai-or-more-shouting-into-the-void-about-private-agents/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-10
- **Read time:** 7 minute read
- **TLDR Summary:** Apple's Siri-AI uses Google Gemini with Apple Private Cloud Compute and Google Confidential Inference. Private context from messages, email, notes, and calendars can improve scheduling and search. Useful agents can leak data when they query search engines or LLMs, and prompt injection in the inbox and on the web can steer an agent into sending private data. A final concern is reporting: an agent with data and messaging access can be configured to flag crimes or pass material to others.

### Hades Cluster PyPI Worm Abuses Python Startup Hooks
- **URL:** https://haltingproblems.com/analysis/hades-cluster-pypi-startup-hook-compromise/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-10
- **Read time:** 12 minute read
- **TLDR Summary:** On June 7, Socket disclosed that attackers gained publishing authority over 19 legitimate scientific and deep-learning packages and uploaded 37 malicious wheels that drop a hades-setup.pth file into site-packages. These wheels exploit Python's path configuration hook to automatically execute _index.js via a bootstrapped Bun runtime at interpreter startup, without any explicit import by the developer. The credential stealer harvested AWS, GCP, and Azure cloud tokens, along with GitHub, npm, and SSH keys, exfiltrated data to attacker-created GitHub repositories labeled "Hades - The End for the Damned", and emitted decoy HTTPS traffic to Anthropic API endpoints to obscure the egress channel. Defenders should audit requirements.txt, poetry.lock, and local site-packages for affected package names (including bramin, executor-engine, executor-http, funcdesc, coolbox, dynamo-release, and magique, among others), treat any environment containing a matched version as fully compromised, rotate all reachable cloud and VCS tokens immediately, and hunt for the IOCs hades-setup.pth and _index.js, along with unexpected Bun runtime downloads, in CI/CD process logs.

### DriverSentinel (GitHub Repo)
- **URL:** https://github.com/bI8d0/DriverSentinel?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-10
- **Read time:** Unknown
- **TLDR Summary:** DriverSentinel is a security tool that detects malicious and vulnerable drivers by comparing them against LoLDrivers.

### A Security (Product Launch)
- **URL:** https://a.security/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-10
- **Read time:** Unknown
- **TLDR Summary:** A Security provides an autonomous offensive security platform that runs continuous, scoped attack simulations across enterprise environments, chains real exploit paths, and then triggers targeted remediation and control adjustments to close those paths before attackers use them.

### Claude Fable 5 and Claude Mythos 5
- **URL:** https://www.anthropic.com/news/claude-fable-5-mythos-5?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-10
- **Read time:** 8 minute read
- **TLDR Summary:** Anthropic's releases Claude Fable 5 as its most capable generally available model and Claude Mythos 5 for selected cyber defenders with relaxed safeguards. Fable 5 routes sensitive cyber, bio, and distillation queries through Opus 4.8 using hardened classifiers and 30‑day log retention. Mythos 5 directly supports Project Glasswing and a gated biology track, with pricing set at $10/M input and $50/M output.

### Miasma Supply Chain Worm Burrows Into 73 Microsoft Repositories
- **URL:** https://www.darkreading.com/application-security/miasma-supply-chain-worm-73-microsoft-repositories?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-10
- **Read time:** 6 minute read
- **TLDR Summary:** A Miasma variant hit 73 Microsoft GitHub repos, mainly in Azure, knocking key Actions like Azure/functions-action offline and breaking CI/CD workflows worldwide. Attackers had earlier compromised Microsoft's durabletask PyPI package with a modular cloud intrusion framework that steals secrets and can deploy a wiper. The worm now abuses AI coding agents via config files, harvesting credentials when developers open tainted repos.

### Apple Passwords can Now Automatically Fix Weak and Compromised Passwords
- **URL:** https://www.macrumors.com/2026/06/08/apple-passwords-can-now-automatically-fix-passwords-with-agentic-ai/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-10
- **Read time:** 1 minute read
- **TLDR Summary:** Apple Passwords can now automatically update weak and compromised passwords using Apple Intelligence. This feature expands Apple Passwords' existing weak and compromised password detection by automating the rotation process.

### Signal says UK plan to scan devices for nude images 'endangers us all'
- **URL:** https://www.theregister.com/security/2026/06/09/signal-uks-child-nude-block-threat-wont-protect-children/5252761?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-10
- **Read time:** 3 minute read
- **TLDR Summary:** Keir Starmer gives tech firms three months to deploy device-level scanning that blocks minors from taking, sharing, or viewing nude images, or face legislation. Signal warns that client-side scanning and age checks create new surveillance and censorship hooks, expand attack surface via updatable abuse databases or models, and break its privacy trust model even if images stay on-device.

### WhatsApp Says It Blocked Pegasus Spyware Campaign Linked to NSO
- **URL:** https://hackread.com/whatsapp-blocked-pegasus-spyware-campaign-nso/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-10
- **Read time:** 3 minute read
- **TLDR Summary:** WhatsApp blocked a new NSO Group Pegasus campaign delivered via spear-phishing links rather than a platform vulnerability, removed associated test accounts and groups, and filed for contempt against NSO for violating an existing permanent injunction.

### OpenSSL Patches High-Severity Vulnerability Found With AI
- **URL:** https://www.securityweek.com/openssl-patches-high-severity-vulnerability-found-with-ai/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-10
- **Read time:** 2 minute read
- **TLDR Summary:** OpenSSL shipped fixes for 18 flaws, including CVE-2026-45447, a heap use-after-free bug in PKCS#7 verification that can lead to remote code execution via crafted PKCS#7 or S/MIME messages.

### Microsoft Patches 200 Vulnerabilities
- **URL:** https://www.securityweek.com/microsoft-patches-200-vulnerabilities/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-10
- **Read time:** 2 minute read
- **TLDR Summary:** Microsoft's June 2026 Patch Tuesday fixed roughly 200 flaws (nearly 40 rated critical across Windows, Azure, Office, Outlook, Exchange, and AI tools).

## Full Text

[AI agents, machines, and remote clients are silently authenticating into your systems (Sponsor)](https://bitwarden.com/go/identity-centric-security-with-bitwarden/?utm_source=tldr_infosec&amp;utm_medium=email&amp;utm_campaign=34103600-TLDR+2026&amp;utm_content=061026_identity-centric-security_header_ai_agents_machines) Most organizations have no unified view and no controls built to secure this. Bitwarden changes that. One end-to-end encrypted platform for credential access across every identity in your organization. Uncover shadow AI being used without explicit IT approval Least-privilege access, password policies, and role-based controls for employees and machines Securely and easily share secrets across AI agents and machines. No hardcoded credentials, no exposed .env files Just-in-time credential access for AI agents, with human approval every time Trusted by NASA, Bitdefender, and over 80,000 businesses worldwide.  [Start a free Bitwarden trial and secure access across employees, machines and AI agents.](https://bitwarden.com/go/identity-centric-security-with-bitwarden/?utm_source=tldr_infosec&utm_medium=email&utm_campaign=34103600-TLDR+2026&utm_content=061026_identity-centric-security_cta_machines_ai_agents)

[New MagicAd Android Malware Floods Devices With Ads Bypassing Restrictions (2 minute read)](https://cybersecuritynews.com/new-magicad-android-malware-flood-device/?utm_source=tldrinfosec) Researchers have uncovered a new Android malware dubbed MagicAd that bypasses OS protections to flood the user's device with ads. The malware was hiding in more than 50 trojanized games on the Xiaomi and other app stores. Once installed, the malware uses a task scheduler to continuously restart its background service to continuously send messages to built-in apps to display the ads as banners.

[One-Character Linux Kernel Flaw Enables Local Root Access, Exploits Now Public (3 minute read)](https://thehackernews.com/2026/06/one-character-linux-kernel-flaw-enables.html?utm_source=tldrinfosec) CVE-2026-23111 is an nf_tables use-after-free bug in the Linux kernel that lets an unprivileged local user gain root and escape containers on common desktop and server setups with user namespaces enabled. Exploits now exist for Debian, Ubuntu, and RHEL, so admins should prioritize kernel updates and consider restricting unprivileged user namespaces until patched.

[Check Point Links VPN Zero-Day Attacks to Qlin Ransomware Gang (2 minute read)](https://www.bleepingcomputer.com/news/security/check-point-links-vpn-zero-day-attacks-to-qilin-ransomware-gang/?utm_source=tldrinfosec) Check Point discovered a new critical vulnerability that allows remote attackers to bypass authentication on targeted Mobile Access/SSL VPNs, Remote Access VPNs, or Spark firewalls to establish a VPN connection. The vulnerability only impacts deployments configured to use IKEv1 key exchange, with security gateways that accept legacy Remote Access clients, and don't require a machine certificate for connections. While working on this vulnerability, Check Point uncovered another vulnerability in the IKEv1 certificate validation implementation, which could allow attackers to launch man-in-the-middle attacks.

[The Sorry State of Skill Distribution (5 minute read)](https://blog.trailofbits.com/2026/06/03/the-sorry-state-of-skill-distribution/?utm_source=tldrinfosec) In an effort to better understand the state of agent skills, Trail of Bits crafted four malicious skills that could bypass the skill security scanners used by Cisco's skill-scanner, Vercel's skills.sh marketplace, and ClawHub. ClawHub's scanner could be defeated by inserting 10,000 new lines between a benign preamble and the prompt injection. The other scanners could be defeated by embedding a malicious payload as a docx or as compiled Python byte code.

[Apple's Siri-AI, or more shouting into the void about “private” agents (7 minute read)](https://blog.cryptographyengineering.com/2026/06/09/apples-siri-ai-or-more-shouting-into-the-void-about-private-agents/?utm_source=tldrinfosec) Apple's Siri-AI uses Google Gemini with Apple Private Cloud Compute and Google Confidential Inference. Private context from messages, email, notes, and calendars can improve scheduling and search. Useful agents can leak data when they query search engines or LLMs, and prompt injection in the inbox and on the web can steer an agent into sending private data. A final concern is reporting: an agent with data and messaging access can be configured to flag crimes or pass material to others.

[Hades Cluster PyPI Worm Abuses Python Startup Hooks (12 minute read)](https://haltingproblems.com/analysis/hades-cluster-pypi-startup-hook-compromise/?utm_source=tldrinfosec) On June 7, Socket disclosed that attackers gained publishing authority over 19 legitimate scientific and deep-learning packages and uploaded 37 malicious wheels that drop a hades-setup.pth file into site-packages. These wheels exploit Python's path configuration hook to automatically execute _index.js via a bootstrapped Bun runtime at interpreter startup, without any explicit import by the developer. The credential stealer harvested AWS, GCP, and Azure cloud tokens, along with GitHub, npm, and SSH keys, exfiltrated data to attacker-created GitHub repositories labeled "Hades - The End for the Damned", and emitted decoy HTTPS traffic to Anthropic API endpoints to obscure the egress channel. Defenders should audit requirements.txt, poetry.lock, and local site-packages for affected package names (including bramin, executor-engine, executor-http, funcdesc, coolbox, dynamo-release, and magique, among others), treat any environment containing a matched version as fully compromised, rotate all reachable cloud and VCS tokens immediately, and hunt for the IOCs hades-setup.pth and _index.js, along with unexpected Bun runtime downloads, in CI/CD process logs.

[What Picus found when they analyzed 1.1M malicious files (Sponsor)](https://hubs.li/Q04jQ3sN0?utm_source=tldrinfosec) Malware now does math to spot humans. When Picus analyzed 15.5M actions and 1.1M malicious files, they mapped the  [10 techniques](https://hubs.li/Q04jQ3sN0)  attackers use most to MITRE ATT&CK. Learn why target evasion and stealthy command and control account for the supermajority of attacks. Download the  [Top 10 Attacker Techniques of 2026](https://hubs.li/Q04jQ3sN0)

[DriverSentinel (GitHub Repo)](https://github.com/bI8d0/DriverSentinel?utm_source=tldrinfosec) DriverSentinel is a security tool that detects malicious and vulnerable drivers by comparing them against LoLDrivers.

[A Security (Product Launch)](https://a.security/?utm_source=tldrinfosec) A Security provides an autonomous offensive security platform that runs continuous, scoped attack simulations across enterprise environments, chains real exploit paths, and then triggers targeted remediation and control adjustments to close those paths before attackers use them.

[Claude Fable 5 and Claude Mythos 5 (8 minute read)](https://www.anthropic.com/news/claude-fable-5-mythos-5?utm_source=tldrinfosec) Anthropic's releases Claude Fable 5 as its most capable generally available model and Claude Mythos 5 for selected cyber defenders with relaxed safeguards. Fable 5 routes sensitive cyber, bio, and distillation queries through Opus 4.8 using hardened classifiers and 30‑day log retention. Mythos 5 directly supports Project Glasswing and a gated biology track, with pricing set at $10/M input and $50/M output.

[Miasma Supply Chain Worm Burrows Into 73 Microsoft Repositories (6 minute read)](https://www.darkreading.com/application-security/miasma-supply-chain-worm-73-microsoft-repositories?utm_source=tldrinfosec) A Miasma variant hit 73 Microsoft GitHub repos, mainly in Azure, knocking key Actions like Azure/functions-action offline and breaking CI/CD workflows worldwide. Attackers had earlier compromised Microsoft's durabletask PyPI package with a modular cloud intrusion framework that steals secrets and can deploy a wiper. The worm now abuses AI coding agents via config files, harvesting credentials when developers open tainted repos.

[Apple Passwords can Now Automatically Fix Weak and Compromised Passwords (1 minute read)](https://www.macrumors.com/2026/06/08/apple-passwords-can-now-automatically-fix-passwords-with-agentic-ai/?utm_source=tldrinfosec) Apple Passwords can now automatically update weak and compromised passwords using Apple Intelligence. This feature expands Apple Passwords' existing weak and compromised password detection by automating the rotation process.

[Signal says UK plan to scan devices for nude images 'endangers us all' (3 minute read)](https://www.theregister.com/security/2026/06/09/signal-uks-child-nude-block-threat-wont-protect-children/5252761?utm_source=tldrinfosec) Keir Starmer gives tech firms three months to deploy device-level scanning that blocks minors from taking, sharing, or viewing nude images, or face legislation. Signal warns that client-side scanning and age checks create new surveillance and censorship hooks, expand attack surface via updatable abuse databases or models, and break its privacy trust model even if images stay on-device.

[WhatsApp Says It Blocked Pegasus Spyware Campaign Linked to NSO (3 minute read)](https://hackread.com/whatsapp-blocked-pegasus-spyware-campaign-nso/?utm_source=tldrinfosec) WhatsApp blocked a new NSO Group Pegasus campaign delivered via spear-phishing links rather than a platform vulnerability, removed associated test accounts and groups, and filed for contempt against NSO for violating an existing permanent injunction.

[OpenSSL Patches High-Severity Vulnerability Found With AI (2 minute read)](https://www.securityweek.com/openssl-patches-high-severity-vulnerability-found-with-ai/?utm_source=tldrinfosec) OpenSSL shipped fixes for 18 flaws, including CVE-2026-45447, a heap use-after-free bug in PKCS#7 verification that can lead to remote code execution via crafted PKCS#7 or S/MIME messages.

[Microsoft Patches 200 Vulnerabilities (2 minute read)](https://www.securityweek.com/microsoft-patches-200-vulnerabilities/?utm_source=tldrinfosec) Microsoft's June 2026 Patch Tuesday fixed roughly 200 flaws (nearly 40 rated critical across Windows, Azure, Office, Outlook, Exchange, and AI tools).

### Fetched Web Text
[AI agents, machines, and remote clients are silently authenticating into your systems (Sponsor)](https://bitwarden.com/go/identity-centric-security-with-bitwarden/?utm_source=tldr_infosec&amp;utm_medium=email&amp;utm_campaign=34103600-TLDR+2026&amp;utm_content=061026_identity-centric-security_header_ai_agents_machines) Most organizations have no unified view and no controls built to secure this. Bitwarden changes that. One end-to-end encrypted platform for credential access across every identity in your organization. Uncover shadow AI being used without explicit IT approval Least-privilege access, password policies, and role-based controls for employees and machines Securely and easily share secrets across AI agents and machines. No hardcoded credentials, no exposed .env files Just-in-time credential access for AI agents, with human approval every time Trusted by NASA, Bitdefender, and over 80,000 businesses worldwide.  [Start a free Bitwarden trial and secure access across employees, machines and AI agents.](https://bitwarden.com/go/identity-centric-security-with-bitwarden/?utm_source=tldr_infosec&utm_medium=email&utm_campaign=34103600-TLDR+2026&utm_content=061026_identity-centric-security_cta_machines_ai_agents)

[New MagicAd Android Malware Floods Devices With Ads Bypassing Restrictions (2 minute read)](https://cybersecuritynews.com/new-magicad-android-malware-flood-device/?utm_source=tldrinfosec) Researchers have uncovered a new Android malware dubbed MagicAd that bypasses OS protections to flood the user's device with ads. The malware was hiding in more than 50 trojanized games on the Xiaomi and other app stores. Once installed, the malware uses a task scheduler to continuously restart its background service to continuously send messages to built-in apps to display the ads as banners.

[One-Character Linux Kernel Flaw Enables Local Root Access, Exploits Now Public (3 minute read)](https://thehackernews.com/2026/06/one-character-linux-kernel-flaw-enables.html?utm_source=tldrinfosec) CVE-2026-23111 is an nf_tables use-after-free bug in the Linux kernel that lets an unprivileged local user gain root and escape containers on common desktop and server setups with user namespaces enabled. Exploits now exist for Debian, Ubuntu, and RHEL, so admins should prioritize kernel updates and consider restricting unprivileged user namespaces until patched.

[Check Point Links VPN Zero-Day Attacks to Qlin Ransomware Gang (2 minute read)](https://www.bleepingcomputer.com/news/security/check-point-links-vpn-zero-day-attacks-to-qilin-ransomware-gang/?utm_source=tldrinfosec) Check Point discovered a new critical vulnerability that allows remote attackers to bypass authentication on targeted Mobile Access/SSL VPNs, Remote Access VPNs, or Spark firewalls to establish a VPN connection. The vulnerability only impacts deployments configured to use IKEv1 key exchange, with security gateways that accept legacy Remote Access clients, and don't require a machine certificate for connections. While working on this vulnerability, Check Point uncovered another vulnerability in the IKEv1 certificate validation implementation, which could allow attackers to launch man-in-the-middle attacks.

[The Sorry State of Skill Distribution (5 minute read)](https://blog.trailofbits.com/2026/06/03/the-sorry-state-of-skill-distribution/?utm_source=tldrinfosec) In an effort to better understand the state of agent skills, Trail of Bits crafted four malicious skills that could bypass the skill security scanners used by Cisco's skill-scanner, Vercel's skills.sh marketplace, and ClawHub. ClawHub's scanner could be defeated by inserting 10,000 new lines between a benign preamble and the prompt injection. The other scanners could be defeated by embedding a malicious payload as a docx or as compiled Python byte code.

[Apple's Siri-AI, or more shouting into the void about “private” agents (7 minute read)](https://blog.cryptographyengineering.com/2026/06/09/apples-siri-ai-or-more-shouting-into-the-void-about-private-agents/?utm_source=tldrinfosec) Apple's Siri-AI uses Google Gemini with Apple Private Cloud Compute and Google Confidential Inference. Private context from messages, email, notes, and calendars can improve scheduling and search. Useful agents can leak data when they query search engines or LLMs, and prompt injection in the inbox and on the web can steer an agent into sending private data. A final concern is reporting: an agent with data and messaging access can be configured to flag crimes or pass material to others.

[Hades Cluster PyPI Worm Abuses Python Startup Hooks (12 minute read)](https://haltingproblems.com/analysis/hades-cluster-pypi-startup-hook-compromise/?utm_source=tldrinfosec) On June 7, Socket disclosed that attackers gained publishing authority over 19 legitimate scientific and deep-learning packages and uploaded 37 malicious wheels that drop a hades-setup.pth file into site-packages. These wheels exploit Python's path configuration hook to automatically execute _index.js via a bootstrapped Bun runtime at interpreter startup, without any explicit import by the developer. The credential stealer harvested AWS, GCP, and Azure cloud tokens, along with GitHub, npm, and SSH keys, exfiltrated data to attacker-created GitHub repositories labeled "Hades - The End for the Damned", and emitted decoy HTTPS traffic to Anthropic API endpoints to obscure the egress channel. Defenders should audit requirements.txt, poetry.lock, and local site-packages for affected package names (including bramin, executor-engine, executor-http, funcdesc, coolbox, dynamo-release, and magique, among others), treat any environment containing a matched version as fully compromised, rotate all reachable cloud and VCS tokens immediately, and hunt for the IOCs hades-setup.pth and _index.js, along with unexpected Bun runtime downloads, in CI/CD process logs.

[What Picus found when they analyzed 1.1M malicious files (Sponsor)](https://hubs.li/Q04jQ3sN0?utm_source=tldrinfosec) Malware now does math to spot humans. When Picus analyzed 15.5M actions and 1.1M malicious files, they mapped the  [10 techniques](https://hubs.li/Q04jQ3sN0)  attackers use most to MITRE ATT&CK. Learn why target evasion and stealthy command and control account for the supermajority of attacks. Download the  [Top 10 Attacker Techniques of 2026](https://hubs.li/Q04jQ3sN0)

[DriverSentinel (GitHub Repo)](https://github.com/bI8d0/DriverSentinel?utm_source=tldrinfosec) DriverSentinel is a security tool that detects malicious and vulnerable drivers by comparing them against LoLDrivers.

[A Security (Product Launch)](https://a.security/?utm_source=tldrinfosec) A Security provides an autonomous offensive security platform that runs continuous, scoped attack simulations across enterprise environments, chains real exploit paths, and then triggers targeted remediation and control adjustments to close those paths before attackers use them.

[Claude Fable 5 and Claude Mythos 5 (8 minute read)](https://www.anthropic.com/news/claude-fable-5-mythos-5?utm_source=tldrinfosec) Anthropic's releases Claude Fable 5 as its most capable generally available model and Claude Mythos 5 for selected cyber defenders with relaxed safeguards. Fable 5 routes sensitive cyber, bio, and distillation queries through Opus 4.8 using hardened classifiers and 30‑day log retention. Mythos 5 directly supports Project Glasswing and a gated biology track, with pricing set at $10/M input and $50/M output.

[Miasma Supply Chain Worm Burrows Into 73 Microsoft Repositories (6 minute read)](https://www.darkreading.com/application-security/miasma-supply-chain-worm-73-microsoft-repositories?utm_source=tldrinfosec) A Miasma variant hit 73 Microsoft GitHub repos, mainly in Azure, knocking key Actions like Azure/functions-action offline and breaking CI/CD workflows worldwide. Attackers had earlier compromised Microsoft's durabletask PyPI package with a modular cloud intrusion framework that steals secrets and can deploy a wiper. The worm now abuses AI coding agents via config files, harvesting credentials when developers open tainted repos.

[Apple Passwords can Now Automatically Fix Weak and Compromised Passwords (1 minute read)](https://www.macrumors.com/2026/06/08/apple-passwords-can-now-automatically-fix-passwords-with-agentic-ai/?utm_source=tldrinfosec) Apple Passwords can now automatically update weak and compromised passwords using Apple Intelligence. This feature expands Apple Passwords' existing weak and compromised password detection by automating the rotation process.

[Signal says UK plan to scan devices for nude images 'endangers us all' (3 minute read)](https://www.theregister.com/security/2026/06/09/signal-uks-child-nude-block-threat-wont-protect-children/5252761?utm_source=tldrinfosec) Keir Starmer gives tech firms three months to deploy device-level scanning that blocks minors from taking, sharing, or viewing nude images, or face legislation. Signal warns that client-side scanning and age checks create new surveillance and censorship hooks, expand attack surface via updatable abuse databases or models, and break its privacy trust model even if images stay on-device.

[WhatsApp Says It Blocked Pegasus Spyware Campaign Linked to NSO (3 minute read)](https://hackread.com/whatsapp-blocked-pegasus-spyware-campaign-nso/?utm_source=tldrinfosec) WhatsApp blocked a new NSO Group Pegasus campaign delivered via spear-phishing links rather than a platform vulnerability, removed associated test accounts and groups, and filed for contempt against NSO for violating an existing permanent injunction.

[OpenSSL Patches High-Severity Vulnerability Found With AI (2 minute read)](https://www.securityweek.com/openssl-patches-high-severity-vulnerability-found-with-ai/?utm_source=tldrinfosec) OpenSSL shipped fixes for 18 flaws, including CVE-2026-45447, a heap use-after-free bug in PKCS#7 verification that can lead to remote code execution via crafted PKCS#7 or S/MIME messages.

[Microsoft Patches 200 Vulnerabilities (2 minute read)](https://www.securityweek.com/microsoft-patches-200-vulnerabilities/?utm_source=tldrinfosec) Microsoft's June 2026 Patch Tuesday fixed roughly 200 flaws (nearly 40 rated critical across Windows, Azure, Office, Outlook, Exchange, and AI tools).

### Source URL
https://tldr.tech/infosec/2026-06-10
