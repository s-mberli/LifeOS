from __future__ import annotations

import datetime
import json
import re
import shutil
import sys
import time
from pathlib import Path

import yaml

# Project root — three levels up from scripts/core/ingest.py
ROOT = Path(__file__).resolve().parent.parent.parent

# Ensure scripts/ is on the path so legacy modules can be imported
_SCRIPTS_DIR = ROOT / "scripts"
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

    if not suggested_title:
        suggested_title = _extract_markdown_title(content)
    if not suggested_title:
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
        from classify_input import classify  # type: ignore
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

def _run_ai_summarisation(title: str, source_url: str, channel: str, transcript: str | None, is_youtube: bool, content: str, fetched_web_text: str, decision: dict, log) -> dict | None:
    log("Running AI summarisation…")
    llm_content = transcript if (is_youtube and transcript) else (
        f"Title: {title}\nChannel: {channel}\nURL: {source_url}" if is_youtube 
        else f"Content:\n{content}\n\nFetched Web Page Text:\n{fetched_web_text}"
    )
    try:
        from llm_client import generate_resource_summary  # type: ignore
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

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def process_one_file(source: str, use_ai: bool = False, status_callback=None) -> dict:
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

    # 4. Deduplicate tags
    tags = _deduplicate_tags(suggested_tags_str)
    result["tags"] = tags

    # 5. Determine output path
    out_filepath = _get_unique_filepath(ROOT / decision["storage_location"], filename)
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
    try:
        from build_fts_index import build_index  # type: ignore
        idx_res = build_index()
        log(f"Auto-rebuilt search index: {idx_res.get('indexed', '?')} files indexed.")
    except Exception as exc:
        log(f"Auto-rebuild of search index failed: {exc}")

    return result

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild-index", action="store_true")
    args = parser.parse_args()
    if args.rebuild_index:
        from build_fts_index import build_index
        build_index()
