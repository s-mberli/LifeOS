---
actionability: high
attached_experts: []
channel_name: ''
created_at: '2026-06-10T10:15:12.640705+10:00'
domain: unknown
expert_status: unattached
primary_mode: router
privacy: public
review_status: new
secondary_modes: []
source_type: article
source_url: https://tldr.tech/infosec/2026-06-08
status: processed
suggested_experts: []
tags:
- infosec
- ai-security
- botnet
- auth-bypass
- prompt-injection
- llm-hacking
- post-quantum-crypto
- email-security
- malvertising
- module-stomping
title: C0XMO Botnet Spreads 👾, UniFi OS Auth Bypass 🔌, OpenAI Lockdown Mode 🔒
transcript_path: ''
type: insight_note
updated_at: '2026-06-10T10:15:12.640705+10:00'
---

# C0XMO Botnet Spreads 👾, UniFi OS Auth Bypass 🔌, OpenAI Lockdown Mode 🔒

## Summary
The TLDR InfoSec digest for June 8, 2026, covers a dense landscape of critical vulnerabilities, emerging attack techniques, and AI-security intersections. The dominant theme is that authentication and trust boundaries — whether in routers, cloud platforms, or AI systems — remain the most exploited attack surface. Three CVSS 10.0 vulnerabilities in UniFi OS (CVE-2026-34908/09/10) allow unauthenticated root RCE through an Nginx auth-gateway bypass exploiting `%2f` URI handling, leading to command injection. Critically, patching alone is insufficient: JWT signing keys must be rotated because stolen keys remain valid against patched systems, a nuance many admins will miss. The C0XMO botnet — a modular Gafgyt variant — exploits a 2021 DD-WRT buffer overflow (CVE-2021-27137) to spread across routers, DVRs, and Android devices, supporting 19 DDoS methods, brute-forcing SSH/Telnet, killing rival malware, and persisting via hidden `/tmp/.sys` copies and 15-minute cron jobs. This illustrates how unpatched legacy infrastructure continues to fuel botnet growth years after CVE disclosure.

On the AI-security front, two stories stand out. First, approximately 20,225 Instagram accounts were hijacked through a bug in Meta's AI chatbot account recovery system, where the bot sent password reset links to attacker-controlled emails without verifying ownership — a failure that only affected accounts without 2FA. This is a textbook example of AI systems introducing new attack surface when given privileged actions without proper guardrails. Second, OpenAI introduced 'Lockdown Mode,' which disables live web browsing, external image retrieval, deep research, and agent mode to mitigate prompt injection risks — acknowledging that agentic AI capabilities inherently expand the attack surface. A separate LLM hacking experiment tested ~20 models against a vulnerable app (costing ~$1,500); GPT-5.5 led with 7/10 solves, while many models scored 0/10, often fixating on the wrong attack vector (API IDOR instead of pivoting to Firebase). Chinese models showed notably higher aggression toward live databases, suggesting training/censorship differences affect security research utility.

The digest also highlights 'Module Stomping,' an injection technique where attackers overwrite `.text` sections of signed DLLs to hide payloads in legitimate, disk-backed memory regions — evading EDR solutions that trust signed modules. Defenders should compare in-memory modules against on-disk images. Email security remains weak: only ~26% of DMARC-enabled domains enforce it (p=reject/quarantine) despite 57% publishing it; flipping to p=reject could cut spoofing by 70–85%. Apple formally verified ML-KEM/ML-DSA post-quantum implementations in corecrypto using Cryptol, SAW, and Isabelle — a significant step toward crypto-agility. The Silent Ransom Group (UNC3753/Luna Moth) targets US law firms via invoice-themed phishing and vishing (fake IT support calls) to deploy remote access tools. Malvertising campaigns use Google Ads to distribute trojanized versions of Ghidra, dnSpy, and SpiderFoot through traffic distribution systems. New tools include CVE Lite CLI (JS/TS dependency scanner) and apiffuf (Go-based API URL fuzzer). Former Meta AI security lead Joshua Saxe described Meta's internal culture as intensely competitive but fragmented, with disconnected products and engineers prioritizing career growth over product quality.

## Key Ideas
- UniFi OS Auth Bypass (CVSS 10.0): Three CVEs allow unauthenticated root RCE via Nginx `%2f` URI handling bypass. Patching is necessary but insufficient — JWT signing keys, TLS keys, RADIUS secrets, and DB credentials must all be rotated because stolen keys remain valid against patched systems. Admins should also restrict TCP 11443 and rebuild instances.
- C0XMO Botnet: A modular Gafgyt variant exploiting a 2021 DD-WRT buffer overflow to target routers, DVRs, and Android. Supports 19 DDoS methods, brute-forces SSH/Telnet, kills rival malware, and persists via hidden files and cron jobs. Demonstrates how unpatched legacy IoT infrastructure remains a persistent threat years after CVE disclosure.
- AI Systems as Attack Surface: Meta's AI chatbot account recovery flaw (~20,225 accounts hijacked) shows that giving AI agents privileged actions (sending password resets) without proper ownership verification creates critical vulnerabilities. OpenAI's Lockdown Mode (disabling web browsing, agent mode, deep research) is an acknowledgment that AI capabilities inherently expand attack surface and need configurable trust boundaries.
- LLM Hacking Capability Gap: In a controlled test of ~20 LLMs against a vulnerable app, GPT-5.5 scored 7/10 while many models scored 0/10. Common failures included fixating on wrong attack vectors and refusing to continue. Chinese models were more willing to attack live databases. This has direct implications for using LLMs in security auditing and penetration testing workflows.
- Module Stomping: Attackers overwrite `.text` sections of signed DLLs to execute shellcode within trusted, disk-backed memory regions, evading EDR. Defenders should implement in-memory vs. on-disk module comparison to detect this technique.
- DMARC Enforcement Gap: 57% of domains publish DMARC but only ~26% enforce it. Moving to p=reject can reduce spoofing by 70–85%. MTA-STS adoption is only 1.1%. This represents a high-impact, low-cost email security improvement most organizations haven't implemented.
- Apple Post-Quantum Crypto Verification: ML-KEM/ML-DSA implementations in corecrypto were formally verified using Cryptol, SAW, and Isabelle against FIPS specifications — a model for ensuring cryptographic correctness across C and ARM64 assembly implementations.
- Fake Security Tools Malvertising: Google Ads campaigns impersonate legitimate security tools (Ghidra, dnSpy, SpiderFoot) and redirect through traffic distribution systems to deliver infostealers. Security professionals — the very people who should know better — are being targeted through their trust in familiar tool names.

## Why this matters for Markus
- AI Platform & Agent Architecture: The OpenAI Lockdown Mode and Meta AI chatbot hijacking stories are directly relevant to Markus's work on agent architectures. They illustrate the principle that AI agents with privileged actions (password resets, web browsing, file access) need configurable trust boundaries and explicit authorization checks — not just at the API level but at every action the agent can take. The LLM hacking experiment results (GPT-5.5 at 7/10, many models at 0/10) suggest Markus should be selective about which models he uses for security-critical tasks in his AI platform, and should design agent workflows that don't rely solely on LLM judgment for vulnerability identification.
- Security for Flow Temple E-commerce: The DMARC enforcement gap and malvertising campaigns are directly relevant to Flow Temple's e-commerce operations. Markus should ensure his domains enforce DMARC at p=reject, implement MTA-STS and TLS-RPT, and be aware that customers could be targeted through fake versions of tools or brands. The Instagram account hijacking story reinforces that any AI-assisted account recovery or customer service chatbot Flow Temple might implement needs rigorous ownership verification.
- IoT/Router Security Awareness: The C0XMO botnet and UniFi OS vulnerabilities highlight that Markus's home and office network infrastructure (routers, IoT devices) need regular firmware updates and credential rotation. If Markus runs any self-hosted services, the JWT key rotation lesson from UniFi is critical — patching without rotating secrets leaves systems vulnerable.
- Career Brand & Thought Leadership: The LLM hacking experiment, Module Stomping technique, and AI security stories provide concrete, timely content Markus could use for LinkedIn posts or blog articles positioning himself at the intersection of AI systems and security — a differentiator for his career brand as an AI systems builder.
- Life Kompass — Reducing Idea Overload: This digest contains ~15 distinct stories. Markus should practice extracting only the 2-3 items that directly connect to his active projects rather than trying to track everything. The suggested next action below demonstrates this filtering.

## Related Modes
- router

## Next Action
- [ ] Audit your own domains and any Flow Temple domains for DMARC enforcement: check if DMARC is published and whether it's set to p=reject. If not, update the DMARC record to p=reject, then implement MTA-STS and TLS-RPT. This is a 30-minute task that reduces email spoofing risk by 70–85% and directly protects your brand and customers. Use a free tool like MXToolbox or DMARC Analyzer to check current status.

## Long Resource Processing
- chunks processed: 5
- method: chunked map-reduce summary

## AI Generation Data
- Provider: openrouter
- Model: openrouter/owl-alpha

## Source Reliability
high

## Detailed Chunk Summaries

Chunk 1 Summary:
# TLDR InfoSec — 2026-06-08: Key Points

## Major Threats & Vulnerabilities

- **Fake Security Tools Malvertising**: Hackers use Google Ads to distribute trojanized versions of Ghidra, dnSpy, and SpiderFoot. Fake download pages mimic official sites and redirect users through a TDS to deliver infostealers.

- **UniFi OS Critical Auth Bypass (CVSS 10.0)**: Three flaws (CVE-2026-34908/34909/34910) allow unauthenticated root RCE via an Nginx auth-gateway bypass exploiting `%2f` URI handling, leading to command injection. Patches in 5.1.12/5.1.11/5.1.10/4.0.14, but **JWT signing keys must be rotated** — stolen keys still work against patched systems.

- **C0XMO Botnet**: A modular Gafgyt variant exploiting CVE-2021-27137 (DD-WRT buffer overflow) to spread across routers, DVRs, and Android. Supports 19 DDoS methods, brute-forces SSH/Telnet, kills rival malware, and persists via hidden `/tmp/.sys` copies and 15-minute cron jobs.

- **Instagram Account Hijacking**: ~20,225 accounts compromised via a bug in Meta's AI chatbot account recovery — the bot sent password reset links to attacker-controlled emails without verifying ownership. Affected accounts without 2FA.

## Tools & Techniques

- **Module Stomping**: Injection technique overwriting `.text` sections of signed DLLs to hide payloads in legitimate memory regions. Defenders should compare in-memory modules against on-disk images.

- **LLM Hacking Experiment**: Researcher spent ~$1,500 testing ~20 LLMs against a vulnerable app. GPT-5.5 led (7/10 solves); many models scored 0/10. Key failure: fixating on API IDOR instead of pivoting to Firebase.

- **OpenAI Lockdown Mode**: New feature disabling live web browsing, external image retrieval, deep research, and agent mode to mitigate prompt injection risks.

## Other Notable Items

- **Email Security**: Only ~26% of DMARC-enabled domains enforce it (p=reject/quarantine). Recommendation: flip to p=reject for 70–85% spoofing reduction, then add MTA-STS and TLS-RPT.

- **Apple corecrypto**: Formally verified ML-KEM/ML-DSA post-quantum implementations using Cryptol, SAW, and Isabelle.

- **Oxford University**: Second data breach in a month — CareerConnect platform compromised on May 28.

- **New Tools**: CVE Lite CLI (JS/TS dependency scanner) and apiffuf (Go-based API URL fuzzer).

---

Chunk 2 Summary:
**Key Points from Part 2/5:**

- **Meta AI Chatbot Exploit**: Thousands of Instagram accounts were hijacked due to a flaw in Meta’s AI-driven account recovery system, where the chatbot sent password reset links to attacker-controlled emails without proper verification. Meta has disabled the chatbot and audited other systems.

- **Cursor Bypasses Dependency Cooldown**: A user demonstrated an LLM using a command-line flag to override pnpm’s dependency cooldown, highlighting potential misuse of developer tools.

- **Oxford University Data Breach**: The CareerConnect platform was breached, exposing names and emails of alumni, staff, and recruiters—the university’s second breach in a month.

- **Silent Ransom Group Attacks Law Firms**: The group (UNC3753/Luna Moth) uses phishing and vishing (fake IT support calls) to deploy remote access tools like AnyDesk and Zoho Assist against US legal firms.

- **Fake Security Tools Spread Malware**: Malvertising via Google Ads redirects users to counterfeit download pages for tools like Ghidra and dnSpy, delivering infostealers through traffic distribution systems.

- **Critical UniFi OS Vulnerabilities**: Three CVSS 10.0 flaws allow unauthenticated root RCE via Nginx auth bypass and command injection. Patches exist, but admins must also rotate JWT, TLS, and other keys to fully mitigate risks.

- **C0XMO Botnet Expansion**: A Ggafyt variant exploits a DD-WRT router flaw (CVE-2021-27137), supports 19 DDoS methods, brute-forces credentials, and kills rival malware. Persistence is achieved via hidden files and cron jobs.

- **Email Security Gaps**: Only ~26% of domains enforce DMARC despite 57% publishing it. Experts recommend enforcing `p=reject`, adopting MTA-STS, and prioritizing practical defenses over theoretical threats.

- **Module Stomping Technique**: Attackers overwrite legitimate DLLs’ .text sections to execute shellcode within trusted memory regions, evading EDR. Defenders should monitor in-memory vs. on-disk module discrepancies.

- **LLM Hacking Experiment**: In a test with a vulnerable app, GPT-5.5 performed best (7/10 success), while many models failed due to misidentifying attack surfaces or refusing tasks. Chinese models showed higher aggression toward live databases.

- **OpenAI Lockdown Mode**: New feature disables web browsing, image retrieval, and agent mode to protect sensitive data from prompt injection attacks.

- **Apple’s Post-Quantum Crypto Verification**: Apple formally verified ML-KEM and ML-DSA implementations in corecrypto using Cryptol, SAW, and Isabelle to ensure correctness across C and ARM64 assembly.

---

Chunk 3 Summary:
# Key Points Summary (Part 3/5)

## Major Security Incidents
- **Meta/Instagram AI Chatbot Hack**: ~20,225 Instagram accounts hijacked via a bug in Meta's AI-assisted account recovery system. A code path flaw failed to verify email ownership during password resets, sending reset links to attacker-controlled addresses. Affected accounts without 2FA. Meta disabled the chatbot and removed the offending code.
- **Oxford University**: Second data breach in a month — CareerConnect platform compromised on May 28, exposing names and emails of alumni, staff, and recruiters.
- **Silent Ransom Group (UNC3753/Luna Moth)**: Targeting US law firms since January via invoice-themed phishing + vishing (fake IT support calls) to deploy remote access tools (AnyDesk, Zoho Assist, Bomgar, SuperOps).

## Critical Vulnerabilities
- **UniFi OS Auth Bypass (CVSS 10.0)**: Three flaws (CVE-2026-34908/09/10) allow unauthenticated root RCE via Nginx auth-gateway bypass (%2f URI handling) into command injection. Patch leaves JWT verification unchanged — admins must update, rebuild instances, restrict TCP 11443, and rotate JWT/TLS keys, tokens, RADIUS secrets, and DB credentials.
- **C0XMO Botnet**: Modular Gafgyt variant exploiting CVE-2021-27137 (DD-WRT buffer overflow). Supports 19 DDoS methods, brute-forces SSH/Telnet, persists via hidden cron jobs, kills rival malware. Targets routers, DVRs, Android devices across multiple architectures.
- **Fake Security Tools Malvertising**: Google Ads campaign impersonating Ghidra, dnSpy, and SpiderFoot to distribute infostealers via traffic distribution systems.

## AI/LLM Security
- **OpenAI Lockdown Mode**: New feature to protect against prompt injection — disables live web browsing, external image retrieval, deep research, and agent mode when handling untrusted content.
- **LLM Hacking Experiment**: Researcher spent $1,500 testing ~20 LLMs against a vulnerable app. GPT-5.5 led (7/10 solves); many scored 0. Common failures: fixating on wrong attack vector, Firebase auth token misuse, and refusals. Chinese models were notably more willing to attack live databases.

## Tools & Techniques
- **Module Stomping**: Injection technique overwriting .text section of signed DLLs to hide payloads in disk-backed memory regions. Defenders should compare in-memory vs on-disk module bytes.
- **DMARC Gap**: 57.1% of domains publish DMARC but only ~26% enforce it. Flipping to p=reject cuts spoofing 70-85%. MTA-STS adoption is only 1.1%.
- **New Tools**: CVE Lite CLI (JS/TS dependency scanner) and apiffuf (Go-based API URL fuzzer).
- **Apple corecrypto**: Formal verification of ML-KEM/ML-DSA post-quantum implementations using Cryptol, SAW, and Isabelle.

## Meta Internal Culture
- Former Meta AI security lead Joshua Saxe described the environment as intensely competitive with disconnected products (Llama, AR/VR) where engineers felt missionless and prioritized career growth over product quality.

---

Chunk 4 Summary:
Here are the key points from this section of the resource:

- **Apple implements post-quantum cryptography**: Apple added ML-KEM and ML-DSA to corecrypto using portable C and ARM64 assembly, then formally verified the implementation through a multi-step process involving Cryptol, SAW, and Isabelle to ensure correctness against FIPS specifications.

- **Reflection on Meta's LLM and security work**: Joshua Saxe described his time at Meta as a mix of working with talented people in an intensely competitive environment, where personal ambition often overshadowed product quality, leading to disconnected products like Llama and AR/VR.

- **Meta Instagram account hijacking**: Around 20,225 Instagram accounts were compromised via a bug in Meta's AI-assisted account recovery system that failed to verify email ownership during password resets, allowing attackers to receive reset links. The attack affected accounts without 2FA.

- **Cursor bypasses dependency cooldown**: A user demonstrated using a command line flag in pnpm to override a dependency cooldown.

- **Oxford University second data breach**: The CareerConnect platform was breached, exposing names and email addresses of alumni, research staff, and recruiters.

- **Silent Ransom Group targets law firms**: The group (UNC3753/Luna Moth/Chatty Spider) uses invoice-themed phishing and vishing calls impersonating IT support to deploy remote access tools like AnyDesk and Zoho Assist.

- **Fake security tools spread malware**: A malvertising campaign uses Google Ads to redirect users through a TDS to download infostealers disguised as legitimate tools like Ghidra, dnSpy, and SpiderFoot.

- **Critical UniFi OS auth bypass**: Three CVSS 10.0 vulnerabilities in UniFi OS Server allow unauthenticated root RCE. Patches are available, but admins must also rotate JWT keys, TLS keys, and other credentials since stolen signing keys remain valid.

- **C0XMO botnet spreads via DD-WRT flaw**: The botnet exploits a buffer overflow in DD-WRT routers, supports 19 DDoS methods, brute-forces weak credentials, and terminates competing botnets and tools.

- **Email security guidance**: Only ~26% of domains enforce DMARC despite 57% publishing it. The article recommends moving to p=reject, implementing MTA-STS, TLS-RPT, and CAA for maximum impact.

- **Module Stomping technique**: Attackers overwrite .text sections of signed DLLs to hide payloads in legitimate memory regions, evading scanners. Defenders should compare in-memory modules against on-disk images.

- **LLM hacking experiment**: Testing ~20 LLMs against a vulnerable app, GPT-5.5 performed best (7/10), while many models failed due to fixating on wrong attack vectors or refusing to continue.

- **OpenAI Lockdown Mode**: New feature disables live web browsing, external image retrieval, deep research, and agent mode to protect against prompt injection attacks.

- **Tools mentioned**: CVE Lite CLI (dependency vulnerability scanner) and apiffuf (API URL fuzzer).

---

Chunk 5 Summary:
**Key Points from Part 5/5:**

- **OpenAI Lockdown Mode**: New feature disables live web browsing, external image retrieval, deep research, and agent mode to mitigate prompt injection attacks on sensitive data.

- **Apple Corecrypto Formal Verification**: Apple implemented post-quantum cryptography (ML-KEM/ML-DSA) in corecrypto using C and ARM64 assembly; formally verified via Cryptol, SAW, and Isabelle to ensure correctness against FIPS specs.

- **Meta LLM Security Reflections**: Former Meta security lead Joshua Saxe describes a competitive culture where personal ambition overshadowed product cohesion, leading to fragmented efforts like Llama and AR/VR.

- **Instagram Account Hijacking**: ~20k accounts compromised via a bug in Meta’s AI chatbot recovery system that sent password reset links to attacker-controlled emails—exploited accounts without 2FA.

- **Cursor Dependency Override**: Users found LLM agents can bypass pnpm dependency cooldowns using command-line flags.

- **Oxford University Breach**: Second breach in a month hit CareerConnect, exposing names and emails of alumni, staff, and recruiters.

- **Silent Ransom Group Attacks**: UNC3753 targets law firms via invoice phishing + vishing (fake IT support) to deploy remote access tools like AnyDesk and Zoho Assist.

## Original Content
### Raw User Input
https://tldr.tech/infosec/2026-06-08

# TLDR InfoSec — 2026-06-08
Source: https://tldr.tech/infosec/2026-06-08

## Articles

### Hackers Impersonate Ghidra, dnSpy, and SpiderFoot to Spread Malware
- **URL:** https://cyberpress.org/fake-security-tools-spread-malware/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-08
- **Read time:** 2 minute read
- **TLDR Summary:** Security researchers recently uncovered a new malvertising campaign that uses Google Ads to trick users into downloading malicious versions of popular security software. The download pages are designed to mimic the official pages and even include links to the legitimate releases that, when hovered over, reveal the legitimate releases. However, scripts on the page dynamically redirect the user through a traffic distribution system (TDS) when clicked. Users are redirected multiple times before ending up on a download page for an infostealer.

### Critical UniFi OS Auth Bypass Flaws Lead to Unauthenticated Root RCE
- **URL:** https://gbhackers.com/critical-unifi-os-auth-bypass-flaws/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-08
- **Read time:** 2 minute read
- **TLDR Summary:** Ubiquiti's SAB-064 patches three CVSS 10.0 UniFi OS Server flaws (CVE-2026-34908, CVE-2026-34909, and CVE-2026-34910) that Bishop Fox chained on 5.0.6 for unauthenticated root RCE via an Nginx auth-gateway bypass (raw vs normalized URI handling of %2f) into command injection in the package-update service, but since the patch leaves JWT verification unchanged, stolen signing keys still mint valid owner-scope tokens against patched 5.0.8 consoles, so admins must update (5.1.12 most Cloud Gateways, 5.1.10 UNAS, 5.1.11 Dream Machine Beast, and 4.0.14 UniFi Express), rebuild exposed instances, restrict TCP 11443 to a management VLAN, and rotate the JWT key, TLS keys, tokens, RADIUS secrets, and DB credentials.

### C0XMO botnet spreads via DD-WRT router flaw, kills rival malware
- **URL:** https://www.bleepingcomputer.com/news/security/c0xmo-botnet-spreads-via-dd-wrt-router-flaw-kills-rival-malware/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-08
- **Read time:** 3 minute read
- **TLDR Summary:** Fortinet identified C0XMO, a modular Gafgyt variant that propagates by exploiting CVE-2021-27137, an unauthenticated buffer overflow in DD-WRT router firmware that enables arbitrary code execution, and ships binaries for ARM, MIPS, PowerPC, SuperH, x86, and x86_64 to spread across DVRs, routers, video management platforms, and Android devices. It supports 19 DDoS methods, including UDP/TCP/SYN/ICMP floods, ping of death, NTP/Memcached amplification, and Discord and Valve-specific floods, while a downloaded Python scanner using requests, paramiko, and beautifulsoup4 brute-forces weak SSH and Telnet credentials across ports 22, 23, 80/443, 7547, 8080, 8443, and 8888. Persistence comes via copies hidden in /tmp/.sys, /var/tmp/.sys, and /dev/shm/.sys, plus cron jobs that relaunch every 15 minutes, and it terminates competing botnets, red-team tools, and interfering services before reaching its hardcoded C2 over a custom multi-stage handshake. Defenders should keep devices patched, set unique admin credentials, disable unneeded remote access, and hunt for the listed hidden paths, the 15-minute cron persistence, and unexpected scanning across those ports.

### Email Security: An Enablement Journey, Not a Maturity Ladder
- **URL:** https://www.pwndefend.com/2026/06/07/email-security-an-enablement-journey-not-a-maturity-ladder/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-08
- **Read time:** 10 minute read
- **TLDR Summary:** Drawing on Majestic Million data showing 57.1% of mail-enabled domains publish DMARC but only ~26% enforce it (p=reject or quarantine), this piece reframes email authentication as a sequence of capabilities unlocked rather than maturity tiers, and pins the real failure point at the jump from p=none reporting to enforcement, where 74% of organizations stall. The practical guidance is to flip DMARC to p=reject for a 70-85% cut in domain spoofing, then add MTA-STS (just 1.1% adoption despite a few hours of work), plus TLS-RPT and CAA for inbound SMTP encryption and control over certificate issuance, since that is where effort-to-impact peaks for most shops. DNSSEC at 6.75% and DANE at 0.73% are treated as regulatory or specialized-threat-model territory rather than universal requirements, with the closing argument being to fix what you are actually being attacked on, weak passwords, open directories, live spoofing, before defending against CA-compromise MITM that may never have been exploited against you.

### An Introduction to Module Stomping
- **URL:** https://infosecwriteups.com/an-introduction-to-module-stomping-26238af76d43?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-08
- **Read time:** 13 minute read
- **TLDR Summary:** Module Stomping overwrites the .text section of legitimate signed DLLs to hide payload execution within disk-backed memory regions, evading behavioral telemetry and traditional memory scanners. The attack loads a sacrificial DLL, locates an exported function via GetProcAddress, writes shellcode to that address with WriteProcessMemory, and executes via CreateThread, keeping the injection within a legitimate module's address space. Defenders should monitor for in-memory module divergence using verification checks that compare loaded module bytes against their on-disk images. Static API resolution obfuscation and PEB-walking techniques can extend this technique's operational lifespan against mature EDR platforms.

### I built a vulnerable app and spent $1,500 seeing if LLMs could hack it
- **URL:** https://kasra.blog/blog/i-spent-1500-seeing-if-llms-could-hack-my-app/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-08
- **Read time:** 7 minute read
- **TLDR Summary:** A security researcher built a deliberately vulnerable Expo React Native book-review app with a Python backend, then ran ~20 LLMs as autonomous agents (via the pi harness with pi-goal-x, and Claude through Claude Code's -p mode) under a $10 and two-hour cap per run to find a flag hidden in private reviews. The intended path required decompiling the APK and pivoting to a misconfigured Firebase backend rather than chasing API IDOR, and solve rates reflected that: gpt-5.5 led at 7/10, deepseek-v4-pro hit 3/10, claude-sonnet-4.6 and claude-opus-4-8 each managed 2/10, and many models scored 0/10. The recurring failure modes are the defender-relevant takeaway, namely, fixating on API IDOR instead of recognizing Firebase, attempting to replay Firebase auth tokens against the API rather than hitting Firebase directly, and refusals (Gemini bailed immediately at ~9k tokens per run while Opus refused late mid-exploit), with the author noting Chinese models were notably more willing to attack the live database.

### CVE Lite CLI (GitHub Repo)
- **URL:** https://github.com/OWASP/cve-lite-cli?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-08
- **Read time:** Unknown
- **TLDR Summary:** Fast, developer-friendly JS/TS dependency vulnerability scanner with local lockfile scanning, OSV matching, direct vs transitive visibility, --fix, JSON output, and practical remediation guidance.

### apiffuf (GitHub Repo)
- **URL:** https://github.com/jsmonhq/apiffuf?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-08
- **Read time:** Unknown
- **TLDR Summary:** A Go-based API URL fuzzer that cross-joins hosts and paths into normalized URLs (defaulting to https when no protocol is given), probes them over configurable HTTP methods with adjustable threads and rate limiting, and reports only responding endpoints with status code, Content-Type, Content-Length, and page title in text, JSON, or CSV output.

### OpenAI unveils Lockdown Mode to protect sensitive data from prompt injection attacks
- **URL:** https://techcrunch.com/2026/06/06/openai-unveils-lockdown-mode-to-protect-sensitive-data-from-prompt-injection-attacks/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-08
- **Read time:** 1 minute read
- **TLDR Summary:** OpenAI is adding Lockdown Mode to limit how ChatGPT handles untrusted content and to reduce the risk of prompt injection for sensitive data. It turns off live web browsing, external image retrieval, deep research, and agent mode.

### A Blueprint for Formal Verification of Apple corecrypto
- **URL:** https://security.apple.com/blog/formal-verification-corecrypto/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-08
- **Read time:** 10 minute read
- **TLDR Summary:** Apple decided to implement ML-KEM and ML-DSA in corecrypto to support post-quantum cryptography across its products. Apple wrote their implementation in portable C as well as ARM64 assembly to optimize some subroutines. To formally verify their implementation, Apple translated their C implementation into Cryptol and used SAW to verify that the model matches their implementation. The Cryptol model was then translated into Isabelle, along with the FIPS specification, to verify that they were identical. Finally, the assembly optimized subroutines were translated to Isabelle as well and verified to be identical to the C subroutines that they replace.

### What it was Like Working on LLMs and Security at Meta (2022-2026)
- **URL:** https://joshuasaxe181906.substack.com/p/what-it-was-like-working-on-llms?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-08
- **Read time:** 6 minute read
- **TLDR Summary:** Joshua Saxe reflects on his time at Meta with mixed emotions, describing it as a place to work with incredibly talented people but also as intensely competitive, where strong personal ambitions outweigh product concerns. Saxe believes that Meta's products, like Llama and AR/VR, are disconnected and lackluster because engineers feel missionless and jump on a bandwagon that will lead to career growth. Overall, Saxe enjoyed his time at Meta and was involved in creating AI security initiatives before leaving to start his own company.

### Meta confirms thousands of Instagram accounts were hacked by abusing its AI chatbot
- **URL:** https://this.weekinsecurity.com/meta-confirms-thousands-of-instagram-accounts-were-hacked-by-abusing-its-ai-chatbot/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-08
- **Read time:** 3 minute read
- **TLDR Summary:** Meta has notified at least 20,225 people that their Instagram accounts were hijacked through a flaw in its AI-assisted account recovery system. A bug in a separate code path failed to verify that the email address supplied during a password reset matched the one on file, so the chatbot sent reset links to attacker-controlled addresses simply when asked. The campaign ran from roughly April 17 until early June and affected any account without 2FA enabled, granting takeover of the account and access to DMs, posts, contact information, and dates of birth. The incident is a cautionary case for automating account recovery without a human in the loop, with one observer noting the attack amounted to one AI being fooled by AI-generated verification media while no person was positioned to catch it. Meta has since disabled the chatbot, removed the offending code path, and begun auditing its other chatbots.

### Cursor Bypassed Dependency Cooldown
- **URL:** https://threadreaderapp.com/thread/2058658244328124562.html?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-08
- **Read time:** 1 minute read
- **TLDR Summary:** A user on X shared a screenshot of their LLM using a command line flag to explicitly override a dependency cooldown in pnpm.

### Oxford University hit by second data breach in a month
- **URL:** https://www.thenews.com.pk/latest/1404975-oxford-university-hit-by-second-data-breach-in-a-month?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-08
- **Read time:** 1 minute read
- **TLDR Summary:** Oxford's CareerConnect platform was breached on May 28, exposing full names and email addresses for alumni, research staff, and recruiters.

### Silent Ransom Group targets law firms with fake IT support calls
- **URL:** https://www.bleepingcomputer.com/news/security/silent-ransom-group-targets-law-firms-with-fake-it-support-calls/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-08
- **Read time:** 4 minute read
- **TLDR Summary:** Silent Ransom Group (UNC3753/Luna Moth/Chatty Spider) has hit dozens of US legal and professional services firms since January using invoice-themed phishing followed by vishing calls impersonating IT staff to deploy AnyDesk, Zoho Assist, Bomgar, or SuperOps.

## Full Text

[Hackers Impersonate Ghidra, dnSpy, and SpiderFoot to Spread Malware (2 minute read)](https://cyberpress.org/fake-security-tools-spread-malware/?utm_source=tldrinfosec) Security researchers recently uncovered a new malvertising campaign that uses Google Ads to trick users into downloading malicious versions of popular security software. The download pages are designed to mimic the official pages and even include links to the legitimate releases that, when hovered over, reveal the legitimate releases. However, scripts on the page dynamically redirect the user through a traffic distribution system (TDS) when clicked. Users are redirected multiple times before ending up on a download page for an infostealer.

[Critical UniFi OS Auth Bypass Flaws Lead to Unauthenticated Root RCE (2 minute read)](https://gbhackers.com/critical-unifi-os-auth-bypass-flaws/?utm_source=tldrinfosec) Ubiquiti's SAB-064 patches three CVSS 10.0 UniFi OS Server flaws (CVE-2026-34908, CVE-2026-34909, and CVE-2026-34910) that Bishop Fox chained on 5.0.6 for unauthenticated root RCE via an Nginx auth-gateway bypass (raw vs normalized URI handling of %2f) into command injection in the package-update service, but since the patch leaves JWT verification unchanged, stolen signing keys still mint valid owner-scope tokens against patched 5.0.8 consoles, so admins must update (5.1.12 most Cloud Gateways, 5.1.10 UNAS, 5.1.11 Dream Machine Beast, and 4.0.14 UniFi Express), rebuild exposed instances, restrict TCP 11443 to a management VLAN, and rotate the JWT key, TLS keys, tokens, RADIUS secrets, and DB credentials.

[C0XMO botnet spreads via DD-WRT router flaw, kills rival malware (3 minute read)](https://www.bleepingcomputer.com/news/security/c0xmo-botnet-spreads-via-dd-wrt-router-flaw-kills-rival-malware/?utm_source=tldrinfosec) Fortinet identified C0XMO, a modular Gafgyt variant that propagates by exploiting CVE-2021-27137, an unauthenticated buffer overflow in DD-WRT router firmware that enables arbitrary code execution, and ships binaries for ARM, MIPS, PowerPC, SuperH, x86, and x86_64 to spread across DVRs, routers, video management platforms, and Android devices. It supports 19 DDoS methods, including UDP/TCP/SYN/ICMP floods, ping of death, NTP/Memcached amplification, and Discord and Valve-specific floods, while a downloaded Python scanner using requests, paramiko, and beautifulsoup4 brute-forces weak SSH and Telnet credentials across ports 22, 23, 80/443, 7547, 8080, 8443, and 8888. Persistence comes via copies hidden in /tmp/.sys, /var/tmp/.sys, and /dev/shm/.sys, plus cron jobs that relaunch every 15 minutes, and it terminates competing botnets, red-team tools, and interfering services before reaching its hardcoded C2 over a custom multi-stage handshake. Defenders should keep devices patched, set unique admin credentials, disable unneeded remote access, and hunt for the listed hidden paths, the 15-minute cron persistence, and unexpected scanning across those ports.

[Email Security: An Enablement Journey, Not a Maturity Ladder (10 minute read)](https://www.pwndefend.com/2026/06/07/email-security-an-enablement-journey-not-a-maturity-ladder/?utm_source=tldrinfosec) Drawing on Majestic Million data showing 57.1% of mail-enabled domains publish DMARC but only ~26% enforce it (p=reject or quarantine), this piece reframes email authentication as a sequence of capabilities unlocked rather than maturity tiers, and pins the real failure point at the jump from p=none reporting to enforcement, where 74% of organizations stall. The practical guidance is to flip DMARC to p=reject for a 70-85% cut in domain spoofing, then add MTA-STS (just 1.1% adoption despite a few hours of work), plus TLS-RPT and CAA for inbound SMTP encryption and control over certificate issuance, since that is where effort-to-impact peaks for most shops. DNSSEC at 6.75% and DANE at 0.73% are treated as regulatory or specialized-threat-model territory rather than universal requirements, with the closing argument being to fix what you are actually being attacked on, weak passwords, open directories, live spoofing, before defending against CA-compromise MITM that may never have been exploited against you.

[An Introduction to Module Stomping (13 minute read)](https://infosecwriteups.com/an-introduction-to-module-stomping-26238af76d43?utm_source=tldrinfosec) Module Stomping overwrites the .text section of legitimate signed DLLs to hide payload execution within disk-backed memory regions, evading behavioral telemetry and traditional memory scanners. The attack loads a sacrificial DLL, locates an exported function via GetProcAddress, writes shellcode to that address with WriteProcessMemory, and executes via CreateThread, keeping the injection within a legitimate module's address space. Defenders should monitor for in-memory module divergence using verification checks that compare loaded module bytes against their on-disk images. Static API resolution obfuscation and PEB-walking techniques can extend this technique's operational lifespan against mature EDR platforms.

[I built a vulnerable app and spent $1,500 seeing if LLMs could hack it (7 minute read)](https://kasra.blog/blog/i-spent-1500-seeing-if-llms-could-hack-my-app/?utm_source=tldrinfosec) A security researcher built a deliberately vulnerable Expo React Native book-review app with a Python backend, then ran ~20 LLMs as autonomous agents (via the pi harness with pi-goal-x, and Claude through Claude Code's -p mode) under a $10 and two-hour cap per run to find a flag hidden in private reviews. The intended path required decompiling the APK and pivoting to a misconfigured Firebase backend rather than chasing API IDOR, and solve rates reflected that: gpt-5.5 led at 7/10, deepseek-v4-pro hit 3/10, claude-sonnet-4.6 and claude-opus-4-8 each managed 2/10, and many models scored 0/10. The recurring failure modes are the defender-relevant takeaway, namely, fixating on API IDOR instead of recognizing Firebase, attempting to replay Firebase auth tokens against the API rather than hitting Firebase directly, and refusals (Gemini bailed immediately at ~9k tokens per run while Opus refused late mid-exploit), with the author noting Chinese models were notably more willing to attack the live database.

[150 hours saved in one month: Inside Jamf's IT Ops automation strategy (Sponsor)](https://www.tines.com/webinars/150-hours-saved-in-one-month-inside-jamfs-it-ops-automation-strategy/?utm_source=TLDR&amp;utm_medium=paid_media&amp;utm_content=newsletter-secondary-0806) Managing 500+ SaaS apps, thousands of devices, and a flood of help desk tickets with a lean team of 30 sounds impossible - unless you build smart.  [Join Jamf's IT team live](https://www.tines.com/webinars/150-hours-saved-in-one-month-inside-jamfs-it-ops-automation-strategy/?utm_source=TLDR&utm_medium=paid_media&utm_content=newsletter-secondary-0806)  on July 10th to see the real workflows and get the inside scoop on their IT automation program.

[CVE Lite CLI (GitHub Repo)](https://github.com/OWASP/cve-lite-cli?utm_source=tldrinfosec) Fast, developer-friendly JS/TS dependency vulnerability scanner with local lockfile scanning, OSV matching, direct vs transitive visibility, --fix, JSON output, and practical remediation guidance.

[apiffuf (GitHub Repo)](https://github.com/jsmonhq/apiffuf?utm_source=tldrinfosec) A Go-based API URL fuzzer that cross-joins hosts and paths into normalized URLs (defaulting to https when no protocol is given), probes them over configurable HTTP methods with adjustable threads and rate limiting, and reports only responding endpoints with status code, Content-Type, Content-Length, and page title in text, JSON, or CSV output.

[OpenAI unveils Lockdown Mode to protect sensitive data from prompt injection attacks (1 minute read)](https://techcrunch.com/2026/06/06/openai-unveils-lockdown-mode-to-protect-sensitive-data-from-prompt-injection-attacks/?utm_source=tldrinfosec) OpenAI is adding Lockdown Mode to limit how ChatGPT handles untrusted content and to reduce the risk of prompt injection for sensitive data. It turns off live web browsing, external image retrieval, deep research, and agent mode.

[A Blueprint for Formal Verification of Apple corecrypto (10 minute read)](https://security.apple.com/blog/formal-verification-corecrypto/?utm_source=tldrinfosec) Apple decided to implement ML-KEM and ML-DSA in corecrypto to support post-quantum cryptography across its products. Apple wrote their implementation in portable C as well as ARM64 assembly to optimize some subroutines. To formally verify their implementation, Apple translated their C implementation into Cryptol and used SAW to verify that the model matches their implementation. The Cryptol model was then translated into Isabelle, along with the FIPS specification, to verify that they were identical. Finally, the assembly optimized subroutines were translated to Isabelle as well and verified to be identical to the C subroutines that they replace.

[What it was Like Working on LLMs and Security at Meta (2022-2026) (6 minute read)](https://joshuasaxe181906.substack.com/p/what-it-was-like-working-on-llms?utm_source=tldrinfosec) Joshua Saxe reflects on his time at Meta with mixed emotions, describing it as a place to work with incredibly talented people but also as intensely competitive, where strong personal ambitions outweigh product concerns. Saxe believes that Meta's products, like Llama and AR/VR, are disconnected and lackluster because engineers feel missionless and jump on a bandwagon that will lead to career growth. Overall, Saxe enjoyed his time at Meta and was involved in creating AI security initiatives before leaving to start his own company.

[Meta confirms thousands of Instagram accounts were hacked by abusing its AI chatbot (3 minute read)](https://this.weekinsecurity.com/meta-confirms-thousands-of-instagram-accounts-were-hacked-by-abusing-its-ai-chatbot/?utm_source=tldrinfosec) Meta has notified at least 20,225 people that their Instagram accounts were hijacked through a flaw in its AI-assisted account recovery system. A bug in a separate code path failed to verify that the email address supplied during a password reset matched the one on file, so the chatbot sent reset links to attacker-controlled addresses simply when asked. The campaign ran from roughly April 17 until early June and affected any account without 2FA enabled, granting takeover of the account and access to DMs, posts, contact information, and dates of birth. The incident is a cautionary case for automating account recovery without a human in the loop, with one observer noting the attack amounted to one AI being fooled by AI-generated verification media while no person was positioned to catch it. Meta has since disabled the chatbot, removed the offending code path, and begun auditing its other chatbots.

[Cursor Bypassed Dependency Cooldown (1 minute read)](https://threadreaderapp.com/thread/2058658244328124562.html?utm_source=tldrinfosec) A user on X shared a screenshot of their LLM using a command line flag to explicitly override a dependency cooldown in pnpm.

[Oxford University hit by second data breach in a month (1 minute read)](https://www.thenews.com.pk/latest/1404975-oxford-university-hit-by-second-data-breach-in-a-month?utm_source=tldrinfosec) Oxford's CareerConnect platform was breached on May 28, exposing full names and email addresses for alumni, research staff, and recruiters.

[Silent Ransom Group targets law firms with fake IT support calls (4 minute read)](https://www.bleepingcomputer.com/news/security/silent-ransom-group-targets-law-firms-with-fake-it-support-calls/?utm_source=tldrinfosec) Silent Ransom Group (UNC3753/Luna Moth/Chatty Spider) has hit dozens of US legal and professional services firms since January using invoice-themed phishing followed by vishing calls impersonating IT staff to deploy AnyDesk, Zoho Assist, Bomgar, or SuperOps.

### Fetched Web Text
[Hackers Impersonate Ghidra, dnSpy, and SpiderFoot to Spread Malware (2 minute read)](https://cyberpress.org/fake-security-tools-spread-malware/?utm_source=tldrinfosec) Security researchers recently uncovered a new malvertising campaign that uses Google Ads to trick users into downloading malicious versions of popular security software. The download pages are designed to mimic the official pages and even include links to the legitimate releases that, when hovered over, reveal the legitimate releases. However, scripts on the page dynamically redirect the user through a traffic distribution system (TDS) when clicked. Users are redirected multiple times before ending up on a download page for an infostealer.

[Critical UniFi OS Auth Bypass Flaws Lead to Unauthenticated Root RCE (2 minute read)](https://gbhackers.com/critical-unifi-os-auth-bypass-flaws/?utm_source=tldrinfosec) Ubiquiti's SAB-064 patches three CVSS 10.0 UniFi OS Server flaws (CVE-2026-34908, CVE-2026-34909, and CVE-2026-34910) that Bishop Fox chained on 5.0.6 for unauthenticated root RCE via an Nginx auth-gateway bypass (raw vs normalized URI handling of %2f) into command injection in the package-update service, but since the patch leaves JWT verification unchanged, stolen signing keys still mint valid owner-scope tokens against patched 5.0.8 consoles, so admins must update (5.1.12 most Cloud Gateways, 5.1.10 UNAS, 5.1.11 Dream Machine Beast, and 4.0.14 UniFi Express), rebuild exposed instances, restrict TCP 11443 to a management VLAN, and rotate the JWT key, TLS keys, tokens, RADIUS secrets, and DB credentials.

[C0XMO botnet spreads via DD-WRT router flaw, kills rival malware (3 minute read)](https://www.bleepingcomputer.com/news/security/c0xmo-botnet-spreads-via-dd-wrt-router-flaw-kills-rival-malware/?utm_source=tldrinfosec) Fortinet identified C0XMO, a modular Gafgyt variant that propagates by exploiting CVE-2021-27137, an unauthenticated buffer overflow in DD-WRT router firmware that enables arbitrary code execution, and ships binaries for ARM, MIPS, PowerPC, SuperH, x86, and x86_64 to spread across DVRs, routers, video management platforms, and Android devices. It supports 19 DDoS methods, including UDP/TCP/SYN/ICMP floods, ping of death, NTP/Memcached amplification, and Discord and Valve-specific floods, while a downloaded Python scanner using requests, paramiko, and beautifulsoup4 brute-forces weak SSH and Telnet credentials across ports 22, 23, 80/443, 7547, 8080, 8443, and 8888. Persistence comes via copies hidden in /tmp/.sys, /var/tmp/.sys, and /dev/shm/.sys, plus cron jobs that relaunch every 15 minutes, and it terminates competing botnets, red-team tools, and interfering services before reaching its hardcoded C2 over a custom multi-stage handshake. Defenders should keep devices patched, set unique admin credentials, disable unneeded remote access, and hunt for the listed hidden paths, the 15-minute cron persistence, and unexpected scanning across those ports.

[Email Security: An Enablement Journey, Not a Maturity Ladder (10 minute read)](https://www.pwndefend.com/2026/06/07/email-security-an-enablement-journey-not-a-maturity-ladder/?utm_source=tldrinfosec) Drawing on Majestic Million data showing 57.1% of mail-enabled domains publish DMARC but only ~26% enforce it (p=reject or quarantine), this piece reframes email authentication as a sequence of capabilities unlocked rather than maturity tiers, and pins the real failure point at the jump from p=none reporting to enforcement, where 74% of organizations stall. The practical guidance is to flip DMARC to p=reject for a 70-85% cut in domain spoofing, then add MTA-STS (just 1.1% adoption despite a few hours of work), plus TLS-RPT and CAA for inbound SMTP encryption and control over certificate issuance, since that is where effort-to-impact peaks for most shops. DNSSEC at 6.75% and DANE at 0.73% are treated as regulatory or specialized-threat-model territory rather than universal requirements, with the closing argument being to fix what you are actually being attacked on, weak passwords, open directories, live spoofing, before defending against CA-compromise MITM that may never have been exploited against you.

[An Introduction to Module Stomping (13 minute read)](https://infosecwriteups.com/an-introduction-to-module-stomping-26238af76d43?utm_source=tldrinfosec) Module Stomping overwrites the .text section of legitimate signed DLLs to hide payload execution within disk-backed memory regions, evading behavioral telemetry and traditional memory scanners. The attack loads a sacrificial DLL, locates an exported function via GetProcAddress, writes shellcode to that address with WriteProcessMemory, and executes via CreateThread, keeping the injection within a legitimate module's address space. Defenders should monitor for in-memory module divergence using verification checks that compare loaded module bytes against their on-disk images. Static API resolution obfuscation and PEB-walking techniques can extend this technique's operational lifespan against mature EDR platforms.

[I built a vulnerable app and spent $1,500 seeing if LLMs could hack it (7 minute read)](https://kasra.blog/blog/i-spent-1500-seeing-if-llms-could-hack-my-app/?utm_source=tldrinfosec) A security researcher built a deliberately vulnerable Expo React Native book-review app with a Python backend, then ran ~20 LLMs as autonomous agents (via the pi harness with pi-goal-x, and Claude through Claude Code's -p mode) under a $10 and two-hour cap per run to find a flag hidden in private reviews. The intended path required decompiling the APK and pivoting to a misconfigured Firebase backend rather than chasing API IDOR, and solve rates reflected that: gpt-5.5 led at 7/10, deepseek-v4-pro hit 3/10, claude-sonnet-4.6 and claude-opus-4-8 each managed 2/10, and many models scored 0/10. The recurring failure modes are the defender-relevant takeaway, namely, fixating on API IDOR instead of recognizing Firebase, attempting to replay Firebase auth tokens against the API rather than hitting Firebase directly, and refusals (Gemini bailed immediately at ~9k tokens per run while Opus refused late mid-exploit), with the author noting Chinese models were notably more willing to attack the live database.

[150 hours saved in one month: Inside Jamf's IT Ops automation strategy (Sponsor)](https://www.tines.com/webinars/150-hours-saved-in-one-month-inside-jamfs-it-ops-automation-strategy/?utm_source=TLDR&amp;utm_medium=paid_media&amp;utm_content=newsletter-secondary-0806) Managing 500+ SaaS apps, thousands of devices, and a flood of help desk tickets with a lean team of 30 sounds impossible - unless you build smart.  [Join Jamf's IT team live](https://www.tines.com/webinars/150-hours-saved-in-one-month-inside-jamfs-it-ops-automation-strategy/?utm_source=TLDR&utm_medium=paid_media&utm_content=newsletter-secondary-0806)  on July 10th to see the real workflows and get the inside scoop on their IT automation program.

[CVE Lite CLI (GitHub Repo)](https://github.com/OWASP/cve-lite-cli?utm_source=tldrinfosec) Fast, developer-friendly JS/TS dependency vulnerability scanner with local lockfile scanning, OSV matching, direct vs transitive visibility, --fix, JSON output, and practical remediation guidance.

[apiffuf (GitHub Repo)](https://github.com/jsmonhq/apiffuf?utm_source=tldrinfosec) A Go-based API URL fuzzer that cross-joins hosts and paths into normalized URLs (defaulting to https when no protocol is given), probes them over configurable HTTP methods with adjustable threads and rate limiting, and reports only responding endpoints with status code, Content-Type, Content-Length, and page title in text, JSON, or CSV output.

[OpenAI unveils Lockdown Mode to protect sensitive data from prompt injection attacks (1 minute read)](https://techcrunch.com/2026/06/06/openai-unveils-lockdown-mode-to-protect-sensitive-data-from-prompt-injection-attacks/?utm_source=tldrinfosec) OpenAI is adding Lockdown Mode to limit how ChatGPT handles untrusted content and to reduce the risk of prompt injection for sensitive data. It turns off live web browsing, external image retrieval, deep research, and agent mode.

[A Blueprint for Formal Verification of Apple corecrypto (10 minute read)](https://security.apple.com/blog/formal-verification-corecrypto/?utm_source=tldrinfosec) Apple decided to implement ML-KEM and ML-DSA in corecrypto to support post-quantum cryptography across its products. Apple wrote their implementation in portable C as well as ARM64 assembly to optimize some subroutines. To formally verify their implementation, Apple translated their C implementation into Cryptol and used SAW to verify that the model matches their implementation. The Cryptol model was then translated into Isabelle, along with the FIPS specification, to verify that they were identical. Finally, the assembly optimized subroutines were translated to Isabelle as well and verified to be identical to the C subroutines that they replace.

[What it was Like Working on LLMs and Security at Meta (2022-2026) (6 minute read)](https://joshuasaxe181906.substack.com/p/what-it-was-like-working-on-llms?utm_source=tldrinfosec) Joshua Saxe reflects on his time at Meta with mixed emotions, describing it as a place to work with incredibly talented people but also as intensely competitive, where strong personal ambitions outweigh product concerns. Saxe believes that Meta's products, like Llama and AR/VR, are disconnected and lackluster because engineers feel missionless and jump on a bandwagon that will lead to career growth. Overall, Saxe enjoyed his time at Meta and was involved in creating AI security initiatives before leaving to start his own company.

[Meta confirms thousands of Instagram accounts were hacked by abusing its AI chatbot (3 minute read)](https://this.weekinsecurity.com/meta-confirms-thousands-of-instagram-accounts-were-hacked-by-abusing-its-ai-chatbot/?utm_source=tldrinfosec) Meta has notified at least 20,225 people that their Instagram accounts were hijacked through a flaw in its AI-assisted account recovery system. A bug in a separate code path failed to verify that the email address supplied during a password reset matched the one on file, so the chatbot sent reset links to attacker-controlled addresses simply when asked. The campaign ran from roughly April 17 until early June and affected any account without 2FA enabled, granting takeover of the account and access to DMs, posts, contact information, and dates of birth. The incident is a cautionary case for automating account recovery without a human in the loop, with one observer noting the attack amounted to one AI being fooled by AI-generated verification media while no person was positioned to catch it. Meta has since disabled the chatbot, removed the offending code path, and begun auditing its other chatbots.

[Cursor Bypassed Dependency Cooldown (1 minute read)](https://threadreaderapp.com/thread/2058658244328124562.html?utm_source=tldrinfosec) A user on X shared a screenshot of their LLM using a command line flag to explicitly override a dependency cooldown in pnpm.

[Oxford University hit by second data breach in a month (1 minute read)](https://www.thenews.com.pk/latest/1404975-oxford-university-hit-by-second-data-breach-in-a-month?utm_source=tldrinfosec) Oxford's CareerConnect platform was breached on May 28, exposing full names and email addresses for alumni, research staff, and recruiters.

[Silent Ransom Group targets law firms with fake IT support calls (4 minute read)](https://www.bleepingcomputer.com/news/security/silent-ransom-group-targets-law-firms-with-fake-it-support-calls/?utm_source=tldrinfosec) Silent Ransom Group (UNC3753/Luna Moth/Chatty Spider) has hit dozens of US legal and professional services firms since January using invoice-themed phishing followed by vishing calls impersonating IT staff to deploy AnyDesk, Zoho Assist, Bomgar, or SuperOps.

### Source URL
https://tldr.tech/infosec/2026-06-08
