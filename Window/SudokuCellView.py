import math
import tkinter as tk
from tkinter import font


class SudokuCellView(tk.Canvas):
    def __init__(self, root, bgcolour, cell, **kwargs):
        super().__init__( root, width=20, height=20, relief='solid',  background=bgcolour, **kwargs)
        self.cell = cell
        self.candidatesFont = font.Font(family='Helvetica', size=7)
        self.finalFont = font.Font(family='Helvetica', size=12, )
        self.rho = round(math.sqrt(cell.Dimension)) # rho x rho dimension of cell = 2, 3, 4 ...

    def show(self):
        self.delete('all')
        if self.cell.Solved:
            # display final number in black in center
            self.create_text( 16, 13 , text=str(self.cell.Number), anchor='nw', font=self.finalFont, fill='black')
        elif self.cell.Changed and self.cell.NewNumber != 0:
            self.create_text( 16, 13 , text=str(self.cell.NewNumber), anchor='nw', font=self.finalFont, fill='lightblue')
        else:
            candidates = self.cell.Candidates
            if self.cell.Changed:
                candidates = self.cell.NewCandidates
            for row in range(self.rho): # y direction for text in canvas
                for col in range(self.rho): # x direction for text in canvas
                    c = row*self.rho + col + 1
                    if c in candidates:
                        self.create_text( 14*col + 5 , 13*row + 4 , text=str(c), anchor='nw', font=self.candidatesFont, fill='black')