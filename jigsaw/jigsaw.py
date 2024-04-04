import math

from jigsaw.colours import Colours
from jigsaw.sudoku import JigsawSudoku
from jigsaw.window import Window

# def takeStep(step):
#     answer = input("Next step " + step + " Y/N?")
#     return (answer == "Y") or (answer=="y")

# def solve(sudoku):
#     steps = {0:"set possible", 1: "set single candidate row", 2: "set single candidate column"
#              , 3: "set single candidate group"}
#     state = 0
#     sudoku.Print()        
#     while (not sudoku.Solved and takeStep(steps[state])):
#         sudoku.DoChange()
#         match state:
#             case 0:
#                 sudoku.SetPossibleCandidate()
#                 if sudoku.Changed:
#                     state = 0
#                 else:
#                     state = 1
#             case 1:
#                 sudoku.SetSinglesRow()
#                 if sudoku.Changed:
#                     state = 0
#                 else:
#                     state = 2
#             case 2:
#                 sudoku.SetSinglesColumn()
#                 if sudoku.Changed:
#                     state = 0
#                 else:
#                     state = 3
#             case 3:
#                 sudoku.SetSinglesGroup()
#                 state = 0
                
#         sudoku.Print(True)        

#main
shape = []
shape.append( [0,0,0,1,1,1,2,2,2] )
shape.append( [0,3,0,1,1,1,2,4,2] )
shape.append( [0,3,0,1,5,1,2,4,2] )
shape.append( [0,3,0,1,5,5,5,4,2] )
shape.append( [6,3,3,3,5,4,4,4,2] )
shape.append( [6,3,5,5,5,7,8,4,8] )
shape.append( [6,3,6,7,5,7,8,4,8] )
shape.append( [6,3,6,7,7,7,8,4,8] )
shape.append( [6,6,6,7,7,7,8,8,8] )
colours = Colours()
sudoku = JigsawSudoku( 9, shape, colours)
sudoku.Set( 0, 0, 1)
sudoku.Set( 0, 3, 4)
sudoku.Set( 0, 8, 9)
sudoku.Set( 1, 5, 2)
sudoku.Set( 1, 8, 4)
sudoku.Set( 3, 3, 9)
sudoku.Set( 3, 4, 8)
sudoku.Set( 3, 8, 7)
sudoku.Set( 4, 1, 8)
sudoku.Set( 4, 2, 7)
sudoku.Set( 4, 4, 6)
sudoku.Set( 4, 6, 2)
sudoku.Set( 4, 7, 5)
sudoku.Set( 5, 0, 6)
sudoku.Set( 5, 4, 9)
sudoku.Set( 5, 5, 8)
sudoku.Set( 7, 0, 3)
sudoku.Set( 7, 3, 1)
sudoku.Set( 8, 0, 8)
sudoku.Set( 8, 5, 9)
sudoku.Set( 8, 8, 5)
sudoku.DoChange() # set the changes

window = Window(sudoku)
window.mainloop()
