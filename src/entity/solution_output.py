"""Solution step output — int[6] 1-index golden format."""

from __future__ import annotations

from entity.blank_loc import find_blank_coords
from entity.constants import BLANK_CELL, BLANK_COUNT

STATUS_OK = "OK"


def format_step_a_output(grid: list[list[int]]) -> str:
    """Format step-a success: status line + int[6] comma-separated (1-index)."""
    coords = find_blank_coords(grid)
    if len(coords) != BLANK_COUNT:
        raise ValueError(f"expected {BLANK_COUNT} blanks, got {len(coords)}")
    r1, c1 = coords[0]
    r2, c2 = coords[1]
    int6 = [r1, c1, BLANK_CELL, r2, c2, BLANK_CELL]
    int6_line = ",".join(str(v) for v in int6)
    return f"{STATUS_OK}\n{int6_line}\n"
