import tkinter as tk
from tkinter import ttk
from tkinter import font
from jigsaw.jigsawSudoku import JigsawSudoku
import math

class JigsawWindow(tk.Toplevel):
    def __init__(self, parent, sudoku):
        super().__init__(parent)
        self.title("Jigsaw Sudoku Solver")
        self.minsize( 400,400)
        self.maxsize( 1000,1200)
        self.geometry("1000x600+50+50")
        
        self.mainFrame = ttk.Frame( self, width=1000, height=600)
        self.mainFrame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.sudoku = sudoku        
        self.leftFrame = LeftFrame( self, 200, 600, self.step)
        self.rightFrame = RightFrame( self, 600, 600, sudoku, CellColours() )

    def step(self):
        result = self.sudoku.TakeStep()
        self.rightFrame.show()
        self.leftFrame.showResult(result)
        print(result)

class LeftFrame(ttk.Frame):
    def __init__(self, root, w, h, step):
        super().__init__( root, width=w, height=h )
        self.grid(row=0, column=0, padx=10, pady=5, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.headLabel=ttk.Label( self, text="Solve jigsaw sudoku")
        self.headLabel.grid(row=0, column=0, padx=5, pady=5)

        self.button = ttk.Button( self, text="Next step >", command=self.takeNextStep)
        self.button.grid(row=1, column=0, padx=5, pady=5)
        
        # Listbox
        self.results = ["Test"]
        self.resultsVar = tk.StringVar(value=self.results)    
        self.listbox = tk.Listbox( self, listvariable=self.resultsVar, height=20, width= 50)         
        self.listbox.grid(row=2, column=0, padx=5, pady=5)

        # Scrollbar to listbox
        self.scrollbar = tk.Scrollbar(self, orient="vertical")
        self.scrollbar.grid(row=2, column=1, sticky=(tk.NS)) 
        self.listbox.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.listbox.yview) 

        self.step = step

    def takeNextStep(self):
        self.step()

    def showResult(self, result):
        self.results.append(result)
        self.resultsVar.set(self.results)
        self.listbox.see("end")

class RightFrame(ttk.Frame):
    def __init__(self, root, w, h, sudoku, colours):
        super().__init__( root, width=w, height=h)
        self.grid(row=0, column=1, padx=10, pady=5, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.sudoku = sudoku
        self.colours = colours
        self.sudokuView = []        
        # TODO bindings for MVC
        for row in range(self.sudoku.Dimension):
            rowView = []
            for col in range(self.sudoku.Dimension):                
                cell = self.sudoku.GetCell(row,col)
                cellView = SudokuCellView(self, self.colours.get(cell.Group), cell)
                cellView.Show()
                cellView.grid( row=row, column=col, padx=5, pady=5, ipadx=10, ipady=10) 
                rowView.append(cellView)
            self.sudokuView.append(rowView)

    def show(self):
        for row in self.sudokuView:
            for cellView in row:
                cellView.Show()        
    
class CellColours:
    def __init__(self):
        self.colours = []
        self.colours.append("#FF7F7F") # 0 light red
        self.colours.append("#7FFF7F") # 1 light green
        self.colours.append("#EF7FFF") # 2 light violet
        self.colours.append("#FFFF7F") # 3 light orange
        self.colours.append("#7FFFFF") # 4 light 
        self.colours.append("#FF7F1F") # 5 light 
        self.colours.append("#FFEFBF") # 6 light 
        self.colours.append("#FFCF1F") # 7 light 
        self.colours.append("#EFFFEF") # 8 light 
    
    def get(self, g):
        return self.colours[g]

class SudokuCellView(tk.Canvas):
    def __init__(self, root, bgcolour, cell, **kwargs):
        super().__init__( root, width=30, height=30, background=bgcolour, **kwargs)
        self.cell = cell
        self.candidatesFont =  font.Font(family='Helvetica', size=10)
        self.finalFont =  font.Font(family='Helvetica', size=16, )
        self.rho = round(math.sqrt(cell.Dimension)) # rho x rho dimension of cell = 2, 3, 4 ...

    def Show(self):
        self.delete('all')
        if self.cell.Solved:
            # display final number in black in center
            self.create_text( 20, 15 , text=str(self.cell.Number), anchor='nw', font=self.finalFont, fill='black')
        elif self.cell.Changed and self.cell.NewNumber != 0:
            self.create_text( 20, 15 , text=str(self.cell.NewNumber), anchor='nw', font=self.finalFont, fill='lightblue')
        else:
            candidates = self.cell.Candidates
            if self.cell.Changed:
                candidates = self.cell.NewCandidates
            for i in range(self.rho):
                for j in range(self.rho):
                    c = i*self.rho + j + 1
                    if c in candidates:
                        self.create_text( 15*i + 8, 15*j + 5 , text=str(c), anchor='nw', font=self.candidatesFont, fill='black')
