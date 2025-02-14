import tkinter as tk
from tkinter import ttk

from Window.CellColours import CellColours
from Window.CommonSudokuFrame import CommonSudokuFrame
from Window.ControlFrame import ControlFrame
from Window.SamuraiSudokuFrame import SamuraiSudokuFrame

class Window(tk.Toplevel):
    def __init__(self, parent, title, sudoku):
        super().__init__(parent, relief='solid')
        self.title(title)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.sudoku = sudoku   
        # TODO Refactor        
        if sudoku.Type in ['Normal', 'Jigsaw', 'Hyper', 'X' ]:
            self.minsize( 400,400)
            self.maxsize( 1200, 800)
            self.geometry("1000x600+50+50")
            self.mainFrame = ttk.Frame( self, width=1000, height=600, relief='solid')
            self.mainFrame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
            self.leftFrame = ControlFrame( self.mainFrame, 200, 600, title, self.step)        
            self.rightFrame = CommonSudokuFrame( self.mainFrame, 600, 600, 0, 1, CellColours(), sudoku )
        elif sudoku.Type in ['Samurai']:
            self.minsize( 400,400)
            self.maxsize( 1800, 1400)
            self.geometry("1800x1300+50+50")
            self.mainFrame = ttk.Frame( self, width=1400, height=1300, relief='solid')
            self.mainFrame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
            self.leftFrame = ControlFrame( self.mainFrame, 200, 1300, title, self.step)        
            self.rightFrame = SamuraiSudokuFrame( self.mainFrame, 1800, 1400, CellColours(), sudoku )

    def step(self):
        result = self.sudoku.TakeStep()
        self.rightFrame.show()
        self.leftFrame.showResult(result)
        print(result)

