import os
import re
import yaml
from pathlib import Path

def load_domains_config():
    config_path = Path(__file__).resolve().parent.parent / 'config' / 'domains.yaml'
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f).get('domains', {})
    return {}

DOMAINS_CONFIG = load_domains_config()

def evaluate_retrieval(text: str) -> dict:
    text_clean = text.lower().strip('.!? ')
    words = text_clean.split()
    
    vague_exact_matches = [
        "this is important", "this is an important decision", "remember this",
        "i feel weird", "big decision", "hmm", "ok", "test", "testing"
    ]
    
    if text_clean in vague_exact_matches:
        return {
            "should_search": False,
            "reason": "Vague or conversational input",
            "query_used": text
        }
        
    question_markers = ["what", "how", "why", "who", "where", "when", "summarize", "find", "search", "show", "can you", "do i"]
    is_question = any(text_clean.startswith(q) or f" {q} " in f" {text_clean} " for q in question_markers)
    
    strong_entities = ['deepseek', 'moxa', 'rag', 'agent', 'project', 'resume', 'portfolio', 'openai', 'claude', 'gemini']
    has_strong_entity = any(ent in text_clean for ent in strong_entities)
    
    if is_question or has_strong_entity or len(words) >= 8:
        return {
            "should_search": True,
            "reason": "Input contains enough context, an explicit question, or a named entity",
            "query_used": text
        }
    else:
        return {
            "should_search": False,
            "reason": "Short statement lacking clear question or named entity",
            "query_used": text
        }

def classify(text: str, filepath: str = None):
    text_lower = text.lower()
    
    domain_scores = {domain: 0 for domain in DOMAINS_CONFIG}
    found_tags = set()
    
    for domain, data in DOMAINS_CONFIG.items():
        for word in data.get('keywords', []):
            if word in text_lower:
                domain_scores[domain] += text_lower.count(word)
                found_tags.add(word)
                
    best_domain = max(domain_scores, key=domain_scores.get) if domain_scores else 'unknown'
    if not domain_scores or domain_scores[best_domain] == 0:
        best_domain = 'unknown'
        
    domain_data = DOMAINS_CONFIG.get(best_domain, {})
    
    primary_mode = domain_data.get('primary_mode', 'router')
    storage_location = domain_data.get('storage_location', 'data/inbox/processed/needs-review/')
    privacy = domain_data.get('privacy', 'public')
    secondary_modes = domain_data.get('secondary_modes', [])
    
    # Sub-folder routing based on YAML config
    if 'sub_categories' in domain_data:
        for sub_cat, sub_data in domain_data['sub_categories'].items():
            if any(w in text_lower for w in sub_data.get('keywords', [])):
                storage_location = sub_data.get('path', storage_location)
                break
                
    output_type = 'insight_note'

    # Check filepath for import/voice overrides
    if filepath:
        normalized_path = filepath.replace('\\', '/')
        if 'inbox/voice' in normalized_path:
            output_type = 'voice_note'
            best_domain = 'life-kompass'
            primary_mode = 'life-kompass'
            storage_location = 'data/private/reflections/'
            privacy = 'private'
        elif 'inbox/imports' in normalized_path:
            output_type = 'imported_chat_note'
            best_domain = 'life-kompass'
            primary_mode = 'life-kompass'
            storage_location = 'data/private/reflections/'
            privacy = 'private'
        elif 'data/private/' in normalized_path:
            privacy = 'private'
            best_domain = 'life-kompass'
            primary_mode = 'life-kompass'
            
    next_action = "Review this resource and extract practical action steps."
    if best_domain == 'life-kompass':
        next_action = "Process this personal reflection / thought for daily alignment."
    elif best_domain == 'body-practice':
        next_action = "Log this in the correct body-practice folder and define one next physical action."
        
    return {
        "primary_domain": best_domain,
        "primary_mode": primary_mode,
        "secondary_modes": secondary_modes,
        "storage_location": storage_location,
        "output_type": output_type,
        "save_needed": True,
        "one_next_action": next_action,
        "suggested_tags": list(found_tags),
        "privacy": privacy,
        "retrieval_decision": evaluate_retrieval(text)
    }
