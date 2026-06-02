import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.core.ingest import _run_cheap_triage
from src.core.frontmatter import read_fm, write_fm

DATA_DIR = ROOT / "data"

def main():
    files = list(DATA_DIR.rglob("*.md"))
    updated_count = 0
    
    for f in files:
        if "experts" in f.parts or "raw" in f.parts: continue
        
        try:
            fm, body = read_fm(f)
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
            if is_youtube and "Transcript" in body:
                transcript = body.split("Transcript")[-1][:1500]
                
            def simple_log(msg):
                print(f"  {msg}")
                
            triage_data = _run_cheap_triage(
                title=title,
                source_url=source_url,
                content=body,
                transcript=transcript,
                is_youtube=is_youtube,
                log=simple_log
            )
            
            if triage_data:
                new_domain = triage_data.get("domain")
                new_tags = triage_data.get("tags", [])
                
                if new_domain: fm["domain"] = new_domain
                if new_tags: fm["tags"] = new_tags
                
                write_fm(f, fm, body)
                updated_count += 1
                
    print(f"\nMetadata backfill complete. Updated {updated_count} files.")

if __name__ == "__main__":
    main()
