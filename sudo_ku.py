import random
import itertools
import re
import math
from operator import sub


#GLOBAL VARIABLES
#initialize 9x9 sudoku as an integer matrix to an empty state
emptyGrid = [
[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]

#a test sudoku to be solved when debugging
testSudoku = [
[0,3,0,9,4,5,0,0,0],[0,4,0,3,0,0,7,0,5],[0,6,0,0,0,0,0,0,0],
[0,0,3,6,0,0,0,8,0],[0,0,7,8,0,0,3,9,0],[4,0,8,7,9,0,2,1,0],
[5,0,4,0,0,2,0,0,0],[0,0,0,0,0,6,9,4,0],[2,0,0,0,3,0,0,0,8]]
doneTestSudoku = [
[7,3,2,9,4,5,8,6,1],[1,4,9,3,6,8,7,2,5],[8,6,5,2,1,7,4,3,9],
[9,1,3,6,2,4,5,8,7],[6,2,7,8,5,1,3,9,4],[4,5,8,7,9,3,2,1,6],
[5,9,4,1,8,2,6,7,3],[3,8,1,5,7,6,9,4,2],[2,7,6,4,3,9,1,5,8]]
manySolutionTestSudoku = [
[0,8,0,0,0,9,7,4,3],[0,5,0,0,0,8,0,1,0],[0,1,0,0,0,0,0,0,0],
[8,0,0,0,0,5,0,0,0],[0,0,0,8,0,4,0,0,0],[0,0,0,3,0,0,0,0,6],
[0,0,0,0,0,0,0,7,0],[0,3,0,5,0,0,0,8,0],[9,7,2,4,0,0,0,5,0]]
matrixTestGrid = [
[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],
[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],
[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],]

#a list of grids used in file IO operations. txt-entries are read into it, and written from it
memory=[]

#declare counter for number of solutions on global scale (countSolutions, testUniquity, solveSudoku)
uniqueCounter=0
counter=0
solutionFound=False

#declare empty grid to hold the solution of solveSudoku on global scale
solution=[
[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]

#list of accepted symbols (later shuffled)
symbols = [1,2,3,4,5,6,7,8,9]
#this table shows the difference in index of a field to fields of the same 3x3 section depending on the row/col index modulo 3
sectionIndexes = [[0,1,2],[-1,0,1],[-2,-1,0]]




#UTILITY FUNCTIONS
#print the grid, used for debugging
def printGrid(grid):
	for row in grid:
		print(row)

#return a deepcopy of the grid that was passed in
def deepcopyGrid(grid):
	copy=[
	[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
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

#return the number of zeros in a grid
def numberOfZeros(grid):
	num=0
	for row, col in itertools.product(range(9), range(9)):
		if grid[row][col]==0:
			num+=1
	return num




#MAIN FUNCTIONS
#fill the empty grid with one random possible solved sudoku.
def fillSudoku(grid):
	grid = deepcopyGrid(grid)
	#the algorithm within the while loop has a chance to fail, leaving zeros on the grid.
	#therefore the grid is reset and the algorithm repeated until a solution is found
	while checkForZeros(grid):
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
	return grid

#attempt every legal step to solve a sudoku until a valid solution is found
#this acts like a recursive "search tree" of possible ways to attempt this sudoku
#this function terminates as soon as the first solution is hit and therefore does not check for the uniquity of the solution
def solveSudoku(grid):
	#the placeholder grid for the solution and the boolean indicating whether a solution has been found are defined globally
	#so that they can be accessed equally throughout all layers of recursion
	global solutionFound
	global solution
	#this subfunction performs the actual recursive depth-first search for a solution
	def inner_solveSudoku(grid):
		global solutionFound
		global solution
		#iterate over every field on the grid
		for row, col in itertools.product(range(9), range(9)):
			#in each iteration, first check if a solution has already been found, if so, abort and return
			if solutionFound:
				return True
			#when an empty field has been found, try inserting every possible number without breaking sudoku rules
			if grid[row][col]==0:
				for x in range(1,10):
					if checkBeforeInsert(grid, row, col, x):
						#when a number has been found, insert it for now
						grid[row][col]=x
						#then check if this insertion results in a solution
						if not checkForZeros(grid):
							#if so, set the solutionFound flag to abort the search process and store the solution
							solution = deepcopyGrid(grid)
							solutionFound = True
							break
						else:
						#otherwise, for each possible value to be inserted try solving the resulting grid recursively
						#progressing down the search tree
							if inner_solveSudoku(deepcopyGrid(grid)):
								return True
				break

	#the outer function handles return values and resets the global variables
	inner_solveSudoku(deepcopyGrid(grid))
	solutionFound=False
	x=solution
	solution = emptyGrid
	return x



#THIS FUNCTION SEEMS NOT TO BE WORKING PROPERLY (but remains in the codebase until i figure out why).

# A working version is provided above (solveSudoku)
#attempt every legal step to solve a sudoku until a valid solution is found
#this acts like a recursive "search tree" of possible ways to attempt this sudoku
#this function terminates as soon as the first solution is hit and therefore does not check for the uniquity of the solution
def XsolveSudoku(grid):
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



#return the number of solutions of a sudoku puzzle.
#passing this function an empty grid or a sudoku with insuffiecient clues will cause runtime issues
def countSolutions(grid):
	#to keep track of the counter throughout multiple layers of recursion it is defined globally
	global counter
	def inner_countSolutions(grid):
		global counter
		#the following code to attempt every possible solution is copied from the solveSudoku function (see comments above) but modified
		#loop through all fields, find the next empty one
		for row, col in itertools.product(range(9), range(9)):
			if grid[row][col]==0:
				#attempt to fill it with every possible value
				for x in range(1,10):
					if checkBeforeInsert(grid, row, col, x):
						#if the insertion does not break any rules, insert the number for now and check if this solves the puzzle
						grid[row][col]=x
						if not checkForZeros(grid):
							#if a solution is found, instead of returning the solved field, we just increment the solution-counter and break
							counter+=1
							break
						else:
							#otherwise, we continue the depth-frist search down the rabbit hole of recursion.
							if inner_countSolutions(deepcopyGrid(grid)):
								return True
				break

	inner_countSolutions(deepcopyGrid(grid))
	x=counter
	counter=0
	return x



#to test the uniquity of a puzzle, it must only exhaustively be tested if there is more than one solution.
#therefore, as soon as two solutions are found the search can be stopped, avoiding long waits on puzzles with many solutions
#or runtime issues on empty grids.
#this is important when attempting to generate sudokus, as a speedy exectuion of this function is almost assured
#return value: true=unique, false=more than one solution
def testUniquity(grid):
	#the inner function performs the actual check, the outer function sets prerequisite variables and controls the return value
	def inner_testUniquity(grid):
		global uniqueCounter
		for row, col in itertools.product(range(9), range(9)):
			#the only difference to the countSolutions function above is this check: if we have found a second solution, return
			#for explanation, see the countSolutions function
			if uniqueCounter>1:
				return True
			if grid[row][col]==0:
				for x in range(1,10):
					if checkBeforeInsert(grid, row, col, x):
						grid[row][col]=x
						if not checkForZeros(grid):
							uniqueCounter+=1
							break
						else:
							if inner_testUniquity(deepcopyGrid(grid)):
								return True
				break

	inner_testUniquity(deepcopyGrid(grid))
	global uniqueCounter
	if uniqueCounter==1:
		uniqueCounter=0
		return True
	else:
		uniqueCounter=0
		return False



#this function is not guaranteed to return a sudoku with the specified amount of clues if doing so
#would result in a non-unique puzzle.
def generateSudoku(clues):
	#first, generate a full sudoku grid
	grid = fillSudoku(emptyGrid)
	#from the filled out grid we want to erase numbers at random positions, unless it results in a non-unique or unsolvable puzzle
	#this is done by shuffling all possible positions to erase numbers and try them, until the desired number of clues
	#is left or there are no more fields that can be erased.
	#all possible "coordinates" in a sudoku (cartesian product of range(9))
	coords = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [1, 0], [1, 1],[1, 2], [1, 3], [1, 4],
	 [1, 5], [1, 6], [1, 7], [1, 8], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5],[2, 6], [2, 7], [2, 8], [3, 0], [3, 1], 
	 [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7], [3, 8], [4, 0],[4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6], [4, 7], 
	 [4, 8], [5, 0], [5, 1], [5, 2], [5, 3], [5, 4],[5, 5], [5, 6], [5, 7], [5, 8], [6, 0], [6, 1], [6, 2], [6, 3], [6, 4], 
	 [6, 5], [6, 6], [6, 7], [6, 8],[7, 0], [7, 1], [7, 2], [7, 3], [7, 4], [7, 5], [7, 6], [7, 7], [7, 8], [8, 0], [8, 1], 
	 [8, 2], [8, 3],[8, 4], [8, 5], [8, 6], [8, 7], [8, 8]]
	random.shuffle(coords)
	#while there are more clues than specified AND not all positions have already been tried,
	#try to remove a clue at the next position in coords
	while len(coords)>0 and (81- numberOfZeros(grid))>clues:
		#save the field value in case removing it would destroy the puzzle and it needs to be put back
		x = grid[coords[0][0]][coords[0][1]]
		#remove the value
		grid[coords[0][0]][coords[0][1]]=0
		#if the grid now fails the uniquity test, put the value back
		if not testUniquity(grid):
			grid[coords[0][0]][coords[0][1]]=x
		#regardless of if the value was removed successfully or unsuccessfully, remove the current coordinate from coords
		coords.pop(0)
	return grid




#TRANSFORMTAION FUNCTIONS
#these functions perform matrix transformations on the sudoku grid, creating new grids without changing
#the number of clues, solvability or number of solutions of the puzzle. 
#especially in the case of difficult puzzles with few clues, generating related sudokus might be enormously faster than creating 
#individual sudokus from scratch using generateSudoku()

#as each of these functions can be applied in serial, a LOT of similar sudokus can be generated (4 * 9! * ...)

#for details on the mathematics, see https://en.wikipedia.org/wiki/Mathematics_of_Sudoku#Enumerating_essentially_different_Sudoku_solutions

#rotate the matrix by 90° clockwise
def matrixRotate(grid):
	a = deepcopyGrid(emptyGrid)	#initialize an empty matrix a
	for i in range(9):
		for j in range(9):
			#the inverted i and j mean a row becomes a column. the 8 - means the first row becomes the last column.
			#this equates to a 90° clockwise rotation
			a[j][8-i]=grid[i][j]	
	return a 

#wrapper function: by applying matrixRotate() twice, a matrix can be "flipped". 
#this way, no seperate algorithms for vertical and horizontal reflection need to be implemented.
def matrixFlip(grid):
	a=matrixRotate(matrixRotate(deepcopyGrid(grid)))
	return a

#combine the two functions above into a function that returns a full list of 0°, 90°, 180° and 270° rotated grids
def allMatrixRotations(grid):
	#add the grid itself to the list of rotations (0°)
	returnList=[grid]	
	for i in range(3):	
		#take the last entry of the list, rotate it again and append it to the list. 
		#this way each entry in the list is rotated once in comparison to its predecessor
		returnList.append(matrixRotate(returnList[-1]))
	return returnList



#return a list of all possible permutations of the symbols used in a sudoku
#for example, a sudoku is mathematically similar, even if all 3s and 8s are swapped etc.

#you can set the maximum number of unchanged numbers compared to the original puzzle to avoid very similar solutions
#the solutions may still, however, be very similar to each other
#	WARNING even maxUnchangedNumbers=0 results in ~20MB worth of sudokus
def allMatrixSymbolPermutations(grid,maxUnchangedNumbers=9):
	returnList=[]
	#find all possible permutations of the numbers 1 to 9 using itertools.
	allPermutations=itertools.permutations(symbols)
	#each entry in that list (9!=362 880 elements) acts like a lookup table:
	#	each number in the grid represents the index of the number to be translated to in that lookup table.
	for table in allPermutations:
		#check the number of values that have been swapped in this permutation. 
		#if more numbers than allowed by maxUnchangedNumbers remain the same in the new puzzle, skip this permutation
		x=tuple(map(sub,table,(1,2,3,4,5,6,7,8,9)))	
		#when the current tuple is subtracted by (1,2,3,4,5,6,7,8,9), unchanged numbers become 0
		#we can then count the number of zeros and compare it to maxUnchangedNumbers
		if x.count(0)>maxUnchangedNumbers:
			continue

		changedGrid=deepcopyGrid(emptyGrid)
		#loop through each field of the grid, skipping zeros
		for row, col in itertools.product(range(9), range(9)):
			if grid[row][col]!=0:
				#for each number, look up its corresponing new number and insert it into changedGrid in the same position
				changedGrid[row][col]=table[grid[row][col]-1]
		#once the entire grid has been translated, append it to the list of solutions
		returnList.append(changedGrid)
	#once all permutations have been considered, return the list
	return returnList





#IO FUNCTIONS
#write a list of strings into the file sudokumemory.txt
#the return value indicates the success of the operation (false = error, true = written)
def writeToFile(listOfStrings):
	#open the file in a try statement to contain possible io errors
	try:
		file = open("sudokumemory.txt",'a')
		#write each string in the list as a seperate line
		for string in listOfStrings:
			file.write(string+"\n")
	except Exception as e:
		return False
	else:
		return True
	finally:
		#flush the memory, close the file
		file.close()



#read the sudokumemory.txt file to import data
#returns a list of strings, each having been sanitized according to the sanitizeIpnut function below
#parameters: 	startline = index of the first line to be read starting with 0
#				numberOfLines = number of lines to be read (specify 0 to read all lines)
def readFromFile(startLine,numberOfLines):
	#list of strings to be returned
	returnList=[]
	#open the file in a try statement to contain possible io errors
	try:
		lineCounter = 0
		linesRead = 0
		file = open("sudokumemory.txt",'r')
		#iterate through every line in the file
		for line in file:
			#only read the file when the index of the current line is greater than or equal to the value specified in the parameters
			if lineCounter >= startLine:
				#also, only read it when numberOfLines=0 or the number of lines to be read has not been reached yet
				if numberOfLines==0 or numberOfLines<linesRead:
					#sanitize the input before adding it to the list of lines to be read according to the
					#rules in the sanitizeInput function. discard empty lines.
					x = sanitizeInput(line)
					if len(x)>0:
						returnList.append(x) 

			#increment counters to keep track of line index and number of lines read
					linesRead +=1
			lineCounter +=1
	except Exception as e:
		#if there was an error, return an empty list
		raise
		return []
	else:
		return returnList
	finally:
		#flush the memory, close the file
		file.close()



#use this function to sanitize the input from the sudokumemory.txt file - NEVER TRUST RAW USER INPUT
#only numbers and a maximum of 162 characters are allowed
def sanitizeInput(rawString):
	#remove anything but numbers
	x = re.sub('\D','',rawString)
	#truncate strings of more than 162 characters
	returnString = x[:162]
	#return the sanitized string
	return returnString



#serialize a sudoku and its solution into a string
#this function works row-wise from top to bottom, left to right
def sudokuToString(grid,solutionGrid=[
[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]):
	returnString=""
	#first, add each digit of the sudoku grid to the string
	for y, x in itertools.product(range(9), range(9)):
		returnString += str(grid[y][x])
	#then, add each digit of its solution to the string
	for y, x in itertools.product(range(9), range(9)):
		returnString += str(solutionGrid[y][x])
	return returnString



#de-serialize a string into a sudoku grid (THIS DISCARDS THE SOLUTION aka the last 81 digits of the 162 character code)
#this requires the first 81 characters to be a valid sudoku
def stringToGrid(string):
	returnGrid = deepcopyGrid(emptyGrid)
	string = string[:81]
	for index in range(81):
		col = index%9 				#the column is the index modulo 9
		row = math.floor(index/9) 	#the row is the integer number of times 9 fits into the index

		returnGrid[row][col]=int(string[index])
	return returnGrid




#CALL FUNCTIONS HERE
#printGrid(fillSudoku(emptyGrid))
#print()
#printGrid(solveSudoku(testSudoku))
#print()
#print(countSolutions(manySolutionTestSudoku))
#print()
#print(testUniquity(testSudoku))
#print(testUniquity(manySolutionTestSudoku))
#print()
#printGrid(generateSudoku(30))

#writeToFile(["12","34","abcdefghijklmnop5678"])
#x=readFromFile(0,0)
#for i in x:
#	print(i)

#printGrid(testSudoku)
#s=sudokuToString(testSudoku,solveSudoku(testSudoku))
#print(s)
#printGrid(stringToGrid(s))

#for x in allMatrixRotations(matrixTestGrid):
#	printGrid(x)
#	print()

#x=allMatrixSymbolPermutations(testSudoku,0)
#print("done")
#strlist=[]
#for entry in x:
#	strlist.append(sudokuToString(entry))
#writeToFile(strlist)


