import random
import itertools

#initialize 9x9 sudoku as an integer matrix to an empty state
emptyGrid = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]

#a test sudoku to be solved when debugging
testSudoku = [[0,3,0,9,4,5,0,0,0],[0,4,0,3,0,0,7,0,5],[0,6,0,0,0,0,0,0,0],[0,0,3,6,0,0,0,8,0],[0,0,7,8,0,0,3,9,0],[4,0,8,7,9,0,2,1,0],[5,0,4,0,0,2,0,0,0],[0,0,0,0,0,6,9,4,0],[2,0,0,0,3,0,0,0,8]]
doneTestSudoku = [[7,3,2,9,4,5,8,6,1],[1,4,9,3,6,8,7,2,5],[8,6,5,2,1,7,4,3,9],[9,1,3,6,2,4,5,8,7],[6,2,7,8,5,1,3,9,4],[4,5,8,7,9,3,2,1,6],[5,9,4,1,8,2,6,7,3],[3,8,1,5,7,6,9,4,2],[2,7,6,4,3,9,1,5,8]]
manySolutionTestSudoku = [[0,8,0,0,0,9,7,4,3],[0,5,0,0,0,8,0,1,0],[0,1,0,0,0,0,0,0,0],[8,0,0,0,0,5,0,0,0],[0,0,0,8,0,4,0,0,0],[0,0,0,3,0,0,0,0,6],[0,0,0,0,0,0,0,7,0],[0,3,0,5,0,0,0,8,0],[9,7,2,4,0,0,0,5,0]]


#list of accepted symbols (later shuffled)
symbols = [1,2,3,4,5,6,7,8,9]
#this table shows the difference in index of a field to fields of the same 3x3 section depending on the row/col index modulo 3
sectionIndexes = [[0,1,2],[-1,0,1],[-2,-1,0]]


#HELPER FUNCTIONS
#print the grid, used for debugging
def printGrid(grid):
	for row in grid:
		print(row)

#return a deepcopy of the grid that was passed in
def deepcopyGrid(grid):
	copy=[[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
	for y in range(9):
		for x in range(9):
			copy[y][x]=grid[y][x]
	return copy


#return the column of the grid at a given index (0-8) as a list
def getColumn(grid, index):
	return [grid[0][index],grid[1][index],grid[2][index],grid[3][index],grid[4][index],grid[5][index],grid[6][index],grid[7][index],grid[8][index]]

#check if a number can legally be inserted into a grid at a given position (x and y are indices from 0-8). true = may be legally inserted.
def checkBeforeInsert(grid, row, col, number):
	#numbers may only appear once per row
	if number in grid[row]:
		return False
	#numbers may only appear once per column
	elif number in getColumn(grid,col):
		return False
	#numbers may only appear once per 3x3 section of fields
	else:
		#look up the differences in index to other fields of the same 3x3 section per row and col
		rowDif = sectionIndexes[row%3]
		colDif = sectionIndexes[col%3]
		for dy in rowDif:
			for dx in colDif:
				#add all possible combinations of these deltas to the index -> get all fields in the same 3x3 section
				if grid[row+dy][col+dx] == number:
					return False
		#if no rule was broken, the number may legally be inserted at the specified position, return true
		return True

#check if a grid has any zeros (true=zeros, false=no zeros)
def checkForZeros(grid):
	for y in range(9):
		for x in range(9):
			if grid[y][x]==0:
				return True
	return False




#MAIN FUNCTIONS

#fill the empty grid with one random possible solved sudoku.
def fillSudoku(grid):
	#the algorithm within the while loop has a chance to fail, leaving zeros on the grid. 
	#therefore the grid is reset and the algorithm repeated until a solution is found
	i=0
	while checkForZeros(grid):
		i+=1
		#reset grid
		for y in range(9):
			for x in range(9):
				grid[y][x]=0

		#iterate through every field left on the grid
		for row in range(9):
			for col in range(9):
				random.shuffle(symbols)
				for number in symbols:
					#if a random number can legally be inserted at this position do so, if not, try the next number
					if checkBeforeInsert(grid,row,col,number):
						grid[row][col]=number
						break;
	#DEBUG
	print("found sudoku in {} tries".format(i))
	return grid



#attempt every legal step to solve a sudoku until a valid solution is found
#this acts like a recursive "search tree" of possible ways to attempt this sudoku
#this function terminates as soon as the first solution is hit and therefore does not check for the uniquity of the solution
def solveSudoku(grid):
	#first, check if sudoku is already solved, if so, return the solved sudoku
	if not checkForZeros(grid):
		return grid
	#check each empty field in order for numbers that may be inserted. 
	for row, col in itertools.product(range(9), range(9)):
		if grid[row][col]==0:
			possibleNumbers=[]
			for x in range(1,10):
				if checkBeforeInsert(grid, row, col, x):
					possibleNumbers.append(x)
			#there are two cases: 
			#A) there are no possible numbers to be inserted into this field. this means the way the sudoku has been filled out
			#so far is incorrect. this terminates a recursive branch by returning an empty grid
			if len(possibleNumbers)==0:
				return emptyGrid
			#B) there are one ore more numbers which may be inserted into this field. recursively try to solve each variant of the 
			#sudoku that results from those possible numbers being inserted
			if len(possibleNumbers)>0:
				for x in possibleNumbers:
					grid[row][col]=x
					#deepcopy to avoid search tree branches affecting each other (byref bugs)
					g = solveSudoku(deepcopyGrid(grid))
					#if the returned grid is a solution (contains no zeros), return the grid, unraveling the layers of recusion until the search tree root is hit
					#if not, continue in the for loop of possibleNumbers to traverse the search tree sideways
					if not checkForZeros(g):
						return g



#function to count the number of solutions of a sudoku puzzle.
#passing this function en empty grid or a sudoku with insuffiecient clues will cause runtime issues
def countSolutions(grid):
	#to keep track of the counter throughout multiple layers of recursion it is defined globally
	#it must be initialized (counter = 0) before countSolutions is called
	global counter
	#the following code to attempt every possible solution is copied from the solveSudoku function (see comments above) but modified
	for row, col in itertools.product(range(9), range(9)):
		if grid[row][col]==0:
			for x in range(1,10):
				if checkBeforeInsert(grid, row, col, x):
					#the first modification: we don't keep track of possibleNumbers to be inserted 
					grid[row][col]=x
					if not checkForZeros(grid):
						#this differentiates the countSolutions function from the sudokuSolver
						#if a solution is found, instead of returning the solved field, we just increment the solution-counter and break
						counter+=1
						break
					else:
						#otherwise, we continue the depth-frist search down the rabbit hole of recursion.
						if countSolutions(deepcopyGrid(grid)):
							return True
			break



#to test the uniquity of a puzzle, it must only exhaustively be tested if there is more than one solution.
#therefore, as soon as two solutions are found the search can be stopped, avoiding long waits on puzzles with many solutions
#or runtime issues on empty grids.
#this is important when attempting to generate sudokus, as a speedy exectuion of this function is almost assured
def testUniquity(grid):
	global counter
	for row, col in itertools.product(range(9), range(9)):
		#the only difference to the countSolutions function above is this check: if we have found a second solution, return
		#for explanation, see the countSolutions function
		if counter>1:
			return True
		if grid[row][col]==0:
			for x in range(1,10):
				if checkBeforeInsert(grid, row, col, x):
					grid[row][col]=x
					if not checkForZeros(grid):
						counter+=1
						break
					else:
						if testUniquity(deepcopyGrid(grid)):
							return True
			break





#CALL FUNCTIONS HERE

counter=0      
x=testUniquity(manySolutionTestSudoku) 
print("{}".format(counter))
print("{}".format(x))

