from tkinter import *
from tkinter import ttk
from tkinter import font

from jigsaw import jigsaw
from normal import normal
from samurai import samurai
from Window.window import Window

class SudokuWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku Solver")
        self.minsize( 100,100)
        self.maxsize( 200,200)
        self.geometry("200x200+50+50")
        self.mainFrame = ttk.Frame( self, width=100, height=100)
        self.mainFrame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.label=ttk.Label( self.mainFrame
                , text="Solve a sudoku").grid(row=0, column=0, padx=5, pady=5)
        
        self.sudokuvar = StringVar()
        self.combo = ttk.Combobox( self.mainFrame, textvariable=self.sudokuvar)
        # TODO self.combo['values'] = ('Normal', 'Jigsaw', 'Hyper', 'X' )
        self.combo['values'] = ('Normal', 'Jigsaw', 'Samurai')
        self.combo.grid(row=1, column=0, padx=5, pady=5)
        self.combo.state(["readonly"])
        self.combo.current(0)        
        runButton = ttk.Button( self.mainFrame, text='Solve', command=self.solvesudoku)
        runButton.grid(row=2, column=0, padx=5, pady=5)

    def solvesudoku(self):
        # call sudoku solver selected
        choice = self.combo.get()
        if choice == "Jigsaw":
            sudoku = jigsaw.createSudoku()
        elif choice == "Normal":
            sudoku = normal.createSudoku()
        elif choice == "Hyper":
            pass
        elif choice == "Samurai":
            sudoku = samurai.createSudoku()
        elif choice == "X":
            pass
        else:
            pass
        window = Window( self, choice, sudoku)
        window.grab_set()


#main
mainWindow = SudokuWindow()
mainWindow.mainloop()
