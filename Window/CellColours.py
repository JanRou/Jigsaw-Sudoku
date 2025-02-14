class CellColours:
    def __init__(self):
        self.colours = []
        self.colours.append("#FF7F7F") # 0 light red
        self.colours.append("#7FFF7F") # 1 light green
        self.colours.append("#EF7FFF") # 2 light violet
        self.colours.append("#FFFF7F") # 3 light yellow
        self.colours.append("#7FFFFF") # 4 light cyan
        self.colours.append("#FF7F1F") # 5 orange
        self.colours.append("#FFEFBF") # 6 light sand
        self.colours.append("#FFCF1F") # 7 yellow
        self.colours.append("#EFFFEF") # 8 very light green

    def get(self, g):
        return self.colours[g]