from basesudoku.basesudoku import BaseSudoku
from basesudoku.basecell import BaseCell
import math

class NormalSudoku(BaseSudoku):
    def __init__(self, dimension):
        self.state = 0
        super().__init__(dimension, self.createCell)

    def createCell(self, dim, rw, cl):
        rho = round(math.sqrt(self.dimension))
        group = (rw//rho)*rho + (cl//rho) # upper left square is indexed 0, next to the right 1, and so forth.
        cell = BaseCell( dim, rw, cl, group)
        return cell    
       
    def GetState(self):
        return self.state
    
    def RemoveCandidatesInGroupForNumber( self, group, number):
        # Common with JigSaw
        # remove candidates in group
        for cell in self.groups[group]:
            cell.Remove(number)

    def RemoveCandidatesHook( self, cell):
        # Common with JigSaw
        self.RemoveCandidatesInGroupForNumber( cell.Group, cell.Number)

    def FindPossibleCandidates(self):
        # Common with JigSaw
        self.FindPossibleCandidatesBase(self.RemoveCandidatesHook)

    def SetSinglesGroup(self):
        # Common with JigSaw
        for group in range( 0, self.dimension):
            singleCandidates = []
            for cell in self.groups[group]:
                singleCandidates = cell.AppendSingleCandidates(singleCandidates)
            for candidate in singleCandidates:
                count = 0
                firstCell = None
                for cell in self.groups[group]:
                    count, firstCell = cell.CountAndSetFirstCellForSingleCandidate(candidate, count, firstCell)
                if count == 1:
                    # The candidate only appears in one cell for the group.
                    firstCell.Number = candidate

    def SetSingles(self):
        self.FindSinglesBase(self.SetSinglesGroup)

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
   