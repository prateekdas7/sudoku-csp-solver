# Implements four Sudoku solving strategies with increasing sophistication:
# 1. Baseline backtracking
# 2. Backtracking with MRV (Minimum Remaining Values) heuristic
# 3. Backtracking with forward checking (constraint propagation)
# 4. Backtracking with MRV + forward checking combined
# Each solver tracks recursive calls and backtracks for performance comparison.

from typing import Dict, Optional, Set, Tuple
from sudoku_board import SudokuBoard

# Type aliases for readability: a Cell is a (row, col) position,
# and Domains maps each cell to its set of remaining possible values.
Cell = Tuple[int, int]
Domains = Dict[Cell, Set[int]]


class SudokuSolver:
    # Metrics tracked across a single solve to measure search efficiency
    def __init__(self) -> None:
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
                # Empty cells: compute valid values from current board state
                # Filled cells: domain is just the assigned value (singleton set)
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

        # Cells in the same row and same column (excluding the cell itself)
        for i in range(9):
            if i != col:
                neighbors.add((row, i))
            if i != row:
                neighbors.add((i, col))

        # Cells in the same 3x3 box (duplicates with row/col are handled by set)
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
        Apply forward checking after assigning 'value' to (row, col).

        Returns updated domains if successful.
        Returns None if any neighbor domain becomes empty.
        """
        # Deep copy so pruning doesn't affect the caller's domains on backtrack
        new_domains = self.copy_domains(domains)
        # Lock this cell's domain to the assigned value
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
        self.recursive_calls += 1 # Count every entry into the solver as a recursive call

        empty_cell = board.find_empty()
        # Base case: no empty cells remain, puzzle is solved
        if empty_cell is None:
            return True

        row, col = empty_cell

        # Try all digits 1-9 in order; no heuristic for variable or value ordering.
        # If a value satisfies constraints, recurse. If recursion fails,
        # undo the assignment (backtrack) and try the next value.
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
        # 10 is larger than any possible domain (max 9), so the first
        # empty cell found always becomes the initial best candidate.
        best_domain_size = 10

        for row in range(9):
            for col in range(9):
                if board.grid[row][col] == 0:
                    domain_size = len(board.get_domain(row, col))
                    # "Fail-first" principle: pick the most constrained cell
                    # to cause early failure and prune the search tree.
                    # Ties are broken by top-left scan order.
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
        # Unlike baseline, iterate only over valid domain values rather than 1-9
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

        # Initialize domains on first call only; recursive calls receive
        # pruned domains passed down from forward checking
        if domains is None:
            domains = self.initialize_domains(board)

        empty_cell = board.find_empty()
        if empty_cell is None:
            return True

        row, col = empty_cell

        # Sorted iteration for deterministic behavior
        for value in sorted(domains[(row, col)]):
            if board.is_valid(row, col, value):
                board.grid[row][col] = value

                new_domains = self.apply_forward_checking(
                    board, row, col, value, domains
                )

                # If forward checking succeeded (no empty domains), recurse
                # with the pruned domains. Otherwise, skip this value.
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

        # Initialize domains on first call only; recursive calls receive
        # pruned domains passed down from forward checking
        if domains is None:
            domains = self.initialize_domains(board)

        empty_cell = self.select_unassigned_variable_mrv_domains(board, domains)
        if empty_cell is None:
            return True

        row, col = empty_cell

        # Sorted iteration for deterministic behavior
        for value in sorted(domains[(row, col)]):
            if board.is_valid(row, col, value):
                board.grid[row][col] = value

                new_domains = self.apply_forward_checking(
                    board, row, col, value, domains
                )

                # If forward checking succeeded (no empty domains), recurse
                # with the pruned domains. Otherwise, skip this value.
                if new_domains is not None:
                    if self.solve_mrv_forward_checking(board, new_domains):
                        return True

                board.grid[row][col] = 0

        self.backtracks += 1
        return False