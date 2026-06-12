import sqlite3
import datetime
import time
import functools
from typing import Callable, Any, Optional
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "indexes" / "lifeOS.db"

# ── Constants ────────────────────────────────────────────────────────────────
MODE_BACKGROUND = "background"
MODE_UI = "ui"
ERR_JSON_DECODE = "JSONDecodeError"
ERR_TIMEOUT = "TimeoutError"
STRATEGY_SCHEMA_CORRECTION = "SchemaCorrectionRepair"
STRATEGY_EXPONENTIAL_BACKOFF = "ExponentialBackoffRepair"
STRATEGY_UNKNOWN = "UnknownRepair"
MAX_ERROR_MESSAGE_LENGTH = 4096


class AgentFailure(Exception):
    pass


class AgentEscalationError(Exception):
    pass


def _classify_repair_strategy(exc: Exception) -> str:
    """Map an exception type to a repair-strategy name."""
    exc_type = type(exc).__name__
    if exc_type == ERR_JSON_DECODE:
        return STRATEGY_SCHEMA_CORRECTION
    if exc_type == ERR_TIMEOUT:
        return STRATEGY_EXPONENTIAL_BACKOFF
    return STRATEGY_UNKNOWN


def _ensure_agent_repair_logs_table(cursor: sqlite3.Cursor) -> None:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_repair_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            function_name TEXT,
            mode TEXT,
            error_type TEXT,
            error_message TEXT,
            attempt INTEGER,
            repair_strategy TEXT
        )
    """)


def log_repair_attempt(
    function_name: str,
    mode: str,
    error_type: str,
    error_message: str,
    attempt: int,
    repair_strategy: str,
    db_path: Path = DB_PATH,
) -> None:
    # Truncate excessively long error messages to prevent DB bloat
    safe_message = error_message[:MAX_ERROR_MESSAGE_LENGTH]

    db_path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        _ensure_agent_repair_logs_table(cursor)
        cursor.execute(
            """INSERT INTO agent_repair_logs
               (timestamp, function_name, mode, error_type, error_message, attempt, repair_strategy)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (now, function_name, mode, error_type, safe_message, attempt, repair_strategy),
        )
        conn.commit()


def execute_with_repair(
    mode: str = MODE_BACKGROUND,
    max_attempts: int = 3,
) -> Callable:
    """
    Decorator that catches exceptions from the wrapped function and applies
    autonomous repair strategies before escalating.

    Parameters
    ----------
    mode : str
        ``'background'`` – allows up to *max_attempts* retries.
        ``'ui'``          – fails fast after a single attempt.
    max_attempts : int
        Maximum number of attempts in *background* mode (ignored in *ui* mode).
    """
    # A "retry" means an attempt after the initial one.
    limit = max_attempts + 1 if mode == MODE_BACKGROUND else 2

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exc: Optional[Exception] = None

            for attempt in range(1, limit + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
                    strategy = _classify_repair_strategy(exc)

                    if strategy == STRATEGY_EXPONENTIAL_BACKOFF and mode == MODE_BACKGROUND:
                        time.sleep(2 ** (attempt - 1))

                    log_repair_attempt(
                        function_name=func.__name__,
                        mode=mode,
                        error_type=type(exc).__name__,
                        error_message=str(exc),
                        attempt=attempt,
                        repair_strategy=strategy,
                    )

            # All attempts exhausted — escalate
            assert last_exc is not None
            raise AgentEscalationError(
                f"Agent failed after {limit} attempt(s) in {mode} mode: {last_exc}"
            ) from last_exc

        return wrapper

    return decorator
