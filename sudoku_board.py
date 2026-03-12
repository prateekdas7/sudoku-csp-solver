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
        puzzle = puzzle.replace(".", "0").replace("\n", "").replace(" ", "")
        if len(puzzle) != 81:
            raise ValueError("Puzzle must contain exactly 81 characters.")

        grid = []
        for i in range(0, 81, 9):
            row = [int(ch) for ch in puzzle[i:i + 9]]
            grid.append(row)

        return cls(grid)

    def copy(self) -> "SudokuBoard":
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
        # Check row
        for c in range(9):
            if self.grid[row][c] == value and c != col:
                return False

        # Check column
        for r in range(9):
            if self.grid[r][col] == value and r != row:
                return False

        # Check 3x3 box
        box_row_start = (row // 3) * 3
        box_col_start = (col // 3) * 3

        for r in range(box_row_start, box_row_start + 3):
            for c in range(box_col_start, box_col_start + 3):
                if self.grid[r][c] == value and (r, c) != (row, col):
                    return False

        return True

    def get_domain(self, row: int, col: int) -> List[int]:
        """
        Return all valid values for a given empty cell.
        """
        if self.grid[row][col] != 0:
            return []

        domain = []
        for value in range(1, 10):
            if self.is_valid(row, col, value):
                domain.append(value)
        return domain

    def __str__(self) -> str:
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