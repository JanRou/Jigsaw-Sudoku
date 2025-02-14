import tkinter as tk
from tkinter import ttk

from Window.CommonSudokuFrame import CommonSudokuFrame
from Window.SudokuCellView import SudokuCellView

class SamuraiSudokuFrame(ttk.Frame): # only grid=5, dimension=9
    def __init__(self, root, w, h, colours, sudoku):
        super().__init__( root, width=w, height=h, relief='solid')
        self.grid(row=0, column=1, padx=10, pady=5, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.sudokuCellViews = []
        sudokusIx = 0
        for sudoku in sudoku.Sudokus:
            (gridRow, gridCol) = self.gridRowCol(sudokusIx)
            if sudokusIx == 2:
                # For the center sudoku create cell views in a cross, so overlapped cells are viewed for the other sudoku's
                for row in range(0,3):
                    for col in range(3,6):
                        self.sudokuCellViews.append(self.createCellView(sudoku, row, col, gridRow, gridCol, colours))
                for row in range(3,6):
                    for col in range(sudoku.Dimension):
                        self.sudokuCellViews.append(self.createCellView(sudoku, row, col, gridRow, gridCol, colours))
                for row in range(6,sudoku.Dimension):
                    for col in range(3,6):
                        self.sudokuCellViews.append(self.createCellView(sudoku, row, col, gridRow, gridCol, colours))
            else:
                for row in range(sudoku.Dimension):
                    for col in range(sudoku.Dimension):
                        self.sudokuCellViews.append(self.createCellView(sudoku, row, col, gridRow, gridCol, colours))
            sudokusIx += 1

    def createCellView( self, sudoku, row, col, gridRow, gridCol, colours):
        cell = sudoku.GetCell(row,col)
        cellView = SudokuCellView(self, colours.get(cell.Group), cell)
        cellView.show()
        cellView.grid( row=gridRow+row, column=gridCol+col, padx=1, pady=1, ipadx=10, ipady=10)
        return cellView

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

    def show(self):
        for cell in self.sudokuCellViews:
            cell.show()
