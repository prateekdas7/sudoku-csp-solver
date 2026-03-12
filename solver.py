from typing import Optional, Tuple
from sudoku_board import SudokuBoard


class SudokuSolver:
    def __init__(self) -> None:
        self.recursive_calls = 0
        self.backtracks = 0

    def reset_metrics(self) -> None:
        self.recursive_calls = 0
        self.backtracks = 0

    def solve_backtracking(self, board: SudokuBoard) -> bool:
        self.recursive_calls += 1

        empty_cell = board.find_empty()
        if empty_cell is None:
            return True

        row, col = empty_cell

        for value in range(1, 10):
            if board.is_valid(row, col, value):
                board.grid[row][col] = value

                if self.solve_backtracking(board):
                    return True

                board.grid[row][col] = 0

        self.backtracks += 1
        return False

    def select_unassigned_variable_mrv(
        self, board: SudokuBoard
    ) -> Optional[Tuple[int, int]]:
        best_cell = None
        best_domain_size = 10

        for row in range(9):
            for col in range(9):
                if board.grid[row][col] == 0:
                    domain_size = len(board.get_domain(row, col))
                    if domain_size < best_domain_size:
                        best_domain_size = domain_size
                        best_cell = (row, col)

        return best_cell

    def solve_backtracking_mrv(self, board: SudokuBoard) -> bool:
        self.recursive_calls += 1

        empty_cell = self.select_unassigned_variable_mrv(board)
        if empty_cell is None:
            return True

        row, col = empty_cell
        domain = board.get_domain(row, col)

        for value in domain:
            board.grid[row][col] = value

            if self.solve_backtracking_mrv(board):
                return True

            board.grid[row][col] = 0

        self.backtracks += 1
        return False
