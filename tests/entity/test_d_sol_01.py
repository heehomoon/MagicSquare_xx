"""D-SOL-01 — step-a int[6] output golden master (entity, Logic Track)."""

from __future__ import annotations

import sys
from pathlib import Path

from entity.solution_output import format_step_a_output

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))
from _approval import assert_matches_golden

_GOLDEN_REL = "golden/d_sol_01_g1_step_a.approved.txt"


def test_d_sol_01_step_a_success(grid_g1: list[list[int]]) -> None:
    # Given: G1 격자 (0이 2개)
    # When: step-a 출력 포맷 생성
    actual = format_step_a_output(grid_g1)
    # Then: golden 고정 포맷 (OK + int[6] 1-index)
    assert_matches_golden(actual, _GOLDEN_REL)
