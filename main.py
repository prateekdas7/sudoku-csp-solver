import time
from sudoku_board import SudokuBoard
from solver import SudokuSolver


def run_solver(name: str, puzzle: str, use_mrv: bool = False) -> None:
    board = SudokuBoard.from_string(puzzle)
    solver = SudokuSolver()

    print(f"\n=== {name} ===")
    print("Original puzzle:\n")
    print(board)
    print("\nSolving...\n")

    start_time = time.perf_counter()

    if use_mrv:
        solved = solver.solve_backtracking_mrv(board)
    else:
        solved = solver.solve_backtracking(board)

    end_time = time.perf_counter()

    if solved:
        print("Solved puzzle:\n")
        print(board)
    else:
        print("No solution found.")

    print("\nMetrics:")
    print(f"Recursive calls: {solver.recursive_calls}")
    print(f"Backtracks: {solver.backtracks}")
    print(f"Elapsed time: {end_time - start_time:.6f} seconds")


def run_example() -> None:
    puzzle = (
        "530070000"
        "600195000"
        "098000060"
        "800060003"
        "400803001"
        "700020006"
        "060000280"
        "000419005"
        "000080079"
    )

    run_solver("Baseline Backtracking", puzzle, use_mrv=False)
    run_solver("Backtracking + MRV", puzzle, use_mrv=True)


if __name__ == "__main__":
    run_example()
