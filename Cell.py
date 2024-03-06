from sty import fg, bg, ef, rs
import math

class Cell:
    def __init__(self, d, r, c, g, colours):
        self._number=0 # 0 means not solved, 1 - n means solved
        self._dimension = d # 9=3x3, 16=4x4, 25=5x5 ...
        self._row=r    # row and column are 0 based
        self._column=c
        self._group=g  # group is shape index, 0 to d-1, the number belongs to
        self._colours = colours
        self._candidates = []
        for i in range(0, self._dimension):
            self._candidates.append(i+1)

    @property
    def Number(self):
        return self._number

    @Number.setter
    def Number(self, n):
        if 0 < n and n <= self._dimension:
            self._number = n
            # clear list of candidates and set the only one
            self._candidates.clear()            
            for i in range(0, self._dimension):
                self._candidates.append(0)
            self._candidates[n-1] = n
        else:
            raise ValueError

    @property
    def Solved(self):
        return self._number != 0

    @property
    def Row(self):
        return self._row

    @property
    def Column(self):
        return self._column
    
    @property
    def Group(self):
        return self._group
    
    @property
    def Candidates(self):
        result = []
        if not self.Solved:            
            for candidate in self._candidates:
                if candidate != 0:
                    result.append(candidate)
        return result

    def Remove(self, number): # argument is the number to remove 1 based
        if 0 < number and number <= self._dimension:
            if not self.Solved:
                self._candidates[number-1]=0
                if self._candidates.count(0) == self._dimension-1:
                    # only one candidate left, set cell solved with the number left
                    for n in self._candidates:
                        if n != 0:
                            self._number = n
                            break
        else:
            raise ValueError

    def Print(self): # Prints n lines per cell with n candidates per line from 1 to dimension, n=sqrt(dimension)
        strings = []
        rho = round(math.sqrt(self._dimension))
        for i in range(rho):
            string = ""
            # TODO refactor to one loop
            if self._number != 0:
                for j in range(rho):
                    if i == round(rho/2)-1 and j == round(rho/2)-1: # center
                        strcan = fg.black + ef.bold + str(self._number) + ef.rs + fg.rs
                    else:
                        strcan= fg.black + " "  + fg.rs # TODO doesn't work for dimensions greater than 9
                    string = string + " " + strcan + " "
            else:
                for j in range(rho):
                    cand = self._candidates[i*rho + j]
                    if cand != 0:
                        strcan = str(self._candidates[i*rho + j])
                    else:
                        strcan= fg.black + " "  + fg.rs# TODO doesn't work for dimensions greater than 9
                    string = string + " " + strcan + " "
            if i < rho-1:
                strings.append( self._colours.Colour(self._group) + string + bg.rs)
            else:
                strings.append( self._colours.Colour(self._group) + ef.underl + string + ef.rs + bg.rs)
                
        return strings
