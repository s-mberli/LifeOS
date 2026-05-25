"""
scripts/llm_client.py — Multi-provider LLM call wrapper for LifeOS using litellm.

Tries providers in the order specified by the ``LLM_PROVIDER_ORDER``
environment variable (default: ``azure,gemini,openrouter``).
"""
import os
import json
import litellm
from litellm import completion, ModelResponse
from pathlib import Path
import yaml

# Disable litellm telemetry and excessive logging
litellm.telemetry = False
litellm.suppress_debug_info = True

def mask_key(key):
    return "yes" if key else "no"

def sanitize_err(e):
    err_str = str(e)
    keys_to_mask = [
        os.environ.get("AZURE_OPENAI_API_KEY"),
        os.environ.get("GEMINI_API_KEY"),
        os.environ.get("OPENROUTER_API_KEY"),
    ]
    for key in keys_to_mask:
        if key and len(key) > 5:
            err_str = err_str.replace(key, "[MASKED]")
    return err_str

def split_text(text, chunk_size=12000, overlap=1000):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def get_model_string(provider: str) -> str:
    """Map our short provider names to litellm model strings."""
    if provider == "azure":
        # litellm expects azure/<deployment_name>
        dep = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
        return f"azure/{dep}"
    elif provider == "gemini":
        mod = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
        return f"gemini/{mod}"
    elif provider == "openrouter":
        mod = os.environ.get("OPENROUTER_MODEL", "openai/gpt-4o-mini")
        return f"openrouter/{mod}"
    return provider

def try_providers(system_prompt: str, user_prompt: str, max_tokens: int, temperature: float = 0.2):
    """
    Attempts to call LLM providers in fallback order.
    Returns: tuple (content, provider_name, model_name, usage_dict) or None
    """
    order_str = os.environ.get("LLM_PROVIDER_ORDER", "azure,gemini,openrouter")
    providers = [p.strip().lower() for p in order_str.split(",")]
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    # Build fallback model list for litellm router
    model_list = [get_model_string(p) for p in providers]
    
    for provider, model_str in zip(providers, model_list):
        print(f"  [{provider.capitalize()}] Attempting model: {model_str} | Max Tokens: {max_tokens}")
        try:
            response = completion(
                model=model_str,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                drop_params=True # Drops unsupported params per provider
            )
            
            content = response.choices[0].message.content.strip()
            usage = response.usage
            
            token_usage = {
                "prompt_tokens": getattr(usage, "prompt_tokens", 0),
                "completion_tokens": getattr(usage, "completion_tokens", 0),
                "total_tokens": getattr(usage, "total_tokens", 0),
            }
            
            return content, provider, model_str, token_usage
            
        except Exception as e:
            print(f"    [!] {provider.capitalize()} call failed: {sanitize_err(e)}")
            continue
            
    return None

def call_llm(
    prompt: str = '',
    system_prompt: str = 'You are a helpful assistant.',
    messages: list | None = None,
    max_tokens: int = 1500,
    temperature: float = 0.2,
    model_type: str = 'smart',
    json_mode: bool = False,
) -> str | None:
    if messages is not None:
        sys_msg = next((m['content'] for m in messages if m.get('role') == 'system'), system_prompt)
        user_msgs = [m for m in messages if m.get('role') != 'system']
        combined_user = '\n\n'.join(m['content'] for m in user_msgs)
    else:
        sys_msg = system_prompt
        combined_user = prompt

    res = try_providers(sys_msg, combined_user, max_tokens, temperature)
    if isinstance(res, tuple):
        return res[0]
    return res

def parse_json_safely(raw_output):
    clean_json = raw_output
    if clean_json.startswith("```json"):
        clean_json = clean_json[7:-3].strip()
    elif clean_json.startswith("```"):
        clean_json = clean_json[3:-3].strip()
        
    try:
        return json.loads(clean_json)
    except Exception as e:
        print(f"  [!] Failed to parse JSON: {e}")
        return None

def load_user_profile():
    base_dir = Path(__file__).resolve().parent.parent
    profile_path = base_dir / "config" / "profile.yml"
    if not profile_path.exists():
        profile_path = base_dir / "config" / "profile.example.yml"
    if profile_path.exists():
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                parsed = yaml.safe_load(f)
                return parsed if isinstance(parsed, dict) else {}
        except Exception:
            pass
    return {}

def generate_resource_summary(title, source_url, domain, primary_mode, secondary_modes, raw_content):
    profile = load_user_profile()
    user_name = profile.get("name", "Markus")
    user_role = profile.get("role", "AI Systems Builder & Wellness Entrepreneur")
    user_prefs = profile.get("preferences", {})
    comm_style = user_prefs.get("communication_style", "direct, structured, action-oriented")
    
    domains_focus = []
    for d_entry in profile.get("core_domains", []):
        d_name = d_entry.get("name", d_entry["id"])
        d_focus = ", ".join(d_entry.get("focus", []))
        domains_focus.append(f"- {d_name} ({d_entry['id']}): Focuses on {d_focus}")
    domains_str = "\n".join(domains_focus) if domains_focus else "- General Life & Career Management"

    system_prompt = (
        f"You are LifeOS Research Resource Mode. You turn raw transcripts, books, and articles into useful, deep, highly personalized structured notes for {user_name}.\n\n"
        f"User Profile:\n"
        f"- Name: {user_name}\n"
        f"- Role: {user_role}\n"
        f"- Core Domains & Focus Areas:\n{domains_str}\n\n"
        f"Style & Preference Guidelines:\n"
        f"- Style: {comm_style}\n"
        f"- Formatting: Rich, deep, analytical, structured. No generic corporate speak or fluff. Be concrete and specific.\n"
        f"- Do not invent facts. Return valid JSON only."
    )
    sec_modes_str = ", ".join(secondary_modes) if secondary_modes else "None"
    
    overall_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    provider_used = "unknown"
    model_used = "unknown"
    
    if len(raw_content) > 18000:
        chunks = split_text(raw_content, chunk_size=12000, overlap=1000)
        print(f"\n  [*] Long content detected ({len(raw_content)} chars). Splitting into {len(chunks)} chunks.")
        
        chunk_summaries = []
        for i, chunk in enumerate(chunks):
            print(f"\n  === Summarizing chunk {i+1}/{len(chunks)} ===")
            chunk_prompt = f"Analyze this part ({i+1}/{len(chunks)}) of the resource '{title}'. Extract key points concisely.\n\nContent:\n{chunk}"
            res = try_providers("You are a helpful research assistant. Summarize the text concisely.", chunk_prompt, 800)
            if res:
                content, p_name, m_name, t_usage = res
                chunk_summaries.append(content)
                provider_used = p_name
                model_used = m_name
                overall_usage["prompt_tokens"] += t_usage.get("prompt_tokens", 0)
                overall_usage["completion_tokens"] += t_usage.get("completion_tokens", 0)
                overall_usage["total_tokens"] += t_usage.get("total_tokens", 0)
            else:
                chunk_summaries.append(f"[Chunk {i+1} failed]")

        combined_summaries = "\n\n---\n\n".join(f"Chunk {i+1} Summary:\n{s}" for i, s in enumerate(chunk_summaries))
        user_prompt = f"""
Analyze this resource in depth:
Title: {title}
URL: {source_url}
Domain: {domain}
Primary Mode: {primary_mode}
Secondary Modes: {sec_modes_str}

Combined Chunk Summaries:
{combined_summaries}

Return JSON only in this exact format:
{{
  "summary": "Detailed multi-paragraph summary of the resource's core arguments and worldview.",
  "key_ideas": [
    "Key concept 1: Actionable, rich description of what it is and how to apply it.",
    "Key concept 2: Actionable, rich description..."
  ],
  "why_this_matters_for_markus": [
    "Specific connection to Markus's projects/focus areas.",
    "Specific connection..."
  ],
  "suggested_tags": ["string"],
  "related_modes": ["string"],
  "next_action": "One concrete, step-by-step next action for Markus to implement.",
  "source_reliability": "string",
  "confidence": "low|medium|high"
}}
"""
        final_res = try_providers(system_prompt, user_prompt, 1500)
        if final_res:
            content, p_name, m_name, t_usage = final_res
            parsed = parse_json_safely(content)
            if parsed:
                parsed["is_chunked"] = True
                parsed["chunks_processed"] = len(chunks)
                parsed["chunk_summaries"] = combined_summaries
                parsed["provider_used"] = p_name
                parsed["model_used"] = m_name
                parsed["token_usage"] = t_usage
                return parsed
        return {"raw_output": "Final synthesis failed.", "is_chunked": True}
            
    else:
        user_prompt = f"""
Analyze this resource in depth:
Title: {title}
URL: {source_url}
Domain: {domain}
Primary Mode: {primary_mode}
Secondary Modes: {sec_modes_str}

Content:
{raw_content}

Return JSON only in this exact format:
{{
  "summary": "Detailed multi-paragraph summary of the resource's core arguments and worldview.",
  "key_ideas": [
    "Key concept 1: Actionable, rich description of what it is and how to apply it.",
    "Key concept 2: Actionable, rich description..."
  ],
  "why_this_matters_for_markus": [
    "Specific connection to Markus's projects/focus areas.",
    "Specific connection..."
  ],
  "suggested_tags": ["string"],
  "related_modes": ["string"],
  "next_action": "One concrete, step-by-step next action for Markus to implement.",
  "source_reliability": "string",
  "confidence": "low|medium|high"
}}
"""
        print("\n  === Generating summary ===")
        res = try_providers(system_prompt, user_prompt, 1500)
        if res:
            content, p_name, m_name, t_usage = res
            parsed = parse_json_safely(content)
            if parsed:
                parsed["is_chunked"] = False
                parsed["provider_used"] = p_name
                parsed["model_used"] = m_name
                parsed["token_usage"] = t_usage
                return parsed
        return None
