import sys
from pathlib import Path
import yaml

ROOT = Path("/Users/markus/markusos")
sys.path.insert(0, str(ROOT))

from src.core.ingest import _run_cheap_triage

DATA_DIR = ROOT / "data"

def load_valid_domains():
    config_path = ROOT / "config" / "domains.yaml"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            domains_data = yaml.safe_load(f)
            if isinstance(domains_data, dict) and "domains" in domains_data:
                return list(domains_data["domains"].keys())
    return ["ai-platform", "flow-temple", "career", "creator-wisdom", "life-kompass", "body-practice"]

def main():
    valid_domains = load_valid_domains()
    print(f"Valid domains: {valid_domains}")
    
    files = list(DATA_DIR.rglob("*.md"))
    updated_count = 0
    scanned_count = 0
    invalid_count = 0
    
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
        
        scanned_count += 1
        domain = fm.get("domain", "")
        
        # Check if the domain is invalid
        if domain not in valid_domains:
            invalid_count += 1
            print(f"\nCorrection needed for [{f.name}] - Current Domain: '{domain}'")
            
            title = fm.get("title", "")
            source_url = fm.get("source_url", "")
            # Check if source_url exists and contains youtube to set is_youtube
            is_youtube = fm.get("is_youtube", False)
            if not is_youtube and source_url and "youtu" in source_url:
                is_youtube = True
                
            transcript = None
            if is_youtube and "Transcript" in content:
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
                
                # Update domain if it's valid
                if new_domain in valid_domains:
                    fm["domain"] = new_domain
                    print(f"  -> Updated domain to: '{new_domain}'")
                else:
                    print(f"  -> LLM returned domain '{new_domain}' which is still invalid. Skipping domain update.")
                
                # Update tags if available
                if new_tags:
                    # Deduplicate tags
                    existing_tags = fm.get("tags", [])
                    combined = list(set(existing_tags + new_tags))
                    fm["tags"] = combined
                    print(f"  -> Combined tags: {combined}")
                
                # Update updated_at timestamp
                import datetime
                fm["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Write back
                new_fm_str = yaml.dump(fm, default_flow_style=False, allow_unicode=True)
                new_content = f"---\n{new_fm_str}---\n{parts[2]}"
                f.write_text(new_content, encoding="utf-8")
                updated_count += 1
            else:
                print(f"  -> Triage returned no data. Skipping.")
                
    print(f"\nScan complete. Scanned {scanned_count} insight notes.")
    print(f"Found {invalid_count} notes with invalid/hallucinated domains.")
    print(f"Successfully corrected and updated {updated_count} files.")

if __name__ == "__main__":
    main()
