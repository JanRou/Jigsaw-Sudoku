import tkinter as tk
from tkinter import ttk


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