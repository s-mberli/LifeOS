import sys
from pathlib import Path
import re

# Resolve project root
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from core.frontmatter import read_fm, write_fm
from core.build_fts_index import build_index

def clean_title(title: str) -> str:
    # If the title ends with " / X" or " | X", strip it
    title = re.sub(r"\s*[/|]\s*X$", "", title, flags=re.IGNORECASE)
    # Remove any extra quotes
    title = title.strip().strip('"\'')
    return title

def slugify(title: str) -> str:
    # Lowercase, replace non-alphanumeric with -
    s = title.lower()
    s = re.sub(r"[^a-z0-9\-]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")

def cleanup_notes():
    directories = [
        ROOT / "data" / "inbox",
        ROOT / "data" / "knowledge",
        ROOT / "data" / "private"
    ]
    
    modified = False
    
    for directory in directories:
        if not directory.exists():
            continue
        for filepath in directory.rglob("*.md"):
            if "raw" in filepath.parts:
                continue
            
            try:
                fm, body = read_fm(filepath)
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
                continue
                
            if not fm or fm.get("type") != "insight_note":
                continue
                
            title = fm.get("title", "")
            needs_update = False
            new_title = ""
            
            # Check if title is generic
            title_lower = str(title).lower()
            if title_lower in ("status", "status_1", "status 1", "web page") or str(title).startswith("http"):
                # Try to extract the title from the body's Fetched Web Text
                # Look for Title: ...
                match = re.search(r"Title:\s*(.+)$", body, re.MULTILINE)
                if match:
                    new_title = clean_title(match.group(1).strip())
                    needs_update = True
                    print(f"Found title in body for {filepath.name}: '{new_title}'")
                else:
                    # Fallback to URL path extraction if present in source_url
                    url = fm.get("source_url", "")
                    if url:
                        from core.ingest import _extract_title_from_url
                        new_title = _extract_title_from_url(url)
                        if new_title and new_title.lower() not in ("status", "status_1", "status 1", "web page"):
                            new_title = clean_title(new_title)
                            needs_update = True
                            print(f"Extracted title from URL for {filepath.name}: '{new_title}'")
                            
            if needs_update and new_title:
                # Update frontmatter title
                fm["title"] = new_title
                
                # Update main header in body
                # The body usually starts with `# Status` or similar. Let's replace it
                lines = body.splitlines()
                for i, line in enumerate(lines[:10]):
                    if line.strip().startswith("# "):
                        lines[i] = f"# {new_title}"
                        break
                new_body = "\n".join(lines)
                
                # Write back
                write_fm(filepath, fm, new_body)
                print(f"Updated title of {filepath.name} to '{new_title}'")
                
                # Rename the file to match the new title
                new_slug = slugify(new_title)
                new_filename = f"{new_slug}.md"
                new_filepath = filepath.parent / new_filename
                
                # Avoid collision
                counter = 1
                while new_filepath.exists() and new_filepath != filepath:
                    new_filename = f"{new_slug}_{counter}.md"
                    new_filepath = filepath.parent / new_filename
                    counter += 1
                
                if new_filepath != filepath:
                    print(f"Renaming {filepath.name} -> {new_filename}")
                    filepath.rename(new_filepath)
                    
                modified = True
                
    if modified:
        print("Rebuilding FTS index...")
        build_index()
        print("FTS index rebuilt.")
    else:
        print("No notes needed title cleanup.")

if __name__ == "__main__":
    cleanup_notes()
