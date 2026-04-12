# Experiment runner: loads puzzles, runs each of the four solving strategies,
# and reports average performance metrics (recursive calls, backtracks, runtime).

import time
from sudoku_board import SudokuBoard
from solver import SudokuSolver


def load_puzzles(filename):
    """Load puzzles from a text file, one 81-character puzzle string per line."""
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]


def run_algorithm(puzzle, method):
    """Run a single puzzle with the specified method and return performance metrics.
        A fresh SudokuSolver is created each time to reset metric counters."""
    board = SudokuBoard.from_string(puzzle)
    solver = SudokuSolver()

    # Use perf_counter for high-resolution wall-clock timing
    start = time.perf_counter()

    if method == "bt":
        solver.solve_backtracking(board)
    elif method == "mrv":
        solver.solve_backtracking_mrv(board)
    elif method == "fc":
        solver.solve_forward_checking(board)
    elif method == "mrv_fc":
        solver.solve_mrv_forward_checking(board)

    end = time.perf_counter()

    return (
        solver.recursive_calls,
        solver.backtracks,
        end - start
    )

def run_experiments():
    puzzles = load_puzzles("puzzles.txt")
    methods = ["bt", "mrv", "fc", "mrv_fc"]

    # Accumulate per-puzzle metrics for each method to compute averages later
    results = {m: {"calls": [], "backtracks": [], "time": []} for m in methods}

    # Run every method on every puzzle and record individual results
    for puzzle in puzzles:
        for m in methods:
            calls, backs, t = run_algorithm(puzzle, m)
            results[m]["calls"].append(calls)
            results[m]["backtracks"].append(backs)
            results[m]["time"].append(t)

    # Compute and display the mean of each metric across all puzzles
    print("\n=== RESULTS ===\n")
    for m in methods:
        avg_calls = sum(results[m]["calls"]) / len(puzzles)
        avg_back = sum(results[m]["backtracks"]) / len(puzzles)
        avg_time = sum(results[m]["time"]) / len(puzzles)

        print(f"{m}:")
        print(f"  Avg Calls: {avg_calls:.2f}")
        print(f"  Avg Backtracks: {avg_back:.2f}")
        print(f"  Avg Time: {avg_time:.6f}\n")


if __name__ == "__main__":
    run_experiments()