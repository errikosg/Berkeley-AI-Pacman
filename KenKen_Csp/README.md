## KenKen Puzzle


KenKen is a famous arithmetic and logic puzzle, similar to Sudoku.

More info about the game: [KenKen Wiki](https://en.wikipedia.org/wiki/KenKen).
Play the game: [KenKen](https://www.kenkenpuzzle.com/).

The implementation of the problem is based on: [csp.py](https://github.com/aimacode/aima-python/blob/master/csp.py).
The problem is modelled like a **CSP (Constraint Satisfaction Problem)** and the algorithms implemented are:

* BT        ( Simple or Chronological Backtracking )
* BT + MRV  ( BT + Minimum Remaining Values heuristic )
* FC        ( Forward Checking )
* FC + MRV
* MAC       ( Maintaining Arc Consistency )

The file **Grids.txt** contains the grids needed to run the program, formatted in a specific way.
