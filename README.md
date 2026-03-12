# Sudoku CSP Solver

This project is part of the *Foundations of AI* final project. The goal is to model Sudoku as a **Constraint Satisfaction Problem (CSP)** and evaluate how different search strategies affect solving efficiency.

Sudoku is formulated as a CSP where:
- **Variables:** grid cells
- **Domains:** possible digits (1–9)
- **Constraints:** row, column, and 3×3 subgrid uniqueness rules

The project explores how AI techniques such as **backtracking search and heuristic variable ordering** improve performance.

---

## Current Progress

At this stage, the project includes:

- Sudoku board representation and puzzle parsing
- Constraint checking for rows, columns, and subgrids
- A **baseline backtracking solver**
- Implementation of the **Minimum Remaining Values (MRV)** heuristic
- Basic performance metrics:
  - recursive calls
  - backtracking steps
  - runtime

Initial testing shows that MRV significantly reduces search effort compared to naive backtracking.

---

## Next Steps

- Implement **forward checking** for constraint propagation
- Evaluate solver performance across **multiple Sudoku puzzles**
- Compare algorithms including:
  - Backtracking
  - Backtracking + MRV
  - Backtracking + Forward Checking
  - Backtracking + MRV + Forward Checking

---

## Project Structure

```
sudoku_solver/
│
├── main.py          # Runs solver and prints results
├── solver.py        # Backtracking and MRV algorithms
├── sudoku_board.py  # Board representation and constraint checking
├── puzzles.txt      # Optional puzzle dataset for testing
└── README.md
```

---

## How to Run

Make sure you are in the project directory and run:

```bash
  python main.py
```

The program will:

1. Load a Sudoku puzzle
2. Solve it using the baseline backtracking algorithm
3. Solve it again using the MRV heuristic
4. Print the solved puzzle and performance metrics (recursive calls, backtracks, runtime)


## Progress Report

The first progress report for this project can be found in:

reports/progress_report_1.pdf