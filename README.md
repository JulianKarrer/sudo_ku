# SUDO_KU

A python implementation of algorithms used to solve and generate sudoku puzzles.
UNIX pun is intended.

## Current Features

* Solve any sudoku
* Generate sudokus
* Count the number of solutions of a sudoku
* Check if a sudoku has a unique solution
* Permutate and transform sudokus to quickly find (up to 2.4 trillion) similar ones
* Store, access and retrive sudokus from a .txt file

## Usage

So far, only raw python functions exists. To use these functions you need to modify the code. 
Where it is not self-explanatory, comments are provided.

### Examples:
Generate and display a sudoku with 30 clues in the console
```
printGrid(generateSudoku(30))
```

Solve and display a sudoku using a brute force depth-first backtracking approach
```
printGrid(solveSudoku(testSudoku))
```

Permutate all numbers in a sudoku to different numbers, than rotate each resulting sudoku by 90° clockwise
```
X = list(map(matrixRotate, allMatrixSymbolPermutations(testSudoku,0)))
```

Check to see if a puzzle has a unique solution or multiple solutions
```
print(testUniquity(testSudoku))
```

