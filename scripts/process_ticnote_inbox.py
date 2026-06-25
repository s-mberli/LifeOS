#!/usr/bin/env python3
import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

# Setup pathing to import from src
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
except ImportError:
    pass

from src.core.frontmatter import read_fm, write_fm
from src.core.llm_client import call_llm
from src.core.build_fts_index import build_index


def sanitize_filename(name: str) -> str:
    """Sanitize the filename by removing invalid characters and replacing spaces with underscores."""
    s = re.sub(r'[^\w\s-]', '', name).strip()
    return re.sub(r'[-\s]+', '_', s)


def format_transcribe_json(raw_json: str) -> str:
    """Format transcribeJson (which could be a JSON string or plain text) into clean readable Markdown."""
    if not raw_json:
        return ""
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError:
        return raw_json

    # If it's a list of segments
    if isinstance(data, list):
        lines = []
        for item in data:
            if isinstance(item, dict):
                speaker = item.get("speaker") or item.get("speakerName") or item.get("speaker_name")
                text = item.get("text") or item.get("content")
                if speaker and text:
                    lines.append(f"**{speaker}**: {text}")
                elif text:
                    lines.append(text)
            elif isinstance(item, str):
                lines.append(item)
        if lines:
            return "\n\n".join(lines)

    # If it's a dict
    if isinstance(data, dict):
        # Check for standard paragraph lists
        for key in ["paragraphs", "segments", "results", "sentences"]:
            if key in data and isinstance(data[key], list):
                lines = []
                for item in data[key]:
                    if isinstance(item, dict):
                        speaker = item.get("speaker") or item.get("speakerName") or item.get("speaker_name")
                        text = item.get("text") or item.get("content")
                        if speaker and text:
                            lines.append(f"**{speaker}**: {text}")
                        elif text:
                            lines.append(text)
                if lines:
                    return "\n\n".join(lines)

        # Check for raw content/text keys
        if "text" in data and isinstance(data["text"], str):
            return data["text"]
        if "content" in data and isinstance(data["content"], str):
            return data["content"]

    # Fallback to pretty-printed JSON if format is unexpected
    try:
        return json.dumps(data, indent=2, ensure_ascii=False)
    except Exception:
        return raw_json


def format_summary_json(raw_json: str) -> str:
    """Format summaryJson (which could be a JSON string or plain text) into clean Markdown insights."""
    if not raw_json:
        return ""
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError:
        return raw_json

    if isinstance(data, dict):
        markdown_parts = []
        
        title = data.get("title") or data.get("summaryTitle")
        if title:
            markdown_parts.append(f"# {title}\n")
            
        summary_text = data.get("summary") or data.get("abstract") or data.get("content")
        if summary_text and isinstance(summary_text, str):
            markdown_parts.append(f"## Summary\n{summary_text}\n")
            
        # Extract key points
        for list_key in ["keyPoints", "key_points", "highlights", "insights"]:
            points = data.get(list_key)
            if points and isinstance(points, list):
                markdown_parts.append("## Key Insights")
                for p in points:
                    markdown_parts.append(f"- {p}")
                markdown_parts.append("")
                
        # Extract action items
        for list_key in ["actionItems", "action_items", "tasks", "todo"]:
            tasks = data.get(list_key)
            if tasks and isinstance(tasks, list):
                markdown_parts.append("## Action Items")
                for t in tasks:
                    if isinstance(t, dict):
                        desc = t.get("description") or t.get("task") or t.get("content")
                        assignee = t.get("assignee") or t.get("owner")
                        if desc:
                            assignee_str = f" (Assignee: {assignee})" if assignee else ""
                            markdown_parts.append(f"- [ ] {desc}{assignee_str}")
                    else:
                        markdown_parts.append(f"- [ ] {t}")
                markdown_parts.append("")
                
        if markdown_parts:
            return "\n".join(markdown_parts)

    try:
        return json.dumps(data, indent=2, ensure_ascii=False)
    except Exception:
        return raw_json


def generate_local_summary(transcript_text: str) -> str:
    """Generate a summary using the configured LLM when TicNote lacks a pre-generated one."""
    system_prompt = (
        "You are an expert executive assistant. Summarize the following meeting transcript. "
        "Extract the main topics discussed, key insights, critical decisions made, and a list of action items with assignees if mentioned. "
        "Use clean, professional Markdown."
    )
    prompt = f"Transcript:\n\n{transcript_text}"
    summary = call_llm(
        prompt=prompt,
        system_prompt=system_prompt,
        max_tokens=2048,
        temperature=0.3
    )
    return summary or "Failed to generate summary."


def process_inbox(inbox_dir: Path, base_dir: Path):
    """Scan inbox recursively, process transcripts, generate insights, and move raw files to knowledge vault."""
    if not inbox_dir.exists():
        print(f"📁 Inbox directory {inbox_dir} does not exist. Creating it.")
        inbox_dir.mkdir(parents=True, exist_ok=True)
        return

    # Find all .md, .txt, and .json files
    supported_extensions = {".md", ".txt", ".json"}
    files_to_process = []
    for filepath in inbox_dir.rglob("*"):
        if filepath.is_file() and filepath.suffix.lower() in supported_extensions:
            # Skip files in any "raw" directory (shouldn't be there, but just in case)
            if "/raw/" in str(filepath.as_posix()):
                continue
            files_to_process.append(filepath)

    if not files_to_process:
        print("📭 Inbox is empty. No files to process.")
        return

    print(f"📥 Found {len(files_to_process)} files to process in inbox.")

    for filepath in files_to_process:
        print(f"\n📄 Processing: {filepath.name}")
        try:
            # Determine project name based on relative path parts
            rel_path = filepath.relative_to(inbox_dir)
            if len(rel_path.parts) > 1:
                project_name = rel_path.parts[0]
            else:
                project_name = "Inbox"

            sanitized_proj = sanitize_filename(project_name)
            sanitized_name = sanitize_filename(filepath.stem)

            raw_dir = base_dir / sanitized_proj / "raw"
            insights_dir = base_dir / sanitized_proj

            raw_path = raw_dir / f"{sanitized_name}.md"
            insights_path = insights_dir / f"{sanitized_name}_insights.md"

            # Check if destination raw file already exists to avoid collisions
            if raw_path.exists():
                # Append a timestamp to avoid overwriting existing files
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                raw_path = raw_dir / f"{sanitized_name}_{timestamp}.md"
                insights_path = insights_dir / f"{sanitized_name}_{timestamp}_insights.md"

            raw_dir.mkdir(parents=True, exist_ok=True)
            insights_dir.mkdir(parents=True, exist_ok=True)

            # Read content
            raw_text = filepath.read_text(encoding="utf-8").strip()
            
            # Initialize empty fields
            transcript_content = ""
            insights_content = ""
            metadata = {}

            # Handle JSON files
            if filepath.suffix.lower() == ".json":
                try:
                    data = json.loads(raw_text)
                    if isinstance(data, dict):
                        # Extract transcript/summary keys if they exist in TicNote API export structure
                        if "transcribeJson" in data:
                            transcript_content = format_transcribe_json(data["transcribeJson"])
                        elif "paragraphs" in data or "segments" in data:
                            transcript_content = format_transcribe_json(raw_text)
                        else:
                            transcript_content = json.dumps(data, indent=2, ensure_ascii=False)

                        if "summaryJson" in data:
                            insights_content = format_summary_json(data["summaryJson"])
                    else:
                        transcript_content = raw_text
                except Exception as e:
                    print(f"  ⚠️ Failed to parse JSON, treating as plain text: {e}")
                    transcript_content = raw_text
            else:
                # Handle Markdown/Text files
                # Parse frontmatter if it exists
                fm, body = read_fm(filepath)
                metadata.update(fm)
                transcript_content = body.strip()

            # Ensure we have transcript content
            if not transcript_content:
                print(f"  ⚠️ File is empty. Skipping.")
                continue

            # Generate insights if not extracted from JSON
            if not insights_content:
                print("  🤖 Generating insights using LLM...")
                insights_content = generate_local_summary(transcript_content)

            # Build frontmatter
            title = metadata.get("title") or filepath.stem.replace("_", " ").title()
            
            raw_fm = {
                "title": f"Raw: {title}",
                "project": project_name,
                "importedAt": datetime.now().isoformat(),
                "originalFilename": filepath.name,
                **{k: v for k, v in metadata.items() if k not in ["title", "project", "importedAt", "originalFilename"]}
            }

            insights_fm = {
                "title": f"Insights: {title}",
                "project": project_name,
                "importedAt": datetime.now().isoformat(),
                "originalFilename": filepath.name,
            }

            # Write raw transcript (with frontmatter)
            write_fm(raw_path, raw_fm, f"\n\n{transcript_content}")
            try:
                print(f"  💾 Saved raw transcript to: {raw_path.relative_to(ROOT)}")
            except ValueError:
                print(f"  💾 Saved raw transcript to: {raw_path}")

            # Write insights
            write_fm(insights_path, insights_fm, f"\n\n{insights_content}")
            try:
                print(f"  💾 Saved insights to: {insights_path.relative_to(ROOT)}")
            except ValueError:
                print(f"  💾 Saved insights to: {insights_path}")

            # Remove the processed file from inbox
            filepath.unlink()
            print(f"  🗑️ Removed original file from inbox.")

        except Exception as e:
            print(f"  ❌ Error processing file {filepath.name}: {e}")


def main():
    inbox_dir = ROOT / "data" / "inbox" / "ticnote"
    base_dir = ROOT / "data" / "knowledge" / "ticnote"

    print("🚀 Starting TicNote Inbox Processing...")
    process_inbox(inbox_dir, base_dir)

    print("\n🔍 Rebuilding FTS search index...")
    try:
        build_index()
        print("✅ FTS search index rebuilt successfully.")
    except Exception as e:
        print(f"❌ Failed to rebuild FTS search index: {e}")

    print("\n🎉 Inbox processing complete!")


if __name__ == "__main__":
    main()
