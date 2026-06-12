"""
scripts/llm_client.py — Multi-provider LLM call wrapper for LifeOS using litellm.

Tries providers in the order specified by the ``LLM_PROVIDER_ORDER``
environment variable (default: ``openrouter,gemini``).
"""
import os
import json
from pathlib import Path
import yaml

import requests
import os
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    ROOT = Path(__file__).resolve().parent.parent.parent
    load_dotenv(ROOT / ".env", override=True)
except ImportError:
    pass


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

def call_openrouter(messages: list, max_tokens: int, temperature: float):
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not set")
    model = os.environ.get("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/s-mberli/LifeOS",
        "X-Title": "MarkusOS",
    }
    
    resp = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    res_body = resp.json()
    content = res_body["choices"][0]["message"]["content"]
    usage = res_body.get("usage", {})
    return content, model, usage

def call_gemini(messages: list, max_tokens: int, temperature: float):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    
    gemini_messages = []
    system_instruction = None
    
    for msg in messages:
        if msg["role"] == "system":
            system_instruction = {"parts": [{"text": msg["content"]}]}
        elif msg["role"] == "user":
            gemini_messages.append({"role": "user", "parts": [{"text": msg["content"]}]})
        elif msg["role"] == "assistant":
            gemini_messages.append({"role": "model", "parts": [{"text": msg["content"]}]})
            
    payload = {
        "contents": gemini_messages,
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens,
        }
    }
    if system_instruction:
        payload["systemInstruction"] = system_instruction
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=60)
    resp.raise_for_status()
    res_body = resp.json()
    content = res_body["candidates"][0]["content"]["parts"][0]["text"]
    usage = res_body.get("usageMetadata", {})
    std_usage = {
        "prompt_tokens": usage.get("promptTokenCount", 0),
        "completion_tokens": usage.get("candidatesTokenCount", 0),
        "total_tokens": usage.get("totalTokenCount", 0),
    }
    return content, model, std_usage

def call_azure(messages: list, max_tokens: int, temperature: float):
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    
    if not api_key or not endpoint:
        raise ValueError("AZURE_OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT not set")
        
    # Fix potential trailing slash and /openai/v1/ suffix in user endpoint config
    endpoint = endpoint.rstrip("/")
    if endpoint.endswith("/openai/v1"):
        endpoint = endpoint[:-10]
        
    url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={api_version}"
    
    payload = {
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json",
    }
    
    resp = requests.post(url, json=payload, headers=headers, timeout=60)
    if resp.status_code == 400:
        try:
            err_data = resp.json()
            err_msg = err_data.get("error", {}).get("message", "")
            if "max_tokens" in err_msg or "temperature" in err_msg or "max_completion_tokens" in err_msg:
                fallback_payload = {
                    "messages": messages,
                    "max_completion_tokens": max_tokens
                }
                resp = requests.post(url, json=fallback_payload, headers=headers, timeout=60)
        except Exception:
            pass

    resp.raise_for_status()
    res_body = resp.json()
    content = res_body["choices"][0]["message"]["content"]
    usage = res_body.get("usage", {})
    return content, deployment, usage


def try_providers(system_prompt: str, user_prompt: str, max_tokens: int, temperature: float = 0.3):
    """
    Attempts to call LLM providers in fallback order using explicit requests.
    Returns: tuple (content, provider_name, model_name, usage_dict) or None
    """
    order_str = os.environ.get("LLM_PROVIDER_ORDER", "openrouter,gemini")
    providers = [p.strip().lower() for p in order_str.split(",")]
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if user_prompt:
        messages.append({"role": "user", "content": user_prompt})
        
    for provider in providers:
        print(f"  [{provider.capitalize()}] Attempting call | Max Tokens: {max_tokens}")
        try:
            if provider == "openrouter":
                content, model_str, usage = call_openrouter(messages, max_tokens, temperature)
            elif provider == "gemini":
                content, model_str, usage = call_gemini(messages, max_tokens, temperature)
            elif provider == "azure":
                content, model_str, usage = call_azure(messages, max_tokens, temperature)
            else:
                continue
                
            if not content:
                raise ValueError("Provider returned empty or filtered content")

            token_usage = {
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0),
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
    max_tokens: int = 4096,
    temperature: float = 0.3,
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
    if not raw_output:
        return None
    clean_json = raw_output.strip()
    if clean_json.startswith("```json"):
        # Remove markdown block start and end if present
        if clean_json.endswith("```"):
            clean_json = clean_json[7:-3].strip()
        else:
            clean_json = clean_json[7:].strip()
    elif clean_json.startswith("```"):
        if clean_json.endswith("```"):
            clean_json = clean_json[3:-3].strip()
        else:
            clean_json = clean_json[3:].strip()
        
    try:
        return json.loads(clean_json)
    except Exception as e:
        print(f"  [!] Failed to parse JSON: {e}")
        print(f"  [!] Raw output was: {repr(raw_output)}")
        return None

def split_text(text: str, chunk_size: int = 12000, overlap: int = 1000) -> list[str]:
    """Splits a long string into chunks with a specified overlap."""
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]
        
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks
