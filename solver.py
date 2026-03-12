from typing import Dict, Optional, Set, Tuple
from sudoku_board import SudokuBoard


Cell = Tuple[int, int]
Domains = Dict[Cell, Set[int]]


class SudokuSolver:
    def __init__(self) -> None:
        self.recursive_calls = 0
        self.backtracks = 0

    def reset_metrics(self) -> None:
        self.recursive_calls = 0
        self.backtracks = 0

    def initialize_domains(self, board: SudokuBoard) -> Domains:
        """
        Create a domain for every cell.
        Filled cells get a singleton domain {value}.
        Empty cells get all currently valid values.
        """
        domains: Domains = {}

        for row in range(9):
            for col in range(9):
                if board.grid[row][col] == 0:
                    domains[(row, col)] = set(board.get_domain(row, col))
                else:
                    domains[(row, col)] = {board.grid[row][col]}

        return domains

    def get_neighbors(self, row: int, col: int) -> Set[Cell]:
        """
        Return all cells that share a row, column, or 3x3 box with (row, col).
        """
        neighbors: Set[Cell] = set()

        for i in range(9):
            if i != col:
                neighbors.add((row, i))
            if i != row:
                neighbors.add((i, col))

        box_row_start = (row // 3) * 3
        box_col_start = (col // 3) * 3

        for r in range(box_row_start, box_row_start + 3):
            for c in range(box_col_start, box_col_start + 3):
                if (r, c) != (row, col):
                    neighbors.add((r, c))

        return neighbors

    def copy_domains(self, domains: Domains) -> Domains:
        """
        Deep-copy domains dictionary.
        """
        return {cell: values.copy() for cell, values in domains.items()}

    def apply_forward_checking(
        self,
        board: SudokuBoard,
        row: int,
        col: int,
        value: int,
        domains: Domains,
    ) -> Optional[Domains]:
        """
        Apply forward checking after assigning `value` to (row, col).

        Returns updated domains if successful.
        Returns None if any neighbor domain becomes empty.
        """
        new_domains = self.copy_domains(domains)
        new_domains[(row, col)] = {value}

        for neighbor_row, neighbor_col in self.get_neighbors(row, col):
            # Skip already-filled cells
            if board.grid[neighbor_row][neighbor_col] != 0:
                continue

            if value in new_domains[(neighbor_row, neighbor_col)]:
                new_domains[(neighbor_row, neighbor_col)].remove(value)

                if not new_domains[(neighbor_row, neighbor_col)]:
                    return None

        return new_domains

    def solve_backtracking(self, board: SudokuBoard) -> bool:
        """
        Baseline backtracking solver.
        Modifies the board in place and returns True if solved.
        """
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
    ) -> Optional[Cell]:
        """
        Minimum Remaining Values heuristic.
        Return the empty cell with the smallest domain.
        """
        best_cell: Optional[Cell] = None
        best_domain_size = 10

        for row in range(9):
            for col in range(9):
                if board.grid[row][col] == 0:
                    domain_size = len(board.get_domain(row, col))
                    if domain_size < best_domain_size:
                        best_domain_size = domain_size
                        best_cell = (row, col)

        return best_cell

    def select_unassigned_variable_mrv_domains(
        self,
        board: SudokuBoard,
        domains: Domains,
    ) -> Optional[Cell]:
        """
        MRV using the maintained domains dictionary.
        """
        best_cell: Optional[Cell] = None
        best_domain_size = 10

        for row in range(9):
            for col in range(9):
                if board.grid[row][col] == 0:
                    domain_size = len(domains[(row, col)])
                    if domain_size < best_domain_size:
                        best_domain_size = domain_size
                        best_cell = (row, col)

        return best_cell

    def solve_backtracking_mrv(self, board: SudokuBoard) -> bool:
        """
        Backtracking solver using MRV.
        """
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

    def solve_forward_checking(
        self,
        board: SudokuBoard,
        domains: Optional[Domains] = None,
    ) -> bool:
        """
        Backtracking + forward checking.
        """
        self.recursive_calls += 1

        if domains is None:
            domains = self.initialize_domains(board)

        empty_cell = board.find_empty()
        if empty_cell is None:
            return True

        row, col = empty_cell

        for value in sorted(domains[(row, col)]):
            if board.is_valid(row, col, value):
                board.grid[row][col] = value

                new_domains = self.apply_forward_checking(
                    board, row, col, value, domains
                )

                if new_domains is not None:
                    if self.solve_forward_checking(board, new_domains):
                        return True

                board.grid[row][col] = 0

        self.backtracks += 1
        return False

    def solve_mrv_forward_checking(
        self,
        board: SudokuBoard,
        domains: Optional[Domains] = None,
    ) -> bool:
        """
        Backtracking + MRV + forward checking.
        """
        self.recursive_calls += 1

        if domains is None:
            domains = self.initialize_domains(board)

        empty_cell = self.select_unassigned_variable_mrv_domains(board, domains)
        if empty_cell is None:
            return True

        row, col = empty_cell

        for value in sorted(domains[(row, col)]):
            if board.is_valid(row, col, value):
                board.grid[row][col] = value

                new_domains = self.apply_forward_checking(
                    board, row, col, value, domains
                )

                if new_domains is not None:
                    if self.solve_mrv_forward_checking(board, new_domains):
                        return True

                board.grid[row][col] = 0

        self.backtracks += 1
        return False