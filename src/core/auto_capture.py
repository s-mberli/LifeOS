import os
import datetime

def determine_triage_category(text: str, decision: dict) -> str:
    text_lower = text.lower()
    domain = decision.get("primary_domain", "") if decision else ""
    
    if any(kw in text_lower for kw in ["decide", "decision", "chose", "opted"]):
        return "decision"
    elif any(kw in text_lower for kw in ["learned", "realized", "insight", "til"]):
        return "learning_update"
    elif any(kw in text_lower for kw in ["project idea", "build a", "create a", "startup idea"]):
        return "project_idea"
    elif any(kw in text_lower for kw in ["pattern", "always happens", "noticed that"]):
        return "pattern_candidate"
    elif any(kw in text_lower for kw in ["context", "currently", "focusing on now", "right now i am"]):
        return "current_context_update"
    elif any(kw in text_lower for kw in ["profile", "who am i", "my identity", "core value"]):
        return "profile_update_candidate"
    elif any(kw in text_lower for kw in ["reflect", "feel", "think about", "wonder", "why do i"]):
        return "reflection"
    elif any(kw in text_lower for kw in ["http://", "https://", "read this", "video", "article"]):
        return "resource"
    
    # Fallback to domain mapping
    if domain == "body-practice":
        return "body_practice"
    elif domain == "flow-temple":
        return "flow_temple"
    elif domain == "career":
        return "career"
    elif domain == "ai-platform":
        return "ai_platform"
    elif domain == "creator-wisdom":
        return "resource"
        
    return "casual"

def capture_input(text: str, decision: dict = None) -> str:
    """
    Saves user input into a private raw-capture directory if it passes the noise filter.
    Returns the file path if captured, or None if ignored.
    """
    text = text.strip()
    if not text:
        return None
        
    text_lower = text.lower()
    
    # Noise filter: < 30 chars must contain specific keywords
    if len(text) < 30:
        keywords = ["remember", "decision", "important", "learned", "focus"]
        if not any(kw in text_lower for kw in keywords):
            return None
            
    # Triage
    triage_cat = determine_triage_category(text, decision)
    
    # Prepare Frontmatter Metadata
    now = datetime.datetime.now(datetime.timezone.utc).astimezone()
    date_str = now.strftime("%Y-%m-%d")
    timestamp_str = now.isoformat()
    safe_time = now.strftime("%H%M%S")
    
    primary_domain = decision.get("primary_domain", "unknown") if decision else "unknown"
    primary_mode = decision.get("primary_mode", "unknown") if decision else "unknown"
    
    # Construct YAML frontmatter safely
    lines = [
        "---",
        f'created_at: "{timestamp_str}"',
        'source: "streamlit_ask"',
        'input_type: "text"',
        f'triage_category: "{triage_cat}"',
        f'primary_domain: "{primary_domain}"',
        f'primary_mode: "{primary_mode}"',
        'promoted: false',
        'privacy: "private"',
        "---",
        "",
        text,
        ""
    ]
    content = "\n".join(lines)
    
    # Write to file
    from pathlib import Path
    ROOT = Path(__file__).resolve().parent.parent.parent
    capture_dir = ROOT / "data" / "private" / "raw-capture" / date_str
    capture_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = capture_dir / f"capture-{safe_time}.md"
    
    file_path.write_text(content, encoding="utf-8")
        
    return file_path
