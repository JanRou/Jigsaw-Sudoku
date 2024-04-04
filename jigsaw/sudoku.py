import math
from sty import fg, bg, ef, rs
from jigsaw.cell import JigsawCell

class BaseSudoku:
    def __init__(self, d, createCell):
        self._dimension = d
        self._sudoku = []  # the sudoku arranged by rows an columns
        for rw in range( 0, self._dimension):
            row = []            
            for col in range( 0, self._dimension):
                cell = createCell(self._dimension, rw, col)
                row.append( cell )
            self._sudoku.append(row)

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

    def GetCell(self, r, c):
        return self._sudoku[r][c]

    @property
    def Sudoku(self):
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

    def Get( self, r, c):
        return self._sudoku[r][c].Number

    def RemoveCandidatesInColumnForNumber( self, column, number):
        # remove candidates in column
        for row in range( 0, self._dimension):
            self._sudoku[row][column].Remove(number)        

    def RemoveCandidatesInRowForNumber( self, row, number):
        # remove candidates in column
        for column in range( 0, self._dimension):
            self._sudoku[row][column].Remove(number)        

    def SetPossibleCandidateBase(self, removeCandidatesHook):
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
            removeCandidatesHook( cell )

    def SetSinglesColumn(self):
        for column in range( 0, self._dimension):
            singleCandidates = []
            for row in range( 0, self._dimension):
                if not self._sudoku[row][column].Solved:
                    for candidate in self._sudoku[row][column].Candidates:
                        if singleCandidates.count(candidate) == 0:
                            singleCandidates.append(candidate)
            for candidate in singleCandidates:
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
            singleCandidates = []
            for column in range( 0, self._dimension):
                if not self._sudoku[row][column].Solved:
                    for candidate in self._sudoku[row][column].Candidates:
                        if singleCandidates.count(candidate) == 0:
                            singleCandidates.append(candidate)
            for candidate in singleCandidates:
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

    def SetSinglesBase(self, setSinglesHook):
        self.SetSinglesRow()
        self.SetSinglesColumn()
        setSinglesHook()


class JigsawSudoku(BaseSudoku): # TODO inherit from BaseSudoku
    def __init__(self, d, shape, colours): 
        # d is dimension of sudoku, usually 4, 9, 16, 25 ...
        # shape is d=nxn row and columns with group indexes 0 based, n=sqrt(d), 
        # where 0 is first group at upper left corner and n is last
        self._shape = shape
        self._colours = colours
        self._groups = []  # the soudoku arranged by groups
        for rw in range( 0, d):
            self._groups.append([])        
        super().__init__(d, self.createCell)
        shapeCheck = self.CheckShape(shape) # returns tuple (bool, message)
        if not shapeCheck[0]:
            raise ValueError("Shape check failed: " + shapeCheck[1])
        self.steps = {0:"set possible", 1: "set single candidate row", 2: "set single candidate column"
        , 3: "set single candidate group"}
        self.state = 0

    # implements abstract method in base class
    def createCell(self, d, rw, col):
        cell = JigsawCell( d, rw, col, self._shape[rw][col], self._colours)
        self._groups[self._shape[rw][col]].append(cell)
        return cell

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
    
    def GetState( self):
        return self.state

    def GetGroup( self, r, c):
        return self._sudoku[r][c].Group

    def RemoveCandidatesInGroupForNumber( self, group, number):
        # remove candidates in group
        for cell in self._groups[group]:
            cell.Remove(number)

    def RemoveCandidatesHook( self, cell):
        self.RemoveCandidatesInGroupForNumber( cell.Group, cell.Number)

    def SetPossibleCandidate(self):
        self.SetPossibleCandidateBase(self.RemoveCandidatesHook)

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
        self.SetSinglesBase(self.SetSinglesGroup)
        
    def TakeStep(self):
        if not self.Solved:
            self.DoChange()
            match self.state:
                case 0:
                    self.SetPossibleCandidate()
                    if self.Changed:
                        self.state = 0
                    else:
                        self.state = 1
                case 1:
                    self.SetSinglesRow()
                    if self.Changed:
                        self.state = 0
                    else:
                        self.state = 2
                case 2:
                    self.SetSinglesColumn()
                    if self.Changed:
                        self.state = 0
                    else:
                        self.state = 3
                case 3:
                    self.SetSinglesGroup()
                    self.state = 0
