import math

class BaseCell:
    def __init__(self, dim, row, col, group):
        self.number = 0 # 0 means not solved, 1 - n means solved
        self.dimension = dim # 4=2x2, 9=3x3, 16=4x4, 25=5x5 ...
        self.row=row    # row and column are 0 based
        self.column=col
        self.changed = False
        self.newNumber = 0 # new number when changed
        self.newCandidates = [] # new candidates when changed
        self.candidates = []
        for col in range(1, 1+self.dimension):
            self.candidates.append(col)
        self.group = group

    @property
    def Dimension(self):
        return self.dimension

    @property
    def Row(self):
        return self.row

    @property
    def Column(self):
        return self.column

    @property
    def Group(self):
        return self.group
    
    @property
    def Number(self):
        return self.number

    @Number.setter
    def Number(self, n): # It doesn't work for inherited class calling base class property?
        self.SetNumber(n)

    def SetNumber(self, n):
        # Assigning to Number means the cell is marked changed and newNumber holds the solution for cell
        if 0 < n and n <= self.dimension:
            self.newNumber = n
            # clear list of candidates and set the only one
            self.candidates.clear()            
            for i in range(0, self.dimension):
                self.candidates.append(0)
            self.candidates[n-1] = n
            self.changed = True
        else:
            raise ValueError

    @property
    def NewNumber(self):
        result = 0
        if self.changed:
            result = self.newNumber
        return result

    @property
    def Solved(self):
        return self.number != 0
    
    @property
    def Changed(self):
        return self.changed

    def DoChange(self):
        # Sets the solution, when newNumber holds a solution and clears list of candidates
        # Clears temporary variables newNumber and newCandidates and changed flag
        if self.newNumber != 0:
            self.number = self.newNumber
            self.candidates = []
        if self.newCandidates != []:
            self.candidates = self.newCandidates
        self.newCandidates = []
        self.newNumber = 0
        self.changed = False

    def SetSingleCandidateToNewNumber(self):
        if len(self.candidates) == 1:
            # only one candidate left, set cell newNumber and flag changed
            for n in self.candidates:
                if n != 0:
                    self.newNumber = n
                    self.changed = True
                    break
                else:
                    raise ValueError

    @property
    def Candidates(self):
        result = []
        if not self.Solved:            
            result = self.candidates
        return result

    @property
    def NewCandidates(self):
        result = []
        for newCandidate in self.newCandidates:
            if newCandidate != 0:
                result.append(newCandidate)
        return result

    def Remove(self, candidateToRemove):
        if 0 < candidateToRemove and candidateToRemove <= self.dimension:
            if not self.Solved:
                if not self.changed:
                    self.newCandidates = self.candidates.copy()
                if candidateToRemove in self.newCandidates:
                    self.changed = True
                    self.newCandidates.remove(candidateToRemove)
        else:
            raise ValueError
        
    def AppendSingleCandidates(self, singleCandidates):
        # Append new single candidates in the cell to the list of single candidates
        # Don't append when already solved.
        if not self.Solved:
            # Find unique singleCandidates from candidates, when cell isn't changed,
            # otherwise use newCandidates, because another FindSingles algorithm
            # may have changed the candidates to a single candidate.
            candidates = self.candidates
            if self.changed:
                candidates = self.newCandidates
            for candidate in candidates:
                if singleCandidates.count(candidate) == 0:
                    singleCandidates.append(candidate)
        return singleCandidates
    
    def CountAndSetFirstCellForSingleCandidate(self, singleCandidate, count, firstCell):
        # Jump over solved cells.
        candidates = self.candidates
        if self.changed:
            candidates = self.newCandidates
        if (not self.Solved) and singleCandidate in candidates:
            count += 1
            if count==1:
                firstCell = self  # return this as first just in case it's the only one
        return (count, firstCell)
    


    


