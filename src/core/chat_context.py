"""
Core logic for LifeOS chat context management and agent loops.
"""

from typing import Optional
from pathlib import Path
from src.core.agent_harness import execute_with_repair

def ask_llm_chat(
    system_prompt: str,
    user_prompt: str,
    history: Optional[list] = None,
) -> str:
    try:
        from src.core.llm_client import call_llm

        messages: list[dict] = [{"role": "system", "content": system_prompt}]
        if history:
            for msg in history:
                if msg.get("role") in ("user", "assistant"):
                    messages.append(msg)
        messages.append({"role": "user", "content": user_prompt})

        result = call_llm(messages=messages, model_type="smart", json_mode=False)
        return result[0] if isinstance(result, tuple) else result
    except Exception as exc:
        return f"[LLM Error] {exc}"

@execute_with_repair(mode="ui")
def execute_agent_search_loop(
    system_prompt: str,
    user_prompt: str,
    history: Optional[list] = None,
    allowed_paths: Optional[set] = None,
    max_turns: int = 3,
    fts_search_fn=None,
    include_private: bool = False,
    starting_source_index: int = 1,
) -> tuple[str, list[tuple[str, str]], list]:
    import re
    tool_instructions = (
        "\n\n=== Tool Access ===\n"
        "You have access to two tools:\n\n"
        "1. fts_search — Query the local knowledge vault for stored notes/transcripts.\n"
        "   Usage: <call:fts_search>your query here</call:fts_search>\n\n"
        "2. fetch_web — Fetch the full content of any URL from the live web.\n"
        "   Use this when you find a link in search results and need its full content.\n"
        "   Usage: <call:fetch_web>https://example.com/article</call:fetch_web>\n\n"
        "Rules:\n"
        "- Output ONLY the XML tag when calling a tool — no surrounding explanation.\n"
        "- Use at most one tool call per turn.\n"
        "- After you output a tool call tag, the system will execute it and return results.\n"
    )
    augmented_system = system_prompt + tool_instructions

    if fts_search_fn is None:
        from src.core.search_knowledge import fts_search as fts_search_fn

    current_history = list(history) if history else []
    calls_made = []
    all_raw_results = []
    current_source_idx = starting_source_index

    # Compile tool regexes once
    _fts_re = re.compile(r"<call:fts_search>(.*?)</call:fts_search>", re.DOTALL)
    _web_re = re.compile(r"<call:fetch_web>(.*?)</call:fetch_web>", re.DOTALL)
    _WEB_CONTENT_LIMIT = 6000  # chars — keeps token cost predictable

    for _ in range(max_turns):
        response = ask_llm_chat(augmented_system, user_prompt, history=current_history)
        if not response:
            break

        fts_match = _fts_re.search(response)
        web_match = _web_re.search(response)

        if not fts_match and not web_match:
            # No tool call — the LLM is done
            return response, calls_made, all_raw_results

        if fts_match:
            query = fts_match.group(1).strip()
            try:
                results = fts_search_fn(query, limit=3, allowed_paths=allowed_paths, include_private=include_private)
            except TypeError:
                results = fts_search_fn(query, limit=3, allowed_paths=allowed_paths)

            if results:
                formatted_list = []
                for r in results:
                    r_title, r_path, r_snippet, r_score = r
                    formatted_list.append(
                        f"### Search Result [{current_source_idx}]: {r_title}\nPath: {r_path}\n\n{r_snippet}"
                    )
                    all_raw_results.append(r)
                    current_source_idx += 1
                results_str = "\n\n---\n\n".join(formatted_list)
            else:
                results_str = "No results found in knowledge base."

            calls_made.append((query, results_str))
            current_history.append({"role": "assistant", "content": response})
            current_history.append({
                "role": "user",
                "content": (
                    f"<response:fts_search>\n{results_str}\n</response:fts_search>\n"
                    "Use the above search results to continue your answer."
                )
            })

        elif web_match:
            url = web_match.group(1).strip()
            import urllib.parse
            parsed_url = urllib.parse.urlparse(url)
            blocked_hosts = ["localhost", "127.0.0.1", "0.0.0.0", "169.254.169.254"]
            
            if parsed_url.hostname in blocked_hosts or (parsed_url.hostname and parsed_url.hostname.startswith(("192.168.", "10.", "172."))):
                web_result = f"fetch_web error: Access to {parsed_url.hostname} is blocked for security."
            else:
                try:
                    from src.core.web import fetch_webpage_content
                    _title, _content = fetch_webpage_content(url)
                    if _content:
                        # Cap content to avoid token overflows
                        if len(_content) > _WEB_CONTENT_LIMIT:
                            _content = _content[:_WEB_CONTENT_LIMIT] + "\n\n[... content truncated for length ...]"
                        web_result = f"### Fetched: {_title or url}\nURL: {url}\n\n{_content}"
                    else:
                        web_result = f"Could not retrieve content from: {url}"
                except Exception as exc:
                    web_result = f"fetch_web error for {url}: {exc}"

            calls_made.append((url, web_result))
            current_history.append({"role": "assistant", "content": response})
            current_history.append({
                "role": "user",
                "content": (
                    f"<response:fetch_web>\n{web_result}\n</response:fetch_web>\n"
                    "Use the above web content to continue your answer."
                )
            })

    final_response = ask_llm_chat(augmented_system, user_prompt, history=current_history)
    return final_response, calls_made, all_raw_results

def extract_mention(prompt: str, existing_experts: list) -> Optional[dict]:
    """Parse a prompt for @mentions to resolve an expert."""
    for e in existing_experts:
        slug_without_prefix = e["slug"].replace("expert--", "")
        if (
            f"@{e['display_name'].lower()}" in prompt.lower()
            or f"@{slug_without_prefix}" in prompt.lower()
        ):
            return e
    return None
