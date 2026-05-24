import os
import re

KEYWORDS = {
    'ai-platform': ['ai', 'agent', 'rag', 'openrouter', 'azure', 'gemini', 'llm', 'python', 'vector', 'embedding', 'mcp', 'deepseek', 'claude', 'model', 'openai'],
    'flow-temple': ['moxa', 'moxibustion', 'tcm', 'acupuncture', 'massage', 'sound healing', 'rednote', 'xiaohongshu'],
    'career': ['linkedin', 'cv', 'resume', 'job', 'portfolio', 'interview', 'business analyst'],
    'creator-wisdom': ['youtube creator', 'channel', 'transcript', 'creator profile'],
    'life-kompass': [
        'routine', 'reflection', 'decision', 'focus', 'weekly review',
        'thought', 'emotion', 'family', 'relationship', 'money feelings',
        'finance feelings', 'memory', 'memories', 'worry', 'feeling', 'anxiety', 'anxious'
    ],
    'body-practice': [
        'gym', 'cut', 'cutting', 'fat loss', 'weight loss', 'calories', 'protein',
        'workout', 'strength', 'calisthenics', 'overcoming gravity', 'crow pose', 'crane pose',
        'handstand', 'ashtanga', 'mobility', 'wrists', 'recovery', 'yoga skill', 'body practice',
        'training', 'planche', 'front lever', 'muscle-up', 'l-sit', 'deload', 'prehab',
        'nutrition', 'deficit', 'body weight', 'pull-up', 'push-up', 'squat', 'deadlift'
    ]
}

MODE_MAPPING = {
    'ai-platform': 'research-resource',
    'flow-temple': 'flow-temple-operator',
    'career': 'career-brand',
    'creator-wisdom': 'creator-wisdom',
    'life-kompass': 'life-kompass',
    'body-practice': 'body-practice',
    'unknown': 'router'
}

STORAGE_MAPPING = {
    'ai-platform': 'data/knowledge/ai-resources/',
    'flow-temple': 'data/business/flow-temple/',
    'career': 'data/career/',
    'creator-wisdom': 'data/knowledge/insights/',
    'life-kompass': 'data/private/reflections/',
    'body-practice': 'data/private/body/',
    'unknown': 'data/knowledge/insights/'
}

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
    
    domain_scores = {domain: 0 for domain in KEYWORDS}
    found_tags = set()
    
    for domain, words in KEYWORDS.items():
        for word in words:
            if word in text_lower:
                domain_scores[domain] += text_lower.count(word)
                found_tags.add(word)
                
    best_domain = max(domain_scores, key=domain_scores.get)
    if domain_scores[best_domain] == 0:
        best_domain = 'unknown'
        
    primary_mode = MODE_MAPPING.get(best_domain, 'router')
    storage_location = STORAGE_MAPPING.get(best_domain, 'data/inbox/processed/needs-review/')
    privacy = 'public'
    
    # Sub-folder routing for body-practice
    if best_domain == 'body-practice':
        privacy = 'private'
        if any(w in text_lower for w in ['skill', 'crow', 'crane', 'handstand', 'planche', 'front lever', 'muscle-up', 'l-sit', 'progression']):
            storage_location = 'data/private/body/skills/'
        elif any(w in text_lower for w in ['nutrition', 'calories', 'protein', 'deficit', 'cut', 'cutting', 'fat loss', 'weight loss']):
            storage_location = 'data/private/body/nutrition/'
        elif any(w in text_lower for w in ['recovery', 'deload', 'rest', 'prehab', 'injury', 'wrists', 'shoulder', 'sleep']):
            storage_location = 'data/private/body/recovery/'
        else:
            storage_location = 'data/private/body/training-log/'

    # Sub-folder routing for life-kompass
    elif best_domain == 'life-kompass':
        privacy = 'private'
        # Check sub-categories
        if any(w in text_lower for w in ['family', 'parent', 'mom', 'dad', 'brother', 'sister', 'sibling']):
            storage_location = 'data/private/family/'
        elif any(w in text_lower for w in ['relationship', 'partner', 'friend', 'dating', 'spouse', 'marriage']):
            storage_location = 'data/private/relationships/'
        elif any(w in text_lower for w in ['money feelings', 'finance feelings', 'money anxiety', 'wealth feelings']):
            storage_location = 'data/private/finance-feelings/'
        elif any(w in text_lower for w in ['money', 'finance', 'budget', 'spending', 'cost']) and any(w in text_lower for w in ['feel', 'worry', 'anxiety', 'anxious', 'stressed']):
            storage_location = 'data/private/finance-feelings/'
        elif any(w in text_lower for w in ['emotion', 'anxious', 'anxiety', 'feeling', 'mood', 'depressed', 'happy', 'sad', 'fear', 'anger']):
            storage_location = 'data/private/emotions/'
        elif any(w in text_lower for w in ['memory', 'memories', 'remember', 'childhood', 'past']):
            storage_location = 'data/private/memories/'
        else:
            storage_location = 'data/private/reflections/'
            
    # Secondary modes heuristic
    secondary_modes = []
    if best_domain == 'ai-platform':
        secondary_modes = ['ai-builder']
    elif best_domain == 'flow-temple':
        secondary_modes = ['moxsensei-operator', 'content-planner']
        
    # Output type heuristic based on domain & file source
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


