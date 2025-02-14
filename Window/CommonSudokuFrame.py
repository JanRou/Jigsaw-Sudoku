import tkinter as tk
from tkinter import ttk

from Window.SudokuCellView import SudokuCellView

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