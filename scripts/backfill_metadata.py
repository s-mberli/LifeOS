import sys
from pathlib import Path
import yaml

ROOT = Path("/Users/markus/markusos")
sys.path.insert(0, str(ROOT))

from src.core.ingest import _run_cheap_triage

DATA_DIR = ROOT / "data"

def main():
    files = list(DATA_DIR.rglob("*.md"))
    updated_count = 0
    
    for f in files:
        if "experts" in f.parts or "raw" in f.parts: continue
        
        try:
            content = f.read_text(encoding="utf-8")
        except Exception:
            continue
            
        if not content.startswith("---"): continue
        parts = content.split("---", 2)
        if len(parts) < 3: continue
        
        try:
            fm = yaml.safe_load(parts[1])
        except Exception:
            continue
            
        if not fm or fm.get("type") != "insight_note": continue
        
        tags = fm.get("tags", [])
        domain = fm.get("domain", "")
        
        if not tags or domain in ["", "unknown", "general"]:
            print(f"\nProcessing missing metadata for: {f.name}")
            title = fm.get("title", "")
            source_url = fm.get("source_url", "")
            is_youtube = fm.get("is_youtube", False)
            transcript = None
            if is_youtube and "Transcript" in content:
                # Naive extraction for cheap triage
                transcript = content.split("Transcript")[-1][:1500]
                
            def simple_log(msg):
                print(f"  {msg}")
                
            triage_data = _run_cheap_triage(
                title=title,
                source_url=source_url,
                content=parts[2],
                transcript=transcript,
                is_youtube=is_youtube,
                log=simple_log
            )
            
            if triage_data:
                new_domain = triage_data.get("domain")
                new_tags = triage_data.get("tags", [])
                
                if new_domain: fm["domain"] = new_domain
                if new_tags: fm["tags"] = new_tags
                
                # Write back
                new_fm_str = yaml.dump(fm, default_flow_style=False, allow_unicode=True)
                new_content = f"---\n{new_fm_str}---\n{parts[2]}"
                f.write_text(new_content, encoding="utf-8")
                updated_count += 1
                
    print(f"\nMetadata backfill complete. Updated {updated_count} files.")

if __name__ == "__main__":
    main()
