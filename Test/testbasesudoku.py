import unittest
import math

from context import jigsaw
from basesudoku.basecell import BaseCell
from basesudoku.basesudoku import BaseSudoku

if __name__ == '__main__':
    unittest.main()

class TestBaseSudoku(unittest.TestCase):

    def testConstructorOk(self):
        # Arrange
        dimension = 4
        dut = self.create4x4TestSudoku(dimension, self.createCell)

        # Act
        resultDim = dut.Dimension
        resultSudoku = dut.Sudoku

        # Assert
        # 4x4 sudoku constructed
        #    Sudoku     Candidates  
        #    0 1 2 3    0
        #   ---------  -----------------------------------------
        # 0 ! . !3. !  !(1,2,3,4).(1,2,3,4)!-        .(1,2,3,4)!
        # 1 !4. ! . !  !-        .(1,2,3,4)!(1,2,3,4).(1,2,3,4)!
        #   !-.-!-.-!  !---------.---------!---------.---------! 
        # 2 ! . ! .1!  !(1,2,3,4)!(1,2,3,4)!(1,2,3,4).-        !
        # 3 ! .4! . !  !(1,2,3,4)!-        !(1,2,3,4).(1,2,3,4)!
        #   ---------  -----------------------------------------
        self.assertEqual(dimension, resultDim)
        self.assertFalse(resultSudoku[0][0].Solved)
        self.assertTrue(resultSudoku[1][0].Solved)
        self.assertEqual(4, resultSudoku[1][0].Number)

    # for testing constructor
    def createCell(self, d, rw, col):
        cell = BaseCell( d, rw, col)
        return cell

    def testDoChange(self):
        # Arrange
        dimension = 4
        dut = self.create4x4TestSudoku(dimension, self.createCell, False)

        # Act        
        resultBeforeChange = dut.Changed
        result02BeforeChange = dut.Sudoku[0][2].Changed
        result10BeforeChange = dut.Sudoku[1][0].Changed
        dut.DoChange()
        resultAfterChange = dut.Changed
        result02AfterChange = dut.Sudoku[0][2].Changed
        result10AfterChange = dut.Sudoku[1][0].Changed

        # Assert
        self.assertTrue(resultBeforeChange)
        self.assertTrue(result02BeforeChange)
        self.assertTrue(result10BeforeChange)
        self.assertFalse(resultAfterChange)
        self.assertFalse(result02AfterChange)
        self.assertFalse(result10AfterChange)

    def testSetSingleCandidatesAsnewNumber(self):
        # Arrange
        dimension = 4
        dut = self.create4x4TestSudoku(dimension, self.createCell)
        self.dut = dut
        # Act
        dut.FindPossibleCandidatesBase(self.removeCandidatesInSquare)
        # After FindPossibleCandidatesBase with classic square formation:
        #    Sudoku     Candidates  
        #    0 1 2 3    0
        #   ---------  -----------------------------------------
        # 0 ! . !3. !  !(1,2)    .(1,2)    !-        .(2,4)    !
        # 1 !4. ! . !  !-        .(1,2,3)  !(1,2)    .(2)      !
        #   !-.-!-.-!  !---------.---------!---------.---------! 
        # 2 ! . ! .1!  !(2,3)    .(2,3)    !(2,4)    .-        !
        # 3 ! .4! . !  !(1,2,3)  .-        !(2)      .(2,3)    !
        #   ---------  -----------------------------------------
        dut.DoChange()
        result13Candidates = dut.Sudoku[1][3].Candidates
        result32Candidates = dut.Sudoku[3][2].Candidates
        result30Candidates = dut.Sudoku[3][0].Candidates
        dut.SetSingleCandidatesAsnewNumber()

        # Assert
        self.assertEqual( 1, len(result13Candidates))
        self.assertIn( 2, result13Candidates)
        self.assertEqual( 1, len(result32Candidates))
        self.assertIn( 2, result32Candidates)
        self.assertEqual( [1,2,3], result30Candidates)
        self.assertEqual( 2, dut.Sudoku[1][3].NewNumber)
        self.assertEqual( 2, dut.Sudoku[3][2].NewNumber)


    def removeCandidatesInSquare(self, cell):
        # 4x4 sudoku for test
        #    Sudoku     Square (=group) 
        #    0 1 2 3                                  
        #   ---------   ---------------------
        # 0 ! . !3. !   ![0][0].  ![0][1].  !
        # 1 !4. ! . !   !-     .  !      .  !
        #   !-.-!-.-!   !------.--!------.--! 
        # 2 ! . ! .1!   ![1][0].  ![1][1].  !
        # 3 ! .4! . !   !      .  !      .  !
        #   ---------  ----------------------
        rho = round(math.sqrt(cell.Dimension))
        sqRow = cell.Row // rho
        sqCol = cell.Column // rho
        for row in range(rho*sqRow, rho*sqRow + rho):
            for col in range(rho*sqCol, rho*sqCol + rho):
                self.dut.Sudoku[row][col].Remove(cell.Number)

    #def test(self):
    #     # Arrange

    #     # Act

    #     # Assert

    def create4x4TestSudoku(self, dimension, createCell, change=True):
        # 4x4 sudoku for test
        #    Sudoku     Candidates  
        #    0 1 2 3    0
        #   ---------  -----------------------------------------
        # 0 ! . !3. !  !(1,2,3,4).(1,2,3,4)!-        .(1,2,3,4)!
        # 1 !4. ! . !  !-        .(1,2,3,4)!(1,2,3,4).(1,2,3,4)!
        #   !-.-!-.-!  !---------.---------!---------.---------! 
        # 2 ! . ! .1!  !(1,2,3,4)!(1,2,3,4)!(1,2,3,4).-        !
        # 3 ! .4! . !  !(1,2,3,4)!-        !(1,2,3,4).(1,2,3,4)!
        #   ---------  -----------------------------------------
        sudoku= BaseSudoku( dimension, self.createCell)
        sudoku.Set( 0, 2, 3)
        sudoku.Set( 1, 0, 4)
        sudoku.Set( 2, 3, 1)
        sudoku.Set( 3, 1, 4)
        if change:
            sudoku.DoChange()
        return sudoku
    

