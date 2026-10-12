"""Configuration validation tests."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from dlp_invest_mcp.config import Settings


@pytest.mark.parametrize(
    ("access_mode", "expected"),
    [
        ("read", "read"),
        (" READ ", "read"),
        ("Write", "write"),
        (" write ", "write"),
    ],
)
def test_access_mode_is_normalized(access_mode: str, expected: str) -> None:
    settings = Settings(_env_file=None, access_mode=access_mode)
    assert settings.access_mode == expected


@pytest.mark.parametrize("access_mode", ["", "reed", "write-all"])
def test_access_mode_rejects_invalid_values(access_mode: str) -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, access_mode=access_mode)
