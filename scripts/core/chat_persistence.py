"""
scripts/core/chat_persistence.py — Persist chat interactions and export insights.

Saves daily chat logs to private directories and converts specific chat QA pairs
into searchable knowledge base notes, automatically attaching them to experts.
"""

from __future__ import annotations

import datetime
import re
from pathlib import Path

# Project root — two levels up from scripts/core/chat_persistence.py
ROOT = Path(__file__).resolve().parent.parent.parent


def append_to_daily_chat_log(
    user_prompt: str,
    assistant_response: str,
    expert_slug: str | None = None,
) -> bool:
    """Append a Q&A interaction to the daily chat log file.

    Saves to data/private/chat-logs/chat-YYYY-MM-DD.md.

    Args:
        user_prompt: The prompt sent by the user.
        assistant_response: The response returned by the assistant.
        expert_slug: The slug of the active expert context, if any.

    Returns:
        True on success, False otherwise.
    """
    try:
        now = datetime.datetime.now(datetime.timezone.utc).astimezone()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")

        log_dir = ROOT / "data" / "private" / "chat-logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"chat-{date_str}.md"

        from scripts.core.frontmatter import read_fm, write_fm

        if not log_file.exists():
            fm = {
                "type": "daily_chat_log",
                "date": date_str,
                "created_at": now.isoformat(),
            }
            body = f"\n# Chat Log for {date_str}\n"
            write_fm(log_file, fm, body)

        fm, body = read_fm(log_file)

        expert_info = f" (Expert: {expert_slug})" if expert_slug else ""
        new_entry = (
            f"\n## [{time_str}] User{expert_info}\n"
            f"{user_prompt}\n\n"
            f"### Assistant\n"
            f"{assistant_response}\n"
        )
        body += new_entry

        write_fm(log_file, fm, body)
        return True
    except Exception as exc:
        print(f"[chat_persistence] Error appending to daily chat log: {exc}")
        return False


def save_message_as_insight(
    user_prompt: str,
    assistant_response: str,
    expert_slug: str | None = None,
    expert_name: str | None = None,
) -> tuple[bool, str]:
    """Format and save a single Q&A pair as a permanent knowledge base note.

    If an expert_slug is provided, the insight is automatically attached
    to that expert using assign_insight_to_expert.

    Args:
        user_prompt: The user's question.
        assistant_response: The assistant's response.
        expert_slug: The slug of the expert to assign to, if any.
        expert_name: The display name of the expert, if any.

    Returns:
        A tuple of (success, filepath_string).
    """
    try:
        from scripts.core.frontmatter import write_fm
        from scripts.core.experts import assign_insight_to_expert

        # Derive a title from the user prompt
        first_line = user_prompt.split("\n")[0].strip()
        clean_title = re.sub(r"[#*`_]", "", first_line)
        if len(clean_title) > 60:
            title = clean_title[:57] + "..."
        else:
            title = clean_title if clean_title else "Saved Chat Insight"

        date_str = datetime.date.today().isoformat()
        safe_title = re.sub(r"[^a-zA-Z0-9-]", "-", title.lower())
        safe_title = re.sub(r"-+", "-", safe_title).strip("-")
        filename = f"chat-insight-{date_str}-{safe_title[:30]}.md"

        insights_dir = ROOT / "data" / "knowledge" / "chat-insights"
        insights_dir.mkdir(parents=True, exist_ok=True)

        out_filepath = insights_dir / filename
        counter = 1
        stem, ext = out_filepath.stem, out_filepath.suffix
        while out_filepath.exists():
            out_filepath = insights_dir / f"{stem}_{counter}{ext}"
            counter += 1

        now_str = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()

        fm = {
            "title": title,
            "source_url": "",
            "type": "insight_note",
            "domain": "general",
            "tags": ["chat", "saved-insight"],
            "created_at": now_str,
            "updated_at": now_str,
            "privacy": "public",
            "status": "processed",
            "expert_status": "unattached",
            "suggested_experts": [],
            "attached_experts": [],
            "review_status": "new",
        }

        body = (
            f"\n# {title}\n\n"
            f"## Question\n{user_prompt}\n\n"
            f"## Answer\n{assistant_response}\n"
        )

        write_fm(out_filepath, fm, body)

        if expert_slug:
            assign_insight_to_expert(
                insight_path=out_filepath,
                expert_slug=expert_slug,
                expert_name=expert_name,
                reason="Saved from Chat session",
            )

        # Rebuild the FTS search index so it is immediately searchable
        from build_fts_index import build_index
        build_index()

        return True, str(out_filepath)
    except Exception as exc:
        print(f"[chat_persistence] Error saving chat insight: {exc}")
        return False, ""
