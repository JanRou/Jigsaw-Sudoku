from sty import fg, bg, ef, rs
import math

class Colours:
    def __init__(self):
        self._colours = [bg.blue, bg.grey, bg.red, bg.green, bg.cyan, bg.yellow, bg.magenta, bg(255, 150, 50), bg(150, 150, 250), bg.li_red, bg.li_green, bg.li_cyan, bg.li_yellow, bg.li_magenta, bg.white ]

    def Colour(self, ix):
        if ix < len(self._colours):
            return self._colours[ix]
        else:
            return bg.black

class Cell:
    def __init__(self, d, r, c, g, colours):
        self._number=0 # 0 means not solved, 1 - n means solved
        self._dimension = d # 9=3x3, 16=4x4, 25=5x5 ...
        self._row=r    # row and column are 0 based
        self._column=c
        self._group=g  # group is shape index, 0 to d-1, the number belongs to
        self._colours = colours
        self._candidates = []
        for i in range(0, self._dimension):
            self._candidates.append(i+1)

    @property
    def Number(self):
        return self._number

    @Number.setter
    def Number(self, n):
        if 0 < n and n <= self._dimension:
            self._number = n
            # clear list of candidates and set the only one
            self._candidates.clear()            
            for i in range(0, self._dimension):
                self._candidates.append(0)
            self._candidates[n-1] = n
        else:
            raise ValueError

    @property
    def Solved(self):
        return self._number != 0

    @property
    def Row(self):
        return self._row

    @property
    def Column(self):
        return self._column
    
    @property
    def Group(self):
        return self._group
    
    @property
    def Candidates(self):
        result = []
        if not self.Solved:            
            for candidate in self._candidates:
                if candidate != 0:
                    result.append(candidate)
        return result

    def Remove(self, number): # argument is the number to remove, 1 to dimension
        if number<0 and self._dimension<=number:
            raise ValueError
        if not self.Solved:
            self._candidates[number-1]=0
        if self._candidates.count(0) == self._dimension-1:
            # only one candidate left, set cell solved with the number left
            for number in self._candidates:
                if number != 0:
                    self._number = number
                    break
        
    def Print(self): # Prints n lines per cell with n candidates per line from 1 to dimension, n=sqrt(dimension)
        strings = []
        rho = round(math.sqrt(self._dimension))
        for i in range(rho):
            string = ""
            # TODO refactor to one loop
            if self._number != 0:
                for j in range(rho):
                    if i == round(rho/2)-1 and j == round(rho/2)-1: # center
                        strcan = fg.black + ef.bold + str(self._number) + ef.rs + fg.rs
                    else:
                        strcan= fg.black + " "  + fg.rs # TODO doesn't work for dimensions greater than 9
                    string = string + " " + strcan + " "
            else:
                for j in range(rho):
                    cand = self._candidates[i*rho + j]
                    if cand != 0:
                        strcan = str(self._candidates[i*rho + j])
                    else:
                        strcan= fg.black + " "  + fg.rs# TODO doesn't work for dimensions greater than 9
                    string = string + " " + strcan + " "
            if i < rho-1:
                strings.append( self._colours.Colour(self._group) + string + bg.rs)
            else:
                strings.append( self._colours.Colour(self._group) + ef.underl + string + ef.rs + bg.rs)
                
        return strings

class Sudoku:
    def __init__(self, d, shape, colours): 
        # d is dimension of sudoku, usually 4, 9, 16, 25 ...
        # shape is d=nxn row and columns with group indexes 0 based, n=sqrt(d), 
        # where 0 is first group at upper left corner and n is last
        self._cells = []
        self._colours = colours
        self._dimension = d
        for rw in range( 0, self._dimension):
            row = []            
            for col in range( 0, self._dimension):
                row.append( Cell( self._dimension, rw, col, shape[rw][col], self._colours) )
            self._cells.append(row)

    def Print(self):
        rho = round(math.sqrt(self._dimension))
        for r in range( 0, self._dimension):
            strings = []
            for i in range(rho):
                strings.append("")
            for c in range( 0, self._dimension):
                cellStrings = self._cells[r][c].Print()
                for i in range(rho):
                    strings[i] = strings[i] + cellStrings[i]
            for i in range(rho):
                print( strings[i] )

    def Set( self, r, c, n):
        self._cells[r][c].Number = n


    def RemoveCandidatesInColumnForNumber( self, column, number):
        # remove candidates in column
        for row in range( 0, self._dimension):
            if not self._cells[row][column].Solved:
                self._cells[row][column].Remove(number)        

    def RemoveCandidatesInRowForNumber( self, row, number):
        # remove candidates in column
        for column in range( 0, self._dimension):
            if not self._cells[row][column].Solved:
                self._cells[row][column].Remove(number)        

    def RemoveCandidatesInGroupForNumber( self, group, number):
        # remove candidates in group
        # TODO optimise
        for row in range( 0, self._dimension):                
            for column in range( 0, self._dimension):
                if (not self._cells[row][column].Solved) and (self._cells[row][column].Group == group):
                    self._cells[row][column].Remove(number)

    def SetPossibleCandidate(self):
        # found solved
        cellsSolved = []
        for row in range( 0, self._dimension):
            for column in range( 0, self._dimension):
                if self._cells[row][column].Solved:
                    cellsSolved.append(self._cells[row][column])

        # remove candidates
        for cell in cellsSolved:
            self.RemoveCandidatesInColumnForNumber( cell.Column, cell.Number)
            self.RemoveCandidatesInRowForNumber( cell.Row, cell.Number)
            self.RemoveCandidatesInGroupForNumber( cell.Group, cell.Number)

    def SetSinglesRow(self):
        for row in range( 0, self._dimension):
            singleCandiates = []
            for column in range( 0, self._dimension):
                if not self._cells[row][column].Solved:
                    for candidate in self._cells[row][column].Candidates:
                        if singleCandiates.count(candidate) == 0:
                            singleCandiates.append(candidate)
            for candidate in singleCandiates:
                count = 0
                cell = None
                for column in range( 0, self._dimension):
                    if (not self._cells[row][column].Solved) and self._cells[row][column].Candidates.count(candidate) == 1: 
                        count += 1
                        if count==1:
                            cell = self._cells[row][column]
                if count == 1:
                    # yahoo got one
                    cell.Number = candidate

    def SetSinglesColumn(self):
        # TODO test
        for column in range( 0, self._dimension):
            singleCandiates = []
            for row in range( 0, self._dimension):
                if not self._cells[row][column].Solved:
                    for candidate in self._cells[row][column].Candidates:
                        if singleCandiates.count(candidate) == 0:
                            singleCandiates.append(candidate)
            for candidate in singleCandiates:
                count = 0
                cell = None
                for row in range( 0, self._dimension):
                    if (not self._cells[row][column].Solved) and self._cells[row][column].Candidates.count(candidate) == 1:
                        count += 1
                        if count==1:
                            cell = self._cells[row][column]
                if count == 1:
                    # yahoo got one
                    cell.Number = candidate

    def SetSinglesGroup(self):
        # HER TIL
        # TODO
        for column in range( 0, self._dimension):
            singleCandiates = []
            for row in range( 0, self._dimension):
                if not self._cells[row][column].Solved:
                    for candidate in self._cells[row][column]:
                        if singleCandiates.count(candidate) == 0:
                            singleCandiates.append(candidate)
            for candidate in singleCandiates:
                count = 0
                cell = None
                for row in range( 0, self._dimension):
                    if (not self._cells[row][column].Solved) and self._cells[row][column].Number == candidate:
                        count += 1
                        cell = self._cells[row][column]
                if count == 1:
                    # yahoo got one
                    cell.Number = candidate


    def SetSingles(self):
        self.SetSinglesRow();
        self.SetSinglesColumn();
        

# main
shape = []
shape.append( [0,0,0,1,1,1,2,2,2] )
shape.append( [0,3,0,1,1,1,2,4,2] )
shape.append( [0,3,0,1,5,1,2,4,2] )
shape.append( [0,3,0,1,5,5,5,4,2] )
shape.append( [6,3,3,3,5,4,4,4,2] )
shape.append( [6,3,5,5,5,7,8,4,8] )
shape.append( [6,3,6,7,5,7,8,4,8] )
shape.append( [6,3,6,7,7,7,8,4,8] )
shape.append( [6,6,6,7,7,7,8,8,8] )
colours = Colours()
sudoku = Sudoku( 9, shape, colours)
sudoku.Set( 0, 0, 1)
sudoku.Set( 0, 3, 4)
sudoku.Set( 0, 8, 9)
sudoku.Set( 1, 5, 2)
sudoku.Set( 1, 8, 4)
sudoku.Set( 3, 3, 9)
sudoku.Set( 3, 4, 8)
sudoku.Set( 3, 8, 7)
sudoku.Set( 4, 1, 8)
sudoku.Set( 4, 2, 7)
sudoku.Set( 4, 4, 6)
sudoku.Set( 4, 6, 2)
sudoku.Set( 4, 7, 5)
sudoku.Set( 5, 0, 6)
sudoku.Set( 5, 4, 9)
sudoku.Set( 5, 5, 8)
sudoku.Set( 7, 0, 3)
sudoku.Set( 7, 3, 1)
sudoku.Set( 8, 0, 8)
sudoku.Set( 8, 5, 9)
sudoku.Set( 8, 8, 5)

# c = Cell(9, 0, 0, 0, colours)
# for string in c.Print():
#     print(string)
# c.Remove(5)
# for string in c.Print():
#     print(string)
# c.Number = 1
# for string in c.Print():
#     print(string)

#sudoku.Print()
sudoku.SetPossibleCandidate()
sudoku.SetSinglesColumn()
# HER TIL sudoku.SetSinglesGroup()
sudoku.Print()