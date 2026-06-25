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

from src.integrations.ticnote.client import TicNoteClient
from src.core.frontmatter import write_fm
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


def process_file_tree(client: TicNoteClient, project_name: str, file_tree: list, base_dir: Path):
    """Recursively process the file tree and download raw transcripts/summaries."""
    for node in file_tree:
        node_type = node.get("type")
        name = node.get("name", "unnamed")
        
        if node_type == "directory":
            children = node.get("children", [])
            if children:
                process_file_tree(client, project_name, children, base_dir)
        else:
            record_id = node.get("id")
            if not record_id:
                continue
                
            sanitized_proj = sanitize_filename(project_name)
            sanitized_name = sanitize_filename(Path(name).stem)
            
            raw_dir = base_dir / sanitized_proj / "raw"
            insights_dir = base_dir / sanitized_proj
            
            raw_path = raw_dir / f"{record_id}_raw.md"
            insights_path = insights_dir / f"{record_id}_insights.md"
            
            # Skip if raw file already exists to avoid redundant downloads
            if raw_path.exists():
                print(f"  ⏭️ Skipping {name} (already synced)")
                continue
                
            print(f"  📥 Syncing: {name} (ID: {record_id})")
            
            try:
                detail = client.get_file_detail(record_id)
                status = detail.get("status")
                
                # Check status (3 is failed; only sync completed / success states)
                if status == 3:
                    print(f"    ❌ Recording transcription failed in TicNote. Skipping.")
                    continue
                elif status not in [2, 4, 5]:  # COMPLETED, TRANSSUC, SUMMARYSUC
                    print(f"    ⏳ Recording still processing in TicNote (status={status}). Skipping for now.")
                    continue
                    
                transcribe_raw = detail.get("transcribeJson")
                if not transcribe_raw:
                    print(f"    ⚠️ No transcript content found. Skipping.")
                    continue
                    
                # Format raw transcript
                transcript_content = format_transcribe_json(transcribe_raw)
                
                # Save raw transcript (with raw in the path, FTS5 skips this to avoid cluttering search)
                raw_dir.mkdir(parents=True, exist_ok=True)
                raw_fm = {
                    "title": f"Raw: {name}",
                    "recordId": record_id,
                    "fileId": detail.get("fileId"),
                    "fileName": name,
                    "duration": detail.get("duration"),
                    "language": detail.get("language"),
                    "updateTime": detail.get("updateTime"),
                    "syncedAt": datetime.now().isoformat(),
                    "project": project_name
                }
                write_fm(raw_path, raw_fm, f"\n\n{transcript_content}")
                try:
                    print(f"    💾 Saved raw transcript to: {raw_path.relative_to(ROOT)}")
                except ValueError:
                    print(f"    💾 Saved raw transcript to: {raw_path}")
                
                # Extract/generate summary
                summary_raw = detail.get("summaryJson")
                if summary_raw:
                    print("    ✨ Found pre-generated summary in TicNote. Using it to save tokens.")
                    insights_content = format_summary_json(summary_raw)
                else:
                    print("    🤖 No pre-generated summary found. Generating insights using LLM...")
                    insights_content = generate_local_summary(transcript_content)
                    
                # Save insights (will be indexed by FTS5 since it's not under /raw/)
                insights_dir.mkdir(parents=True, exist_ok=True)
                insights_fm = {
                    "title": f"Insights: {name}",
                    "recordId": record_id,
                    "fileId": detail.get("fileId"),
                    "fileName": name,
                    "project": project_name,
                    "syncedAt": datetime.now().isoformat(),
                }
                write_fm(insights_path, insights_fm, f"\n\n{insights_content}")
                try:
                    print(f"    💾 Saved insights to: {insights_path.relative_to(ROOT)}")
                except ValueError:
                    print(f"    💾 Saved insights to: {insights_path}")
                
            except Exception as e:
                print(f"    ❌ Error processing {name}: {e}")


def main():
    api_key = os.getenv("TICNOTE_API_KEY")
    if not api_key:
        print("❌ Error: TICNOTE_API_KEY environment variable is not set.")
        print("\n=== How to obtain your TicNote API Key ===")
        print("1. Log in to TicNote:")
        print("   - Domestic: https://www.ticnote.cn")
        print("   - Overseas: https://www.ticnote.com")
        print("2. Navigate to Settings -> API Keys (or Developer Settings).")
        print("3. Click 'Create API Key' (or 'New Secret Key').")
        print("4. Copy the API Key (starts with tncn_sk_ or tnovs_sk_).")
        print("5. Add it to your .env file:")
        print("   TICNOTE_API_KEY=\"your_key_here\"")
        sys.exit(1)
        
    print("🚀 Starting TicNote Sync...")
    client = TicNoteClient(api_key)
    try:
        client.login()
    except Exception as e:
        print(f"❌ Login failed: {e}")
        sys.exit(1)
        
    base_dir = ROOT / "data" / "knowledge" / "ticnote"
    base_dir.mkdir(parents=True, exist_ok=True)
    
    print("📁 Fetching projects...")
    try:
        projects = client.list_projects()
    except Exception as e:
        print(f"❌ Failed to fetch projects: {e}")
        sys.exit(1)
        
    print(f"ℹ️ Found {len(projects)} projects.")
    
    for proj in projects:
        proj_name = proj.get("name") or proj.get("project_name") or "default"
        proj_id = proj.get("project_id") or proj.get("id")
        if not proj_id:
            continue
            
        print(f"\n📂 Project: {proj_name} (ID: {proj_id})")
        try:
            file_tree = client.list_files(proj_id)
            process_file_tree(client, proj_name, file_tree, base_dir)
        except Exception as e:
            print(f"  ❌ Failed to sync files for project {proj_name}: {e}")
            
    print("\n🔍 Rebuilding FTS search index...")
    try:
        build_index()
        print("✅ FTS search index rebuilt successfully.")
    except Exception as e:
        print(f"❌ Failed to rebuild FTS search index: {e}")
        
    print("\n🎉 Sync complete!")


if __name__ == "__main__":
    main()
