---
actionability: high
attached_experts: []
channel_name: ''
created_at: '2026-06-05T08:40:22.517025+10:00'
domain: unknown
expert_status: unattached
primary_mode: router
privacy: public
review_status: new
secondary_modes: []
source_type: article
source_url: https://tldr.tech/infosec/2026-06-03
status: processed
suggested_experts: []
tags: []
title: Red Hat npm Backdoor ⛓️, 1-Click GitHub Theft 🐙, MS Android Token Leak 🔑
transcript_path: ''
type: insight_note
updated_at: '2026-06-05T08:40:22.517025+10:00'
---

# Red Hat npm Backdoor ⛓️, 1-Click GitHub Theft 🐙, MS Android Token Leak 🔑

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
https://tldr.tech/infosec/2026-06-03

You can't stop agentic AI - so you'd better secure the data that's feeding it (Sponsor) Security teams are finding out the hard way: when you give AI agents access to data, they inherit years of overpermissioned files, shadow datasets, and unclassified content. You can't block AI adoption. But you can use  Sentra  to get a continuous view of the  full AI data surface,  and the tools to secure it: → See the data AI systems can access: cloud, SaaS, on-prem → Classify sensitive data at 98% accuracy (3rd-party validated) → Eliminate ROT data before it reaches training / RAG → Data never leaves your environment ✅ Trusted by Expedia, Lyft, Nestlé, Marqeta ⭐ 4.9/5 on Gartner Peer Insights See your AI data exposure →

WordPress Malware Campaign Hides Payloads in Steam Profiles (2 minute read) GoDaddy detected a new malware campaign that had infected nearly 2,000 WordPress sites. The malware uses Steam Community profile comments that contain hidden Unicode characters containing the malicious payloads. The decoded payload is used to build a malicious JavaScript file that is injected into every frontend page and is used to deploy a PHP backdoor.

CVE-2026-31525: Linux Kernel Privilege Escalation Flaw (3 minute read) CVE-2026-31525 (CVSS 7.8) is a Linux kernel BPF interpreter flaw where the sdiv32 and smod32 handlers call the kernel abs() macro on an s32 operand equal to S32_MIN, triggering undefined signed-overflow behavior that diverges from the verifier's abstract interpretation and lets a local attacker who can load BPF programs achieve out-of-bounds BPF map value access (CWE-787) leading to memory corruption and privilege escalation. Exploitation requires the interpreter path, which is active only when the BPF JIT is disabled or unavailable, affecting Linux Kernel 7.0-rc1 through 7.0-rc4. Apply the upstream commits introducing the abs_s32() helper, and as interim hardening set kernel.unprivileged_bpf_disabled=1, enable the JIT with net.core.bpf_jit_enable=1, and restrict CAP_BPF and CAP_SYS_ADMIN to trusted services.

Red Hat npm packages compromised to steal developer credentials (3 minute read) A new Shai-Hulud variant dubbed "Miasma" backdoored 32 packages and 96 versions under Red Hat's @redhat-cloud-services npm namespace, totaling roughly 117,000 weekly downloads, after attackers compromised an employee's GitHub account and pushed commits that abused a GitHub Actions OIDC token to publish via npm's trusted publishing endpoint. The packages carried a preinstall hook executing a 4.2 MB obfuscated index.js payload that harvests GitHub Actions secrets, AWS, GCP, and Azure credentials, HashiCorp Vault and Kubernetes tokens, npm and PyPI publishing tokens, SSH keys, Docker credentials, GPG keys, and .env files, with 309 GitHub repositories compromised so far. Organizations that installed any affected version should immediately rotate all credentials, secrets, and tokens used on the infected device, as Red Hat states the compromise was confined to internal development tooling and never reached customer-facing console.redhat.com systems.

Device Code Phishing Forensics: What We Learned Investigating BEC in the Wild (12 minute read) Researchers describe a surge in device code phishing used for Business Email Compromise, where attackers abuse Microsoft's device code flow so victims enter codes on a real Microsoft domain while attackers capture tokens. They explain why forensics are difficult when attackers and victims share session IDs, and how to use Entra non‑interactive logs and linkable token IDs to track attacker activity. They cover browser‑extension detections for static and JavaScript phishing kits, Entra KQL detections, and Conditional Access policies that block or tightly limit device code sign‑ins.

1-Click GitHub Token Stealing via a VSCode Bug (12 minute read) GitHub's github.dev editor runs a browser-based VSCode that receives a broad OAuth token from github.com, which can access all repositories the user can reach, including private ones. The token sits inside a large, complex VSCode web app, which makes the environment attractive for bug hunting and token theft. The write-up explains a VSCode webview security issue that lets a crafted link execute code in this environment and exfiltrate that GitHub token with a single user click.

xz, two years on: what scanners still cannot catch (4 minute read) CVE-2024-3094 was a maintainer-trust hijack rather than a code flaw, with "Jia Tan" spending two years earning co-maintainer commit rights before slipping a backdoor into the autotools m4 macros that generated xz-utils release tarballs, leaving the git tree clean so that lockfile-versus-CVE scanners returned clean right up until an engineer noticed a 500ms SSH login slowdown. The structural gap is that CVE-driven scanning answers whether a version is known-bad, not whether it is safe, and the same trust-hijack and postinstall-script shape recurred in the lottie-player and Solana web3.js compromises. Defenders should pin direct dependencies, enforce lockfile-diff review on every PR to catch unfamiliar contributor names and cadence changes, subscribe to a real-time feed like OSV, and pause upgrades when a package signals a maintainer shift, such as a new email, signing key, or sudden release burst.

Workcell (GitHub Repo) Workcell runs coding agents inside a bounded local runtime on Apple Silicon macOS using a harder container inside a dedicated Colima VM.

claude-red (GitHub Repo) claude-red is a library of 58 offensive-security SKILL.md files across 13 categories that prime Claude's Skills system to act as a context-aware red team operator, with skills loading on demand from conversational triggers spanning web (SQLi, SSRF, deserialization), Active Directory (Kerberoast, ADCS ESC1-15), wireless, cloud, EDR evasion, exploit development, fuzzing, and AI attacks like prompt injection and RAG poisoning. The author positions it for authorized engagements, bug bounty triage, CTF prep, and operator training, with a seven-phase roadmap targeting roughly 107 skills.

TailscaleHound (GitHub Repo) TailscaleHound is a BloodHound OpenGraph collector for Tailscale that collects tailnet users, devices, groups, tags, ACLs, grants, SSH rules, routes, and other data.

How One Line of Code Put Billions of Microsoft Android App Downloads at Risk (4 minute read) A forgotten debug flag in six Microsoft 365 Android apps (Word, Excel, PowerPoint, Copilot, Loop, and OneNote) let any Android app request and receive Microsoft account access tokens. Attackers only needed about 15 lines of code inside a widely installed or updated app to silently steal tokens and reuse or refresh them over time. Stolen FOCI tokens exposed email, files, documents, communications, and calendars until Microsoft patched the flaws in May and pushed fixes via Patch Tuesday and Google Play.

I found a second vote.gov - and it's registered to the White House (7 minute read) The Drey Dossier investigated the TrumpRx webpage and found a byline stating that it was designed by the National Design Studio, which was created by executive order and staffed by many ex-DOGE employees. National Design Studio is also redesigning many other agency websites, such as passport.gov and login.gov, with control no longer under the appropriate agencies. The report also noted that the TrumpRx page used PostHog to collect analytics, despite the privacy policy stating that it didn't.

A Single Web Page Could Spy on Your Other Tabs – Hidden Code Inside (3 minute read) FROST (Fingerprinting Remotely using OPFS-based SSD Timing) is a browser side-channel where a malicious page writes a large file into the Origin Private File System, then uses performance.now() to repeatedly time reads of that file, inferring SSD contention caused by other tabs and applications. By correlating the resulting latency patterns, an attacker-controlled site can guess what else the victim has open, such as a banking session, and time a phishing popup to coincide with it, all using ordinary JavaScript without camera, microphone, or extension access. The technique frames OPFS and high-resolution timers as a privacy-leaking primitive, a reminder that timing side channels reachable from unprivileged web content remain a hard problem for browser sandboxing.

Anthropic scales Claude Mythos to critical infrastructure in 15+ countries (3 minute read) Anthropic is extending Project Glasswing and access to its Claude Mythos model to about 150 organizations in over 15 countries.

FSB Group Gamaredon Hides Worm in Windows Data Streams (2 minute read) Sekoia attributes a fileless VBScript worm dubbed GammaWorm to FSB-linked Gamaredon.

Microsoft reaches for olive branch after public dustup with 0-day researcher (4 minute read) Microsoft walks back earlier hardline language and says it will not pursue legal action against people who conduct or publish security research, reserving referrals for clearly malicious activity that harms customers.

### Fetched Web Text
You can't stop agentic AI - so you'd better secure the data that's feeding it (Sponsor) Security teams are finding out the hard way: when you give AI agents access to data, they inherit years of overpermissioned files, shadow datasets, and unclassified content. You can't block AI adoption. But you can use  Sentra  to get a continuous view of the  full AI data surface,  and the tools to secure it: → See the data AI systems can access: cloud, SaaS, on-prem → Classify sensitive data at 98% accuracy (3rd-party validated) → Eliminate ROT data before it reaches training / RAG → Data never leaves your environment ✅ Trusted by Expedia, Lyft, Nestlé, Marqeta ⭐ 4.9/5 on Gartner Peer Insights See your AI data exposure →

WordPress Malware Campaign Hides Payloads in Steam Profiles (2 minute read) GoDaddy detected a new malware campaign that had infected nearly 2,000 WordPress sites. The malware uses Steam Community profile comments that contain hidden Unicode characters containing the malicious payloads. The decoded payload is used to build a malicious JavaScript file that is injected into every frontend page and is used to deploy a PHP backdoor.

CVE-2026-31525: Linux Kernel Privilege Escalation Flaw (3 minute read) CVE-2026-31525 (CVSS 7.8) is a Linux kernel BPF interpreter flaw where the sdiv32 and smod32 handlers call the kernel abs() macro on an s32 operand equal to S32_MIN, triggering undefined signed-overflow behavior that diverges from the verifier's abstract interpretation and lets a local attacker who can load BPF programs achieve out-of-bounds BPF map value access (CWE-787) leading to memory corruption and privilege escalation. Exploitation requires the interpreter path, which is active only when the BPF JIT is disabled or unavailable, affecting Linux Kernel 7.0-rc1 through 7.0-rc4. Apply the upstream commits introducing the abs_s32() helper, and as interim hardening set kernel.unprivileged_bpf_disabled=1, enable the JIT with net.core.bpf_jit_enable=1, and restrict CAP_BPF and CAP_SYS_ADMIN to trusted services.

Red Hat npm packages compromised to steal developer credentials (3 minute read) A new Shai-Hulud variant dubbed "Miasma" backdoored 32 packages and 96 versions under Red Hat's @redhat-cloud-services npm namespace, totaling roughly 117,000 weekly downloads, after attackers compromised an employee's GitHub account and pushed commits that abused a GitHub Actions OIDC token to publish via npm's trusted publishing endpoint. The packages carried a preinstall hook executing a 4.2 MB obfuscated index.js payload that harvests GitHub Actions secrets, AWS, GCP, and Azure credentials, HashiCorp Vault and Kubernetes tokens, npm and PyPI publishing tokens, SSH keys, Docker credentials, GPG keys, and .env files, with 309 GitHub repositories compromised so far. Organizations that installed any affected version should immediately rotate all credentials, secrets, and tokens used on the infected device, as Red Hat states the compromise was confined to internal development tooling and never reached customer-facing console.redhat.com systems.

Device Code Phishing Forensics: What We Learned Investigating BEC in the Wild (12 minute read) Researchers describe a surge in device code phishing used for Business Email Compromise, where attackers abuse Microsoft's device code flow so victims enter codes on a real Microsoft domain while attackers capture tokens. They explain why forensics are difficult when attackers and victims share session IDs, and how to use Entra non‑interactive logs and linkable token IDs to track attacker activity. They cover browser‑extension detections for static and JavaScript phishing kits, Entra KQL detections, and Conditional Access policies that block or tightly limit device code sign‑ins.

1-Click GitHub Token Stealing via a VSCode Bug (12 minute read) GitHub's github.dev editor runs a browser-based VSCode that receives a broad OAuth token from github.com, which can access all repositories the user can reach, including private ones. The token sits inside a large, complex VSCode web app, which makes the environment attractive for bug hunting and token theft. The write-up explains a VSCode webview security issue that lets a crafted link execute code in this environment and exfiltrate that GitHub token with a single user click.

xz, two years on: what scanners still cannot catch (4 minute read) CVE-2024-3094 was a maintainer-trust hijack rather than a code flaw, with "Jia Tan" spending two years earning co-maintainer commit rights before slipping a backdoor into the autotools m4 macros that generated xz-utils release tarballs, leaving the git tree clean so that lockfile-versus-CVE scanners returned clean right up until an engineer noticed a 500ms SSH login slowdown. The structural gap is that CVE-driven scanning answers whether a version is known-bad, not whether it is safe, and the same trust-hijack and postinstall-script shape recurred in the lottie-player and Solana web3.js compromises. Defenders should pin direct dependencies, enforce lockfile-diff review on every PR to catch unfamiliar contributor names and cadence changes, subscribe to a real-time feed like OSV, and pause upgrades when a package signals a maintainer shift, such as a new email, signing key, or sudden release burst.

Workcell (GitHub Repo) Workcell runs coding agents inside a bounded local runtime on Apple Silicon macOS using a harder container inside a dedicated Colima VM.

claude-red (GitHub Repo) claude-red is a library of 58 offensive-security SKILL.md files across 13 categories that prime Claude's Skills system to act as a context-aware red team operator, with skills loading on demand from conversational triggers spanning web (SQLi, SSRF, deserialization), Active Directory (Kerberoast, ADCS ESC1-15), wireless, cloud, EDR evasion, exploit development, fuzzing, and AI attacks like prompt injection and RAG poisoning. The author positions it for authorized engagements, bug bounty triage, CTF prep, and operator training, with a seven-phase roadmap targeting roughly 107 skills.

TailscaleHound (GitHub Repo) TailscaleHound is a BloodHound OpenGraph collector for Tailscale that collects tailnet users, devices, groups, tags, ACLs, grants, SSH rules, routes, and other data.

How One Line of Code Put Billions of Microsoft Android App Downloads at Risk (4 minute read) A forgotten debug flag in six Microsoft 365 Android apps (Word, Excel, PowerPoint, Copilot, Loop, and OneNote) let any Android app request and receive Microsoft account access tokens. Attackers only needed about 15 lines of code inside a widely installed or updated app to silently steal tokens and reuse or refresh them over time. Stolen FOCI tokens exposed email, files, documents, communications, and calendars until Microsoft patched the flaws in May and pushed fixes via Patch Tuesday and Google Play.

I found a second vote.gov - and it's registered to the White House (7 minute read) The Drey Dossier investigated the TrumpRx webpage and found a byline stating that it was designed by the National Design Studio, which was created by executive order and staffed by many ex-DOGE employees. National Design Studio is also redesigning many other agency websites, such as passport.gov and login.gov, with control no longer under the appropriate agencies. The report also noted that the TrumpRx page used PostHog to collect analytics, despite the privacy policy stating that it didn't.

A Single Web Page Could Spy on Your Other Tabs – Hidden Code Inside (3 minute read) FROST (Fingerprinting Remotely using OPFS-based SSD Timing) is a browser side-channel where a malicious page writes a large file into the Origin Private File System, then uses performance.now() to repeatedly time reads of that file, inferring SSD contention caused by other tabs and applications. By correlating the resulting latency patterns, an attacker-controlled site can guess what else the victim has open, such as a banking session, and time a phishing popup to coincide with it, all using ordinary JavaScript without camera, microphone, or extension access. The technique frames OPFS and high-resolution timers as a privacy-leaking primitive, a reminder that timing side channels reachable from unprivileged web content remain a hard problem for browser sandboxing.

Anthropic scales Claude Mythos to critical infrastructure in 15+ countries (3 minute read) Anthropic is extending Project Glasswing and access to its Claude Mythos model to about 150 organizations in over 15 countries.

FSB Group Gamaredon Hides Worm in Windows Data Streams (2 minute read) Sekoia attributes a fileless VBScript worm dubbed GammaWorm to FSB-linked Gamaredon.

Microsoft reaches for olive branch after public dustup with 0-day researcher (4 minute read) Microsoft walks back earlier hardline language and says it will not pursue legal action against people who conduct or publish security research, reserving referrals for clearly malicious activity that harms customers.

### Source URL
https://tldr.tech/infosec/2026-06-03
