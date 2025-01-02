from samurai.samuraiSudoku import SamuraiSudoku
def createSudoku():
    grid = 5
    dimension = 9
    sudoku = SamuraiSudoku( dimension, grid)
    tempsudokus = []
    tempsudoku = []
    tempsudoku.append([2,0,0,7,0,0,3,0,4])
    tempsudoku.append([0,0,0,1,0,3,0,6,0])
    tempsudoku.append([0,0,8,0,5,0,9,0,0])
    tempsudoku.append([0,0,3,0,9,4,0,0,0])
    tempsudoku.append([0,0,0,5,0,8,0,0,3])
    tempsudoku.append([0,0,4,0,0,0,7,0,0])
    tempsudoku.append([0,0,0,0,0,0,0,0,0])
    tempsudoku.append([0,3,0,9,0,2,0,0,0])
    tempsudoku.append([1,0,0,3,0,7,0,0,0])
    tempsudokus.append(tempsudoku)
    tempsudoku = []
    tempsudoku.append([4,0,1,0,0,8,0,0,9])
    tempsudoku.append([0,7,0,3,0,9,0,0,0])
    tempsudoku.append([0,0,3,0,2,0,5,0,0])
    tempsudoku.append([0,0,0,7,6,0,9,0,0])
    tempsudoku.append([7,0,0,4,0,2,0,0,0])
    tempsudoku.append([0,0,6,0,0,0,4,0,0])
    tempsudoku.append([0,0,0,0,0,0,0,0,0])
    tempsudoku.append([0,0,0,5,0,7,0,2,0])
    tempsudoku.append([0,0,0,2,0,3,0,0,4])
    tempsudokus.append(tempsudoku)
    tempsudoku = []
    tempsudoku.append([0,0,0,0,0,0,0,0,0])
    tempsudoku.append([0,0,0,2,0,9,0,0,0])
    tempsudoku.append([0,0,0,0,4,0,0,0,0])
    tempsudoku.append([0,0,5,0,1,0,9,0,0])
    tempsudoku.append([7,0,0,0,0,0,0,0,5])
    tempsudoku.append([0,0,4,0,5,0,2,0,0])
    tempsudoku.append([0,0,0,0,3,0,0,0,0])
    tempsudoku.append([0,0,0,7,0,5,0,0,0])
    tempsudoku.append([0,0,0,0,0,0,0,0,0])    
    tempsudokus.append(tempsudoku)        
    tempsudoku = []
    tempsudoku.append([4,0,0,3,0,9,0,0,0])
    tempsudoku.append([0,8,0,4,0,5,0,0,0])
    tempsudoku.append([0,0,0,0,0,0,0,0,0])
    tempsudoku.append([0,0,4,0,0,0,7,0,0])
    tempsudoku.append([0,0,0,6,0,3,0,0,1])
    tempsudoku.append([0,0,8,0,9,1,0,0,0])
    tempsudoku.append([0,0,2,0,3,0,8,0,0])
    tempsudoku.append([0,0,0,5,0,6,0,2,0])
    tempsudoku.append([9,0,0,2,0,0,4,0,5])
    tempsudokus.append(tempsudoku)
    tempsudoku = []
    tempsudoku.append([0,0,0,2,0,4,0,0,9])
    tempsudoku.append([0,0,0,5,0,8,0,3,0])
    tempsudoku.append([0,0,0,0,0,0,0,0,0])
    tempsudoku.append([0,0,1,0,0,0,7,0,0])
    tempsudoku.append([5,0,0,7,0,2,0,0,0])
    tempsudoku.append([0,0,0,3,4,0,8,0,0])
    tempsudoku.append([0,0,4,0,2,0,9,0,0])
    tempsudoku.append([0,8,0,9,0,7,0,0,0])
    tempsudoku.append([9,0,7,0,0,6,0,0,3])
    tempsudokus.append(tempsudoku)

    for s in range(grid):
        for row in range(dimension):
            for col in range(dimension):
                if tempsudokus[s] != [] and tempsudokus[s][row][col]!=0:
                    sudoku.Set( s, row, col, tempsudokus[s][row][col])

    sudoku.DoChange() # set the changes
    return sudoku
