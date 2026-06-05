from __future__ import annotations

import datetime
import json
import re
import shutil
import sys
import time
from pathlib import Path

import yaml

# Project root — three levels up from src/core/ingest.py
ROOT = Path(__file__).resolve().parent.parent.parent

# Ensure scripts/ is on the path so legacy modules can be imported
_SCRIPTS_DIR = ROOT / "src"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _clean_url(url: str) -> str:
    return url.strip().strip(' "\'.,;!)]>')

def _extract_markdown_title(content: str) -> str:
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    for line in content.splitlines():
        line = line.strip()
        if line and not line.startswith("<!--") and not line.startswith("---"):
            clean = re.sub(r"^[#\s\-*+>]+", "", line)
            clean = re.sub(r"[*_`]", "", clean).strip()
            if clean:
                return clean
    return ""

def _deduplicate_tags(tag_str: str, extra: list[str] | None = None) -> str:
    parts = [t.strip() for t in tag_str.split(",") if t.strip()]
    if extra:
        parts.extend(extra)
    seen = set()
    unique = []
    for tag in parts:
        key = tag.lower()
        if key not in seen:
            seen.add(key)
            unique.append(tag)
    return ", ".join(unique[:10])

def _build_note_content(
    *,
    title: str,
    source_url: str,
    decision: dict,
    channel: str,
    transcript_path: str,
    tags: str,
    now_str: str,
    ai_data: dict | None,
    warning_text: str,
    transcript_display: str,
    raw_content: str,
    suggested_experts_yaml: str,
) -> str:
    sec_modes = decision.get("secondary_modes", [])
    privacy_val = decision.get("privacy", "public")
    source_type = "youtube_video" if (channel and "youtu" in source_url) else ("article" if source_url else "text")

    fm: dict = {
        "title": title,
        "source_url": source_url,
        "type": "insight_note",
        "domain": decision.get("primary_domain", ""),
        "primary_mode": decision.get("primary_mode", ""),
        "secondary_modes": sec_modes,
        "tags": [t.strip() for t in tags.split(",") if t.strip()],
        "created_at": now_str,
        "updated_at": now_str,
        "privacy": privacy_val,
        "status": "processed",
        "actionability": "high",
        "expert_status": "unattached",
        "suggested_experts": [s.strip() for s in suggested_experts_yaml.split(",") if s.strip()],
        "attached_experts": [],
        "review_status": "new",
        "channel_name": channel,
        "transcript_path": transcript_path,
        "source_type": source_type,
    }
    fm_yaml = yaml.dump(fm, default_flow_style=False, allow_unicode=True)
    note = f"---\n{fm_yaml}---\n\n# {title}\n\n"

    if ai_data and "summary" in ai_data:
        note += f"## Summary\n{warning_text}{ai_data.get('summary', '')}\n\n"
        note += "## Key Ideas\n"
        for idea in ai_data.get("key_ideas", []):
            note += f"- {idea}\n"
        note += "\n## Why this matters for Markus\n"
        for reason in ai_data.get("why_this_matters_for_markus", []):
            note += f"- {reason}\n"
        note += "\n## Related Modes\n"
        for mode in ai_data.get("related_modes", []):
            note += f"- {mode}\n"
        note += f"\n## Next Action\n- [ ] {ai_data.get('next_action', '')}\n"

        if ai_data.get("is_chunked"):
            note += (
                f"\n## Long Resource Processing\n"
                f"- chunks processed: {ai_data['chunks_processed']}\n"
                "- method: chunked map-reduce summary\n"
            )

        provider = ai_data.get("provider_used", "Unknown")
        model = ai_data.get("model_used", "Unknown")
        note += f"\n## AI Generation Data\n- Provider: {provider}\n- Model: {model}\n"

        reliability = ai_data.get("source_reliability", "Based on resource content.")
        note += f"\n## Source Reliability\n{reliability}\n"

    elif ai_data and "raw_output" in ai_data:
        provider = ai_data.get("provider_used", "Unknown")
        model = ai_data.get("model_used", "Unknown")
        note += (
            f"## Summary\n{warning_text}AI summarization succeeded, but JSON parsing failed.\n\n"
            f"## AI Raw Output\n```text\n{ai_data['raw_output']}\n```\n\n"
            "## Key Ideas\n- Refer to the AI Raw Output above.\n\n"
            "## Why this matters for Markus\n- Refer to the AI Raw Output above.\n\n"
            f"## Related Modes\n- {decision.get('primary_mode', '')}\n"
        )
        for m in sec_modes:
            note += f"- {m}\n"
        note += f"\n## AI Generation Data\n- Provider: {provider}\n- Model: {model}\n"
        note += (
            "\n## Next Action\n"
            "- [ ] Review raw AI output and extract action items manually.\n\n"
            "## Source Reliability\nAI summarization was performed but parsing failed.\n"
        )
    else:
        note += (
            f"## Summary\n{warning_text}**Manual summary needed.**\n\n"
            "## Key Ideas\n- Manual extraction needed.\n\n"
            f"## Why this matters for Markus\n"
            f"- Suggested based on routing to {decision.get('primary_domain', '')}.\n\n"
            f"## Related Modes\n- {decision.get('primary_mode', '')}\n"
        )
        for m in sec_modes:
            note += f"- {m}\n"
        one_next = decision.get("one_next_action", "Review and summarise manually.")
        note += f"\n## Next Action\n- [ ] {one_next}\n\n## Source Reliability\nBased on raw user input and metadata.\n"

    if ai_data and ai_data.get("is_chunked") and ai_data.get("chunk_summaries"):
        note += f"\n## Detailed Chunk Summaries\n\n{ai_data['chunk_summaries']}\n"

    note += f"\n## Original Content\n### Raw User Input\n{raw_content}\n\n### Source URL\n{source_url}{transcript_display}\n"
    return note


def _extract_title_from_url(url: str) -> str:
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        path = parsed.path.strip("/")
        
        segments = [s for s in path.split("/") if s]
        netloc_lower = parsed.netloc.lower()
        
        # Special handling for Twitter / X URLs
        if "x.com" in netloc_lower or "twitter.com" in netloc_lower:
            if len(segments) >= 1:
                username = segments[0]
                if username not in ("home", "explore", "notifications", "messages", "search", "i"):
                    return f"X Post by @{username}"
                    
        if not path:
            netloc = parsed.netloc
            if netloc.startswith("www."):
                netloc = netloc[4:]
            return netloc.split(".")[0].title()
        
        if not segments:
            return "Web Page"
        last_segment = segments[-1]
        
        if re.match(r"^\d+$", last_segment) and len(segments) > 1:
            last_segment = segments[-2]
            
        if "." in last_segment:
            last_segment = last_segment.split(".")[0]
            
        clean = last_segment.replace("-", " ").replace("_", " ").strip()
        title = clean.title()
        return title if title else "Web Page"
    except Exception:
        return "Web Page"



def _extract_metadata(content: str, filepath: Path, log) -> dict:
    from core.youtube import fetch_video_metadata, fetch_transcript
    from core.web import fetch_webpage_content
    
    suggested_url = ""
    suggested_title = ""
    channel = ""
    transcript: str | None = None
    is_youtube = False
    fetched_web_text = ""

    urls = re.findall(r"(https?://[^\s>\])'\"]+)", content)
    if urls:
        suggested_url = _clean_url(urls[0])
        if "youtube.com" in suggested_url or "youtu.be" in suggested_url:
            is_youtube = True
            log(f"Detected YouTube URL: {suggested_url}")
            meta = fetch_video_metadata(suggested_url)
            suggested_title = meta.get("title", "")
            channel = meta.get("uploader", "")
            if suggested_title:
                log(f"YouTube title: {suggested_title}")
            transcript = fetch_transcript(suggested_url)
            if transcript:
                log(f"Transcript fetched ({len(transcript)} chars)")
            else:
                log("Transcript unavailable")
        else:
            log(f"Detected web URL: {suggested_url}")
            suggested_title, fetched_web_text = fetch_webpage_content(suggested_url)

    if not suggested_title or suggested_title.startswith("http://") or suggested_title.startswith("https://"):
        if suggested_url:
            suggested_title = _extract_title_from_url(suggested_url)
        else:
            suggested_title = _extract_markdown_title(content)

    if not suggested_title or suggested_title.startswith("http://") or suggested_title.startswith("https://"):
        if suggested_url:
            suggested_title = _extract_title_from_url(suggested_url)
        else:
            suggested_title = filepath.stem

    return {
        "title": suggested_title,
        "source_url": suggested_url,
        "channel": channel,
        "transcript": transcript,
        "is_youtube": is_youtube,
        "fetched_web_text": fetched_web_text
    }

def _get_routing_decision(content: str, title: str, source_url: str, is_youtube: bool, channel: str, transcript: str | None, filepath: Path, log) -> dict:
    if is_youtube:
        transcript_excerpt = transcript[:2000] if transcript else ""
        combined_text = f"{title} {channel} {source_url} {transcript_excerpt}"
    else:
        combined_text = f"{content} {title} {source_url}"

    try:
        from src.core.classify_input import classify  # type: ignore
        decision = classify(combined_text, filepath=str(filepath))
    except Exception as exc:
        log(f"Warning: classify_input failed ({exc}), using fallback routing")
        decision = {
            "primary_domain": "general",
            "primary_mode": "router",
            "secondary_modes": [],
            "storage_location": "data/inbox/processed/needs-review/",
            "suggested_tags": [],
            "one_next_action": "Review manually.",
            "privacy": "public",
        }

    # YouTube AI-keyword override
    if is_youtube and title:
        ai_keywords = ["deepseek", "ai", "llm", "model", "openai", "gemini", "claude", "rag", "agent", "embedding"]
        if any(kw in title.lower() for kw in ai_keywords):
            decision["primary_domain"] = "ai-platform"
            decision["primary_mode"] = "research-resource"
            decision["secondary_modes"] = ["ai-builder"]
            decision["storage_location"] = "data/knowledge/ai-resources/"

    return decision

def load_user_profile():
    base_dir = Path(__file__).resolve().parent.parent.parent
    profile_path = base_dir / "config" / "profile.yml"
    if not profile_path.exists():
        profile_path = base_dir / "config" / "profile.example.yml"
    if profile_path.exists():
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                parsed = yaml.safe_load(f)
                return parsed if isinstance(parsed, dict) else {}
        except Exception:
            pass
    return {}

def generate_resource_summary(title, source_url, domain, primary_mode, secondary_modes, raw_content):
    profile = load_user_profile()
    user_name = profile.get("name", "Markus")
    user_role = profile.get("role", "AI Systems Builder & Wellness Entrepreneur")
    user_prefs = profile.get("preferences", {})
    comm_style = user_prefs.get("communication_style", "direct, structured, action-oriented")
    
    domains_focus = []
    for d_entry in profile.get("core_domains", []):
        d_name = d_entry.get("name", d_entry["id"])
        d_focus = ", ".join(d_entry.get("focus", []))
        domains_focus.append(f"- {d_name} ({d_entry['id']}): Focuses on {d_focus}")
    domains_str = "\n".join(domains_focus) if domains_focus else "- General Life & Career Management"

    system_prompt = (
        f"You are LifeOS Research Resource Mode. You turn raw transcripts, books, and articles into useful, deep, highly personalized structured notes for {user_name}.\n\n"
        f"User Profile:\n"
        f"- Name: {user_name}\n"
        f"- Role: {user_role}\n"
        f"- Core Domains & Focus Areas:\n{domains_str}\n\n"
        f"Style & Preference Guidelines:\n"
        f"- Style: {comm_style}\n"
        f"- Formatting: Rich, deep, analytical, structured. No generic corporate speak or fluff. Be concrete and specific.\n"
        f"- Do not invent facts. Return valid JSON only."
    )
    sec_modes_str = ", ".join(secondary_modes) if secondary_modes else "None"
    
    from src.core.llm_client import try_providers, parse_json_safely, split_text
    overall_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    provider_used = "unknown"
    model_used = "unknown"
    
    if len(raw_content) > 18000:
        chunks = split_text(raw_content, chunk_size=12000, overlap=1000)
        print(f"\n  [*] Long content detected ({len(raw_content)} chars). Splitting into {len(chunks)} chunks.")
        
        chunk_summaries = []
        for i, chunk in enumerate(chunks):
            print(f"\n  === Summarizing chunk {i+1}/{len(chunks)} ===")
            chunk_prompt = f"Analyze this part ({i+1}/{len(chunks)}) of the resource '{title}'. Extract key points concisely.\n\nContent:\n{chunk}"
            res = try_providers("You are a helpful research assistant. Summarize the text concisely.", chunk_prompt, 800)
            if res:
                content, p_name, m_name, t_usage = res
                chunk_summaries.append(content)
                provider_used = p_name
                model_used = m_name
                overall_usage["prompt_tokens"] += t_usage.get("prompt_tokens", 0)
                overall_usage["completion_tokens"] += t_usage.get("completion_tokens", 0)
                overall_usage["total_tokens"] += t_usage.get("total_tokens", 0)
            else:
                chunk_summaries.append(f"[Chunk {i+1} failed]")

        combined_summaries = "\n\n---\n\n".join(f"Chunk {i+1} Summary:\n{s}" for i, s in enumerate(chunk_summaries))
        user_prompt = f"""
Analyze this resource in depth:
Title: {title}
URL: {source_url}
Domain: {domain}
Primary Mode: {primary_mode}
Secondary Modes: {sec_modes_str}

Combined Chunk Summaries:
{combined_summaries}

Return JSON only in this exact format:
{{
  "summary": "Detailed multi-paragraph summary of the resource's core arguments and worldview.",
  "key_ideas": [
    "Key concept 1: Actionable, rich description of what it is and how to apply it.",
    "Key concept 2: Actionable, rich description..."
  ],
  "why_this_matters_for_markus": [
    "Specific connection to Markus's projects/focus areas.",
    "Specific connection..."
  ],
  "suggested_tags": ["string"],
  "related_modes": ["string"],
  "next_action": "One concrete, step-by-step next action for Markus to implement.",
  "source_reliability": "string",
  "confidence": "low|medium|high"
}}
"""
        final_res = try_providers(system_prompt, user_prompt, 1500)
        if final_res:
            content, p_name, m_name, t_usage = final_res
            parsed = parse_json_safely(content)
            if parsed:
                parsed["is_chunked"] = True
                parsed["chunks_processed"] = len(chunks)
                parsed["chunk_summaries"] = combined_summaries
                parsed["provider_used"] = p_name
                parsed["model_used"] = m_name
                parsed["token_usage"] = t_usage
                return parsed
        return {"raw_output": "Final synthesis failed.", "is_chunked": True}
            
    else:
        user_prompt = f"""
Analyze this resource in depth:
Title: {title}
URL: {source_url}
Domain: {domain}
Primary Mode: {primary_mode}
Secondary Modes: {sec_modes_str}

Content:
{raw_content}

Return JSON only in this exact format:
{{
  "summary": "Detailed multi-paragraph summary of the resource's core arguments and worldview.",
  "key_ideas": [
    "Key concept 1: Actionable, rich description of what it is and how to apply it.",
    "Key concept 2: Actionable, rich description..."
  ],
  "why_this_matters_for_markus": [
    "Specific connection to Markus's projects/focus areas.",
    "Specific connection..."
  ],
  "suggested_tags": ["string"],
  "related_modes": ["string"],
  "next_action": "One concrete, step-by-step next action for Markus to implement.",
  "source_reliability": "string",
  "confidence": "low|medium|high"
}}
"""
        print("\n  === Generating summary ===")
        res = try_providers(system_prompt, user_prompt, 1500)
        if res:
            content, p_name, m_name, t_usage = res
            parsed = parse_json_safely(content)
            if parsed:
                parsed["is_chunked"] = False
                parsed["provider_used"] = p_name
                parsed["model_used"] = m_name
                parsed["token_usage"] = t_usage
                return parsed
        return None

def _run_ai_summarisation(title: str, source_url: str, channel: str, transcript: str | None, is_youtube: bool, content: str, fetched_web_text: str, decision: dict, log) -> dict | None:
    log("Running AI summarisation…")
    llm_content = transcript if (is_youtube and transcript) else (
        f"Title: {title}\nChannel: {channel}\nURL: {source_url}" if is_youtube 
        else f"Content:\n{content}\n\nFetched Web Page Text:\n{fetched_web_text}"
    )
    try:
        ai_data = generate_resource_summary(
            title=title,
            source_url=source_url,
            domain=decision["primary_domain"],
            primary_mode=decision["primary_mode"],
            secondary_modes=decision["secondary_modes"],
            raw_content=llm_content,
        )
        if ai_data and "raw_output" not in ai_data:
            log("AI summarisation successful")
        elif ai_data and "raw_output" in ai_data:
            log("AI summarisation completed but JSON parsing failed")
        else:
            log("All LLM providers failed — using manual placeholder")
        return ai_data
    except Exception as exc:
        log(f"AI summarisation error: {exc}")
        return None

def _get_unique_filepath(target_dir: Path, filename: str) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    out_filename = filename[:-4] + ".md" if filename.endswith(".txt") else filename
    out_filepath = target_dir / out_filename
    counter = 1
    stem, ext = out_filepath.stem, out_filepath.suffix
    while out_filepath.exists():
        out_filepath = target_dir / f"{stem}_{counter}{ext}"
        counter += 1
    return out_filepath

def _run_cheap_triage(title: str, source_url: str, content: str, transcript: str | None, is_youtube: bool, log) -> dict | None:
    from src.core.llm_client import try_providers, parse_json_safely
    log("Running cheap AI triage (tags & domain only)…")
    
    if is_youtube and transcript:
        sample_text = transcript[:1500]
    else:
        sample_text = content[:1500]
        
    # Load valid domains from config/domains.yaml
    domains_list = []
    try:
        config_path = ROOT / "config" / "domains.yaml"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                domains_data = yaml.safe_load(f)
                if isinstance(domains_data, dict) and "domains" in domains_data:
                    domains_list = list(domains_data["domains"].keys())
    except Exception as e:
        log(f"Error loading domains.yaml in triage: {e}")

    # Fallback list if domains.yaml loading fails or is empty
    if not domains_list:
        domains_list = ["ai-platform", "flow-temple", "career", "creator-wisdom", "life-kompass", "body-practice"]

    system_prompt = (
        "You are a fast router. Analyze the text and output a JSON object with 'domain' (a short string) "
        "and 'tags' (a list of 3-5 string keywords).\n"
        f"CRITICAL: The 'domain' value MUST be one of these exact keys: {domains_list}. Do NOT make up any other domain.\n"
        "Output ONLY valid JSON. No markdown blocks, no backticks, no explanations."
    )
    user_prompt = (
        f"Title: {title}\nURL: {source_url}\n\nContent Sample:\n{sample_text}\n\n"
        f"Return EXACTLY this format (domain MUST be one of {domains_list}):\n"
        "{\n\"domain\": \"...\",\n\"tags\": [\"...\"]\n}"
    )
    
    try:
        res = try_providers(system_prompt, user_prompt, 1000, 0.1)
        if res:
            llm_text, p_name, m_name, t_usage = res
            parsed = parse_json_safely(llm_text)
            if parsed:
                domain_val = parsed.get("domain")
                if domain_val not in domains_list:
                    # Try simple normalization (e.g., lowercase, replace space/underscore with dash)
                    normalized = str(domain_val).lower().replace("_", "-").replace(" ", "-")
                    if normalized in domains_list:
                        parsed["domain"] = normalized
                    else:
                        log(f"Cheap triage returned invalid domain '{domain_val}'. Rejecting invalid domain.")
                        parsed["domain"] = None
                log(f"Cheap triage successful: domain='{parsed.get('domain')}', tags={parsed.get('tags')}")
                return parsed
        return None
    except Exception as exc:
        log(f"Cheap triage error: {exc}")
        return None

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def process_one_file(source: str, use_ai: bool = False, status_callback=None, rebuild_index_after: bool = True) -> dict:
    from core.youtube import extract_video_id, save_transcript  # type: ignore
    from core.experts import _suggest_experts_for_domain  # type: ignore

    result: dict = {
        "success": False, "out_filepath": None, "decision": None, "title": None,
        "tags": None, "ai_used": False, "ai_parsed": False, "ai_data": None,
        "transcript_path": None, "chunk_report_path": None, "process_time_sec": 0.0,
        "log": [], "error": None,
    }
    start_time = time.time()

    def log(msg: str) -> None:
        result["log"].append(msg)
        if status_callback: status_callback(msg)

    filepath = Path(source)
    filename = filepath.name

    try:
        content = filepath.read_text(encoding="utf-8")
    except OSError as exc:
        result["error"] = f"Could not read file: {exc}"
        return result

    # 1. Metadata extraction
    meta = _extract_metadata(content, filepath, log)
    title, source_url = meta["title"], meta["source_url"]
    is_youtube, transcript = meta["is_youtube"], meta["transcript"]
    channel, fetched_web_text = meta["channel"], meta["fetched_web_text"]
    
    if fetched_web_text:
        content += f"\n\n### Fetched Web Text\n{fetched_web_text}"

    # 2. Routing decision
    decision = _get_routing_decision(content, title, source_url, is_youtube, channel, transcript, filepath, log)
    result["decision"], result["title"] = decision, title
    log(f"Routed → {decision['primary_mode']} | {decision['storage_location']}")
    suggested_tags_str = ", ".join(decision.get("suggested_tags", []))

    # 3. Optional AI summarisation
    ai_data: dict | None = None
    warning_text = "Transcript unavailable. Summary is based only on title/metadata.\n\n" if (is_youtube and not transcript) else ""

    if use_ai:
        result["ai_used"] = True
        ai_data = _run_ai_summarisation(title, source_url, channel, transcript, is_youtube, content, fetched_web_text, decision, log)
        if ai_data and "raw_output" not in ai_data:
            result["ai_parsed"] = True
            suggested_tags_str = _deduplicate_tags(suggested_tags_str, ai_data.get("suggested_tags", []))
        result["ai_data"] = ai_data
    else:
        triage_data = _run_cheap_triage(title, source_url, content, transcript, is_youtube, log)
        if triage_data:
            new_domain = triage_data.get("domain")
            if new_domain and decision.get("primary_domain") in ["unknown", "general", ""]:
                decision["primary_domain"] = new_domain
            new_tags = triage_data.get("tags", [])
            if new_tags:
                suggested_tags_str = _deduplicate_tags(suggested_tags_str, new_tags)

    # 4. Deduplicate tags
    tags = _deduplicate_tags(suggested_tags_str)
    result["tags"] = tags

    # 5. Determine output path
    slugified_name = filename
    if filename.startswith("tmp") and title:
        # Create a clean slug from the title
        clean_title = re.sub(r'[^a-zA-Z0-9\s-]', '', title).strip().lower()
        slugified_name = re.sub(r'[\s-]+', '-', clean_title) + ".md"
        if not slugified_name or slugified_name == ".md":
            slugified_name = filename

    out_filepath = _get_unique_filepath(ROOT / decision["storage_location"], slugified_name)
    saved_stem = out_filepath.stem

    # 6. Save transcript
    transcript_display = ""
    saved_transcript_path = ""
    if is_youtube:
        if transcript:
            raw_transcript_dir = ROOT / "data" / "knowledge" / "ai-resources" / "raw"
            transcript_file = save_transcript(transcript, f"{saved_stem}_transcript", raw_transcript_dir)
            saved_transcript_path = str(transcript_file)
            result["transcript_path"] = saved_transcript_path
            log(f"Transcript saved to: {transcript_file}")
            excerpt = transcript[:1500] + ("..." if len(transcript) > 1500 else "")
            transcript_display = f"\n### Transcript Excerpt (max 1500 chars)\n{excerpt}\n\n### Full Transcript File\n[full_transcript](file://{transcript_file})"
        else:
            transcript_display = "\n### Transcript\nTranscript unavailable."

    # 7. Suggested experts
    suggested_experts_yaml = ", ".join(_suggest_experts_for_domain(
        domain=decision["primary_domain"], tags=[t.strip() for t in tags.split(",") if t.strip()], channel=channel or "", root=ROOT
    ))

    # 8. Build note content
    now_str = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()
    note_content = _build_note_content(
        title=title, source_url=source_url, decision=decision, channel=channel,
        transcript_path=saved_transcript_path, tags=tags, now_str=now_str, ai_data=ai_data,
        warning_text=warning_text, transcript_display=transcript_display,
        raw_content=content, suggested_experts_yaml=suggested_experts_yaml
    )

    # 9. Save chunk report
    chunk_report_path = None
    if ai_data and ai_data.get("is_chunked") and "chunk_summaries" in ai_data:
        chunk_report = ROOT / "outputs" / "reports" / f"{saved_stem}_chunks{out_filepath.suffix}"
        chunk_report.parent.mkdir(parents=True, exist_ok=True)
        try:
            chunk_report.write_text(f"# Chunk Summaries for {title}\n\n{ai_data['chunk_summaries']}", encoding="utf-8")
            log(f"Chunk summaries saved to: {chunk_report}")
            chunk_report_path = str(chunk_report)
            result["chunk_report_path"] = chunk_report_path
        except OSError as exc:
            log(f"Failed to save chunk summaries: {exc}")

    # 10. Write note
    try:
        out_filepath.write_text(note_content, encoding="utf-8")
        log(f"Note saved to: {out_filepath}")
        
        # Queue in automation_outbox
        try:
            import sqlite3
            db_path = ROOT / "indexes" / "lifeos.db"
            db_path.parent.mkdir(parents=True, exist_ok=True)
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS automation_outbox (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        note_path TEXT,
                        source_url TEXT,
                        word_count INTEGER,
                        added_at TEXT,
                        processed_at TEXT,
                        score INTEGER,
                        is_actionable INTEGER,
                        hermes_run_at TEXT
                    )
                """)
                relative_note_path = str(out_filepath.relative_to(ROOT))
                cursor.execute("""
                    INSERT INTO automation_outbox (note_path, source_url, word_count, added_at)
                    VALUES (?, ?, ?, ?)
                """, (relative_note_path, source_url, len(note_content.split()), now_str))
                conn.commit()
                log(f"Queued in automation_outbox: {relative_note_path}")
        except Exception as db_exc:
            log(f"Warning: failed to queue note in automation_outbox: {db_exc}")
            
    except OSError as exc:
        result["error"] = f"Failed to save note: {exc}"
        result["process_time_sec"] = round(time.time() - start_time, 2)
        return result

    # 11. Move raw file to processed/raw
    processed_inbox = ROOT / "data" / "inbox" / "processed" / "raw"
    dest = _get_unique_filepath(processed_inbox, filename)
    try:
        shutil.move(str(filepath), str(dest))
        log(f"Raw file moved to: {dest}")
    except OSError as exc:
        log(f"Warning: could not move raw file: {exc}")

    result["success"], result["out_filepath"] = True, str(out_filepath)
    result["process_time_sec"] = round(time.time() - start_time, 2)

    # 12. Write ingestion log
    log_entry = {
        "timestamp": now_str, "source_url": source_url, "title": title,
        "detected_type": "youtube" if is_youtube else "web/text",
        "primary_domain": decision.get("primary_domain", ""), "primary_mode": decision.get("primary_mode", ""),
        "secondary_modes": decision.get("secondary_modes", []), "provider_used": ai_data.get("provider_used", "") if ai_data else "",
        "model_used": ai_data.get("model_used", "") if ai_data else "", "input_length_chars": len(content),
        "transcript_length_chars": len(transcript) if transcript else 0, "chunk_count": ai_data.get("chunks_processed", 0) if ai_data else 0,
        "process_time_sec": result["process_time_sec"], "output_note_path": str(out_filepath),
        "transcript_path": saved_transcript_path or None, "chunk_report_path": chunk_report_path,
        "index_rebuilt": False, "token_usage": ai_data.get("token_usage", {}) if ai_data else {},
        "estimated_cost_usd": None, "errors": result.get("error"),
    }
    log_file = ROOT / "logs" / "ingestion.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    try:
        with log_file.open("a", encoding="utf-8") as lf:
            lf.write(json.dumps(log_entry) + "\n")
    except OSError as exc:
        log(f"Warning: could not write to ingestion log: {exc}")

    # 13. Rebuild FTS index
    if rebuild_index_after:
        try:
            from src.core.build_fts_index import build_index  # type: ignore
            idx_res = build_index()
            log(f"Auto-rebuilt search index: {idx_res.get('indexed', '?')} files indexed.")
        except Exception as exc:
            log(f"Auto-rebuild of search index failed: {exc}")

    return result

def process_directory(dir_path: Path, use_ai: bool = False, status_callback=None) -> dict:
    """Recursively scan a directory for .txt and .md files and ingest them.

    To protect the original files, this function creates a temporary copy
    of each file, processes the copy, and deletes/cleans up, leaving the
    original files completely untouched.
    """
    import tempfile

    results = {"success": True, "processed": [], "failed": []}

    if not dir_path.exists() or not dir_path.is_dir():
        return {"success": False, "error": f"Path {dir_path} does not exist or is not a directory."}

    # Walk directory
    files_to_process = []
    for ext in ("*.txt", "*.md"):
        files_to_process.extend(list(dir_path.rglob(ext)))

    # Sort files to process them consistently
    files_to_process.sort()

    if not files_to_process:
        if status_callback:
            status_callback("No .txt or .md files found in the directory.")
        return results

    for i, file_path in enumerate(files_to_process):
        filename = file_path.name
        if status_callback:
            status_callback(f"Processing ({i + 1}/{len(files_to_process)}): {filename}")

        try:
            # Create a temporary file to hold the copy, so process_one_file doesn't move the original file
            with tempfile.TemporaryDirectory() as tmpdir:
                tmp_copy = Path(tmpdir) / filename
                shutil.copy2(file_path, tmp_copy)

                # Run process_one_file on the copy
                res = process_one_file(str(tmp_copy), use_ai=use_ai, status_callback=status_callback)

                if res.get("success"):
                    results["processed"].append({
                        "original_path": str(file_path),
                        "output_path": res.get("out_filepath"),
                    })
                else:
                    results["failed"].append({
                        "original_path": str(file_path),
                        "error": res.get("error"),
                    })
        except Exception as exc:
            results["failed"].append({
                "original_path": str(file_path),
                "error": str(exc),
            })
            if status_callback:
                status_callback(f"Error processing {filename}: {exc}")

    return results


def regenerate_insight_summary(insight_path: Path) -> dict:
    """Regenerate the AI summary for an existing insight note.

    Reads the raw content from the bottom of the note (or transcript file)
    and calls the LLM to generate a fresh summary, key ideas, and metadata.
    Updates the note's frontmatter and body, overwriting the old summary sections.

    Args:
        insight_path: Path to the insight note markdown file.

    Returns:
        Dict with keys ``success`` (bool), ``error`` (str on failure).
    """
    from src.core.frontmatter import read_fm, write_fm

    try:
        if not insight_path.exists():
            return {"success": False, "error": f"File {insight_path} does not exist."}

        fm, body = read_fm(insight_path)

        # 1. Identify raw/original content to send to LLM
        raw_content = ""
        transcript_path_str = fm.get("transcript_path")
        is_youtube = fm.get("source_type") == "youtube_video" or (fm.get("source_url") and "youtu" in fm.get("source_url"))

        if transcript_path_str:
            t_path = Path(transcript_path_str)
            if not t_path.is_absolute():
                t_path = ROOT / t_path
            if t_path.exists():
                try:
                    raw_content = t_path.read_text(encoding="utf-8")
                except Exception:
                    pass

        if not raw_content:
            # Fallback: extract from note body
            idx = body.find("## Original Content")
            if idx != -1:
                orig_section = body[idx:]
                sub_idx = orig_section.find("### Raw User Input")
                if sub_idx != -1:
                    start = sub_idx + len("### Raw User Input")
                    end_idx = orig_section.find("### Source URL", start)
                    if end_idx != -1:
                        raw_content = orig_section[start:end_idx].strip()
                    else:
                        raw_content = orig_section[start:].strip()
                else:
                    raw_content = orig_section[len("## Original Content"):].strip()
            else:
                raw_content = body.strip()

        if not raw_content:
            return {"success": False, "error": "Could not extract raw content or transcript to summarize."}

        # 2. Call LLM to generate summary
        title = fm.get("title", insight_path.stem)
        source_url = fm.get("source_url", "")
        domain = fm.get("domain", "")
        primary_mode = fm.get("primary_mode", "")
        secondary_modes = fm.get("secondary_modes", [])

        ai_data = generate_resource_summary(
            title=title,
            source_url=source_url,
            domain=domain,
            primary_mode=primary_mode,
            secondary_modes=secondary_modes,
            raw_content=raw_content,
        )

        if not ai_data:
            return {"success": False, "error": "LLM summarization failed."}

        # 3. Update frontmatter tags and metadata
        now_str = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()
        fm["updated_at"] = now_str

        # If LLM returned tags, merge them
        if "suggested_tags" in ai_data:
            existing_tags = fm.get("tags", [])
            new_tags = ai_data["suggested_tags"]
            merged_tags = list(existing_tags)
            for tag in new_tags:
                if tag.lower() not in [t.lower() for t in merged_tags]:
                    merged_tags.append(tag)
            fm["tags"] = merged_tags

        # 4. Rebuild the body
        warning_text = "Transcript unavailable. Summary is based only on title/metadata.\n\n" if (is_youtube and not transcript_path_str) else ""

        new_body = f"\n# {title}\n\n"

        if "summary" in ai_data:
            new_body += f"## Summary\n{warning_text}{ai_data.get('summary', '')}\n\n"
            new_body += "## Key Ideas\n"
            for idea in ai_data.get("key_ideas", []):
                new_body += f"- {idea}\n"
            new_body += "\n## Why this matters for Markus\n"
            for reason in ai_data.get("why_this_matters_for_markus", []):
                new_body += f"- {reason}\n"
            new_body += "\n## Related Modes\n"
            for mode in ai_data.get("related_modes", []):
                new_body += f"- {mode}\n"
            new_body += f"\n## Next Action\n- [ ] {ai_data.get('next_action', '')}\n"

            if ai_data.get("is_chunked"):
                new_body += (
                    f"\n## Long Resource Processing\n"
                    f"- chunks processed: {ai_data['chunks_processed']}\n"
                    "- method: chunked map-reduce summary\n"
                )

            provider = ai_data.get("provider_used", "Unknown")
            model = ai_data.get("model_used", "Unknown")
            new_body += f"\n## AI Generation Data\n- Provider: {provider}\n- Model: {model}\n"

            reliability = ai_data.get("source_reliability", "Based on resource content.")
            new_body += f"\n## Source Reliability\n{reliability}\n"
        elif "raw_output" in ai_data:
            provider = ai_data.get("provider_used", "Unknown")
            model = ai_data.get("model_used", "Unknown")
            new_body += (
                f"## Summary\n{warning_text}AI summarization succeeded, but JSON parsing failed.\n\n"
                f"## AI Raw Output\n```text\n{ai_data['raw_output']}\n```\n\n"
                "## Key Ideas\n- Refer to the AI Raw Output above.\n\n"
                "## Why this matters for Markus\n- Refer to the AI Raw Output above.\n\n"
                f"## Related Modes\n- {primary_mode}\n"
            )
            for m in secondary_modes:
                new_body += f"- {m}\n"
            new_body += f"\n## AI Generation Data\n- Provider: {provider}\n- Model: {model}\n"
            new_body += (
                "\n## Next Action\n"
                "- [ ] Review raw AI output and extract action items manually.\n\n"
                "## Source Reliability\nAI summarization was performed but parsing failed.\n"
            )

        if ai_data.get("is_chunked") and ai_data.get("chunk_summaries"):
            new_body += f"\n## Detailed Chunk Summaries\n\n{ai_data['chunk_summaries']}\n"

        # Find where ## Original Content started in the original body
        orig_idx = body.find("## Original Content")
        if orig_idx != -1:
            orig_content_block = body[orig_idx:]
            new_body += f"\n{orig_content_block.strip()}\n"
        else:
            # Reconstruct original content section
            transcript_display = ""
            if transcript_path_str and Path(transcript_path_str).exists():
                transcript_display = f"\n### Full Transcript File\n[full_transcript](file://{transcript_path_str})"
            new_body += f"\n## Original Content\n### Raw User Input\n{raw_content}\n\n### Source URL\n{source_url}{transcript_display}\n"

        # 5. Write the file back
        write_fm(insight_path, fm, new_body)

        # 6. Rebuild FTS index
        try:
            from src.core.build_fts_index import build_index  # type: ignore
            build_index()
        except Exception:
            pass

        return {"success": True}

    except Exception as exc:
        return {"success": False, "error": str(exc)}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild-index", action="store_true")
    args = parser.parse_args()
    if args.rebuild_index:
        from src.core.build_fts_index import build_index
        build_index()
