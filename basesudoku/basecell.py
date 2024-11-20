import math

class BaseCell:
    def __init__(self, d, r, c):
        self._number = 0 # 0 means not solved, 1 - n means solved
        self._dimension = d # 4=2x2, 9=3x3, 16=4x4, 25=5x5 ...
        self._row=r    # row and column are 0 based
        self._column=c
        self._candidates = []
        self._changed = False
        self._newNumber = 0 # new number when changed
        self._newCandidates = [] # new candidates when changed
        for c in range(1, 1+self._dimension):
            self._candidates.append(c)

    @property
    def Dimension(self):
        return self._dimension

    @property
    def Row(self):
        return self._row

    @property
    def Column(self):
        return self._column

    @property
    def Number(self):
        return self._number

    @Number.setter
    def Number(self, n):
        # Assigning to Number means the cell is marked changed and newNumber holds the solution for cell
        if 0 < n and n <= self._dimension:
            self._newNumber = n
            # clear list of candidates and set the only one
            self._candidates.clear()            
            for i in range(0, self._dimension):
                self._candidates.append(0)
            self._candidates[n-1] = n
            self._changed = True
        else:
            raise ValueError

    @property
    def Solved(self):
        return self._number != 0
    
    @property
    def Changed(self):
        return self._changed

    @property
    def NewNumber(self):
        result = 0
        if self._changed:
            result = self._newNumber
        return result

    def DoChange(self):
        # Sets the solution, when newNumber holds a solution and clears list of candidates
        # Clears temporary variables newNumber and newCandidates and changed flag
        if self._newNumber != 0:
            self._number = self._newNumber
            self._candidates = []
        if self._newCandidates != []:
            self._candidates = self._newCandidates
        self._newCandidates = []
        self._newNumber = 0
        self._changed = False

    def SetSingleCandidateToNewNumber(self):
        if len(self._candidates) == 1:
            # only one candidate left, set cell newNumber and flag changed
            for n in self._candidates:
                if n != 0:
                    self._newNumber = n
                    self._changed = True
                    break
                else:
                    raise ValueError
    @property
    def Row(self):
        return self._row

    @property
    def Column(self):
        return self._column

    @property
    def Candidates(self):
        result = []
        if not self.Solved:            
            result = self._candidates
        return result

    @property
    def NewCandidates(self):
        result = []
        for newCandidate in self._newCandidates:
            if newCandidate != 0:
                result.append(newCandidate)
        return result

    def Remove(self, candidateToRemove):
        if 0 < candidateToRemove and candidateToRemove <= self._dimension:
            if not self.Solved:
                if not self._changed:
                    self._newCandidates = self._candidates.copy()
                if candidateToRemove in self._newCandidates:
                    self._changed = True
                    self._newCandidates.remove(candidateToRemove)
        else:
            raise ValueError
        
    def AppendSingleCandidates(self, singleCandidates):
        # Append new single candidates in the cell to the list of single candidates
        # Don't append when already solved.
        if not self.Solved:
            # Find unique singleCandidates from candidates, when cell isn't changed,
            # otherwise use newCandidates, because another FindSingles algorithm
            # may have changed the candidates to a single candidate.
            candidates = self._candidates
            if self._changed:
                candidates = self._newCandidates
            for candidate in candidates:
                if singleCandidates.count(candidate) == 0:
                    singleCandidates.append(candidate)
        return singleCandidates
    
    def CountAndSetFirstCellForSingleCandidate(self, singleCandidate, count, firstCell):
        # Jump over solved cells.
        candidates = self._candidates
        if self._changed:
            candidates = self._newCandidates
        if (not self.Solved) and singleCandidate in candidates:
            count += 1
            if count==1:
                firstCell = self  # return this as first just in case it's the only one
        return (count, firstCell)
    


    


