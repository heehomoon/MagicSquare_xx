"""Golden Master approval helpers."""

from __future__ import annotations

import os
from pathlib import Path

_TESTS_ROOT = Path(__file__).resolve().parent


def assert_matches_golden(actual: str, relative: str) -> None:
    """Compare actual text to tests/<relative>, or update when UPDATE_GOLDEN=1."""
    golden_path = _TESTS_ROOT / relative
    if os.environ.get("UPDATE_GOLDEN") == "1":
        golden_path.parent.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(actual, encoding="utf-8", newline="\n")
        return

    if not golden_path.is_file():
        raise AssertionError(f"Golden file missing: {golden_path}")

    expected = golden_path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(
            f"Golden mismatch: {relative}\n"
            f"--- expected ---\n{expected!r}\n"
            f"--- actual ---\n{actual!r}"
        )
