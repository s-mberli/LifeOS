---
actionability: high
attached_experts: []
channel_name: ''
created_at: '2026-06-10T10:12:08.211632+10:00'
domain: unknown
expert_status: unattached
primary_mode: router
privacy: public
review_status: new
secondary_modes: []
source_type: article
source_url: https://tldr.tech/infosec/2026-06-09
status: processed
suggested_experts: []
tags:
- infosec
- supply-chain-attack
- ai-security
- cursor-ide
- sandbox-escape
- credential-theft
- ci-cd-security
- password-manager
- mxc-sandbox
- skillspector
title: MS Open Source Tools Hacked 🔓, Cursor Sandbox Escape 💻, Dashlane Vaults Stolen
  🔑
transcript_path: ''
type: insight_note
updated_at: '2026-06-10T10:12:08.211632+10:00'
---

# MS Open Source Tools Hacked 🔓, Cursor Sandbox Escape 💻, Dashlane Vaults Stolen 🔑

## Summary
This TLDR Infosec digest from June 9, 2026 captures a dense snapshot of the current threat landscape, with a clear throughline: supply chain attacks and credential abuse are the dominant vectors, and the AI tooling ecosystem is both the target and the solution. The report covers 15+ incidents and tool releases, but the most architecturally significant threads are the Microsoft open-source supply chain compromise (~70 GitHub projects infected), the Cursor sandbox escape (NomShub) demonstrating how AI-native tooling introduces novel attack surfaces, and the Dashlane vault theft showing that even Argon2-hardened master passwords can't save users with weak/reused credentials when 2FA APIs are brute-forceable. On the defensive side, Microsoft's MXC sandbox announcement signals a shift toward OS-level isolation for agentic code, NVIDIA's SkillSpector brings structured security scanning to AI agent skills (64 vulnerability patterns), and Astral's uv audit shows the Python ecosystem catching up on supply chain hygiene. The recurring theme: every layer of the stack—from CI/CD pipelines to IDE sandboxes to password manager APIs—is being probed, and defenders who don't pin dependencies, mask secrets, and assume breach at the identity layer will be compromised.

## Key Ideas
- Supply chain attacks are scaling through open-source ecosystems: ~70 Microsoft-affiliated GitHub projects (Azure, Claude Code, Gemini CLI, VS Code tools) were compromised with credential-stealing malware, likely via a prior compromise of Microsoft's Durable Task project. This is not a one-off—it's repeated access exploitation. Defenders must pin all includes/images to commit SHAs, use masked/protected CI variables, and treat any third-party dependency as potentially hostile.
- AI-native tooling creates novel attack surfaces: Cursor's NomShub vulnerability allowed remote code execution with zero user interaction beyond opening a repo, exploiting shell built-in commands (export, cd, echo) to hijack the cursor-tunnel binary via Microsoft Dev Tunnels. This is a pattern, not an anomaly—any AI IDE or agent runtime that executes shell commands without strict allowlisting is vulnerable.
- Identity and 2FA APIs are the new perimeter: Dashlane vault theft worked not by cracking Argon2 but by brute-forcing 2FA codes through device-enrollment API spraying, registering new devices on <20 accounts, and downloading encrypted vaults. The lesson: API rate limiting and device enrollment flows are as critical as password hashing strength.
- OS-level sandboxing is becoming mandatory for agentic code: Microsoft's MXC announcement (platform-agnostic, supporting AppContainer, WSL microVMs, NanVix, macOS Seatbelt) signals that app-level sandboxes (like those in Codex/Claude Code) are insufficient. Any system running untrusted AI-generated code needs kernel-level isolation.
- CI/CD pipelines are massively exposed: GoGatoZ's scan of 3,757 public GitLab projects found 7,331 issues (1,580 HIGH severity), dominated by unprotected fork merge request pipelines (1,971), privileged Docker runners (259), and plaintext secrets (347). The kill chain is: fork repo → submit MR → pipeline runs with access to secrets → exfiltrate. Disable fork MR pipeline access to secrets immediately.
- AI security tooling is maturing rapidly: NVIDIA's SkillSpector scans AI agent skills for 64 vulnerability patterns (prompt injection, data exfiltration, supply chain, MCP least privilege, tool poisoning) using static analysis, AST inspection, taint tracking, and YARA signatures with SARIF output. This is directly applicable to any AI platform building agent skills or MCP servers.
- Consumer IoT is an unmonitored attack surface: Bright Data's SDK in free Samsung/LG/Roku apps silently converts smart TVs into residential proxy exit nodes (200 GB/month cap), and the hijacked polyfill[.]io domain reactivated to trigger credential prompts on major brand websites. These are supply chain compromises hiding in plain sight.

## Why this matters for Markus
- AI Platform Security (ai-platform): The Cursor sandbox escape and Microsoft MXC announcement are directly relevant to any AI agent or IDE-adjacent platform Markus builds. If his platform executes code or shells out to commands, he needs strict command allowlisting and OS-level sandboxing—not just app-level isolation. The NomShub exploit pattern (shell built-ins bypassing parsers) is a concrete vulnerability class to audit against.
- Supply Chain Hardening (ai-platform): The Microsoft open-source compromise (~70 projects) and GitLab CI/CD kill chain findings are a wake-up call for any project using third-party dependencies or CI/CD pipelines. Markus should immediately audit his GitHub Actions/GitLab CI configs for fork MR access, plaintext secrets, and unpinned dependencies. The GoGatoZ tool is worth running against his own repos.
- AI Agent Security Scanning (ai-platform): NVIDIA's SkillSpector (64 vulnerability patterns, SARIF output) is a tool Markus should evaluate for integration into his AI platform's skill/agent validation pipeline. If he's building MCP servers or agent skills, this is the current state-of-the-art for automated security scanning.
- Credential & Identity Security (life-kompass, career): The Dashlane vault theft demonstrates that even strong password hashing (Argon2) doesn't protect against API-level 2FA brute-forcing. Markus should audit his own password manager setup, ensure unique master passwords everywhere, and consider hardware security keys (FIDO2/WebAuthn) which are resistant to this attack class.
- Content & Thought Leadership (flow-temple, career): This digest is rich material for LinkedIn posts or newsletter content. The intersection of AI tooling security, supply chain attacks, and identity API abuse is a high-engagement topic for the infosec and AI builder communities. Markus could write a technical breakdown of the NomShub exploit or a 'state of AI tooling security' analysis.

## Related Modes
- ai-platform
- career
- life-kompass

## Next Action
- [ ] Run a supply chain and CI/CD security audit on all active GitHub/GitLab repos: (1) Pin all Docker images and CI includes to full commit SHAs, not tags or branches. (2) Disable fork merge request pipeline access to secrets in project settings. (3) Audit for plaintext secrets using git-secrets or truffleHog. (4) If any repo executes shell commands (AI agents, build scripts), implement strict command allowlisting to prevent NomShub-style escapes. (5) Evaluate NVIDIA SkillSpector for integration into any AI skill/agent validation pipeline. Estimated time: 2-3 hours for a small portfolio.

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

1. **Lansing Community College Data Breach**: 174,307 individuals impacted after attackers accessed systems using compromised credentials, exposing names, addresses, birth dates, driver's license data, and Social Security numbers. No evidence of data misuse yet; 24 months of credit monitoring offered.

2. **UK NHS Patient Records Stolen**: Mid and South Essex NHS Foundation Trust confirmed 2,380 records stolen from a third-party testing provider, with other trusts also affected. Exposed data includes names, DOB, patient numbers, NHS numbers, postcodes, and test results.

3. **Microsoft Open Source Tools Hacked**: ~70 GitHub-hosted open source projects (Azure, Claude Code, Gemini CLI, VS Code) were taken down after malware was found that captured developer passwords/credentials. Likely linked to a prior compromise of Microsoft's Durable Task project.

4. **Cursor Sandbox Escape (NomShub)**: A now-patched vulnerability in Cursor allowed code execution with no user interaction beyond opening a repository. Exploited a sandbox breakout via shell built-in commands (export, cd, echo) to hijack Cursor's tunnel binary for unauthenticated shell access via Microsoft Dev Tunnels.

5. **Microsoft MXC Sandbox Internals**: Microsoft announced MXC, a platform-agnostic OS-level sandbox for untrusted/agentic code, supporting backends like AppContainer, disposable Windows VMs, WSL microVMs, NanVix, bubblewrap, and macOS Seatbelt.

6. **GitLab CI/CD Kill Chain (GoGatoZ)**: Black Hills InfoSec scanned 3,757 public GitLab projects, finding 7,331 issues (1,580 HIGH severity). Key risks: unprotected fork merge request pipelines, privileged Docker runners, curl|bash patterns, shell injection, exposed self-hosted runners, and plaintext secrets. Defenders should pin includes/images to commit SHAs, use masked/protected CI variables, and disable fork MR pipeline access.

7. **Offroad (Product Launch)**: Autonomous security agents for identity risk identification and remediation across users, machines, AI agents, and SaaS/OAuth apps.

8. **NVIDIA SkillSpector**: Open-source security scanner for AI agent skills covering 64 vulnerability patterns (prompt injection, data exfiltration, supply chain, MCP least privilege, tool poisoning) with static analysis, AST inspection, taint tracking, YARA signatures, and optional LLM evaluation.

9. **Aether**: Windows memory forensics and threat hunting tool for scanning live process memory.

10. **uv Package Manager Security Features**: Astral added `uv audit` (4-10x faster than pip-audit) and an opt-in OSV-based malware check to block malicious PyPI distributions before execution.

11. **Dashlane Vault Breach**: Attackers abused device-enrollment APIs to spray 2FA codes, brute-force tokens, register new devices on <20 accounts, and download encrypted vaults. Master passwords hardened with Argon2, but weak/reused passwords remain at risk.

12. **VS Code Extension Update Delay**: Microsoft added a 2-hour auto-update delay for extensions (except trusted publishers like Microsoft, GitHub, OpenAI) to limit supply chain attacks. Similar cooldowns exist in npm, Yarn, Bun, etc.

13. **York Council Email Blunder**: City of York Council exposed hundreds of disabled residents' email addresses by failing to use BCC.

14. **Polyfill[.]io Reactivated**: The hijacked domain returned HTTP 401 responses causing browser-native credential prompts on Toshiba, Muji, and other major brand websites.

15. **Smart TV Proxy Abuse**: Bright Data's SDK in free Samsung, LG, and Roku apps silently turns TVs into residential proxy exit nodes with a 200 GB monthly cap.

---

Chunk 2 Summary:
### Key Points from Part 2/4 of "MS Open Source Tools Hacked 🔓, Cursor Sandbox Escape 💻, Dashlane Vaults Stolen 🔑"

1. **Lansing Community College Data Breach**  
   - 174,307 individuals affected; exposed data includes names, addresses, birth dates, driver’s license numbers, and Social Security numbers.  
   - Attackers used compromised credentials; no evidence of data misuse yet. LCC offers 24 months of credit monitoring.

2. **UK NHS Patient Records Stolen**  
   - Mid and South Essex NHS Foundation Trust confirmed 2,380 patient records stolen via a third-party testing provider breach.  
   - Exposed data: names, DOBs, patient/NHS numbers, postcodes, and test results. Other trusts also impacted.

3. **Microsoft Open Source Tools Compromised**  
   - ~70 GitHub-hosted projects (including Azure, Claude Code, Gemini CLI, VS Code tools) infected with malware to steal developer credentials.  
   - Linked to prior compromise of Microsoft’s Durable Task project—suggesting repeated access exploitation.

4. **Cursor IDE Sandbox Escape Vulnerability (NomShub)**  
   - Patched flaw allowed remote code execution without user interaction beyond opening a repo in Cursor.  
   - Exploited shell built-ins (`export`, `cd`, `echo`) to hijack Cursor’s tunnel binary via Microsoft Dev Tunnels for unauthenticated shell access.

5. **Microsoft MXC Sandbox System Introduced**  
   - New OS-level, platform-agnostic sandbox for untrusted/agentic code (unlike app-level sandboxes in Codex/Claude Code).  
   - Supports multiple backends: AppContainer, WSL microVM, NanVix, macOS Seatbelt, etc.

6. **GitLab CI/CD Kill Chain Auditing (GoGatoZ Tool)**  
   - Black Hills InfoSec scanned 3,757 public GitLab projects; found 7,331 issues (1,580 HIGH severity).  
   - Top risks: unprotected fork MR pipelines, privileged Docker runners, `curl | bash` patterns, shell injection, exposed runners, plaintext secrets.  
   - Defenses: pin includes/images to SHAs, protect CI variables, disable fork access to secrets, restrict runners, drop privileged mode.

7. **Dashlane Vault Breach via 2FA Brute-Forcing**  
   - Attackers abused device-enrollment APIs to brute-force 2FA codes, register devices on <20 accounts, and download encrypted vaults.  
   - Master passwords still protected by Argon2, but weak/reused passwords at risk. Users urged to change credentials.

8. **VS Code Adds 2-Hour Extension Update Delay**  
   - Auto-updates now delayed by 2 hours (except for trusted publishers like Microsoft/GitHub/OpenAI) to limit supply chain attacks.  
   - Manual updates still allowed; similar cooldowns exist in npm, Yarn, Bun, etc.

9. **Polyfill[.]io Hijack Reactivates**  
   - Hijacked domain (since 2024) returned HTTP 401s in May 2026, triggering fake login prompts on sites like Toshiba, Muji, Samsung Smart TVs.  
   - Caused by unremoved embedded script references.

10. **Smart TVs Turned into AI Proxies**  
    - Bright Data SDK in free Samsung/LG/Roku apps silently converts TVs into residential proxy nodes (200 GB/month cap).  
    - Apps include `ignore_screen_on:true`, enabling background operation.

11. **New Security Tools Released**  
    - **SkillSpector** (NVIDIA): Scans AI agent skills for 64 vulnerability patterns (prompt injection, data exfiltration, etc.) with SARIF output.  
    - **Aether**: Windows memory forensics tool for live process threat hunting.  
    - **uv audit** (Astral): Fast native dependency scanner + opt-in malware checks via OSV.dev to block malicious PyPI packages.

12. **Human Error: York Council Exposes Disabled Residents**  
    - Email sent without BCC to Blue Badge holders, revealing email addresses and implying disability status.

---

Chunk 3 Summary:
Here are the key points from this section (3/4) of the resource:

**Data Breaches & Healthcare**
- **Mid and South Essex NHS Trust**: 2,380 patient records stolen from a third-party testing provider; data includes names, DOB, NHS numbers, postcodes, and test results. Other hospital trusts' data was also compromised.
- **Lansing Community College**: 174,307 people impacted after attackers used compromised credentials to access systems containing names, addresses, SSNs, and driver's license data.

**Microsoft Open Source Supply Chain Attack**
- ~70 GitHub-hosted open source projects (Azure, Claude Code, Gemini CLI, VS Code tools) were taken down after malware was discovered. Attackers captured developer passwords/credentials. Likely linked to a prior compromise of Microsoft's Durable Task project.

**Cursor Sandbox Escape (NomShub)**
- A now-patched vulnerability allowed code execution with no user interaction beyond opening a repository. Exploited a sandbox breakout via shell built-in commands (export, cd, echo) to hijack Cursor's tunnel binary for unauthenticated shell access via Microsoft Dev Tunnels.

**Microsoft MXC Sandbox**
- New platform-agnostic sandbox for untrusted/agentic code announced at Build 2026. Runs at OS level using AppContainer, isolation brokers, disposable VMs, WSL microVM, NanVix, bubblewrap, or macOS Seatbelt.

**GitLab CI/CD Kill Chain**
- GoGatoZ tool scanned 3,757 public projects, finding 7,331 issues (1,580 HIGH severity). Key risks: unprotected fork merge request pipelines, privileged Docker runners, curl|bash patterns, shell variable injection, exposed self-hosted runners, and plaintext secrets.

**Dashlane Vault Theft**
- Attackers abused device-enrollment APIs to brute-force 2FA codes, register new devices on <20 accounts, and download encrypted vaults. Master passwords hardened with Argon2, but weak/reused passwords remain at risk.

**VS Code Extension Update Delay**
- Microsoft added a 2-hour auto-update delay for extensions (except trusted publishers like Microsoft, GitHub, OpenAI) to limit supply chain attacks.

**Other Notable Items**
- **Polyfill[.]io** reactivated with HTTP 401 responses causing credential prompts on Toshiba, Muji, and other sites.
- **Samsung/LG Smart TV apps** found silently converting devices into residential AI proxy nodes via Bright Data's SDK.
- **City of York Council** exposed hundreds of disabled residents' email addresses via a BCC blunder.
- **uv package manager** added native vulnerability scanning and optional malware checks.
- **NVIDIA SkillSpector**: Open-source security scanner for AI agent skills covering 64 vulnerability patterns.

---

Chunk 4 Summary:
## Key Points Summary

**Cursor Sandbox Escape (NomShub):** A now-patched vulnerability in Cursor allowed remote code execution with zero user interaction beyond opening a repo. The flaw stemmed from Cursor's shell command parser failing to block built-ins (`export`, `cd`, `echo`), enabling hijacking of the `cursor-tunnel` binary for unauthenticated shell access via Microsoft Dev Tunnels.

**Microsoft MXC Sandbox:** Microsoft announced MXC, a platform-agnostic OS-level sandbox for untrusted/agentic code. Backends include AppContainer, disposable Windows VMs, WSL/NanVix microVMs, bubblewrap namespaces, or macOS Seatbelt.

**GitLab CI/CD Kill Chain:** GoGatoZ scanned 3,757 public GitLab projects, finding 7,331 issues (1,580 HIGH). Top risks: unprotected fork MR pipelines (1,971), privileged Docker runners (259), shell injection via CI variables (288), exposed self-hosted runners (177), and 347 plaintext secrets. Defenders should pin includes/images to commit SHAs, mask secrets, disable fork MR variable access, and drop privileged Docker mode.

**Dashlane Vault Theft:** Attackers brute-forced 2FA codes via device-enrollment API spraying, registered new devices on <20 accounts, and downloaded encrypted vaults. Master passwords hardened with Argon2, but weak/reused passwords remain at risk.

**VS Code Extension Delay:** Microsoft added a 2-hour auto-update delay for extensions (excluding trusted publishers) to limit supply chain attacks. Similar cooldowns exist in npm, Yarn, Bun, Bundler, and pnpm.

**Other Notable Items:**
- **uv (Python):** Astral shipped `uv audit` (4–10× faster than pip-audit) and an opt-in OSV-based malware check blocking quarantined PyPI distributions.
- **polyfill[.]io:** The hijacked domain reactivated, triggering spurious credential prompts on Toshiba, Muji, Samsung Smart TV, and other sites.
- **Smart TV Proxies:** Bright Data's SDK in free Samsung/LG/Roku apps silently turns TVs into residential proxy exit nodes (200 GB/month cap).
- **NVIDIA SkillSpector:** Open-source AI agent skill scanner covering 64 vulnerability patterns with SARIF output.
- **York Council Data Breach:** A single email without BCC exposed hundreds of disabled residents' addresses and disability status.

## Original Content
### Raw User Input
https://tldr.tech/infosec/2026-06-09

# TLDR InfoSec — 2026-06-09
Source: https://tldr.tech/infosec/2026-06-09

## Articles

### 174,000 Impacted by Lansing Community College Data Breach
- **URL:** https://www.securityweek.com/174000-impacted-by-lansing-community-college-data-breach/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-09
- **Read time:** 2 minute read
- **TLDR Summary:** In February 2025, Lansing Community College detected that attackers had accessed some systems using compromised credentials, exposing names, addresses, birth dates, driver's license data, Social Security numbers, and other records for 174,307 people. LCC offers 24 months of credit monitoring and identity protection, reports no evidence of data exfiltration or misuse so far, and withholds any attribution to a specific threat group.

### Thousands of Patient Records Taken in UK Cyberattack
- **URL:** https://www.bbc.com/news/articles/c072797rlx5o?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-09
- **Read time:** 2 minute read
- **TLDR Summary:** Mid and South Essex NHS Foundation Trust (MSE), one of the largest hospital trusts in England, confirmed that 2,380 records were stolen in a breach. The data was stolen from a third-party testing provider that analyzed blood, urine, and tissue samples, which confirmed that other hospital trusts' data was also stolen in the same breach. The exposed data includes names, dates of birth, patient numbers, NHS numbers, postcodes, and test results.

### Microsoft's open source tools were hacked to steal passwords of AI developers
- **URL:** https://techcrunch.com/2026/06/08/microsofts-open-source-tools-were-hacked-to-steal-passwords-of-ai-developers/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-09
- **Read time:** 2 minute read
- **TLDR Summary:** Microsoft took down about 70 GitHub-hosted open source projects after malware was found in tools tied to Azure, Claude Code, Gemini's CLI, and VS Code. Attackers used the infected packages to capture passwords and credentials when developers opened the tools. The incident appears to be linked to an earlier compromise of Microsoft's Durable Task project, suggesting the same access was compromised again.

### NomShub: Weaponizing Cursor's Remote Tunnel Through Indirect Prompt Injection and Sandbox Breakout
- **URL:** https://www.straiker.ai/blog/nomshub-cursor-remote-tunneling-sandbox-breakout?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-09
- **Read time:** 10 minute read
- **TLDR Summary:** Researchers uncovered a now-patched vulnerability in Cursor that could allow an attacker to execute code on a victim's system with no user interaction beyond opening the repository in Cursor. The vulnerability exploits a sandbox breakout caused by Cursor's shouldBlockShellCommand parser failing to block shell built-ins such as export, cd, and echo. Attackers can exploit this to hijack Cursor's cursor-tunnel binary, which uses Microsoft's Dev Tunnels infrastructure to obtain unauthenticated shell access.

### MXC Internals: How Microsoft's eXecution Containers Actually Isolate Agent Code
- **URL:** https://www.originhq.com/research/mxc-execution-containers-internals?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-09
- **Read time:** 10 minute read
- **TLDR Summary:** At Build 2026, Microsoft announced MXC as a new, platform-agnostic sandbox system for running untrusted and agentic code. The sandbox runs at the OS level rather than at the application level, unlike those shipped with Codex or Claude Code. Based on the OS and available features, the sandbox will run a backend using either AppContainer, Windows.AI.IsolationBroker, a disposable Windows VM, a WSL microVM, a NanVix microVM, a bubblewrap namespace, or macOS Seatbelt.

### Auditing GitLab: The CI/CD Kill Chain
- **URL:** https://www.blackhillsinfosec.com/auditing-gitlab-the-ci-cd-kill-chain/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-09
- **Read time:** 16 minute read
- **TLDR Summary:** Black Hills Information Security released GoGatoZ, a Go-based GitLab CI/CD auditing tool ported from Gato-X, and used it to scan 3,757 public gitlab.com projects across three campaigns (broad DevOps keywords, Fortune 500 targeting, and industry verticals), surfacing 7,331 findings, including 1,580 HIGH severity issues with roughly two-thirds of projects exhibiting at least one misconfiguration. Dominant attack classes included unprotected fork merge request pipelines (1,971 findings) that let attackers modify .gitlab-ci.yml in a fork to exfiltrate CI variables, privileged Docker runners (259) enabling container-to-host escape, curl | bash patterns in 150 pipelines, $CI_COMMIT_REF_NAME and $CI_MERGE_REQUEST_TITLE injection into shell scripts (288), exposed self-hosted runners (177), and 347 plaintext secrets, with a systematic false-positive workflow trimming about 40% of keyword-targeted findings as noise. Defenders should pin all include directives and container images to commit SHAs, move secrets to masked and protected CI variables, disable fork MR pipeline access to variables, restrict self-hosted runners to protected branches only, drop privileged mode on Docker runners exposed to public projects, and integrate scanners like GoGatoZ into regular audits of internal GitLab instances.

### Offroad (Product Launch)
- **URL:** https://offroad.ai/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-09
- **Read time:** Unknown
- **TLDR Summary:** Offroad provides autonomous security agents that identify identity risks across users, machines, AI agents, and SaaS/OAuth apps, gather context from fragmented systems, and then automatically remediate or govern access, with human oversight where needed.

### SkillSpector (GitHub Repo)
- **URL:** https://github.com/nvidia/skillspector?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-09
- **Read time:** Unknown
- **TLDR Summary:** NVIDIA has released SkillSpector, a security scanner for AI agent skills that combines static analysis, AST-based behavioral inspection, taint tracking, YARA signatures, and optional LLM semantic evaluation across 64 vulnerability patterns spanning prompt injection, data exfiltration, supply chain, MCP least privilege, and tool poisoning, with live OSV.dev CVE lookups and SARIF output for CI integration.

### Aether (GitHub Repo)
- **URL:** https://github.com/0xsp-SRD/aether?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-09
- **Read time:** Unknown
- **TLDR Summary:** Aether is a Windows memory forensics and threat hunting tool that scans live process memory for various malicious activities.

### Vulnerability and malware checks in uv
- **URL:** https://astral.sh/blog/uv-audit?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-09
- **Read time:** 4 minute read
- **TLDR Summary:** Astral has shipped two preview security features in the uv Python package manager: uv audit, a native dependency scanner for known vulnerabilities and adverse project statuses that runs 4x to 10x faster than pip-audit by leveraging uv's locked resolutions, and an opt-in OSV-based malware check (enabled via UV_MALWARE_CHECK=1) that queries MAL advisories on every sync to abort installation before quarantined-but-still-fetchable malicious distributions execute. The malware check closes a specific gap in locking installers where lockfiles reference object storage directly, allowing distributions removed from the PyPI index to still install from their underlying storage URLs.

### Dashlane explains how attackers managed to download encrypted password vaults
- **URL:** https://arstechnica.com/security/2026/06/dashlane-explains-how-attackers-managed-to-download-encrypted-password-vaults/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-09
- **Read time:** 3 minute read
- **TLDR Summary:** Attackers abused Dashlane's device-enrollment APIs to spray one-time 2FA codes across many accounts and brute force valid tokens, letting them register new devices on fewer than 20 accounts and download encrypted vaults. They still need to crack master passwords, which Dashlane hardens with Argon2, but weak or reused passwords remain exposed, so affected users should change master passwords and stored credentials.

### VS Code Adds 2-Hour Extension Auto-Update Delay to Limit Supply Chain Attacks
- **URL:** https://thehackernews.com/2026/06/vs-code-adds-2-hour-extension-auto.html?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-09
- **Read time:** 2 minute read
- **TLDR Summary:** Microsoft now delays automatic VS Code extension updates by two hours, except for trusted publishers like Microsoft, GitHub, and OpenAI, which still update immediately. Users can still trigger manual updates and see why updates are pending. Similar cooldown controls in Bundler, Bun, npm, pnpm, and Yarn limit how quickly newly published, potentially malicious packages reach developer environments.

### Council in UK's City of York outs hundreds of disabled residents with a single email blunder
- **URL:** https://www.theregister.com/security/2026/06/05/council-in-uks-city-of-york-outs-hundreds-of-disabled-residents-with-a-single-email-blunder/5251214?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-09
- **Read time:** 3 minute read
- **TLDR Summary:** City of York Council emailed Blue Badge holders without BCC, exposing hundreds of recipients' addresses and implicitly their disability status.

### Suspicious Polyfill login prompts pop up on Toshiba, Muji websites
- **URL:** https://www.bleepingcomputer.com/news/security/suspicious-polyfill-login-prompts-pop-up-on-toshiba-muji-websites/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-09
- **Read time:** 2 minute read
- **TLDR Summary:** The polyfill[.]io domain, hijacked by a Chinese entity in 2024 and abandoned by site owners who never removed embedded script references, reactivated in late May and began returning HTTP 401 responses that surfaced as browser-native credential prompts on Toshiba, Muji, Zojirushi, FiNC Technologies, Ishiyaku Publishers, Hobonichi, and Samsung Smart TV sites.

### Free Apps on Samsung and LG Smart TVs Secretly Turning Your Devices Into AI Proxies
- **URL:** https://cybersecuritynews.com/free-apps-turning-smart-tvs-into-proxies/?utm_source=tldrinfosec
- **Via:** TLDR InfoSec, 2026-06-09
- **Read time:** 4 minute read
- **TLDR Summary:** Include Security disclosed that Bright Data's SDK, embedded in free Samsung, LG, and Roku apps from partners including PlayWorks Digital, CloudTV, and Viber, silently converts connected TVs into residential proxy exit nodes with ignore_screen_on:true flags and a 200 GB monthly cap.

## Full Text

[174,000 Impacted by Lansing Community College Data Breach (2 minute read)](https://www.securityweek.com/174000-impacted-by-lansing-community-college-data-breach/?utm_source=tldrinfosec) In February 2025, Lansing Community College detected that attackers had accessed some systems using compromised credentials, exposing names, addresses, birth dates, driver's license data, Social Security numbers, and other records for 174,307 people. LCC offers 24 months of credit monitoring and identity protection, reports no evidence of data exfiltration or misuse so far, and withholds any attribution to a specific threat group.

[Thousands of Patient Records Taken in UK Cyberattack (2 minute read)](https://www.bbc.com/news/articles/c072797rlx5o?utm_source=tldrinfosec) Mid and South Essex NHS Foundation Trust (MSE), one of the largest hospital trusts in England, confirmed that 2,380 records were stolen in a breach. The data was stolen from a third-party testing provider that analyzed blood, urine, and tissue samples, which confirmed that other hospital trusts' data was also stolen in the same breach. The exposed data includes names, dates of birth, patient numbers, NHS numbers, postcodes, and test results.

[Microsoft's open source tools were hacked to steal passwords of AI developers (2 minute read)](https://techcrunch.com/2026/06/08/microsofts-open-source-tools-were-hacked-to-steal-passwords-of-ai-developers/?utm_source=tldrinfosec) Microsoft took down about 70 GitHub-hosted open source projects after malware was found in tools tied to Azure, Claude Code, Gemini's CLI, and VS Code. Attackers used the infected packages to capture passwords and credentials when developers opened the tools. The incident appears to be linked to an earlier compromise of Microsoft's Durable Task project, suggesting the same access was compromised again.

[NomShub: Weaponizing Cursor's Remote Tunnel Through Indirect Prompt Injection and Sandbox Breakout (10 minute read)](https://www.straiker.ai/blog/nomshub-cursor-remote-tunneling-sandbox-breakout?utm_source=tldrinfosec) Researchers uncovered a now-patched vulnerability in Cursor that could allow an attacker to execute code on a victim's system with no user interaction beyond opening the repository in Cursor. The vulnerability exploits a sandbox breakout caused by Cursor's shouldBlockShellCommand parser failing to block shell built-ins such as export, cd, and echo. Attackers can exploit this to hijack Cursor's cursor-tunnel binary, which uses Microsoft's Dev Tunnels infrastructure to obtain unauthenticated shell access.

[MXC Internals: How Microsoft's eXecution Containers Actually Isolate Agent Code (10 minute read)](https://www.originhq.com/research/mxc-execution-containers-internals?utm_source=tldrinfosec) At Build 2026, Microsoft announced MXC as a new, platform-agnostic sandbox system for running untrusted and agentic code. The sandbox runs at the OS level rather than at the application level, unlike those shipped with Codex or Claude Code. Based on the OS and available features, the sandbox will run a backend using either AppContainer, Windows.AI.IsolationBroker, a disposable Windows VM, a WSL microVM, a NanVix microVM, a bubblewrap namespace, or macOS Seatbelt.

[Auditing GitLab: The CI/CD Kill Chain (16 minute read)](https://www.blackhillsinfosec.com/auditing-gitlab-the-ci-cd-kill-chain/?utm_source=tldrinfosec) Black Hills Information Security released GoGatoZ, a Go-based GitLab CI/CD auditing tool ported from Gato-X, and used it to scan 3,757 public gitlab.com projects across three campaigns (broad DevOps keywords, Fortune 500 targeting, and industry verticals), surfacing 7,331 findings, including 1,580 HIGH severity issues with roughly two-thirds of projects exhibiting at least one misconfiguration. Dominant attack classes included unprotected fork merge request pipelines (1,971 findings) that let attackers modify .gitlab-ci.yml in a fork to exfiltrate CI variables, privileged Docker runners (259) enabling container-to-host escape, curl | bash patterns in 150 pipelines, $CI_COMMIT_REF_NAME and $CI_MERGE_REQUEST_TITLE injection into shell scripts (288), exposed self-hosted runners (177), and 347 plaintext secrets, with a systematic false-positive workflow trimming about 40% of keyword-targeted findings as noise. Defenders should pin all include directives and container images to commit SHAs, move secrets to masked and protected CI variables, disable fork MR pipeline access to variables, restrict self-hosted runners to protected branches only, drop privileged mode on Docker runners exposed to public projects, and integrate scanners like GoGatoZ into regular audits of internal GitLab instances.

[Centralizing identity security = $2.2M ROI, annually (Sponsor)](https://delinea.com/resources/delinea-platform-roi?utm_medium=paid-newsletter&amp;utm_source=TLDR&amp;utm_campaign=FF-FY26Q2_TLDR_*VisIP&amp;utm_content=TLDR%20Send%205&amp;utm_term=Secondary) And here's the data to prove it. Delinea partnered with independent research firm UserEvidence to  [evaluate annual ROI](https://delinea.com/resources/delinea-platform-roi?utm_medium=paid-newsletter&utm_source=TLDR&utm_campaign=FF-FY26Q2_TLDR_*VisIP&utm_content=TLDR%20Send%205&utm_term=Secondary)  at over 200 Delinea Platform customers. By centralizing identity security, improving visibility and control over privileged access, and automating workflows, customers averaged $2.2M ROI per year.  [Get the whitepaper](https://delinea.com/resources/delinea-platform-roi?utm_medium=paid-newsletter&utm_source=TLDR&utm_campaign=FF-FY26Q2_TLDR_*VisIP&utm_content=TLDR%20Send%205&utm_term=Secondary)

[Offroad (Product Launch)](https://offroad.ai/?utm_source=tldrinfosec) Offroad provides autonomous security agents that identify identity risks across users, machines, AI agents, and SaaS/OAuth apps, gather context from fragmented systems, and then automatically remediate or govern access, with human oversight where needed.

[SkillSpector (GitHub Repo)](https://github.com/nvidia/skillspector?utm_source=tldrinfosec) NVIDIA has released SkillSpector, a security scanner for AI agent skills that combines static analysis, AST-based behavioral inspection, taint tracking, YARA signatures, and optional LLM semantic evaluation across 64 vulnerability patterns spanning prompt injection, data exfiltration, supply chain, MCP least privilege, and tool poisoning, with live OSV.dev CVE lookups and SARIF output for CI integration.

[Aether (GitHub Repo)](https://github.com/0xsp-SRD/aether?utm_source=tldrinfosec) Aether is a Windows memory forensics and threat hunting tool that scans live process memory for various malicious activities.

[Vulnerability and malware checks in uv (4 minute read)](https://astral.sh/blog/uv-audit?utm_source=tldrinfosec) Astral has shipped two preview security features in the uv Python package manager: uv audit, a native dependency scanner for known vulnerabilities and adverse project statuses that runs 4x to 10x faster than pip-audit by leveraging uv's locked resolutions, and an opt-in OSV-based malware check (enabled via UV_MALWARE_CHECK=1) that queries MAL advisories on every sync to abort installation before quarantined-but-still-fetchable malicious distributions execute. The malware check closes a specific gap in locking installers where lockfiles reference object storage directly, allowing distributions removed from the PyPI index to still install from their underlying storage URLs.

[Dashlane explains how attackers managed to download encrypted password vaults (3 minute read)](https://arstechnica.com/security/2026/06/dashlane-explains-how-attackers-managed-to-download-encrypted-password-vaults/?utm_source=tldrinfosec) Attackers abused Dashlane's device-enrollment APIs to spray one-time 2FA codes across many accounts and brute force valid tokens, letting them register new devices on fewer than 20 accounts and download encrypted vaults. They still need to crack master passwords, which Dashlane hardens with Argon2, but weak or reused passwords remain exposed, so affected users should change master passwords and stored credentials.

[VS Code Adds 2-Hour Extension Auto-Update Delay to Limit Supply Chain Attacks (2 minute read)](https://thehackernews.com/2026/06/vs-code-adds-2-hour-extension-auto.html?utm_source=tldrinfosec) Microsoft now delays automatic VS Code extension updates by two hours, except for trusted publishers like Microsoft, GitHub, and OpenAI, which still update immediately. Users can still trigger manual updates and see why updates are pending. Similar cooldown controls in Bundler, Bun, npm, pnpm, and Yarn limit how quickly newly published, potentially malicious packages reach developer environments.

[Council in UK's City of York outs hundreds of disabled residents with a single email blunder (3 minute read)](https://www.theregister.com/security/2026/06/05/council-in-uks-city-of-york-outs-hundreds-of-disabled-residents-with-a-single-email-blunder/5251214?utm_source=tldrinfosec) City of York Council emailed Blue Badge holders without BCC, exposing hundreds of recipients' addresses and implicitly their disability status.

[Suspicious Polyfill login prompts pop up on Toshiba, Muji websites (2 minute read)](https://www.bleepingcomputer.com/news/security/suspicious-polyfill-login-prompts-pop-up-on-toshiba-muji-websites/?utm_source=tldrinfosec) The polyfill[.]io domain, hijacked by a Chinese entity in 2024 and abandoned by site owners who never removed embedded script references, reactivated in late May and began returning HTTP 401 responses that surfaced as browser-native credential prompts on Toshiba, Muji, Zojirushi, FiNC Technologies, Ishiyaku Publishers, Hobonichi, and Samsung Smart TV sites.

[Free Apps on Samsung and LG Smart TVs Secretly Turning Your Devices Into AI Proxies (4 minute read)](https://cybersecuritynews.com/free-apps-turning-smart-tvs-into-proxies/?utm_source=tldrinfosec) Include Security disclosed that Bright Data's SDK, embedded in free Samsung, LG, and Roku apps from partners including PlayWorks Digital, CloudTV, and Viber, silently converts connected TVs into residential proxy exit nodes with ignore_screen_on:true flags and a 200 GB monthly cap.

### Fetched Web Text
[174,000 Impacted by Lansing Community College Data Breach (2 minute read)](https://www.securityweek.com/174000-impacted-by-lansing-community-college-data-breach/?utm_source=tldrinfosec) In February 2025, Lansing Community College detected that attackers had accessed some systems using compromised credentials, exposing names, addresses, birth dates, driver's license data, Social Security numbers, and other records for 174,307 people. LCC offers 24 months of credit monitoring and identity protection, reports no evidence of data exfiltration or misuse so far, and withholds any attribution to a specific threat group.

[Thousands of Patient Records Taken in UK Cyberattack (2 minute read)](https://www.bbc.com/news/articles/c072797rlx5o?utm_source=tldrinfosec) Mid and South Essex NHS Foundation Trust (MSE), one of the largest hospital trusts in England, confirmed that 2,380 records were stolen in a breach. The data was stolen from a third-party testing provider that analyzed blood, urine, and tissue samples, which confirmed that other hospital trusts' data was also stolen in the same breach. The exposed data includes names, dates of birth, patient numbers, NHS numbers, postcodes, and test results.

[Microsoft's open source tools were hacked to steal passwords of AI developers (2 minute read)](https://techcrunch.com/2026/06/08/microsofts-open-source-tools-were-hacked-to-steal-passwords-of-ai-developers/?utm_source=tldrinfosec) Microsoft took down about 70 GitHub-hosted open source projects after malware was found in tools tied to Azure, Claude Code, Gemini's CLI, and VS Code. Attackers used the infected packages to capture passwords and credentials when developers opened the tools. The incident appears to be linked to an earlier compromise of Microsoft's Durable Task project, suggesting the same access was compromised again.

[NomShub: Weaponizing Cursor's Remote Tunnel Through Indirect Prompt Injection and Sandbox Breakout (10 minute read)](https://www.straiker.ai/blog/nomshub-cursor-remote-tunneling-sandbox-breakout?utm_source=tldrinfosec) Researchers uncovered a now-patched vulnerability in Cursor that could allow an attacker to execute code on a victim's system with no user interaction beyond opening the repository in Cursor. The vulnerability exploits a sandbox breakout caused by Cursor's shouldBlockShellCommand parser failing to block shell built-ins such as export, cd, and echo. Attackers can exploit this to hijack Cursor's cursor-tunnel binary, which uses Microsoft's Dev Tunnels infrastructure to obtain unauthenticated shell access.

[MXC Internals: How Microsoft's eXecution Containers Actually Isolate Agent Code (10 minute read)](https://www.originhq.com/research/mxc-execution-containers-internals?utm_source=tldrinfosec) At Build 2026, Microsoft announced MXC as a new, platform-agnostic sandbox system for running untrusted and agentic code. The sandbox runs at the OS level rather than at the application level, unlike those shipped with Codex or Claude Code. Based on the OS and available features, the sandbox will run a backend using either AppContainer, Windows.AI.IsolationBroker, a disposable Windows VM, a WSL microVM, a NanVix microVM, a bubblewrap namespace, or macOS Seatbelt.

[Auditing GitLab: The CI/CD Kill Chain (16 minute read)](https://www.blackhillsinfosec.com/auditing-gitlab-the-ci-cd-kill-chain/?utm_source=tldrinfosec) Black Hills Information Security released GoGatoZ, a Go-based GitLab CI/CD auditing tool ported from Gato-X, and used it to scan 3,757 public gitlab.com projects across three campaigns (broad DevOps keywords, Fortune 500 targeting, and industry verticals), surfacing 7,331 findings, including 1,580 HIGH severity issues with roughly two-thirds of projects exhibiting at least one misconfiguration. Dominant attack classes included unprotected fork merge request pipelines (1,971 findings) that let attackers modify .gitlab-ci.yml in a fork to exfiltrate CI variables, privileged Docker runners (259) enabling container-to-host escape, curl | bash patterns in 150 pipelines, $CI_COMMIT_REF_NAME and $CI_MERGE_REQUEST_TITLE injection into shell scripts (288), exposed self-hosted runners (177), and 347 plaintext secrets, with a systematic false-positive workflow trimming about 40% of keyword-targeted findings as noise. Defenders should pin all include directives and container images to commit SHAs, move secrets to masked and protected CI variables, disable fork MR pipeline access to variables, restrict self-hosted runners to protected branches only, drop privileged mode on Docker runners exposed to public projects, and integrate scanners like GoGatoZ into regular audits of internal GitLab instances.

[Centralizing identity security = $2.2M ROI, annually (Sponsor)](https://delinea.com/resources/delinea-platform-roi?utm_medium=paid-newsletter&amp;utm_source=TLDR&amp;utm_campaign=FF-FY26Q2_TLDR_*VisIP&amp;utm_content=TLDR%20Send%205&amp;utm_term=Secondary) And here's the data to prove it. Delinea partnered with independent research firm UserEvidence to  [evaluate annual ROI](https://delinea.com/resources/delinea-platform-roi?utm_medium=paid-newsletter&utm_source=TLDR&utm_campaign=FF-FY26Q2_TLDR_*VisIP&utm_content=TLDR%20Send%205&utm_term=Secondary)  at over 200 Delinea Platform customers. By centralizing identity security, improving visibility and control over privileged access, and automating workflows, customers averaged $2.2M ROI per year.  [Get the whitepaper](https://delinea.com/resources/delinea-platform-roi?utm_medium=paid-newsletter&utm_source=TLDR&utm_campaign=FF-FY26Q2_TLDR_*VisIP&utm_content=TLDR%20Send%205&utm_term=Secondary)

[Offroad (Product Launch)](https://offroad.ai/?utm_source=tldrinfosec) Offroad provides autonomous security agents that identify identity risks across users, machines, AI agents, and SaaS/OAuth apps, gather context from fragmented systems, and then automatically remediate or govern access, with human oversight where needed.

[SkillSpector (GitHub Repo)](https://github.com/nvidia/skillspector?utm_source=tldrinfosec) NVIDIA has released SkillSpector, a security scanner for AI agent skills that combines static analysis, AST-based behavioral inspection, taint tracking, YARA signatures, and optional LLM semantic evaluation across 64 vulnerability patterns spanning prompt injection, data exfiltration, supply chain, MCP least privilege, and tool poisoning, with live OSV.dev CVE lookups and SARIF output for CI integration.

[Aether (GitHub Repo)](https://github.com/0xsp-SRD/aether?utm_source=tldrinfosec) Aether is a Windows memory forensics and threat hunting tool that scans live process memory for various malicious activities.

[Vulnerability and malware checks in uv (4 minute read)](https://astral.sh/blog/uv-audit?utm_source=tldrinfosec) Astral has shipped two preview security features in the uv Python package manager: uv audit, a native dependency scanner for known vulnerabilities and adverse project statuses that runs 4x to 10x faster than pip-audit by leveraging uv's locked resolutions, and an opt-in OSV-based malware check (enabled via UV_MALWARE_CHECK=1) that queries MAL advisories on every sync to abort installation before quarantined-but-still-fetchable malicious distributions execute. The malware check closes a specific gap in locking installers where lockfiles reference object storage directly, allowing distributions removed from the PyPI index to still install from their underlying storage URLs.

[Dashlane explains how attackers managed to download encrypted password vaults (3 minute read)](https://arstechnica.com/security/2026/06/dashlane-explains-how-attackers-managed-to-download-encrypted-password-vaults/?utm_source=tldrinfosec) Attackers abused Dashlane's device-enrollment APIs to spray one-time 2FA codes across many accounts and brute force valid tokens, letting them register new devices on fewer than 20 accounts and download encrypted vaults. They still need to crack master passwords, which Dashlane hardens with Argon2, but weak or reused passwords remain exposed, so affected users should change master passwords and stored credentials.

[VS Code Adds 2-Hour Extension Auto-Update Delay to Limit Supply Chain Attacks (2 minute read)](https://thehackernews.com/2026/06/vs-code-adds-2-hour-extension-auto.html?utm_source=tldrinfosec) Microsoft now delays automatic VS Code extension updates by two hours, except for trusted publishers like Microsoft, GitHub, and OpenAI, which still update immediately. Users can still trigger manual updates and see why updates are pending. Similar cooldown controls in Bundler, Bun, npm, pnpm, and Yarn limit how quickly newly published, potentially malicious packages reach developer environments.

[Council in UK's City of York outs hundreds of disabled residents with a single email blunder (3 minute read)](https://www.theregister.com/security/2026/06/05/council-in-uks-city-of-york-outs-hundreds-of-disabled-residents-with-a-single-email-blunder/5251214?utm_source=tldrinfosec) City of York Council emailed Blue Badge holders without BCC, exposing hundreds of recipients' addresses and implicitly their disability status.

[Suspicious Polyfill login prompts pop up on Toshiba, Muji websites (2 minute read)](https://www.bleepingcomputer.com/news/security/suspicious-polyfill-login-prompts-pop-up-on-toshiba-muji-websites/?utm_source=tldrinfosec) The polyfill[.]io domain, hijacked by a Chinese entity in 2024 and abandoned by site owners who never removed embedded script references, reactivated in late May and began returning HTTP 401 responses that surfaced as browser-native credential prompts on Toshiba, Muji, Zojirushi, FiNC Technologies, Ishiyaku Publishers, Hobonichi, and Samsung Smart TV sites.

[Free Apps on Samsung and LG Smart TVs Secretly Turning Your Devices Into AI Proxies (4 minute read)](https://cybersecuritynews.com/free-apps-turning-smart-tvs-into-proxies/?utm_source=tldrinfosec) Include Security disclosed that Bright Data's SDK, embedded in free Samsung, LG, and Roku apps from partners including PlayWorks Digital, CloudTV, and Viber, silently converts connected TVs into residential proxy exit nodes with ignore_screen_on:true flags and a 200 GB monthly cap.

### Source URL
https://tldr.tech/infosec/2026-06-09
