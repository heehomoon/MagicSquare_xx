"""Shared pytest fixtures — data only, no domain logic."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(_SRC))
for _mod in list(sys.modules):
    if _mod == "entity" or _mod.startswith("entity."):
        del sys.modules[_mod]

from entity.constants import GRID_SIZE, MAGIC_CONSTANT, MAX_CELL_VALUE

# G1: 4×4, 빈칸(0) 2개, row-major → 1-index (2,2) then (3,3)
_GRID_G1_ROWS: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]


@pytest.fixture
def grid_g1() -> list[list[int]]:
    """G1: partial 4×4, two blanks at 1-index (2,2) and (3,3) in row-major order."""
    _ = (GRID_SIZE, MAGIC_CONSTANT, MAX_CELL_VALUE)  # SSOT import used in fixture scope
    return [row[:] for row in _GRID_G1_ROWS]
