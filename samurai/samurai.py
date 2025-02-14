from samurai.samuraiSudoku import SamuraiSudoku
def createSudoku():
    grid = 5
    dimension = 9
    sudoku = SamuraiSudoku( dimension, grid)
    tempsudokus = []
    s1 = []
    s1.append([2,0,0,7,0,0,3,0,4])
    s1.append([0,0,0,1,0,3,0,6,0])
    s1.append([0,0,8,0,5,0,9,0,0])
    s1.append([0,0,3,0,9,4,0,0,0])
    s1.append([0,0,0,5,0,8,0,0,3])
    s1.append([0,0,4,0,0,0,7,0,0])
    s1.append([0,0,0,0,0,0,0,0,0])
    s1.append([0,3,0,9,0,2,0,0,0])
    s1.append([1,0,0,3,0,7,0,0,0])
    tempsudokus.append(s1)
    s2 = []
    s2.append([4,0,1,0,0,8,0,0,9])
    s2.append([0,7,0,3,0,9,0,0,0])
    s2.append([0,0,3,0,2,0,5,0,0])
    s2.append([0,0,0,7,6,0,9,0,0])
    s2.append([7,0,0,4,0,2,0,0,0])
    s2.append([0,0,6,0,0,0,4,0,0])
    s2.append([0,0,0,0,0,0,0,0,0])
    s2.append([0,0,0,5,0,7,0,2,0])
    s2.append([0,0,0,2,0,3,0,0,4])
    tempsudokus.append(s2)
    s3 = []
    s3.append([0,0,0,0,0,0,0,0,0])
    s3.append([0,0,0,2,0,9,0,0,0])
    s3.append([0,0,0,0,4,0,0,0,0])
    s3.append([0,0,5,0,1,0,9,0,0])
    s3.append([7,0,0,0,0,0,0,0,5])
    s3.append([0,0,4,0,5,0,2,0,0])
    s3.append([0,0,0,0,3,0,0,0,0])
    s3.append([0,0,0,7,0,5,0,0,0])
    s3.append([0,0,0,0,0,0,0,0,0])    
    tempsudokus.append(s3)
    s4 = []
    s4.append([4,0,0,3,0,9,0,0,0])
    s4.append([0,8,0,4,0,5,0,0,0])
    s4.append([0,0,0,0,0,0,0,0,0])
    s4.append([0,0,4,0,0,0,7,0,0])
    s4.append([0,0,0,6,0,3,0,0,1])
    s4.append([0,0,8,0,9,1,0,0,0])
    s4.append([0,0,2,0,3,0,8,0,0])
    s4.append([0,0,0,5,0,6,0,2,0])
    s4.append([9,0,0,2,0,0,4,0,5])
    tempsudokus.append(s4)
    s5 = []
    s5.append([0,0,0,2,0,4,0,0,9])
    s5.append([0,0,0,5,0,8,0,3,0])
    s5.append([0,0,0,0,0,0,0,0,0])
    s5.append([0,0,1,0,0,0,7,0,0])
    s5.append([5,0,0,7,0,2,0,0,0])
    s5.append([0,0,0,3,4,0,8,0,0])
    s5.append([0,0,4,0,2,0,9,0,0])
    s5.append([0,8,0,9,0,7,0,0,0])
    s5.append([9,0,7,0,0,6,0,0,3])
    tempsudokus.append(s5)
    
    for sudokuIx in range(grid):
        for row in range(dimension):
            for col in range(dimension):
                if tempsudokus[sudokuIx] != [] and tempsudokus[sudokuIx][row][col]!=0:
                    sudoku.Set( sudokuIx, row, col, tempsudokus[sudokuIx][row][col], True)

    sudoku.DoChange() # set the changes
    return sudoku
