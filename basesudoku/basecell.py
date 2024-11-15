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
        for i in range(0, self._dimension):
            self._candidates.append(i+1)

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
        if self._newNumber != 0:
            self._number = self._newNumber
            self._candidates = []
        if self._newCandidates != []:
            self._candidates = self._newCandidates
        self._newCandidates = []
        self._changed = False
        self._newNumber = 0

    def SetSingleCandidateToNewNumber(self):
        if len(self._candidates) == 1:
            # only one candidate left, set cell newNumber
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

    def Remove(self, candidate): # argument is the candidate to remove 1 based
        if 0 < candidate and candidate <= self._dimension:
            if not self.Solved:
                if not self._changed:
                    self._newCandidates = self._candidates.copy() # copy unchanged list of candidates with zeros
                if candidate in self._newCandidates:
                    self._changed = True
                    self._newCandidates.remove(candidate)
        else:
            raise ValueError
