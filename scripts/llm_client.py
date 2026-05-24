"""
scripts/llm_client.py — Multi-provider LLM call wrapper for LifeOS.

Tries providers in the order specified by the ``LLM_PROVIDER_ORDER``
environment variable (default: ``azure,gemini,openrouter``).  Falls back to
the next provider if the current one fails.

Public interface
----------------
call_llm      : unified wrapper — accepts a simple prompt or messages list
generate_resource_summary : structured JSON summarisation pipeline
parse_json_safely         : robust JSON extraction from raw LLM output
"""
import os
import json


def mask_key(key):
    if not key:
        return "no"
    return "yes"

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
            prefix = key[:6]
            if len(prefix) >= 4:
                err_str = err_str.replace(prefix, "[MASKED_PREFIX]")
    return err_str

def split_text(text, chunk_size=12000, overlap=1000):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def call_azure(system_prompt, user_prompt, requested_max_tokens, temperature=0.2):
    try:
        from openai import OpenAI
        import openai
    except ImportError:
        print("    [!] OpenAI SDK not installed. Install with: pip install openai")
        return None

    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT") or os.environ.get("AZURE_EXISTING_AIPROJECT_ENDPOINT")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    max_tokens_env = int(os.environ.get("AZURE_OPENAI_MAX_TOKENS", "1200"))
    
    max_tokens = min(requested_max_tokens, max_tokens_env, 4000)

    print(f"  [Azure] Deployment: {deployment} | Max Tokens: {max_tokens} | Key Found: {mask_key(api_key)}")
    if not api_key or not endpoint:
        print("    [!] Azure missing API key or endpoint in .env.")
        return None

    client = OpenAI(base_url=endpoint, api_key=api_key)
    try:
        try:
            # Prefer Responses API
            response = client.responses.create(
                model=deployment,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_output_tokens=max_tokens,
                temperature=temperature
            )
            if hasattr(response, 'choices') and response.choices:
                content = response.choices[0].message.content.strip()
            elif hasattr(response, 'content'):
                content = response.content.strip()
            elif hasattr(response, 'output'):
                content = response.output.strip()
            else:
                content = str(response).strip()
                
            usage = getattr(response, "usage", None)
            token_usage = {
                "prompt_tokens": getattr(usage, "prompt_tokens", 0) if usage else 0,
                "completion_tokens": getattr(usage, "completion_tokens", 0) if usage else 0,
                "total_tokens": getattr(usage, "total_tokens", 0) if usage else 0,
            }
            return content, "azure", deployment, token_usage
        except (AttributeError, Exception):
            # Fall back to chat.completions.create if Responses API is unavailable or fails
            response = client.chat.completions.create(
                model=deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_completion_tokens=max_tokens,
                temperature=temperature
            )
            content = response.choices[0].message.content.strip()
            usage = getattr(response, "usage", None)
            token_usage = {
                "prompt_tokens": getattr(usage, "prompt_tokens", 0) if usage else 0,
                "completion_tokens": getattr(usage, "completion_tokens", 0) if usage else 0,
                "total_tokens": getattr(usage, "total_tokens", 0) if usage else 0,
            }
            return content, "azure", deployment, token_usage
    except Exception as e:
        if isinstance(e, openai.AuthenticationError) or '401' in str(e):
            print("    [!] 401 Authentication failed for Azure. Check AZURE_OPENAI_API_KEY.")
        elif '402' in str(e) or 'quota' in str(e).lower() or '429' in str(e):
            print("    [!] Quota or token limit error for Azure. Check tokens or credits.")
        else:
            print(f"    [!] Azure API call failed: {sanitize_err(e)}")
        return None

def call_gemini(system_prompt, user_prompt, requested_max_tokens, temperature=0.2):
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("    [!] Gemini provider unavailable. Install with: pip install google-genai")
        return None

    api_key = os.environ.get("GEMINI_API_KEY")
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    max_tokens_env = int(os.environ.get("GEMINI_MAX_TOKENS", "1200"))
    max_tokens = min(requested_max_tokens, max_tokens_env, 4000)

    print(f"  [Gemini] Model: {model} | Max Tokens: {max_tokens} | Key Found: {mask_key(api_key)}")
    if not api_key:
        print("    [!] GEMINI_API_KEY missing in .env.")
        return None

    client = genai.Client(api_key=api_key)
    try:
        contents = f"System: {system_prompt}\n\nUser: {user_prompt}"
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=types.GenerateContentConfig(
                max_output_tokens=max_tokens,
                temperature=temperature
            )
        )
        content = response.text.strip()
        usage = getattr(response, "usage_metadata", None)
        token_usage = {
            "prompt_tokens": getattr(usage, "prompt_token_count", 0) if usage else 0,
            "completion_tokens": getattr(usage, "candidates_token_count", 0) if usage else 0,
            "total_tokens": getattr(usage, "total_token_count", 0) if usage else 0,
        }
        return content, "gemini", model, token_usage
    except Exception as e:
        if '401' in str(e) or 'API_KEY_INVALID' in str(e):
            print("    [!] 401 Authentication failed for Gemini. Check GEMINI_API_KEY.")
        elif '402' in str(e) or 'quota' in str(e).lower() or '429' in str(e):
            print("    [!] Quota error for Gemini. Check credits.")
        else:
            print(f"    [!] Gemini API call failed: {sanitize_err(e)}")
        return None

def call_openrouter(system_prompt, user_prompt, requested_max_tokens, temperature=0.2):
    try:
        from openai import OpenAI
        import openai
    except ImportError:
        print("    [!] OpenAI SDK not installed. Install with: pip install openai")
        return None

    api_key = os.environ.get("OPENROUTER_API_KEY")
    model = os.environ.get("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    max_tokens_env = int(os.environ.get("OPENROUTER_MAX_TOKENS", "1200"))
    max_tokens = min(requested_max_tokens, max_tokens_env, 4000)

    print(f"  [OpenRouter] Model: {model} | Max Tokens: {max_tokens} | Key Found: {mask_key(api_key)}")
    if not api_key:
        print("    [!] OPENROUTER_API_KEY missing in .env.")
        return None

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        content = response.choices[0].message.content.strip()
        usage = getattr(response, "usage", None)
        token_usage = {
            "prompt_tokens": getattr(usage, "prompt_tokens", 0) if usage else 0,
            "completion_tokens": getattr(usage, "completion_tokens", 0) if usage else 0,
            "total_tokens": getattr(usage, "total_tokens", 0) if usage else 0,
        }
        return content, "openrouter", model, token_usage
    except Exception as e:
        if isinstance(e, openai.AuthenticationError) or '401' in str(e):
            print("    [!] 401 Authentication failed for OpenRouter. Check OPENROUTER_API_KEY.")
        elif '402' in str(e) or 'quota' in str(e).lower() or '429' in str(e):
            print("    [!] 402 Credit error for OpenRouter. Lower max tokens or add credits.")
        else:
            print(f"    [!] OpenRouter API call failed: {sanitize_err(e)}")
        return None

def try_providers(system_prompt, user_prompt, max_tokens, temperature=0.2):
    order_str = os.environ.get("LLM_PROVIDER_ORDER", "azure,gemini,openrouter")
    providers = [p.strip().lower() for p in order_str.split(",")]
    
    for provider in providers:
        if provider == "azure":
            res = call_azure(system_prompt, user_prompt, max_tokens, temperature)
        elif provider == "gemini":
            res = call_gemini(system_prompt, user_prompt, max_tokens, temperature)
        elif provider == "openrouter":
            res = call_openrouter(system_prompt, user_prompt, max_tokens, temperature)
        else:
            print(f"  [!] Unknown provider: {provider}")
            continue
            
        if res is not None:
            return res
            
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
    """Unified LLM call wrapper.

    If ``messages`` is provided (OpenAI-style list), it is used directly.
    Otherwise, ``prompt`` + ``system_prompt`` are used to build the messages
    list.

    Args:
        prompt:        Simple string prompt (used when messages is None).
        system_prompt: System context (used when messages is None).
        messages:      OpenAI-style message list [{role, content}, ...].
        max_tokens:    Maximum output tokens.
        temperature:   Sampling temperature.
        model_type:    ``'fast'`` for cheaper model, ``'smart'`` for best
                       available.  Currently informational only — provider
                       selection is controlled by ``LLM_PROVIDER_ORDER``.
        json_mode:     Hint to prefer JSON output (not enforced at SDK level).

    Returns:
        Response string, or ``None`` if all providers fail.
    """
    if messages is not None:
        # Extract system and user content from messages list
        sys_msg = next(
            (m['content'] for m in messages if m.get('role') == 'system'),
            system_prompt,
        )
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
    import yaml
    from pathlib import Path
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
    
    # Format domains for context
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
    
    # Accumulate usage
    overall_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    provider_used = "unknown"
    model_used = "unknown"
    
    # 1. Chunking Logic
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
                print(f"  [!] All providers failed for chunk {i+1}.")
                chunk_summaries.append(f"[Chunk {i+1} failed]")

        print("\n  === Synthesizing final summary from chunks ===")
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
    "Specific connection to Markus's projects/focus areas (e.g. Flow Temple, AI Brain, routines).",
    "Specific connection..."
  ],
  "suggested_tags": ["string"],
  "related_modes": ["string"],
  "next_action": "One concrete, step-by-step next action for Markus to implement (e.g., 'Stack this routine with...', 'Implement this agent workflow...').",
  "source_reliability": "string",
  "confidence": "low|medium|high"
}}

Note:
- In "suggested_tags", provide between 6 and 10 high-signal tags.
- In "source_reliability", explain whether the note is based on video commentary, original paper, official docs, etc.
- Avoid generic high-level statements. Make every bullet point specific, technical, and concrete.
"""
        final_res = try_providers(system_prompt, user_prompt, 1500)
        if final_res:
            content, p_name, m_name, t_usage = final_res
            provider_used = p_name
            model_used = m_name
            overall_usage["prompt_tokens"] += t_usage.get("prompt_tokens", 0)
            overall_usage["completion_tokens"] += t_usage.get("completion_tokens", 0)
            overall_usage["total_tokens"] += t_usage.get("total_tokens", 0)
            
            parsed = parse_json_safely(content)
            if parsed:
                parsed["is_chunked"] = True
                parsed["chunks_processed"] = len(chunks)
                parsed["chunk_summaries"] = combined_summaries
                parsed["provider_used"] = provider_used
                parsed["model_used"] = model_used
                parsed["token_usage"] = overall_usage
                return parsed
            else:
                return {
                    "raw_output": content, 
                    "is_chunked": True, 
                    "chunks_processed": len(chunks), 
                    "chunk_summaries": combined_summaries,
                    "provider_used": provider_used,
                    "model_used": model_used,
                    "token_usage": overall_usage
                }
        else:
            return {
                "raw_output": "Final synthesis failed across all providers.",
                "is_chunked": True,
                "chunks_processed": len(chunks),
                "chunk_summaries": combined_summaries,
                "provider_used": provider_used,
                "model_used": model_used,
                "token_usage": overall_usage
            }
            
    else:
        # Single Pass Logic
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
    "Specific connection to Markus's projects/focus areas (e.g. Flow Temple, AI Brain, routines).",
    "Specific connection..."
  ],
  "suggested_tags": ["string"],
  "related_modes": ["string"],
  "next_action": "One concrete, step-by-step next action for Markus to implement (e.g., 'Stack this routine with...', 'Implement this agent workflow...').",
  "source_reliability": "string",
  "confidence": "low|medium|high"
}}

Note:
- In "suggested_tags", provide between 6 and 10 high-signal tags.
- In "source_reliability", explain whether the note is based on video commentary, original paper, official docs, etc.
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
            else:
                return {
                    "raw_output": content, 
                    "is_chunked": False,
                    "provider_used": p_name,
                    "model_used": m_name,
                    "token_usage": t_usage
                }
        return None
