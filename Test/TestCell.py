import unittest
import math

from context import jigsaw
from jigsaw.colours import Colours
from jigsaw.cell import Cell

if __name__ == '__main__':
    unittest.main()
    
class TestCell(unittest.TestCase):

    def testConstructor(self):
        # Arrange
        colors = Colours()
        dimension = 4
        group = 0
        row = 0
        column = 0
        expectedcandidates = []
        for c in range(1,dimension+1):
            expectedcandidates.append(c)
        dut = Cell( dimension, row, column, group, colors)

        # Act
        solvedResult = dut.Solved
        candidatesResult = dut.Candidates
        groupResult = dut.Group
        rowResult = dut.Row
        columnResult = dut.Column

        # Assert
        self.assertFalse(solvedResult)
        self.assertEqual(expectedcandidates, candidatesResult)
        self.assertEqual(row, rowResult)
        self.assertEqual(column, columnResult)
        self.assertEqual(group, groupResult)

    def testRemoveOk(self):
        # Arrange
        colors = Colours()
        dimension = 4
        group = 0
        row = 0
        column = 0
        expectedcandidates = []
        # removes 1, so start from 2
        for c in range( 2, dimension+1):
            expectedcandidates.append(c)
        dut = Cell( dimension, row, column, group, colors)

        # Act
        dut.Remove(1)

        # Assert
        self.assertEqual(expectedcandidates, dut.Candidates)

    def testRemoveFail(self):
        # Arrange
        colors = Colours()
        dimension = 4
        group = 0
        row = 0
        column = 0
        numberLow = 0
        numberHigh = 5
        dut = Cell( dimension, row, column, group, colors)

        # Assert
        with self.assertRaises(ValueError):
            dut.Remove(numberLow)

        with self.assertRaises(ValueError):
            dut.Remove(numberHigh)

    def testSetAndGetNumberOk(self):
        # Arrange
        colors = Colours()
        dimension = 4
        group = 0
        row = 0
        column = 0
        number = 2
        dut = Cell( dimension, row, column, group, colors)

        # Act
        getResult1 = dut.Number
        dut.Number = number
        getResult2 = dut.Number
        solvedResult = dut.Solved

        # Assert
        self.assertEqual( 0, getResult1)
        self.assertEqual( number, getResult2)
        self.assertTrue(solvedResult)

    def testSetAndGetNumberFail(self):
        # Arrange
        colors = Colours()
        dimension = 4
        group = 0
        row = 0
        column = 0
        numberLow = 0
        numberHigh = 5
        dut = Cell( dimension, row, column, group, colors)

        # Assert
        with self.assertRaises(ValueError):
            dut.Number = numberHigh

        with self.assertRaises(ValueError):
            dut.Number = numberLow


    def testPrint(self):
        # Arrange
        colors = Colours()
        dimension = 4
        group = 0
        row = 0
        column = 0
        dut = Cell( dimension, row, column, group, colors)

        # Act
        result = dut.Print()

        # Assert
        self.assertEqual( round(math.sqrt(dimension)), len(result))

    # def test(self):
    #     # Arrange

    #     # Act

    #     # Assert
