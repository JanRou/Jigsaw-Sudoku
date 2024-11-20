from basesudoku.basecell import BaseCell
from sty import fg, bg, ef, rs
import math

class JigsawCell(BaseCell):
    def __init__(self, d, r, c, g, colours):
        super().__init__( d, r, c)
        self._group=g  # group is shape index, 0 to d-1, the number belongs to
        self._colours = colours
    
    @property
    def Group(self):
        return self._group
    
    # For debug of sudoku solving
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
                    # Is the candidate in position i,j present?
                    if (i*rho + j + 1) in self._candidates:
                        cand = i*rho + j + 1
                    else:
                        cand = 0
                    if cand != 0:
                        strcan = str(cand)
                    else:
                        strcan= fg.black + " " + fg.rs# TODO doesn't work for dimensions greater than 9
                    string = string + " " + strcan + " "
            if i < rho-1:
                strings.append( self._colours.Colour(self._group) + string + bg.rs)
            else:
                strings.append( self._colours.Colour(self._group) + ef.underl + string + ef.rs + bg.rs)
                
        return strings