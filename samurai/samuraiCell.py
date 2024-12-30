from basesudoku.basecell import BaseCell

class SamuraiCell(BaseCell):
    def __init__(self, dim, row, col, group):
        super().__init__(dim, row, col, group)
        self.SetShared(None)

    def SetShared(self, shared):
        self.shared = shared
        self.hasShared = self.shared is not None
   
    @property
    def Number(self):
        return BaseCell.Number
    
    @Number.setter
    def Number(self, n):
        self.Number = n
        if self.hasShared:
            self.shared.SetSharedNumber(n)
    
    def SetSharedNumber(self, n):
        self.number = n

    def SetSingleCandidateToNewNumber(self):
        BaseCell.SetSingleCandidateToNewNumber(self)
        if self.hasShared:
            self.shared.SharedSetSingleCandidateToNewNumber()

    def ShareedSetSingleCandidateToNewNumber(self):
        BaseCell.SetSingleCandidateToNewNumber(self)

    def DoChange(self):
        BaseCell.DoChange(self)
        if self.hasShared:
            self.shared.SharedDoChange()

    def SharedDoChange(self):
        BaseCell.DoChange(self)

    def Remove(self, candidateToRemove):
        BaseCell.Remove(self, candidateToRemove)
        if self.hasShared:
            self.shared.SharedRemove(candidateToRemove)

    def SharedRemove(self, candidateToRemove):
        BaseCell.Remove(self, candidateToRemove)

