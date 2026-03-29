# Sudoku CSP Solver

This project is part of the *Foundations of Artificial Intelligence* final project. The goal is to model Sudoku as a **Constraint Satisfaction Problem (CSP)** and evaluate how different search strategies affect solving efficiency.

Sudoku is formulated as a CSP where:
- **Variables:** grid cells
- **Domains:** possible digits (1–9)
- **Constraints:** row, column, and 3×3 subgrid uniqueness rules

The project explores how AI techniques such as **backtracking search, heuristic variable ordering, and constraint propagation** improve performance.

---

## Implemented Methods

The following solving strategies have been implemented and compared:

- **Backtracking (Baseline)**
- **Backtracking + MRV (Minimum Remaining Values)**
- **Backtracking + Forward Checking**
- **Backtracking + MRV + Forward Checking**

---

## Results Summary

Experiments were conducted on a set of Sudoku puzzles, and performance was evaluated using:
- number of recursive calls
- number of backtracking steps
- runtime

### Key Observations:

- Baseline backtracking is highly inefficient due to large search space.
- MRV significantly reduces search effort by prioritizing constrained variables.
- Forward checking improves pruning but is less effective than MRV alone in this setup.
- The combination of **MRV + Forward Checking** performs best, achieving the lowest search cost and fastest runtime.

---

## Project Structure

sudoku_solver/<br>
│<br>
├── main.py # Runs experiments and prints results <br>
├── solver.py # All solving algorithms (BT, MRV, FC, MRV+FC)<br>
├── sudoku_board.py # Board representation and constraint checking<br>
├── puzzles.txt # Dataset of Sudoku puzzles<br>
├── README.md <br>
└── reports/<br>
&emsp;&emsp;&emsp;├── first_progress_report.pdf<br>
&emsp;&emsp;&emsp;└── final_progress_report.pdf<br>


---

## How to Run

Make sure you are in the project directory and run:

```bash
  python main.py
```

The program will:
 - Load multiple Sudoku puzzles from puzzles.txt
 - Run all solving strategies
 - Print average performance metrics for each method