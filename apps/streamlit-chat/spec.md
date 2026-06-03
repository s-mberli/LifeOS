# Spec: LifeOS Chat UI Polish

## Objective
Take the functional Streamlit application and transform it into a premium, consumer-grade product. Meticulously polish the UI/UX focusing on visual hierarchy, layout optimization (whitespace, empty states), micro-copy, button alignment, tooltips, and custom CSS injections.

## Tech Stack
- Core: Streamlit (Python framework)
- HTML & CSS (Vanilla CSS injected via `st.markdown`)
- Testing: pytest + Streamlit AppTest framework

## Commands
- Run app: `streamlit run apps/streamlit-chat/app.py`
- Test: `.venv/bin/pytest tests/test_ui.py`
- Lint: `.venv/bin/flake8` or standard linter if available

## Project Structure
- `apps/streamlit-chat/ui/chat.py` - Core chat interface implementation (CSS injection, empty state, chat logic)
- `tests/test_ui.py` - Streamlit AppTest integration tests

## Code Style
- **Clean Python:** Keep Streamlit components clean, avoid inline complex styling directly on elements where possible.
- **Structured Custom CSS:** Inject CSS via a single, well-commented `<style>` tag block at the beginning of the chat body rendering.
- **Python Conventions:** Adhere to `AGENTS.md` guidelines (e.g. no programmatic source code modification via regex/scripts, use pathlib.Path).

Example of Custom CSS block style:
```python
def inject_custom_css() -> None:
    st.markdown(
        """
        <style>
            /* Custom CSS rules go here */
            .stButton > button {
                border-radius: 8px !important;
                transition: background-color 0.2s ease, transform 0.1s ease;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
```

## Testing Strategy
- Leverage pytest and the Streamlit AppTest framework (`streamlit.testing.v1.AppTest`).
- Write integration tests in `tests/test_ui.py` that check if the UI contains the new elements (e.g., verifying that empty state components are rendered, and that tooltips/help arguments are configured).
- Since CSS layout styling is visual, manual verification using the app is the primary method to confirm styles look premium.

## Boundaries
- **Always:** Use custom CSS to polish default Streamlit styles; ensure the app works in both light and dark mode.
- **Ask first:** Installing new Streamlit styling plugins.
- **Never:** Programmatically modify files using scripts; remove existing business logic or RAG search features.

## Success Criteria
- **Visual Hierarchy & Layout:**
  - An empty state welcoming the user is displayed when the chat message history (`st.session_state.messages`) is empty.
  - The empty state section is beautifully formatted, showing welcoming text and onboarding hints.
  - Spacing is clean and uses `st.divider()` or markdown margins to separate the chat history/empty state from scope select boxes.
  - Columns for message actions are balanced (`[1, 1, 2]` or similar custom column spacing) to look clean and neat.
- **Micro-Copy & Button Polish:**
  - Buttons and inputs have polished, punchy micro-copy with consistent emoji usage.
  - Tooltips (`help="..."`) are added to the scopes multiselect and response length selectbox.
- **Custom CSS:**
  - Standard buttons have softened border radius and a hover scale/shadow transition.
  - Chat bubbles are styled with a modern aesthetic, distinct styling for user vs. assistant, and smooth margins.
  - The chat input has adjusted border radius and shadow.

## Open Questions
- None.

## Assumptions
1. We are targeting default Streamlit elements, utilizing their class selectors (like `.stButton > button` or `[data-testid="stChatMessage"]`) for custom styling.
2. The user runs this app locally and will manually view the visual layout.
3. Tests should execute and verify element presence rather than visual pixel comparisons.
