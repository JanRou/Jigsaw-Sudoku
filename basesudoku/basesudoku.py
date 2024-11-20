import math

class BaseSudoku:
    def __init__(self, d, createCell):
        self._dimension = d
        self._sudoku = []  # the sudoku arranged by rows and columns
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

    def SetSingleCandidatesAsnewNumber(self):
        for row in range( 0, self._dimension):
            for col in range( 0, self._dimension):
                self._sudoku[row][col].SetSingleCandidateToNewNumber()

    def GetCell(self, r, c):
        return self._sudoku[r][c]

    @property
    def Sudoku(self):
        return self._sudoku

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

    def FindPossibleCandidatesBase(self, removeCandidatesHook):
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
            removeCandidatesHook( cell ) # remove from square, cross, group or other formation

    def FindSinglesColumn(self):
        for column in range( 0, self._dimension):
            singleCandidates = [] # list of unique candidates in the column
            for row in range( 0, self._dimension):
                singleCandidates = self._sudoku[row][column].AppendSingleCandidates(singleCandidates)
            for candidate in singleCandidates:
                count = 0
                firstCell = None
                for row in range( 0, self._dimension):
                    count, firstCell = self._sudoku[row][column].CountAndSetFirstCellForSingleCandidate(candidate, count, firstCell)
                if count == 1:
                    # The candidate only appears in one cell for the column.
                    firstCell.Number = candidate

    def FindSinglesRow(self):
        for row in range( 0, self._dimension):
            singleCandidates = []
            for column in range( 0, self._dimension):
                singleCandidates = self._sudoku[row][column].AppendSingleCandidates(singleCandidates)
            for candidate in singleCandidates:
                count = 0
                firstCell = None
                for column in range( 0, self._dimension):
                    count, firstCell = self._sudoku[row][column].CountAndSetFirstCellForSingleCandidate(candidate, count, firstCell)
                if count == 1:
                    # The candidate only appears in one cell for the row.
                    firstCell.Number = candidate

    def FindSinglesBase(self, setSinglesHook):
        self.FindSinglesRow()
        self.FindSinglesColumn()
        setSinglesHook()

    # For debug of sudoku solving
    def Print(self):
        rho = round(math.sqrt(self._dimension))
        for r in range( 0, self._dimension):
            strings = []
            for i in range(rho):
                strings.append("")
            for c in range( 0, self._dimension):
                cellStrings = self._sudoku[r][c].Print()
                for i in range(rho):
                    strings[i] = strings[i] + cellStrings[i]
            for i in range(rho):
                print( strings[i] )
