"""Unit tests for the fixed-window rate limiter."""

from __future__ import annotations

import pytest
from fastapi import HTTPException

from app.ratelimit import FixedWindowLimiter


def test_allows_up_to_limit_then_blocks() -> None:
    limiter = FixedWindowLimiter(limit=2, window_s=60)
    limiter.check("1.2.3.4")
    limiter.check("1.2.3.4")
    with pytest.raises(HTTPException) as exc:
        limiter.check("1.2.3.4")
    assert exc.value.status_code == 429
    assert "Retry-After" in exc.value.headers


def test_separate_keys_have_separate_budgets() -> None:
    limiter = FixedWindowLimiter(limit=1, window_s=60)
    limiter.check("a")
    limiter.check("b")  # different key — should not raise
    with pytest.raises(HTTPException):
        limiter.check("a")
