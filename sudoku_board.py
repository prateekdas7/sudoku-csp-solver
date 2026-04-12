# Represents a 9x9 Sudoku grid and provides methods for constraint checking.
# Each cell holds an int: 1-9 for filled cells, 0 for empty cells.

from typing import List, Optional, Tuple


class SudokuBoard:
    def __init__(self, grid: List[List[int]]) -> None:
        self.grid = grid

    @classmethod
    def from_string(cls, puzzle: str) -> "SudokuBoard":
        """
        Create a SudokuBoard from an 81-character string.
        Use 0 or . for empty cells.
        """
        puzzle = puzzle.replace(".", "0").replace("\n", "").replace(" ", "") # Normalize input: accept '.' as empty, strip whitespace/newlines
        if len(puzzle) != 81:
            raise ValueError("Puzzle must contain exactly 81 characters.")

        # Convert flat string into a 9x9 grid (list of lists), 9 chars per row
        grid = []
        for i in range(0, 81, 9):
            row = [int(ch) for ch in puzzle[i:i + 9]]
            grid.append(row)

        return cls(grid)

    def copy(self) -> "SudokuBoard":
        """Return a deep copy of the board so modifications don't affect the original."""
        return SudokuBoard([row[:] for row in self.grid])

    def find_empty(self) -> Optional[Tuple[int, int]]:
        """
        Return the row, col of the first empty cell, or None if full.
        """
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    return row, col
        return None

    def is_valid(self, row: int, col: int, value: int) -> bool:
        """
        Check whether placing value at (row, col) is valid.
        """
        # Ensure no other cell in this row already holds this value
        for c in range(9):
            if self.grid[row][c] == value and c != col:
                return False

        # Ensure no other cell in this column already holds this value
        for r in range(9):
            if self.grid[r][col] == value and r != row:
                return False

        # Check 3x3 box: find the top-left corner of the box this cell belongs to
        box_row_start = (row // 3) * 3
        box_col_start = (col // 3) * 3

        for r in range(box_row_start, box_row_start + 3):
            for c in range(box_col_start, box_col_start + 3):
                if self.grid[r][c] == value and (r, c) != (row, col):
                    return False

        return True

    def get_domain(self, row: int, col: int) -> List[int]:
        # Already-filled cells have no remaining domain to choose from
        if self.grid[row][col] != 0:
            return []

        # Try each digit 1-9 and keep those that don't violate any constraint
        domain = []
        for value in range(1, 10):
            if self.is_valid(row, col, value):
                domain.append(value)
        return domain

    def __str__(self) -> str:
        """Format the grid for display, with dividers between 3x3 boxes."""
        lines = []
        for r in range(9):
            if r % 3 == 0 and r != 0:
                lines.append("-" * 21)

            row_values = []
            for c in range(9):
                if c % 3 == 0 and c != 0:
                    row_values.append("|")

                val = self.grid[r][c]
                row_values.append(str(val) if val != 0 else ".")
            lines.append(" ".join(row_values))

        return "\n".join(lines)