# Skill Security Scanning for LifeOS Agent Plugins

## Problem
LifeOS supports a plugin/skill ecosystem where third-party skills can be installed to extend agent capabilities. As demonstrated by the Zcash infinite-mint bug (introduced via undetected vulnerabilities in complex code) and the general risk of prompt injection, malicious or vulnerable skills pose a critical threat. A skill with hidden malicious patterns could exfiltrate data, manipulate agent behavior, or introduce exploits.

## Proposed Solution
Integrate a **Skill Security Scanner** into LifeOS's skill installation pipeline, inspired by NVIDIA's SkillSpector:
- Before any skill is installed or updated, it is statically analyzed for known vulnerability patterns, malicious code signatures, and dangerous capability requests (e.g., unrestricted network access, filesystem writes outside sandbox).
- Skills are assigned a risk score; high-risk skills require explicit user approval.
- Maintain a curated skill registry with verified, audited skills that bypass deep scanning.
- Run skills in a permissioned capability model where declared intents are enforced at runtime (e.g., a skill that declares "read calendar" cannot access contacts).
- Provide a `skill audit log` so users can review what each skill was granted access to.

## Source
https://github.com/NVIDIA/SkillSpector

## Status
Proposed

## Effort
Medium