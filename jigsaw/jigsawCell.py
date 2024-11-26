from basesudoku.basecell import BaseCell
from sty import fg, bg, ef, rs
import math

class JigsawCell(BaseCell):
    def __init__(self, dim, row, col, group, colours):
        super().__init__( dim, row, col, group)
        self.group=group 
        self.colours = colours
    
