import unittest
import math

from Colours import Colours 
from Sudoku import Sudoku

if __name__ == '__main__':
    unittest.main()

class TestSudoku(unittest.TestCase):

    def testConstructor(self):
        # Arrange
        #colours = Colours()
        dimension = 4
        shape = []
        rho = round(math.sqrt(dimension))
        for r in range(dimension):
            row = []
            for c in range(dimension):
                row.append( ( r // rho )* rho + (c // rho ) )  # operator // is integer division 
            shape.append(row)
        dut = Sudoku( 4, shape, None)

        # Act
        solvedResult = dut.Solved

        # Assert
        self.assertFalse(solvedResult)

    def testCheckShapeOk(self):
        # Arrange
        #colours = Colours()
        dimension = 4
        shape = []
        rho = round(math.sqrt(dimension))
        for r in range(dimension):
            row = []
            for c in range(dimension):
                row.append( ( r // rho )* rho + (c // rho ) )  # operator // is integer division 
            shape.append(row)
        dut = Sudoku( 4, shape, None)

        # Act
        checkShapeResult = dut.CheckShape(shape)

        # Assert
        self.assertTrue(checkShapeResult)

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
        dut = Sudoku( 4, shape, colours)
        # change shape to a failing shape
        shape[dimension-1][dimension-1] = 2 # overwrites 3 with 2

        # Act
        checkShapeResult = dut.CheckShape(shape)

        # Assert
        self.assertFalse(checkShapeResult)

    # def test(self):
    #     # Arrange

    #     # Act

    #     # Assert
