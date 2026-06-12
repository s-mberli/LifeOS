import pytest
from unittest.mock import patch
from src.core.agent_harness import execute_with_repair, AgentEscalationError


def test_json_decode_error_repair_success():
    calls = []

    @execute_with_repair(mode="background", max_attempts=3)
    def flaky_json_parser():
        calls.append(1)
        if len(calls) < 3:
            raise type("JSONDecodeError", (Exception,), {})("Expecting value")
        return "success"

    result = flaky_json_parser()
    assert result == "success"
    assert len(calls) == 3


def test_timeout_error_backoff():
    calls = []

    @execute_with_repair(mode="background", max_attempts=3)
    def flaky_timeout():
        calls.append(1)
        if len(calls) < 2:
            raise TimeoutError("Connection timed out")
        return "success"

    with patch("time.sleep") as mock_sleep:
        result = flaky_timeout()
        assert result == "success"
        assert len(calls) == 2
        mock_sleep.assert_called_once()
        mock_sleep.assert_called_once_with(1)  # 2**0 = 1


def test_agent_escalation_error():
    calls = []

    @execute_with_repair(mode="background", max_attempts=3)
    def persistently_failing():
        calls.append(1)
        raise ValueError("Persistent error")

    with pytest.raises(AgentEscalationError) as exc_info:
        persistently_failing()

    assert len(calls) == 4  # Initial + 3 retries = 4
    assert "Agent failed after 4 attempt(s) in background mode" in str(exc_info.value)


def test_ui_mode_fast_fail():
    calls = []

    @execute_with_repair(mode="ui")
    def persistently_failing():
        calls.append(1)
        raise ValueError("Persistent error")

    with pytest.raises(AgentEscalationError) as exc_info:
        persistently_failing()

    assert len(calls) == 2  # Initial + 1 quick retry = 2
    assert "Agent failed after 2 attempt(s) in ui mode" in str(exc_info.value)
