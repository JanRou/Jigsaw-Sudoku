import unittest
import math

from context import jigsaw
from jigsaw.colours import Colours
from jigsaw.jigsawSudoku import JigsawSudoku

if __name__ == '__main__':
    unittest.main()

class TestJigsawSudoku(unittest.TestCase):

    def testConstructorOk(self):
        # Arrange
        colours = Colours()
        dimension = 4
        dut = self.create4x4TestSudoku( dimension, colours)

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

    def testCheckShapeOk(self):
        # Arrange
        colors = Colours()
        dimension = 4
        shape = []
        rho = round(math.sqrt(dimension))
        for r in range(dimension):
            row = []
            for c in range(dimension):
                row.append( ( r // rho )* rho + (c // rho ) )  # operator // is integer division 
            shape.append(row)
        dut = JigsawSudoku( dimension, shape, colors)

        # Act
        checkShapeResult = dut.CheckShape(shape)

        # Assert
        self.assertTrue(checkShapeResult[0])
        self.assertEqual( "", checkShapeResult[1])

    def testCheckShapeFail(self):
        # Arrange
        colours = Colours()
        dimension = 4
        shape = []
        rho = round(math.sqrt(dimension))
        for r in range(dimension):
            row = []
            for c in range(dimension):
                row.append( ( r // rho )* rho + (c // rho ) )  # operator // is integer division 
            shape.append(row)        
        dut = JigsawSudoku( dimension, shape, colours)
        # change shape to a failing shape
        shape[dimension-1][dimension-1] = 2 # overwrites 3 with 2

        # Act
        checkShapeResult = dut.CheckShape(shape)

        # Assert
        self.assertFalse(checkShapeResult[0])
        self.assertNotEqual("", checkShapeResult[1])

    def testConstructorFails(self):
        # Arrange
        colours = Colours()
        dimension = 4
        shape = []
        rho = round(math.sqrt(dimension))
        for r in range(dimension):
            row = []
            for c in range(dimension):
                row.append( ( r // rho )* rho + (c // rho ) )  # operator // is integer division 
            shape.append(row)        
        dut = JigsawSudoku( 4, shape, colours)
        # change shape to a failing shape
        shape[dimension-1][dimension-1] = 2 # overwrites 3 with 2

        # Act and Assert
        with self.assertRaises(ValueError):
            dut = JigsawSudoku( dimension, shape, colours)

    def testSolvedFalse(self):
        # Arrange
        colors = Colours()
        dimension = 4
        shape = []
        rho = round(math.sqrt(dimension))
        for r in range(dimension):
            row = []
            for c in range(dimension):
                row.append( ( r // rho )* rho + (c // rho ) )  # operator // is integer division 
            shape.append(row)
        dut = JigsawSudoku( 4, shape, colors)

        # Act
        result = dut.Solved

        # Assert
        self.assertFalse(result)

    def testSolvedTrue(self):
        # Arrange
        colours = Colours()
        dimension = 4
        shape = []
        rho = round(math.sqrt(dimension))
        for r in range(dimension):
            row = []
            for c in range(dimension):
                row.append( ( r // rho )* rho + (c // rho ) )  # operator // is integer division 
            shape.append(row)
        dut = JigsawSudoku( 4, shape, colours)
        for r in range(dimension):
            for c in range(dimension):
                dut.Set( r, c, c+1)
        dut.DoChange()

        # Act            
        result = dut.Solved

        # Assert
        self.assertTrue(result)

    def testRemoveCandidatesInColumnForNumber(self):
        # Arrange
        colours = Colours()
        dimension = 4
        dut = self.create4x4TestSudoku( dimension, colours)

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
        colours = Colours()
        dimension = 4
        dut = self.create4x4TestSudoku( dimension, colours)

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

    def testRemoveCandidatesInGroupForNumber(self):
        # Arrange
        colours = Colours()
        dimension = 4
        dut = self.create4x4TestSudoku( dimension, colours)

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

    def testFindPossibleCandidates(self):
        # Arrange
        colours = Colours()
        dimension = 4
        dut = self.create4x4TestSudoku( dimension, colours)

        # Act
        dut.FindPossibleCandidates()
        result = dut.Sudoku

        # Assert
        # 4x4 sudoku after SetPossible
        #    Sudoku     Candidates  
        #    0 1 2 3    0
        #   ---------  -----------------------------
        # 0 ! . !3. !  !(1,2)  .(1,2)  !-    .(2,4)!
        # 1 !4. ! .2!  !-      .(1,2,3)!(1,2).-    !
        #   !-.-!-.-!  !-------.-------!-----.-----! 
        # 2 ! . ! .1!  !(2,3)  !(1,2,3)!(2,4).-    !
        # 3 ! .4!2. !  !(1,2,3)!-      !-    .(2,3)!
        #   ---------  -----------------------------
        self.assertTrue( result[1][3].Changed)
        self.assertEqual(1, len(result[1][3].NewCandidates))
        self.assertIn(2, result[1][3].NewCandidates)
        self.assertTrue( result[3][2].Changed)
        self.assertEqual(1, len(result[3][2].NewCandidates))
        self.assertIn(2, result[3][2].NewCandidates)
        self.assertEqual([1,2], result[0][0].NewCandidates)
        self.assertEqual([1,2,3], result[3][0].NewCandidates)

    def testFindSinglesColumn(self):
        # Arrange
        colours = Colours()
        dimension = 4
        dut = self.create4x4TestSudoku( dimension, colours)
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
        colours = Colours()
        dimension = 4
        dut = self.create4x4TestSudoku( dimension, colours)
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

    def testFindSinglesGroup(self):
        # Arrange
        colours = Colours()
        dimension = 4
        dut = self.create4x4TestSudoku( dimension, colours)
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
        dut.SetSinglesGroup()
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

    def create4x4TestSudoku(self, dimension, colours):
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
        shape = []
        rho = round(math.sqrt(dimension))
        for r in range(dimension):
            row = []
            for c in range(dimension):
                row.append( ( r // rho )* rho + (c // rho ) )  # operator // is integer division 
            shape.append(row)

        sudoku= JigsawSudoku( dimension, shape, colours)
        sudoku.Set( 0, 2, 3)
        sudoku.Set( 1, 0, 4)
        sudoku.Set( 2, 3, 1)
        sudoku.Set( 3, 1, 4)
        sudoku.DoChange()
        return sudoku

    # def test(self):
    #     # Arrange

    #     # Act

    #     # Assert