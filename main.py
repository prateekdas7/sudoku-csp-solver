import time
from sudoku_board import SudokuBoard
from solver import SudokuSolver


def load_puzzles(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]


def run_algorithm(puzzle, method):
    board = SudokuBoard.from_string(puzzle)
    solver = SudokuSolver()

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

    results = {m: {"calls": [], "backtracks": [], "time": []} for m in methods}

    for puzzle in puzzles:
        for m in methods:
            calls, backs, t = run_algorithm(puzzle, m)
            results[m]["calls"].append(calls)
            results[m]["backtracks"].append(backs)
            results[m]["time"].append(t)

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