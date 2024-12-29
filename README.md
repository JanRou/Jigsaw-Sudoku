*Sudoku Solver - Work in Progress*

The sudoku solver solves normal or jig-saw puzzles using rules. The solver will be extended with other types of sudoku puzzles like hyper, X and samurai. The solver is written in python in order to learn python and program a simple user interface. And, it uses rule based solving, so it's a kind of artificial intelligence.
The project is organized in folders:
* basesudoku holds the base classes to handle a sudoku and cells,
* root holds main that initializes a sudoku window and set a jigsaw puzzle for solving,
* test holds the unit test classes performed by python unittest lib,
* normal extends basesudoku with normal puzzle behaviour and rules for solving normal sudoku puzzles,
* jigsaw extends basesudoku with jigsaw puzzle behaviour and rules for solving jigsaw sudoku puzzles,
* hyper is empty and is the start of hyper sudoku puzzle type,
* x is empty and is the start of sudoku-x sudoku puzzle type,
* samurai is empty and is the start of samurai sudoku puzzle type.

The normal sudoku puzzle solving rules are implemented in normalSudoku.py, jigsaw rules in jigsawSudoku.py and so forth. 
