"""Blank cell location — row-major scan, 1-index coordinates."""

from __future__ import annotations

from entity.constants import BLANK_CELL, GRID_SIZE, INDEX_BASE


def find_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]:
    """Return 1-index (row, col) of blank cells in row-major order."""
    coords: list[tuple[int, int]] = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == BLANK_CELL:
                coords.append((row + INDEX_BASE, col + INDEX_BASE))
    return coords
