from basesudoku.basecell import BaseCell

class JigsawCell(BaseCell):
    def __init__(self, d, r, c, g, colours):
        super().__init__( d, r, c)
        self._group=g  # group is shape index, 0 to d-1, the number belongs to
        self._colours = colours
    
    @property
    def Group(self):
        return self._group
    