
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

    def FindSinglesRow(self):
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

    def FindSinglesBase(self, setSinglesHook):
        self.FindSinglesRow()
        self.FindSinglesColumn()
        setSinglesHook()
