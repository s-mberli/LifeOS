"""
Core logic for LifeOS chat context management and agent loops.
"""

from typing import Optional
from pathlib import Path

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
        "You have access to a search tool: fts_search.\n"
        "If you need to query the database/vault for specific facts, insights, or details "
        "not present in your active context, output an XML tag exactly like this:\n"
        "<call:fts_search>your query here</call:fts_search>\n"
        "Do not explain the call, do not output any other text when calling a tool.\n"
        "After you output the tag, the system will execute it and provide the results.\n"
    )
    augmented_system = system_prompt + tool_instructions
    
    if fts_search_fn is None:
        from src.core.search_knowledge import fts_search as fts_search_fn

    current_history = list(history) if history else []
    calls_made = []
    all_raw_results = []
    current_source_idx = starting_source_index

    for _ in range(max_turns):
        response = ask_llm_chat(augmented_system, user_prompt, history=current_history)
        if not response:
            break

        match = re.search(r"<call:fts_search>(.*?)</call:fts_search>", response, re.DOTALL)
        if not match:
            return response, calls_made, all_raw_results

        query = match.group(1).strip()
        # Some fts_search_fn signatures might not support include_private, so handle carefully if needed.
        # But we know we are passing the core fts_search which does.
        try:
            results = fts_search_fn(query, limit=3, allowed_paths=allowed_paths, include_private=include_private)
        except TypeError:
            results = fts_search_fn(query, limit=3, allowed_paths=allowed_paths)
        
        if results:
            formatted_list = []
            for r in results:
                r_title, r_path, r_snippet, r_score = r
                formatted_list.append(f"### Search Result [{current_source_idx}]: {r_title}\nPath: {r_path}\n\n{r_snippet}")
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
                f"Use the above search results to complete your answer."
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
