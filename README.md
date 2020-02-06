# SUDO_KU

A python implementation of algorithms used to solve and generate sudoku puzzles.  
UNIX pun is intended.

## Current Features

* Solve any sudoku
* Generate sudokus
* Display sudokus in HTML format for printing
* Check sudoku difficulty / technique required
* Check if a sudoku has a unique solution or multitudes
* Check if it can be solved without guessing
* Permutate and transform sudokus to quickly find (up to 2.4 trillion) similar ones
* Store, access and retrive sudokus from a .txt file

## Usage

So far, only raw python functions exist. To use these functions you need to write a script in the sudo_ku.py file itself or use the "import" statement to use it as a library. For example, copy the sudo_ku.py file into your working directory and run
```
from sudo_ku import *
```
Where the code is not self-explanatory, comments are provided.  
sudo_ku.py has no dependencies.  


### Examples
Generate and display a sudoku with 30 clues in the console:
```
printGrid(generateSudoku(30))
```

Solve and display a sudoku using a brute force depth-first backtracking approach:
```
printGrid(solveSudoku(testSudoku))
```

Check if a sudoku can be solved without guessing or advanced strategy:
```
print(sudokuIsEasy(testSudoku))
```

Generate five sudokus with 35 clues each and their solutions and output them in HTML for printing:
```
sudokus=generateSudokus(5,35)
outputHtml(sudokus + solveSudokus(sudokus))
```

Permutate all numbers in a sudoku to different numbers, then rotate each resulting sudoku by 90° clockwise:
```
X = list(map(matrixRotate, allMatrixSymbolPermutations(testSudoku,0)))
```

Check to see if a puzzle has a unique solution or multiple solutions:
```
print(testUniquity(testSudoku))
```
