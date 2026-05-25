#!/usr/bin/env python3
"""
LifeOS - Agent Skills Installer

This script registers LifeOS agent skills with common AI assistants (like Claude, Cursor, Gemini)
by linking the `.gemini/config/skills/` directory to the appropriate global or user configs,
or by just validating that the local skills are present.
"""
import os
import sys
from pathlib import Path

def main():
    root_dir = Path(__file__).resolve().parent.parent
    skills_dir = root_dir / ".gemini" / "config" / "skills"
    
    if not skills_dir.exists():
        print(f"Error: Skills directory not found at {skills_dir}")
        sys.exit(1)
        
    print(f"Found LifeOS Agent Skills at: {skills_dir}")
    print("Skills available:")
    for skill in skills_dir.iterdir():
        if skill.is_dir() and (skill / "SKILL.md").exists():
            print(f" - {skill.name}")
            
    print("\nLifeOS skills are ready to be used by any agentic coding assistant in this workspace.")

if __name__ == "__main__":
    main()
