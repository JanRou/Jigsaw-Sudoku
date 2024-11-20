import unittest
import math

from context import jigsaw
from jigsaw.colours import Colours
from jigsaw.cell import JigsawCell

if __name__ == '__main__':
    unittest.main()
    
class TestJigsawCell(unittest.TestCase):

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
        dut = JigsawCell( dimension, row, column, group, colors)

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
        dut = JigsawCell( dimension, row, column, group, colors)

        # Act
        dut.Remove(1)

        # Assert
        self.assertEqual(expectedcandidates, dut.NewCandidates)

    def testRemoveFail(self):
        # Arrange
        colors = Colours()
        dimension = 4
        group = 0
        row = 0
        column = 0
        numberLow = 0
        numberHigh = 5
        dut = JigsawCell( dimension, row, column, group, colors)

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
        dut = JigsawCell( dimension, row, column, group, colors)

        # Act
        getResult1 = dut.Number
        dut.Number = number
        changeResult = dut.Changed
        dut.DoChange()
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
        dut = JigsawCell( dimension, row, column, group, colors)

        # Assert
        with self.assertRaises(ValueError):
            dut.Number = numberHigh

        with self.assertRaises(ValueError):
            dut.Number = numberLow

    def testSetSingleCandidateToNewNumberOk(self):
        # Arrange
        colors = Colours()
        dimension = 4
        group = 0
        row = 0
        column = 0
        dut = JigsawCell( dimension, row, column, group, colors)

        # Act
        dut.Remove(1)
        dut.Remove(2)
        dut.Remove(3)
        resultNewCandidates = dut.NewCandidates
        dut.DoChange()
        resultCandidates = dut.Candidates
        dut.SetSingleCandidateToNewNumber()
        resultNewNumber = dut.NewNumber
        dut.DoChange()

        # Assert
        self.assertEqual( 1, len(resultNewCandidates))
        self.assertIn( 4, resultNewCandidates)
        self.assertEqual( 1, len(resultCandidates))
        self.assertIn( 4, resultCandidates)
        self.assertEqual( 4, resultNewNumber)
        self.assertTrue( dut.Solved)

    def testAppendSingleCandidatesNotChanged(self):
        # Arrange
        colors = Colours()
        dimension = 4
        group = 0
        row = 0
        column = 0
        dut = JigsawCell( dimension, row, column, group, colors)
        dut.Remove(1)
        dut.DoChange()
        singleCandidates = [2]

        # Act
        result = dut.AppendSingleCandidates(singleCandidates)

        # Assert
        self.assertEqual( 3, len(result))
        self.assertNotIn( 1, result)
        self.assertIn( 2, result)

    def testAppendSingleCandidatesChanged(self):
        # Arrange
        colors = Colours()
        dimension = 4
        group = 0
        row = 0
        column = 0
        dut = JigsawCell( dimension, row, column, group, colors)
        singleCandidates = [2]
        dut.Remove(1)

        # Act
        result = dut.AppendSingleCandidates(singleCandidates)

        # Assert
        self.assertEqual( 3, len(result))
        self.assertNotIn( 1, result)
        self.assertIn( 2, result)


    def testCountAndSetFirstCellForSingleCandidateNotChanged(self):
        # Arrange
        colors = Colours()
        dimension = 4
        group = 0
        row = 0
        column = 0
        dut = JigsawCell( dimension, row, column, group, colors)
        dut.Remove(1)
        dut.DoChange()
        firstCell = None
        count = 0

        # Act
        resultCount, resultFirstCell = dut.CountAndSetFirstCellForSingleCandidate(2,count,firstCell)

        # Assert
        self.assertEqual( 1, resultCount)
        self.assertIs( dut, resultFirstCell)

    def testCountAndSetFirstCellForSingleCandidateChanged(self):
        # Arrange
        colors = Colours()
        dimension = 4
        group = 0
        row = 0
        column = 0
        dut = JigsawCell( dimension, row, column, group, colors)
        dut.Remove(1)
        firstCell = None
        count = 0

        # Act
        resultCount, resultFirstCell = dut.CountAndSetFirstCellForSingleCandidate(2,count,firstCell)

        # Assert
        self.assertEqual( 1, resultCount)
        self.assertIs( dut, resultFirstCell)


    # def test(self):
    #     # Arrange

    #     # Act

    #     # Assert
