---
actionability: high
attached_experts: []
channel_name: ''
created_at: '2026-06-05T08:44:40.324181+10:00'
domain: unknown
expert_status: unattached
primary_mode: router
privacy: public
review_status: new
secondary_modes: []
source_type: article
source_url: https://tldr.tech/infosec/2026-05-27
status: processed
suggested_experts: []
tags: []
title: 600K Lithuanian Records Leaked 🇱🇹, KnowledgeDeliver 0-Day RCE 💥, Google Family
  Link Hijack 📱
transcript_path: ''
type: insight_note
updated_at: '2026-06-05T08:44:40.324181+10:00'
---

# 600K Lithuanian Records Leaked 🇱🇹, KnowledgeDeliver 0-Day RCE 💥, Google Family Link Hijack 📱

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
https://tldr.tech/infosec/2026-05-27

How Veriff achieves 99.6% IDV accuracy (Sponsor) Most ID verification vendors claim they track 100s of signals, but under the hood they're just a  chain of third-party APIs . This leads to false positives, false negatives, and lost revenue.  Veriff is a  proven global leader  in identity verification, and that comes with unique network effects. Veriff tracks 1,000+ signals, which means better detection for fraud networks and a platform that keeps getting smarter. With rampant deepfakes and more sophisticated fraud, you can't afford fragmented fraud detection. Trusted by over 3,000 customers, including Webull, Monzo, and Bolt, who rely on Veriff's unified platform. Want to go deeper?  Get a technical demo.

Charter Confirms Data Breach After ShinyHunters Extortion Threat (2 minute read) Charter Communications has confirmed that it suffered a data breach after the ShinyHunters ransomware gang posted an extortion threat. ShinyHunters claimed that it obtained access to the company's Salesforce instance by compromising an employee's Microsoft Entra account via vishing. Charter claims that no customer information was stolen. However, ShinyHunters claim to have stolen customer names, phone numbers, phone types, plan information, and some customer proprietary network information (CPNI).

Lithuania Suspects Foreign Involvement in Data Leak of Over 600k National Register Entries (2 minute read) Lithuanian authorities have disclosed that they suffered a data leak of over 600k entries from national data registers, which they believe was perpetrated by a foreign entity. The data was primarily obtained from registers of legal entities and real estate, accessed using the login credentials of authorized institutions. The stolen data includes addresses of intelligence officers, military personnel, diplomats, and politicians.

Supply Chain Attack Targets Laravel-Lang Packages with Credential Stealer (3 minute read) An attacker compromised 233 versions across three Laravel-Lang repositories, including laravel-lang/lang (7.8k stars), by abusing GitHub's version-tagging system to point tags at commits in an attacker-controlled fork, allowing malicious code to load via Composer's autoloader without touching the official repos. The injected src/helpers.php dropper fingerprints the host, decodes the C2 domain flipboxstudio[.]info from an integer array, and fetches a ~5,900-line PHP stealer that harvests cloud and infrastructure credentials, SSH keys, browser and password-manager vaults, crypto wallets, and communication-platform tokens. It then encrypts the exfiltrated data with AES-256 and deletes itself. Defenders should audit Composer dependencies for the affected versions, block flipboxstudio[.]info, hunt for a marker and dropped .php/.vbs artifacts, and rotate any credentials exposed on affected hosts.

Automating Security Operations with AI: Triaging Renovate PRs (19 minute read) Marco Lancini describes how he configures Renovate to create a monthly PR with dependency updates. He then uses a Claude Code Routine to review the updates and provide a summary risk matrix for the different updates. The skill used by Claude Code and the Renovate config are available in the post.

Exploitation of KnowledgeDeliver via ViewState Deserialization Vulnerability (4 minute read) An unknown threat actor exploited CVE-2026-5426 as a zero-day, abusing hardcoded ASP.NET machineKey values shipped identically across pre-February KnowledgeDeliver LMS deployments to forge malicious ViewState payloads and achieve unauthenticated RCE. Post-exploitation, the actor deployed the in-memory BLUEBEAM (Godzilla) web shell inside w3wp.exe, used icacls to grant "Everyone" full access to the web root, and tampered with an application JavaScript file to serve a fake security plugin that delivered an organization-specific Cobalt Strike BEACON. Defenders should rotate machine keys to unique per-instance values, restrict LMS access by IP, and hunt for Application Event ID 1316 ViewState failures, anomalous w3wp.exe child processes, web-root, .js/.aspx/.config tampering, and concatenated dual-identifier User-Agent strings.

How my minimal, memory-safe Go rsync steers clear of vulnerabilities (10 minute read) Examining all 12 rsync CVEs from the January 2025 and May 2026 batches, the author shows that gokrazy/rsync, a minimal Go reimplementation, avoided 8 of them purely by not implementing the vulnerable features (incremental recursion, compression, proxy support, and hostname ACLs) and that Go's structural defenses neutralized most of the rest: runtime bounds checks convert heap overflows into panics, zero-initialization eliminates stack info leaks, and the traversal-resistant os.Root API closes the TOCTOU symlink races, leaving only one logic bug (CVE-2026-43617) that the language could not have prevented. The practical takeaways are to upgrade to rsync 3.4.3+ or gokrazy/rsync v0.3.3+, layer in defense-in-depth via mount namespaces, systemd hardening, or Landlock, and prefer implementations whose complexity is proportional to the use case, since avoiding unneeded protocol features measurably shrinks the attack surface.

Threat Modeling MCP Server (GitHub Repo) This MCP server provides tools for threat modeling, including business context analysis, architecture analysis, threat actor analysis, trust boundary analysis, asset flow analysis, code security validation, and comprehensive report generation.

iron-proxy (GitHub Repo) iron-proxy is a MitM egress proxy with a built-in DNS server that sits between untrusted workloads and the internet.

IDA Pro MCP (GitHub Repo) An MCP server that exposes IDA Pro's decompilation, disassembly, cross-referencing, and patching to LLM clients, supporting both a GUI plugin and a headless idalib mode that manages multiple databases across worker processes. It ships a broad batch-first toolset spanning decompilation, type and structure operations, memory reads, an optional debugger extension, and py_eval for arbitrary in-IDA Python. Reverse engineers should note the project's own caveat that LLMs hallucinate on number-based conversions and perform poorly on obfuscated code, so deobfuscation and FLIRT/Lumina resolution remain prerequisites for reliable results.

Google APIs Keys Keep Working After You Delete Them (6 minute read) Researchers from Aikido security discovered that Google API key deletion is eventually consistent and can take up to 23 minutes to fully propagate. Gemini API keys and Google Service Account keys propagated in one minute and 5 seconds, respectively. Google initially closed the bug report as “won't fix” but reopened it as a P0 after the researchers published their findings.

CISA Enhances Known Exploited Vulnerabilities Catalog to include New Nomination Form (2 minute read) The Cybersecurity and Information Security Agency (CISA) announced the availability of a new nomination form to enable researchers, vendors, and partners to report known exploited vulnerabilities. The trial of this update is to expedite CISA's ability to identify and act on new KEVs. This move comes after NIST announced changes to its NVD program.

Paved With Intent: ROADtools and Nation-State Tactics in the Cloud (5 minute read) ROADtools, an open-source Python framework for Entra ID enumeration and OAuth token manipulation, has evolved from a red-team utility into an attack platform adopted by nation-state actors, including Cloaked Ursa (APT29), Curious Serpens (APT33), and UTA0355, mapping cleanly to MITRE persistence (T1098.005 device registration), defense evasion (T1550), and discovery (T1087). The tool operates entirely through legitimate Microsoft APIs and customizable user-agent strings, so its activity blends into normal cloud operations and resists traditional file-based detection. The broader lesson is the dual-use dilemma of identity tooling: defenders should counter it with layered controls such as Entra ID token protection, conditional access restrictions on device code flow, OAuth app audits, and SIEM correlation of Graph API logs to surface scripted Python-based access and bursty enumeration.

Uniswap Google Ads phishing nets at least $400,000 from fake wallet approvals (2 minute read) Attackers bought cloaked Google-sponsored links impersonating Uniswap to send searchers to cloned trading interfaces that trick victims into signing malicious wallet permissions, draining at least $400,000 in a campaign SEAL ties to a broader malvertising surge of 356+ malicious ad links and $1.27 million in losses since March.

Microsoft Copilot Cowork Exfiltrates Files (1 minute read) Microsoft Copilot Cowork lets agents send unapproved emails to a user's own inbox that render external images, so a prompt injection could exfiltrate data and leak pre-authenticated OneDrive download links to an attacker when the victim opens the message.

Google Family Link exploit that locks out victims permanently (2 minute read) Attackers with stolen credentials or session cookies abuse Google Family Link by editing the victim's date of birth to under 13 and linking the account to an attacker-controlled "Parent," which overrides 2FA, recovery phone, and backup email, grants the hacker location tracking and remote device lock, and leaves no automated recovery path short of YouTube (@TeamYouTube) escalation or paid Google One support.

### Fetched Web Text
How Veriff achieves 99.6% IDV accuracy (Sponsor) Most ID verification vendors claim they track 100s of signals, but under the hood they're just a  chain of third-party APIs . This leads to false positives, false negatives, and lost revenue.  Veriff is a  proven global leader  in identity verification, and that comes with unique network effects. Veriff tracks 1,000+ signals, which means better detection for fraud networks and a platform that keeps getting smarter. With rampant deepfakes and more sophisticated fraud, you can't afford fragmented fraud detection. Trusted by over 3,000 customers, including Webull, Monzo, and Bolt, who rely on Veriff's unified platform. Want to go deeper?  Get a technical demo.

Charter Confirms Data Breach After ShinyHunters Extortion Threat (2 minute read) Charter Communications has confirmed that it suffered a data breach after the ShinyHunters ransomware gang posted an extortion threat. ShinyHunters claimed that it obtained access to the company's Salesforce instance by compromising an employee's Microsoft Entra account via vishing. Charter claims that no customer information was stolen. However, ShinyHunters claim to have stolen customer names, phone numbers, phone types, plan information, and some customer proprietary network information (CPNI).

Lithuania Suspects Foreign Involvement in Data Leak of Over 600k National Register Entries (2 minute read) Lithuanian authorities have disclosed that they suffered a data leak of over 600k entries from national data registers, which they believe was perpetrated by a foreign entity. The data was primarily obtained from registers of legal entities and real estate, accessed using the login credentials of authorized institutions. The stolen data includes addresses of intelligence officers, military personnel, diplomats, and politicians.

Supply Chain Attack Targets Laravel-Lang Packages with Credential Stealer (3 minute read) An attacker compromised 233 versions across three Laravel-Lang repositories, including laravel-lang/lang (7.8k stars), by abusing GitHub's version-tagging system to point tags at commits in an attacker-controlled fork, allowing malicious code to load via Composer's autoloader without touching the official repos. The injected src/helpers.php dropper fingerprints the host, decodes the C2 domain flipboxstudio[.]info from an integer array, and fetches a ~5,900-line PHP stealer that harvests cloud and infrastructure credentials, SSH keys, browser and password-manager vaults, crypto wallets, and communication-platform tokens. It then encrypts the exfiltrated data with AES-256 and deletes itself. Defenders should audit Composer dependencies for the affected versions, block flipboxstudio[.]info, hunt for a marker and dropped .php/.vbs artifacts, and rotate any credentials exposed on affected hosts.

Automating Security Operations with AI: Triaging Renovate PRs (19 minute read) Marco Lancini describes how he configures Renovate to create a monthly PR with dependency updates. He then uses a Claude Code Routine to review the updates and provide a summary risk matrix for the different updates. The skill used by Claude Code and the Renovate config are available in the post.

Exploitation of KnowledgeDeliver via ViewState Deserialization Vulnerability (4 minute read) An unknown threat actor exploited CVE-2026-5426 as a zero-day, abusing hardcoded ASP.NET machineKey values shipped identically across pre-February KnowledgeDeliver LMS deployments to forge malicious ViewState payloads and achieve unauthenticated RCE. Post-exploitation, the actor deployed the in-memory BLUEBEAM (Godzilla) web shell inside w3wp.exe, used icacls to grant "Everyone" full access to the web root, and tampered with an application JavaScript file to serve a fake security plugin that delivered an organization-specific Cobalt Strike BEACON. Defenders should rotate machine keys to unique per-instance values, restrict LMS access by IP, and hunt for Application Event ID 1316 ViewState failures, anomalous w3wp.exe child processes, web-root, .js/.aspx/.config tampering, and concatenated dual-identifier User-Agent strings.

How my minimal, memory-safe Go rsync steers clear of vulnerabilities (10 minute read) Examining all 12 rsync CVEs from the January 2025 and May 2026 batches, the author shows that gokrazy/rsync, a minimal Go reimplementation, avoided 8 of them purely by not implementing the vulnerable features (incremental recursion, compression, proxy support, and hostname ACLs) and that Go's structural defenses neutralized most of the rest: runtime bounds checks convert heap overflows into panics, zero-initialization eliminates stack info leaks, and the traversal-resistant os.Root API closes the TOCTOU symlink races, leaving only one logic bug (CVE-2026-43617) that the language could not have prevented. The practical takeaways are to upgrade to rsync 3.4.3+ or gokrazy/rsync v0.3.3+, layer in defense-in-depth via mount namespaces, systemd hardening, or Landlock, and prefer implementations whose complexity is proportional to the use case, since avoiding unneeded protocol features measurably shrinks the attack surface.

Threat Modeling MCP Server (GitHub Repo) This MCP server provides tools for threat modeling, including business context analysis, architecture analysis, threat actor analysis, trust boundary analysis, asset flow analysis, code security validation, and comprehensive report generation.

iron-proxy (GitHub Repo) iron-proxy is a MitM egress proxy with a built-in DNS server that sits between untrusted workloads and the internet.

IDA Pro MCP (GitHub Repo) An MCP server that exposes IDA Pro's decompilation, disassembly, cross-referencing, and patching to LLM clients, supporting both a GUI plugin and a headless idalib mode that manages multiple databases across worker processes. It ships a broad batch-first toolset spanning decompilation, type and structure operations, memory reads, an optional debugger extension, and py_eval for arbitrary in-IDA Python. Reverse engineers should note the project's own caveat that LLMs hallucinate on number-based conversions and perform poorly on obfuscated code, so deobfuscation and FLIRT/Lumina resolution remain prerequisites for reliable results.

Google APIs Keys Keep Working After You Delete Them (6 minute read) Researchers from Aikido security discovered that Google API key deletion is eventually consistent and can take up to 23 minutes to fully propagate. Gemini API keys and Google Service Account keys propagated in one minute and 5 seconds, respectively. Google initially closed the bug report as “won't fix” but reopened it as a P0 after the researchers published their findings.

CISA Enhances Known Exploited Vulnerabilities Catalog to include New Nomination Form (2 minute read) The Cybersecurity and Information Security Agency (CISA) announced the availability of a new nomination form to enable researchers, vendors, and partners to report known exploited vulnerabilities. The trial of this update is to expedite CISA's ability to identify and act on new KEVs. This move comes after NIST announced changes to its NVD program.

Paved With Intent: ROADtools and Nation-State Tactics in the Cloud (5 minute read) ROADtools, an open-source Python framework for Entra ID enumeration and OAuth token manipulation, has evolved from a red-team utility into an attack platform adopted by nation-state actors, including Cloaked Ursa (APT29), Curious Serpens (APT33), and UTA0355, mapping cleanly to MITRE persistence (T1098.005 device registration), defense evasion (T1550), and discovery (T1087). The tool operates entirely through legitimate Microsoft APIs and customizable user-agent strings, so its activity blends into normal cloud operations and resists traditional file-based detection. The broader lesson is the dual-use dilemma of identity tooling: defenders should counter it with layered controls such as Entra ID token protection, conditional access restrictions on device code flow, OAuth app audits, and SIEM correlation of Graph API logs to surface scripted Python-based access and bursty enumeration.

Uniswap Google Ads phishing nets at least $400,000 from fake wallet approvals (2 minute read) Attackers bought cloaked Google-sponsored links impersonating Uniswap to send searchers to cloned trading interfaces that trick victims into signing malicious wallet permissions, draining at least $400,000 in a campaign SEAL ties to a broader malvertising surge of 356+ malicious ad links and $1.27 million in losses since March.

Microsoft Copilot Cowork Exfiltrates Files (1 minute read) Microsoft Copilot Cowork lets agents send unapproved emails to a user's own inbox that render external images, so a prompt injection could exfiltrate data and leak pre-authenticated OneDrive download links to an attacker when the victim opens the message.

Google Family Link exploit that locks out victims permanently (2 minute read) Attackers with stolen credentials or session cookies abuse Google Family Link by editing the victim's date of birth to under 13 and linking the account to an attacker-controlled "Parent," which overrides 2FA, recovery phone, and backup email, grants the hacker location tracking and remote device lock, and leaves no automated recovery path short of YouTube (@TeamYouTube) escalation or paid Google One support.

### Source URL
https://tldr.tech/infosec/2026-05-27
