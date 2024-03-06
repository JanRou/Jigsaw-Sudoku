import unittest
import math

from jigsaw.colours import Colours
from jigsaw.sudoku import Sudoku

if __name__ == '__main__':
    unittest.main()

class TestSudoku(unittest.TestCase):

    def testConstructor(self):
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
        dut = Sudoku( 4, shape, colors)

        # Act
        result = dut.Dimension

        # Assert
        self.assertEqual(dimension, result)

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
        dut = Sudoku( 4, shape, colors)

        # Act
        checkShapeResult = dut.CheckShape(shape)

        # Assert
        self.assertTrue(checkShapeResult)

    def testCheckShapeFail(self):
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
        dut = Sudoku( 4, shape, colors)
        # change shape to a failing shape
        shape[dimension-1][dimension-1] = 2 # overwrites 3 with 2

        # Act
        checkShapeResult = dut.CheckShape(shape)

        # Assert
        self.assertFalse(checkShapeResult)

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
        dut = Sudoku( 4, shape, colors)

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
        dut = Sudoku( 4, shape, colours)
        for r in range(dimension):
            for c in range(dimension):
                dut.Set( r, c, c+1)
        # Act
        result = dut.Solved

        # Assert
        self.assertTrue(result)


    # def test(self):
    #     # Arrange

    #     # Act

    #     # Assert
