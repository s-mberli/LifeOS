import os
import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = BASE_DIR / "templates" / "daily-focus.md"
DAILY_DIR = BASE_DIR / "data" / "private" / "daily"

def create_daily_note():
    # Get current date and local timezone-aware ISO timestamp
    local_now = datetime.datetime.now(datetime.timezone.utc).astimezone()
    date_str = local_now.strftime("%Y-%m-%d")
    timestamp_str = local_now.isoformat()
    
    output_filename = f"{date_str}-daily-focus.md"
    output_path = DAILY_DIR / output_filename
    
    if output_path.exists():
        print(f"Daily note already exists for today: {output_path}")
        return
        
    if not TEMPLATE_PATH.exists():
        print(f"Error: Template not found at {TEMPLATE_PATH}")
        return
        
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template_content = f.read()
        
    # Replace placeholders
    note_content = template_content.replace("{date}", date_str).replace("{created_at}", timestamp_str)
    
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(note_content)
        
    print(f"[+] Daily focus note created successfully!")
    print(f"Path: {output_path}")

if __name__ == "__main__":
    create_daily_note()
