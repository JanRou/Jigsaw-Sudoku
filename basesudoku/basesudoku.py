import math

class BaseSudoku:
    def __init__(self, dimension, createCell, type):
        self.dimension = dimension # = rho*rho
        self.type = type # Enumeration: ('Normal', 'Jigsaw', 'Hyper', 'Samurai', 'X' )
        self.sudoku = []  # the sudoku arranged by rows and columns
        self.groups = []  # the soudoku arranged by groups
        for g in range( 0, dimension):
            self.groups.append([])
        for r in range( 0, self.dimension):
            row = []            
            for c in range( 0, self.dimension):
                cell = createCell(self.dimension, r, c)
                self.groups[cell.Group].append(cell)
                row.append( cell )
            self.sudoku.append(row)

    @property
    def Dimension(self):
        return self.dimension
    
    @property
    def Type(self):
        return self.type
    
    @property
    def Solved(self):
        result = True
        for r in range(self.dimension):
            for c in range(self.dimension):
                result = result and self.sudoku[r][c].Solved
                if not result:
                    break
            if not result:
                break
        return result
    
    @property
    def Changed(self):
        result = False
        for r in range(self.dimension):
            for c in range(self.dimension):
                result = result or self.sudoku[r][c].Changed
                if result:
                    break
            if result:
                break
        return result

    def DoChange(self):
        for r in range(self.dimension):
            for c in range(self.dimension):
                self.sudoku[r][c].DoChange()

    def SetSingleCandidatesAsnewNumber(self):
        for row in range( 0, self.dimension):
            for col in range( 0, self.dimension):
                self.sudoku[row][col].SetSingleCandidateToNewNumber()

    def GetCell(self, r, c):
        return self.sudoku[r][c]

    def SetCell(self, r, c, cell):
        self.sudoku[r][c] = cell

    @property
    def Sudoku(self):
        return self.sudoku

    @property
    def Groups(self):
        return self.groups
    
    def Set( self, row, col, number, isInitial=False):
        self.sudoku[row][col].SetNumber(number, isInitial)

    def Get( self, row, col):
        return self.sudoku[row][col].Number

    def RemoveCandidatesInColumnForNumber( self, column, number):
        # remove candidates in column
        for row in range( 0, self.dimension):
            self.sudoku[row][column].Remove(number)        

    def RemoveCandidatesInRowForNumber( self, row, number):
        # remove candidates in column
        for column in range( 0, self.dimension):
            self.sudoku[row][column].Remove(number)        

    def RemoveCandidatesInGroupForNumber( self, group, number):
        # remove candidates in group for normal, jigsaw and samurai sudoku
        for cell in self.groups[group]:
            cell.Remove(number)

    def FindPossibleCandidatesBase(self, removeCandidatesHook):
        # find solved
        cellsSolved = []
        for row in range( 0, self.dimension):
            for column in range( 0, self.dimension):
                if self.sudoku[row][column].Solved:
                    cellsSolved.append(self.sudoku[row][column])

        # remove candidates
        for cell in cellsSolved:
            self.RemoveCandidatesInColumnForNumber( cell.Column, cell.Number)
            self.RemoveCandidatesInRowForNumber( cell.Row, cell.Number)
            removeCandidatesHook( cell ) # remove from square, cross, group or other formation

    def FindSinglesColumn(self):
        for column in range( 0, self.dimension):
            singleCandidates = [] # list of unique candidates in the column
            for row in range( 0, self.dimension):
                singleCandidates = self.sudoku[row][column].AppendSingleCandidates(singleCandidates)
            for candidate in singleCandidates:
                count = 0
                firstCell = None
                for row in range( 0, self.dimension):
                    count, firstCell = self.sudoku[row][column].CountAndSetFirstCellForSingleCandidate(candidate, count, firstCell)
                if count == 1:
                    # The candidate only appears in one cell for the column.
                    firstCell.Number = candidate

    def FindSinglesRow(self):
        for row in range( 0, self.dimension):
            singleCandidates = []
            for column in range( 0, self.dimension):
                singleCandidates = self.sudoku[row][column].AppendSingleCandidates(singleCandidates)
            for candidate in singleCandidates:
                count = 0
                firstCell = None
                for column in range( 0, self.dimension):
                    count, firstCell = self.sudoku[row][column].CountAndSetFirstCellForSingleCandidate(candidate, count, firstCell)
                if count == 1:
                    # The candidate only appears in one cell for the row.
                    firstCell.Number = candidate

    def FindSinglesGroup(self):
        for group in self.Groups:
            singleCandidates = []
            for cell in group:
                singleCandidates = cell.AppendSingleCandidates(singleCandidates)
            for candidate in singleCandidates:
                count = 0
                firstCell = None
                for cell in group:
                    count, firstCell = cell.CountAndSetFirstCellForSingleCandidate(candidate, count, firstCell)
                if count == 1:
                    # The candidate only appears in one cell for the group.
                    firstCell.Number = candidate

    def FindSinglesBase(self, setSinglesHook):
        self.FindSinglesRow()
        self.FindSinglesColumn()
        setSinglesHook()