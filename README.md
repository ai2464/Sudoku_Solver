## Overview

This Sudoku Solver is designed to efficiently tackle Sudoku puzzles. It incorporates a blend of advanced algorithms, including backtracking, heuristic-driven cell selection (Most Constrained Variable), and forward checking for domain updates. 

## Features

- **Backtracking**: Systematically fills in cells and reverts to a prior state if an invalid state is reached, ensuring a comprehensive search for the solution.
- **Heuristic-Driven Cell Selection (MRV)**: Prioritizes cells with the fewest legal values in its domain to reduce the search space.
- **Forward Checking**: Proactively checks the domain of possible values for other cells after filling a cell to optimize the backtracking process.

## Usage

You can run the Sudoku solver in two ways:

1. **Single Board**
   ```bash
   python3 sudoku.py <input_string>

2. **Multiple Boards**
   ```bash
   python3 sudoku.py
  This will process all boards in sudokus_start.txt.
  The solved boards will be written to output.txt.

## Performance
The Sudoku Solver demonstrated exceptional performance in tests:

Successfully solved 1000 out of 1000 boards.
- Min solve time: 0.00683 seconds
- Max solve time: 0.75021 seconds
- Mean solve time: 0.06824 seconds
- Standard Deviation of solve times: 0.08870 seconds

## Source Code Overview

- Helper functions to print the board and convert the board dictionary to a string format.
- Functions for domain checking, constraints validation, and heuristic implementation.
- Main algorithm implementation using backtracking and forward checking.
- Command-line interface for processing either single board input or multiple boards from a file.

   
