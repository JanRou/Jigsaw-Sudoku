import tkinter as tk
from tkinter import ttk
from tkinter import font
import math

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

class ControlFrame(ttk.Frame):
    def __init__(self, root, w, h, title, step):
        super().__init__( root, width=w, height=h, relief='solid')
        self.grid(row=0, column=0, padx=10, pady=5, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.headLabel=ttk.Label( self, text='Solve ' + title + ' sudoku')
        self.headLabel.grid(row=0, column=0, padx=5, pady=5)

        self.button = ttk.Button( self, text="Next step >", command=self.takeNextStep)
        self.button.grid(row=1, column=0, padx=5, pady=5)
        
        # Listbox
        self.results = []
        self.resultsVar = tk.StringVar(value=self.results)    
        self.listbox = tk.Listbox( self, listvariable=self.resultsVar, height=30, width= 50)         
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

class CommonSudokuFrame(ttk.Frame):
    def __init__(self, root, w, h, gridRow, gridCol, colours, sudoku):
        super().__init__( root, width=w, height=h, relief='solid')
        self.grid(row=gridRow, column=gridCol, padx=10, pady=5, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.sudoku = sudoku
        self.colours = colours
        self.sudokuView = []        
        for row in range(self.sudoku.Dimension):
            rowView = []
            for col in range(self.sudoku.Dimension):                
                cell = self.sudoku.GetCell(row,col)
                cellView = SudokuCellView(self, self.colours.get(cell.Group), cell)
                cellView.Show()
                cellView.grid( row=row, column=col, padx=1, pady=1, ipadx=10, ipady=10) 
                rowView.append(cellView)
            self.sudokuView.append(rowView)

    def show(self):
        for row in self.sudokuView:
            for cellView in row:
                cellView.Show()        

class SamuraiSudokuFrame(ttk.Frame): # only grid=5, dimension=9
    def __init__(self, root, w, h, colours, sudoku):
        super().__init__( root, width=w, height=h, relief='solid')
        self.grid(row=0, column=1, padx=10, pady=5, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.sudokuFrames = []
        sudokuSix = 0
        for sudoku in sudoku.Sudokus:
            if sudokuSix==0:
                gridRow = 0
                gridCol = 0
            elif sudokuSix==1:
                gridRow = 0
                gridCol = 2
            elif sudokuSix==2:
                gridRow = 1
                gridCol = 1
            elif sudokuSix==3:
                gridRow = 2
                gridCol = 0
            elif sudokuSix==4:
                gridRow = 2
                gridCol = 2

            sudokuSix += 1

            sf = CommonSudokuFrame( self, 600, 600, gridRow, gridCol, colours, sudoku)
            self.sudokuFrames.append(sf)

        # self.grid(row=0, column=1, padx=10, pady=5, sticky=(tk.N, tk.W, tk.E, tk.S))
        # self.sudoku = sudoku
        # self.colours = colours
        # self.sudokuView = []        
        # gridDimension = self.sudoku.Dimension*2 + round(math.sqrt(self.dimension))
        # for row in range(gridDimension):
        #     rowView = []
        #     for col in range(gridDimension):
        #         cell = self.sudoku.GetCell(row,col)
        #         cellView = SudokuCellView(self, self.colours.get(cell.Group), cell)
        #         cellView.Show()
        #         cellView.grid( row=row, column=col, padx=5, pady=5, ipadx=10, ipady=10) 
        #         rowView.append(cellView)
        #     self.sudokuView.append(rowView)

    def show(self):
        for sf in self.sudokuFrames:
            sf.show()        

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

class SudokuCellView(tk.Canvas):
    def __init__(self, root, bgcolour, cell, **kwargs):
        super().__init__( root, width=20, height=20, relief='solid',  background=bgcolour, **kwargs)
        self.cell = cell
        self.candidatesFont = font.Font(family='Helvetica', size=7)
        self.finalFont = font.Font(family='Helvetica', size=12, )
        self.rho = round(math.sqrt(cell.Dimension)) # rho x rho dimension of cell = 2, 3, 4 ...

    def Show(self):
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
            for i in range(self.rho):
                for j in range(self.rho):
                    c = i*self.rho + j + 1
                    if c in candidates:
                        self.create_text( 14*i + 5, 13*j + 4 , text=str(c), anchor='nw', font=self.candidatesFont, fill='black')
