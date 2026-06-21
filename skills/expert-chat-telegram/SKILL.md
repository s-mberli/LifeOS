---
name: expert-chat-telegram
description: Handle expert chat mode via Telegram. Load expert profiles (profile.md, playbook.md, principles.md, sources) and respond as the selected expert. Triggered by /expert commands in Telegram.
---

# Expert Chat — Telegram Mode

Let users talk to LifeOS expert profiles through Telegram, just like the Streamlit expert chat.

## State File

`/root/markusos/data/expert_chat_state.json`

Format: `{"<telegram_chat_id>": "<expert_slug>"}`

Example: `{"655978940": "expert--david-deida"}`

## Commands

### `/expert list`
List available experts with their insight counts.

### `/expert <name or slug>`
Activate expert mode. Match by slug (`expert--david-deida`) or fuzzy name (`david deida`, `deida`, `lenny`).
Load expert context and confirm activation.

### `/expert off`
Deactivate expert mode for this chat.

### `/expert status`
Show currently active expert.

### Any other message while in expert mode
Load the active expert's full context and respond AS that expert.

## How to Load Expert Context

Run the helper script:

```bash
cd /root/markusos && .venv/bin/python scripts/expert_chat.py load <slug>
```

This returns the full system prompt: profile + principles + playbook + source excerpts.

For listing:

```bash
cd /root/markusos && .venv/bin/python scripts/expert_chat.py list
```

## Response Format

When in expert mode, prepend responses with a subtle indicator like `🎭 **David Deida**` so the user knows which expert is active. Then respond in the expert's voice using their principles and playbook.

## State Management

Read/write the state file on every message:

```python
import json
from pathlib import Path

STATE_FILE = Path("/root/markusos/data/expert_chat_state.json")

def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}

def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, indent=2))

def get_active_expert(chat_id: str) -> str | None:
    return load_state().get(chat_id)

def set_active_expert(chat_id: str, slug: str | None):
    state = load_state()
    if slug is None:
        state.pop(chat_id, None)
    else:
        state[chat_id] = slug
    save_state(state)
```

## Fuzzy Name Matching

When user types `/expert david` or `/expert deida`, use the match script:

```bash
cd /root/markusos && .venv/bin/python scripts/expert_chat.py match <query>
```

- If single match → activate that expert
- If multiple matches → list them and ask user to be specific
- If no match → show available experts

Also accept full slugs directly: `/expert expert--david-deida`

## Important

- The expert context is the **system prompt** — the user's message is the user message
- Keep responses in the expert's voice and style based on their profile
- If sources are loaded, reference them naturally ("As I said in...")
- Don't break character unless the user says `/expert off`
