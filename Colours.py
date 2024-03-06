from sty import fg, bg, ef, rs

class Colours:
    def __init__(self):
        self._colours = [bg.blue, bg.grey, bg.red, bg.green, bg.cyan, bg.yellow, bg.magenta, bg(255, 150, 50), bg(150, 150, 250), bg.li_red, bg.li_green, bg.li_cyan, bg.li_yellow, bg.li_magenta, bg.white ]

    def Colour(self, ix):
        if ix < len(self._colours):
            return self._colours[ix]
        else:
            return bg.black
