import unittest
import math

from context import normal
from samurai.samuraiSudoku import SamuraiSudoku

if __name__ == '__main__':
    unittest.main()

class TestSamuraiSudoku(unittest.TestCase):

    def testConstructorOk(self):
        # Arrange
        dimension = 4
        grid = 5
        dut = self.create2x2plus1TestSamuraiSudoku( dimension, grid)

        # Act
        resultDimension = dut.Dimension
        resultGrid = dut.Grid
        resultSudokus = dut.Sudoku

        # Assert
        #    0 1 2 3 0 1 2 3
        #   -----------------
        # 0 !2.1!3.4|3.4!2.1!
        # 1 !4.3!1.2|1.2!4.3!
        # 2 !3.2! . ! . !1.4!
        # 3 !1.4! . ! . !3.2!
        #   !===!---!---!===!
        # 0 !2.1! . ! . !4.3!
        # 1 !4.3! . ! . !2.1!
        # 2 !3.4!2.1|2.1!3.4!
        # 3 !2.1!4.3|4.3!1.2!
        #   ---------  -----------------------------------------
        self.assertEqual(dimension, resultDimension)
        self.assertEqual(grid, resultGrid)
        self.assertTrue(resultSudokus[0].Sudoku[0][0].Solved)
        self.assertFalse(resultSudokus[0].Sudoku[2][3].Solved)
        self.assertEqual(2, resultSudokus[0].Sudoku[0][0].Number)
        self.assertEqual(1, resultSudokus[0].Sudoku[0][1].Number)

    def testSharedCellsAreOk(self):
        # Arrange
        dimension = 4
        grid = 5
        dut = self.create2x2plus1TestSamuraiSudoku( dimension, grid)

        # Act
        # Set cell nummber for sudokus not in the middle => middle sudoku is changed
        dut.Set( 0, 2, 2, 4)
        dut.Set( 4, 0, 0, 1)
        # Set cell nummber for sudoku in the middle => not in the middle sudokus changed
        dut.Set( 2, 0, 3, 3)
        dut.Set( 2, 2, 1, 2)
        
        resultSudokus = dut.Sudoku

        # Assert
        self.assertEqual(resultSudokus[0].Sudoku[2][2].Number, resultSudokus[2].Sudoku[0][0].Number)
        self.assertEqual(resultSudokus[4].Sudoku[0][0].Number, resultSudokus[2].Sudoku[2][2].Number)
        self.assertEqual(resultSudokus[2].Sudoku[0][3].Number, resultSudokus[1].Sudoku[2][1].Number)
        self.assertEqual(resultSudokus[2].Sudoku[2][1].Number, resultSudokus[3].Sudoku[0][3].Number)

    def testRemoveCandidatesHookForSharedCells(self):
        #Arrange
        dimension = 4
        grid = 5
        dut = self.create2x2plus1TestSamuraiSudoku( dimension, grid)
        # Set upper left cell in the group to 4
        cell00Middle = dut.Sudoku[2].Sudoku[0][0]
        cell00Middle.Number = 4
        cell00Middle.DoChange()

        #Act
        dut.RemoveCandidatesHook(cell00Middle, dut.Sudoku[2])
        dut.DoChange()
        resultUpperLeftSudoku = dut.Sudoku[0].Sudoku

        #Assert
        # Is 4 removed from the shared cells in the lower right group of the upper left sudoku?
        self.assertEqual([1,2,3], resultUpperLeftSudoku[2][3].Candidates)
        self.assertEqual([1,2,3], resultUpperLeftSudoku[3][2].Candidates)
        self.assertEqual([1,2,3], resultUpperLeftSudoku[3][3].Candidates)

    def testFindPossibleCandidates(self):
        #Arrange
        dimension = 4
        grid = 5
        dut = self.create2x2plus1TestSamuraiSudoku( dimension, grid)

        #Act
        dut.FindPossibleCandidates()
        result = dut.Sudoku[2].Sudoku

        #Assert
        # Do all the cells of middle sudoku a single candidate?        
        for r in range(dimension):
            for c in range(dimension):
                self.assertTrue(result[r][c].Changed)
                self.assertEqual(1, len(result[r][c].NewCandidates))

    def create2x2plus1TestSamuraiSudoku(self, dimension, grid):
        #    0 1 2 3 0 1 2 3
        #   -----------------
        # 0 !2.1!3.4|3.4!2.1!
        # 1 !4.3!1.2|1.2!4.3!
        # 2 !3.2! . ! . !1.4!
        # 3 !1.4! . ! . !3.2!
        #   !===!---!---!===!
        # 0 !2.1! . ! . !4.3!
        # 1 !4.3! . ! . !2.1!
        # 2 !3.4!2.1|2.1!3.4!
        # 3 !2.1!4.3|4.3!1.2!
        testSudoku = []   [[2,1,3,4,3,4,2,1]
                        ,[4,3,1,2,1,2,4,3]
                        ,[3,2, , , , ,1,4]
                        ,[1,4, , , , ,3,2]
                        ,[2,1, , , , ,4,3]
                        ,[4,3, , , , ,2,1]
                        ,[3,4,2,1,2,1,3,4]
                        ,[2,1,4,3,4,3,1,2]]

        sudoku= SamuraiSudoku( dimension, grid)

        sudoku.Set( 0, 0, 0, 2)
        sudoku.Set( 0, 0, 1, 1)
        sudoku.Set( 0, 0, 2, 3)
        sudoku.Set( 0, 0, 3, 4)
        sudoku.Set( 0, 1, 0, 4)
        sudoku.Set( 0, 1, 1, 3)
        sudoku.Set( 0, 1, 2, 1)
        sudoku.Set( 0, 1, 3, 2)
        sudoku.Set( 0, 2, 0, 3)
        sudoku.Set( 0, 2, 1, 2)
        sudoku.Set( 0, 3, 0, 1)
        sudoku.Set( 0, 3, 1, 4)
        sudoku.Set( 1, 0, 0, 3)
        sudoku.Set( 1, 0, 1, 4)
        sudoku.Set( 1, 0, 2, 2)
        sudoku.Set( 1, 0, 3, 1)
        sudoku.Set( 1, 1, 0, 1)
        sudoku.Set( 1, 1, 1, 2)
        sudoku.Set( 1, 1, 2, 4)
        sudoku.Set( 1, 1, 3, 3)
        sudoku.Set( 1, 2, 2, 1)
        sudoku.Set( 1, 2, 3, 4)
        sudoku.Set( 1, 3, 2, 2)
        sudoku.Set( 1, 3, 3, 2)
        sudoku.Set( 3, 0, 0, 2)
        sudoku.Set( 3, 0, 1, 1)
        sudoku.Set( 3, 1, 0, 4)
        sudoku.Set( 3, 1, 1, 3)
        sudoku.Set( 3, 2, 0, 3)
        sudoku.Set( 3, 2, 1, 4)
        sudoku.Set( 3, 2, 2, 2)
        sudoku.Set( 3, 2, 3, 1)
        sudoku.Set( 3, 3, 0, 1)
        sudoku.Set( 3, 3, 1, 2)
        sudoku.Set( 3, 3, 0, 4)
        sudoku.Set( 3, 3, 1, 3)
        sudoku.Set( 4, 0, 2, 4)
        sudoku.Set( 4, 0, 3, 3)
        sudoku.Set( 4, 1, 2, 2)
        sudoku.Set( 4, 1, 3, 1)
        sudoku.Set( 4, 2, 0, 2)
        sudoku.Set( 4, 2, 1, 1)
        sudoku.Set( 4, 2, 2, 3)
        sudoku.Set( 4, 2, 3, 4)
        sudoku.Set( 4, 3, 0, 4)
        sudoku.Set( 4, 3, 1, 3)
        sudoku.Set( 4, 3, 2, 1)
        sudoku.Set( 4, 3, 3, 2)
        sudoku.DoChange()
        return sudoku
