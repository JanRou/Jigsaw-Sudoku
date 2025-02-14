import tkinter as tk
from tkinter import ttk

from Window.CommonSudokuFrame import CommonSudokuFrame
from Window.SudokuCellView import SudokuCellView

class SamuraiSudokuFrame(ttk.Frame): # only grid=5, dimension=9
    # def __init__(self, root, w, h, colours, sudoku):
    #     super().__init__( root, width=w, height=h, relief='solid')
    #     self.grid(row=0, column=1, padx=10, pady=5, sticky=(tk.N, tk.W, tk.E, tk.S))
    #     self.sudokuFrames = []
    #     sudokusIx = 0
    #     for sudoku in sudoku.Sudokus:
    #         # sf = CommonSudokuFrame( self, 600, 600, gridRow, gridCol, colours, sudoku)
    #         self.sudokuFrames.append(sf)
    #         sudokusIx += 1

    def __init__(self, root, w, h, colours, sudoku):
        super().__init__( root, width=w, height=h, relief='solid')
        self.grid(row=0, column=1, padx=10, pady=5, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.sudokuCells = []
        sudokusIx = 0
        for sudoku in sudoku.Sudokus:
            (gridRow, gridCol) = self.gridRowCol(sudokusIx)
            for row in range(sudoku.Dimension):
                for col in range(sudoku.Dimension):
                    cell = sudoku.GetCell(row,col)
                    cellView = SudokuCellView(self, colours.get(cell.Group), cell)
                    cellView.Show()
                    cellView.grid( row=gridRow+row, column=gridCol+col, padx=1, pady=1, ipadx=10, ipady=10)
                    self.sudokuCells.append(cellView)
            sudokusIx += 1

    def gridRowCol(self, sudokusIx):
        gridRow = 0
        gridCol = 0
        if sudokusIx==0:
            gridRow = 0
            gridCol = 0
        elif sudokusIx==1:
            gridRow = 0
            gridCol = 12
        elif sudokusIx==2:
            gridRow = 6
            gridCol = 6
        elif sudokusIx==3:
            gridRow = 12
            gridCol = 0
        elif sudokusIx==4:
            gridRow = 12
            gridCol = 12
        return (gridRow, gridCol)

    def Show(self):
        for cell in self.sudokuCells:
            cell.Show()

class CommonSamuraiSudokuFrame(ttk.Frame):
    def __init__(self, root, w, h, sudokusIx, colours, sudoku):
        super().__init__( root, width=w, height=h, relief='solid')
        (gridRow, gridCol) = self.sudokuGridRowCol(sudokusIx)
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

    def sudokuGridRowCol(self, sudokusIx):
        gridRow = 0
        gridCol = 0
        if sudokusIx==0:
            gridRow = 0
            gridCol = 0
        elif sudokusIx==1:
            gridRow = 0
            gridCol = 2
        elif sudokusIx==2:
            gridRow = 1
            gridCol = 1
        elif sudokusIx==3:
            gridRow = 2
            gridCol = 0
        elif sudokusIx==4:
            gridRow = 2
            gridCol = 2
        return (gridRow, gridCol)

    def show(self):
        for row in self.sudokuView:
            for cellView in row:
                cellView.Show()