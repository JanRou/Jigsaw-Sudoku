import math
from sty import fg, bg, ef, rs

from jigsaw.cell import Cell

class Sudoku:
    def __init__(self, d, shape, colours): 
        # d is dimension of sudoku, usually 4, 9, 16, 25 ...
        # shape is d=nxn row and columns with group indexes 0 based, n=sqrt(d), 
        # where 0 is first group at upper left corner and n is last
        self._colours = colours
        self._dimension = d
        shapeCheck = self.CheckShape(shape) # returns tuple (bool, message)
        if not shapeCheck[0]:
            raise ValueError("Shape check failed: " + shapeCheck[1])
        self._groups = []  # the soudoku arranged by groups
        for rw in range( 0, self._dimension):
            self._groups.append([])
        self._sudoku = []  # the sudoku arranged by rows an columns
        for rw in range( 0, self._dimension):
            row = []            
            for col in range( 0, self._dimension):
                cell = Cell( self._dimension, rw, col, shape[rw][col], self._colours)
                row.append( cell )
                self._groups[shape[rw][col]].append(cell)
            self._sudoku.append(row)

    def CheckShape(self, shape): # returns tuple (bool, message)
        # each group index from 0 to dimension-1 must appear dimension times in shape
        groupIndexes = {} # dictionary to hold group indexes and counts as values
        msg = ""
        for r in range( 0, self._dimension):
            for c in range( 0, self._dimension):
                if shape[r][c] in groupIndexes:
                    # found the group, so increment count of group
                    groupIndexes[shape[r][c]] += 1
                else:
                    # not found group index, so add group and set count to 1
                    groupIndexes[shape[r][c]] = 1
        result = True
        for group in range(self._dimension):
            result = result and group in groupIndexes
            if not result: # group index missing
                msg = "Group index " + str(group) + " is not found in shape"
                break
            result = result and groupIndexes[group] == self._dimension
            if not result: # group index count not equal to dimension
                msg = "Count of group " + str(group) + " indexes is not equal to dimension, " + str(self._dimension)
                break
        return (result, msg)

    @property
    def Dimension(self):
        return self._dimension
    
    @property
    def Solved(self):
        # TODO check that the sudoku is really solved not just all cells have a number set!
        result = True
        for r in range(self._dimension):
            for c in range(self._dimension):
                result = result and self._sudoku[r][c].Solved
                if not result:
                    break
            if not result:
                break
        return result
    
    @property
    def Changed(self):
        result = False
        for r in range(self._dimension):
            for c in range(self._dimension):
                result = result or self._sudoku[r][c].Changed
                if result:
                    break
            if result:
                break
        return result

    def DoChange(self):
        for r in range(self._dimension):
            for c in range(self._dimension):
                self._sudoku[r][c].DoChange()

    @property
    def GetSudoku(self):
        return self._sudoku

    def Print(self, changed=False):
        rho = round(math.sqrt(self._dimension))
        for r in range( 0, self._dimension):
            strings = []
            for i in range(rho):
                strings.append("")
            for c in range( 0, self._dimension):
                cellStrings = self._sudoku[r][c].Print(changed)
                for i in range(rho):
                    strings[i] = strings[i] + cellStrings[i]
            for i in range(rho):
                print( strings[i] )

    def Set( self, r, c, n):
        self._sudoku[r][c].Number = n


    def RemoveCandidatesInColumnForNumber( self, column, number):
        # remove candidates in column
        for row in range( 0, self._dimension):
            self._sudoku[row][column].Remove(number)        

    def RemoveCandidatesInRowForNumber( self, row, number):
        # remove candidates in column
        for column in range( 0, self._dimension):
            self._sudoku[row][column].Remove(number)        

    def RemoveCandidatesInGroupForNumber( self, group, number):
        # remove candidates in group
        for cell in self._groups[group]:
            cell.Remove(number)

    def SetPossibleCandidate(self):
        # find solved
        cellsSolved = []
        for row in range( 0, self._dimension):
            for column in range( 0, self._dimension):
                if self._sudoku[row][column].Solved:
                    cellsSolved.append(self._sudoku[row][column])

        # remove candidates
        for cell in cellsSolved:
            self.RemoveCandidatesInColumnForNumber( cell.Column, cell.Number)
            self.RemoveCandidatesInRowForNumber( cell.Row, cell.Number)
            self.RemoveCandidatesInGroupForNumber( cell.Group, cell.Number)

    def SetSinglesColumn(self):
        for column in range( 0, self._dimension):
            singleCandiates = []
            for row in range( 0, self._dimension):
                if not self._sudoku[row][column].Solved:
                    for candidate in self._sudoku[row][column].Candidates:
                        if singleCandiates.count(candidate) == 0:
                            singleCandiates.append(candidate)
            for candidate in singleCandiates:
                count = 0
                firstCell = None
                for row in range( 0, self._dimension):
                    if (not self._sudoku[row][column].Solved) and candidate in self._sudoku[row][column].Candidates:
                        count += 1
                        if count==1:
                            firstCell = self._sudoku[row][column] # set first just in case it's the only one
                if count == 1:
                    # got one
                    firstCell.Number = candidate

    def SetSinglesRow(self):
        for row in range( 0, self._dimension):
            singleCandiates = []
            for column in range( 0, self._dimension):
                if not self._sudoku[row][column].Solved:
                    for candidate in self._sudoku[row][column].Candidates:
                        if singleCandiates.count(candidate) == 0:
                            singleCandiates.append(candidate)
            for candidate in singleCandiates:
                count = 0
                firstCell = None
                for column in range( 0, self._dimension):
                    if (not self._sudoku[row][column].Solved) and candidate in self._sudoku[row][column].Candidates: 
                        count += 1
                        if count==1:
                            firstCell = self._sudoku[row][column]  # set first just in case it's the only one
                if count == 1:
                    # got one
                    firstCell.Number = candidate

    def SetSinglesGroup(self):
        for group in range( 0, self._dimension):
            singleCandiates = []
            for cell in self._groups[group]:
                if not cell.Solved:
                    for candidate in cell.Candidates:
                        if singleCandiates.count(candidate) == 0:
                            singleCandiates.append(candidate)
            for candidate in singleCandiates:
                count = 0
                firstCell = None
                for cell in self._groups[group]:
                    if (not cell.Solved) and candidate in cell.Candidates:
                        count += 1
                        if count==1:
                            firstCell = cell  # set first just in case it's the only one
                if count == 1:
                    # got one
                    firstCell.Number = candidate

    def SetSingles(self):
        self.SetSinglesRow()
        self.SetSinglesColumn()
        self.SetSinglesGroup()        
