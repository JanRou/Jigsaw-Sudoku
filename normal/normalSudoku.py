from basesudoku.basesudoku import BaseSudoku
from basesudoku.basecell import BaseCell
import math

class NormalSudoku(BaseSudoku):
    def __init__(self, dimension):
        self.state = 0
        super().__init__(dimension, self.createCell, 'Normal')

    def createCell(self, dim, rw, cl):
        rho = round(math.sqrt(self.dimension))
        group = (rw//rho)*rho + (cl//rho) # upper left square is indexed 0, next to the right 1, and so forth.
        cell = BaseCell( dim, rw, cl, group)
        return cell    
       
    def GetState(self):
        return self.state
    
    def RemoveCandidatesHook( self, cell):
        # Common with JigSaw
        self.RemoveCandidatesInGroupForNumber( cell.Group, cell.Number)

    def FindPossibleCandidates(self):
        # Common with JigSaw
        self.FindPossibleCandidatesBase(self.RemoveCandidatesHook)

    def SetSingles(self):
        self.FindSinglesBase(self.FindSinglesGroup) # uses standard base hook

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
   