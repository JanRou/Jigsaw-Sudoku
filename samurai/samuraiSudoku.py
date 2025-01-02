from basesudoku.basesudoku import BaseSudoku
from samurai.samuraiCell import SamuraiCell
import math
import functools

class SamuraiSudoku():
    def __init__(self, dimension, grid):
        # grid can be 5 for normal samurai 2x2+(2-1)^2
        # TODO 8 for super samurai 3x2+3-1
        # TODO or 13 for 3x3+(3-1)^2
        # TODO grids = [5,8,13]
        grids = [5]
        if not grid in grids:
            raise ValueError("Samurai grid not supported. Grid of 5 is supported: " + grid)
        self.sudokus = []
        self.dimension = dimension
        self.grid = grid
        self.state = 0        
        self.rho = round(math.sqrt(self.dimension)) 
        # Create grid sudokus
        for s in range(grid):
            sudoku = BaseSudoku(dimension, self.createCell)
            self.sudokus.append(sudoku)
        # TODO Set shared cells for all grids
        # Set upper left corner cells of sudoku 2 in the middle to be shared with sudoku 0 lower right corner        
        self.SetSharedCells(self.sudokus[2].Sudoku, 0, 0, self.sudokus[0].Sudoku, self.rho, self.rho)
        # Set upper right corner cells of sudoku 2 in the middle to be shared with sudoku 1 lower left corner
        self.SetSharedCells(self.sudokus[2].Sudoku, 0, self.rho, self.sudokus[1].Sudoku, self.rho, 0 )
        # Set lower left corner cells of sudoku 2 in the middle to be shared with sudoku 3 upper right corner
        self.SetSharedCells(self.sudokus[2].Sudoku, self.rho, 0, self.sudokus[3].Sudoku, 0, self.rho )
        # Set lower right corner cells of sudoku 2 in the middle to be shared with sudoku 4 upper left corner
        self.SetSharedCells(self.sudokus[2].Sudoku, self.rho, self.rho, self.sudokus[4].Sudoku, 0, 0 )

    def SetSharedCells(self, sudokuInMiddle, baseRowMiddle, baseColMiddle, sudokuLeaf, baseRow, baseCol):
        for r in range(self.rho):
            for c in range(self.rho):
                cellMiddle =  sudokuInMiddle[r+baseRowMiddle][c+baseColMiddle]
                cell = sudokuLeaf[r+baseRow][c+baseCol]
                cellMiddle.SetShared(cell)
                cell.SetShared(cellMiddle)

    def createCell(self, dim, rw, cl):        
        group = (rw//self.rho)*self.rho + (cl//self.rho) # upper left square is indexed 0, next to the right 1, and so forth.
        cell = SamuraiCell( dim, rw, cl, group)      
        return cell

    @property
    def Dimension(self):
        return self.dimension

    @property
    def Grid(self):
        return self.grid

    @property
    def Solved(self):
        result = True
        for sudoku in self.sudokus:
            result = result and sudoku.Solved
            if not result:
                break
        return result
    
    @property
    def Changed(self):
        result = False
        for sudoku in self.sudokus:
            result = result or sudoku.Changed
            if result:
                break
        return result

    def DoChange(self):
        for sudoku in self.sudokus:
            sudoku.DoChange()

    def SetSingleCandidatesAsnewNumber(self):
        for sudoku in self.sudokus:
            sudoku.SetSingleCandidatesAsnewNumber()

    @property
    def Sudoku(self):
        return self.sudokus
    
    def Set( self, sudokuIndex, row, col, number):
        self.sudokus[sudokuIndex].Sudoku[row][col].Number = number

    def RemoveCandidatesHook( self, cellWithCandidate, sudoku):
        sudoku.RemoveCandidatesInGroupForNumber(cellWithCandidate.group, cellWithCandidate.Number)
    
    def makeRemoveCandidatesHook( self, sudoku):
        return functools.partial(self.RemoveCandidatesHook, sudoku=sudoku)

    def FindPossibleCandidates(self):
        for sudoku in self.sudokus:
            removeCandidatesHook = self.makeRemoveCandidatesHook(sudoku)
            sudoku.FindPossibleCandidatesBase(removeCandidatesHook)
            # TODO this is standard base sudoku rule. Samurai rule is different for shared corners

    def SetSinglesGroup(self, sudoku):
        sudoku.FindSinglesGroup()  # uses standard base hook

    def makeSetSinglesGroup( self, sudoku):
        return functools.partial(self.SetSinglesGroup, sudoku=sudoku)

    def SetSingles(self):
        for sudoku in self.sudokus:
            setSinglesHook = self.makeSetSinglesGroup(sudoku)
            sudoku.FindSinglesBase(setSinglesHook)
            # TODO this is standard base sudoku rule. Samurai rule is different for shared corners

    def GetState(self):
        return self.state
    
    def TakeStep(self):
        # TODO add more rules and more states
        self.steps = { 0: 'Find single candidate as solution', 1: 'Find possible candidates'
                , 2: 'Find single candidate in row, column and group', 3: 'Update sudoku'
                , 4: "Done, solved"}
        if not self.Solved:
            result = self.steps[self.state]
            match self.state:
                case 0:
                    self.SetSingleCandidatesAsnewNumber()
                    if self.Changed:
                        result = result + ", yes"
                        self.state = 3
                    else:
                        result = result + ", no"
                        self.state = 1
                case 1:
                    self.FindPossibleCandidates()
                    if self.Changed:
                        result = result + ", yes"
                        self.state = 3
                    else:
                        result = result + ", no"
                        self.state = 2
                case 2:
                    self.SetSingles()
                    if self.Changed:
                        result = result + ", yes"
                        self.state = 3
                    else:
                        result = result + ", no"
                    self.state = 3
                case 3:
                    self.DoChange()
                    self.state = 0
        else:
            result = self.steps[4]

        return result
   