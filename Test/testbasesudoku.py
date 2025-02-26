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
    def createCell(self, dim, rw, cl):
        rho = round(math.sqrt(dim))
        group = (rw//rho)*rho + (cl//rho) # upper left square is indexed 0, next to the right 1, and so forth.
        cell = BaseCell( dim, rw, cl, group)
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


    def testSolvedTrue(self):
        # Arrange
        dimension = 4
        dut = self.create4x4TestSudoku(dimension, self.createCell, False)
        for r in range(dimension):
            for c in range(dimension):
                dut.Set( r, c, c+1)
        dut.DoChange()

        # Act            
        result = dut.Solved

        # Assert
        self.assertTrue(result)

    def testSolvedFalse(self):
        # Arrange
        dimension = 4
        dut = self.create4x4TestSudoku(dimension, self.createCell, False)
 
        # Act
        result = dut.Solved

        # Assert
        self.assertFalse(result)

    def testRemoveCandidatesInColumnForNumber(self):
        # Arrange
        dimension = 4
        dut = self.create4x4TestSudoku(dimension, self.createCell, False)

        # Act
        dut.RemoveCandidatesInColumnForNumber( 0, 4)
        dut.DoChange()
        result = dut.Sudoku

        # Assert
        # 4x4 test sudoku after removal of candidates
        #    Sudoku     Candidates  
        #    0 1 2 3    0
        #   !-.-!-.-!  !---------.---------!---------.---------!
        # 0 ! . !3. !  !(1,2,3)  .(1,2,3,4)!-        .(1,2,3,4)!
        # 1 !4. ! . !  !-        .(1,2,3,4)!(1,2,3,4).(1,2,3,4)!
        #   !-.-!-.-!  !---------.---------!---------.---------! 
        # 2 ! . ! .1!  !(1,2,3,) .(1,2,3,4)!(1,2,3,4).-        !
        # 3 ! .4! . !  !(1,2,3,) .-        !(1,2,3,4).(1,2,3,4)!
        #   !-.-!-.-!  !---------.---------!---------.---------!
        self.assertEqual([1,2,3], result[0][0].Candidates)
        self.assertEqual([1,2,3], result[2][0].Candidates)
        self.assertEqual([1,2,3], result[3][0].Candidates)

    def testRemoveCandidatesInRowForNumber(self):
        # Arrange
        dimension = 4
        dut = self.create4x4TestSudoku(dimension, self.createCell, False)

        # Act
        dut.RemoveCandidatesInRowForNumber( 0, 3)
        dut.DoChange()
        result = dut.Sudoku

        # Assert
        # 4x4 test sudoku after removal of candidates
        #    Sudoku     Candidates  
        #    0 1 2 3    0
        #   !-.-!-.-!  !----------.---------!---------.---------!
        # 0 ! . !3. !  !(1,2,4)   .(1,2,4)  !-        .(1,2,4)  !
        # 1 !4. ! . !  !-         .(1,2,3,4)!(1,2,3,4).(1,2,3,4)!
        #   !-.-!-.-!  !----------.---------!---------.---------! 
        # 2 ! . ! .1!  !(1,2,3,4) .(1,2,3,4)!(1,2,3,4).-        !
        # 3 ! .4! . !  !(1,2,3,4) .-        !(1,2,3,4).(1,2,3,4)!
        #   !-.-!-.-!  !----------.---------!---------.---------!
        self.assertEqual([1,2,4], result[0][0].Candidates)
        self.assertEqual([1,2,4], result[0][0].Candidates)
        self.assertEqual([1,2,4], result[0][3].Candidates)

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

    def testFindSinglesColumn(self):
        # Arrange
        dimension = 4
        dut = self.create4x4TestSudoku(dimension, self.createCell)
        sudoku = dut.Sudoku
        sudoku[0][0].Remove(3)
        sudoku[0][0].Remove(4)
        sudoku[2][0].Remove(2)
        sudoku[2][0].Remove(4)
        sudoku[3][0].Number = 1
        dut.DoChange()
        # 4x4 test sudoku before set singles in columns. It is not a real situation
        #    Sudoku     Candidates  
        #    0 1 2 3    0
        #   !-.-!-.-!  !----------.---------!---------.---------!
        # 0 ! . !3. !  !(1,2)     .(1,2,3,4)!-        .(1,2,3,4)!
        # 1 !4. ! . !  !-         .(1,2,3,4)!(1,2,3,4).(1,2,3,4)!
        #   !-.-!-.-!  !----------.---------!---------.---------! 
        # 2 ! . ! .1!  !(1,3)     .(1,2,3,4)!(1,2,3,4).-        !
        # 3 !1.4! . !  !-         .-        !(1,2,3,4).(1,2,3,4)!
        #   !-.-!-.-!  !----------.---------!---------.---------!

        # Act
        dut.FindSinglesColumn()
        dut.DoChange()
        result = dut.Sudoku

        # Assert
        # 4x4 test sudoku after set singles in columns.
        #    Sudoku     Candidates  
        #    0 1 2 3    0
        #   !-.-!-.-!  !----------.---------!---------.---------!
        # 0 !2. !3. !  !-         .(1,2,3,4)!-        .(1,2,3,4)!
        # 1 !4. ! . !  !-         .(1,2,3,4)!(1,2,3,4).(1,2,3,4)!
        #   !-.-!-.-!  !----------.---------!---------.---------! 
        # 2 !3. ! .1!  !-         .(1,2,3,4)!(1,2,3,4).-        !
        # 3 !1.4! . !  !-         .-        !(1,2,3,4).(1,2,3,4)!
        #   !-.-!-.-!  !----------.---------!---------.---------!
        self.assertTrue(    result[0][0].Solved)
        self.assertEqual(2, result[0][0].Number)
        self.assertTrue(    result[1][0].Solved)
        self.assertEqual(4, result[1][0].Number)
        self.assertTrue(    result[2][0].Solved)
        self.assertEqual(3, result[2][0].Number)
        self.assertTrue(    result[3][0].Solved)
        self.assertEqual(1, result[3][0].Number)

    def testFindSinglesRow(self):
        # Arrange
        dimension = 4
        dut = self.create4x4TestSudoku(dimension, self.createCell)
        sudoku = dut.Sudoku
        sudoku[0][0].Remove(3)
        sudoku[0][0].Remove(1)
        sudoku[0][1].Remove(2)
        sudoku[0][1].Remove(4)
        sudoku[0][3].Remove(1)
        sudoku[0][3].Remove(2)
        dut.DoChange()        
        # 4x4 test sudoku before set singles in columns. It is not a real situation
        #    Sudoku     Candidates  
        #    0 1 2 3    0
        #   !-.-!-.-!  !---------.---------!---------.---------!
        # 0 ! . !3. !  !(2,3)    .(1,3)    !-        .(3,4)    !
        # 1 !4. ! . !  !-        .(1,2,3,4)!(1,2,3,4).(1,2,3,4)!
        #   !-.-!-.-!  !---------.---------!---------.---------! 
        # 2 ! . ! .1!  !(1,2,3,4).(1,2,3,4)!(1,2,3,4).-        !
        # 3 !1.4! . !  !-        .-        !(1,2,3,4).(1,2,3,4)!
        #   !-.-!-.-!  !---------.---------!---------.---------!

        # Act
        dut.FindSinglesRow()
        dut.DoChange()
        result = dut.Sudoku

        # Assert
        # 4x4 test sudoku after set singles in columns.
        #    Sudoku     Candidates  
        #    0 1 2 3    0
        #   !-.-!-.-!  !---------.---------!---------.---------!
        # 0 !2.1!3.4!  !-        .-        !-        .-        !
        # 1 !4. ! . !  !(1,2,3,4).(1,2,3,4)!(1,2,3,4).(1,2,3,4)!
        #   !-.-!-.-!  !---------.---------!---------.---------! 
        # 2 ! . ! .1!  !(1,2,3,4).(1,2,3,4)!(1,2,3,4).-        !
        # 3 ! .4! . !  !(1,2,3,4).-        !(1,2,3,4).(1,2,3,4)!
        #   !-.-!-.-!  !---------.---------!---------.---------!
        self.assertTrue(    result[0][0].Solved)
        self.assertEqual(2, result[0][0].Number)
        self.assertTrue(    result[0][1].Solved)
        self.assertEqual(1, result[0][1].Number)
        self.assertTrue(    result[0][2].Solved)
        self.assertEqual(3, result[0][2].Number)
        self.assertTrue(    result[0][3].Solved)
        self.assertEqual(4, result[0][3].Number)

    def testSetSinglesGroup(self):
        # Arrange
        dimension = 4
        dut = self.create4x4TestSudoku(dimension, self.createCell)
        sudoku = dut.Sudoku
        sudoku[0][0].Remove(3)
        sudoku[0][0].Remove(1)
        sudoku[0][1].Remove(2)
        sudoku[0][1].Remove(3)
        sudoku[1][1].Remove(1)
        sudoku[1][1].Remove(2)
        dut.DoChange()
        # 4x4 test sudoku before set singles in columns. It's not a real situation
        #    Sudoku     Candidates  
        #    0 1 2 3    0
        #   !-.-!-.-!  !---------.---------!---------.---------!
        # 0 ! . !3. !  !(2,4)    .(1,4)    !-        .(1,2,3,4)!
        # 1 !4. ! . !  !-        .(3,4)    !(1,2,3,4).(1,2,3,4)!
        #   !-.-!-.-!  !---------.---------!---------.---------! 
        # 2 ! . ! .1!  !(1,2,3,4).(1,2,3,4)!(1,2,3,4).-        !
        # 3 !1.4! . !  !-        .-        !(1,2,3,4).(1,2,3,4)!
        #   !-.-!-.-!  !---------.---------!---------.---------!

        # Act
        dut.FindSinglesGroup()
        dut.DoChange()
        result = dut.Sudoku

        # Assert
        # 4x4 test sudoku after set singles in columns.
        #    Sudoku     Candidates  
        #    0 1 2 3    0
        #   !-.-!-.-!  !---------.---------!---------.---------!
        # 0 !2.1!3. !  !-        .-        !(1,2,3,4).(1,2,3,4)!
        # 1 !4.3! . !  !-        .-        !(1,2,3,4).(1,2,3,4)!
        #   !-.-!-.-!  !---------.---------!---------.---------! 
        # 2 ! . ! .1!  !(1,2,3,4).(1,2,3,4)!(1,2,3,4).-        !
        # 3 ! .4! . !  !(1,2,3,4).-        !(1,2,3,4).(1,2,3,4)!
        #   !-.-!-.-!  !---------.---------!---------.---------!
        self.assertEqual(0, result[0][0].Group)
        self.assertTrue(    result[0][0].Solved)
        self.assertEqual(2, result[0][0].Number)
        self.assertEqual(0, result[0][1].Group)
        self.assertTrue(    result[0][1].Solved)
        self.assertEqual(1, result[0][1].Number)
        self.assertEqual(0, result[1][0].Group)
        self.assertTrue(    result[1][0].Solved)
        self.assertEqual(4, result[1][0].Number)
        self.assertEqual(0, result[1][1].Group)
        self.assertTrue(    result[1][1].Solved)
        self.assertEqual(3, result[1][1].Number)

    def testRemoveCandidatesInGroupForNumber(self):
        # Arrange
        dimension = 4
        dut = self.create4x4TestSudoku(dimension, self.createCell)

        # Act
        dut.RemoveCandidatesInGroupForNumber( 0, 4)
        dut.DoChange()
        result = dut.Sudoku

        # Assert
        # 4x4 test sudoku after removal of candidates
        #    Sudoku     Candidates  
        #    0 1 2 3    0
        #   !-.-!-.-!  !----------.---------!---------.---------!
        # 0 ! . !3. !  !(1,2,3)   .(1,2,3)  !-        .(1,2,3,4)!
        # 1 !4. ! . !  !-         .(1,2,3)  !(1,2,3,4).(1,2,3,4)!
        #   !-.-!-.-!  !----------.---------!---------.---------! 
        # 2 ! . ! .1!  !(1,2,3,4) .(1,2,3,4)!(1,2,3,4).-        !
        # 3 ! .4! . !  !(1,2,3,4) .-        !(1,2,3,4).(1,2,3,4)!
        #   !-.-!-.-!  !----------.---------!---------.---------!
        self.assertEqual([1,2,3], result[0][0].Candidates)
        self.assertEqual([1,2,3], result[0][1].Candidates)
        self.assertEqual([1,2,3], result[1][1].Candidates)

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
        sudoku= BaseSudoku( dimension, createCell, 'Test')
        sudoku.Set( 0, 2, 3)
        sudoku.Set( 1, 0, 4)
        sudoku.Set( 2, 3, 1)
        sudoku.Set( 3, 1, 4)
        if change:
            sudoku.DoChange()
        return sudoku
