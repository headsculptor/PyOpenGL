import math
class Grids:
    def __init__(self):
        self.length = 5
        self.height = 5
        self.gridmap = self.newGrid()
        self.active_grids = []
        self.active_symbol = '■'
        self.inactive_symbol = '□'
        return None
    def size(self, length, height):
        try:
            self.length = int(length)
            self.height = int(height)
            return True
        except:
            return False
    def newGrid(self):
        gridmap = []
        row = []
        for y in range(self.length):
            row.append(0)
        for x in range(self.height):
            gridmap.append(row)
        return gridmap
    def resetGrid(self):
        self.gridmap = self.newGrid()
        return True
    def getGridString(self, active_symbol = '■', inactive_symbol = '□'):
        try:
            self.active_symbol = str(active_symbol)
            self.inactive_symbol = str(inactive_symbol)
            grid_string = ''
            for x in range(self.height):
                for y in range(self.length):
                    if [y+1,x+1] in self.active_grids:
                        grid_string += self.active_symbol
                    else:
                        grid_string += self.inactive_symbol
                    grid_string += ' '
                grid_string += '\n'
            return grid_string
        except:
            return False
    def setGrid(self, gridx, gridy, active):
        if active:
            if [gridx, self.height-gridy+1] not in self.active_grids:
                self.active_grids.append([gridx, self.height-gridy+1])
        else:
            if [gridx, self.height-gridy+1] in self.active_grids:
                self.active_grids.pop(self.active_grids.index([gridx, self.height-gridy+1]))
        return True
    def getLength(self):
        return self.length
    def getHeight(self):
        return self.height
    def drawLine(self, startx, starty, endx, endy):
        if endx-startx != 0 and endy-starty != 0:
            gradient = (endy-starty)/(endx-startx)
        else:
            gradient = 0
            #y = mx + c
            constant = starty - gradient*startx
            print(constant)
            if endx-startx > 0:
                for x in range((endx+1)-startx):
                    y = gradient*(x+startx) + constant
                    y = math.floor(y)
                    self.setGrid(x+startx, y, active = True)
            elif endx-startx < 0:
                for x in range((startx+1)-endx):
                    y = gradient*(endx-x) + constant
                    y = math.floor(y)
                    self.setGrid(endx-x, y, active = True)
        return True
    def existsGrid(self, gridx, gridy):
        if gridx <= self.getLength() and gridx > 0:
            if gridy <= self.getHeight() and gridy > 0:
                return True
        return False
    def checkGrid(self, gridx, gridy):
        if self.existsGrid(gridx, gridy):
            tempstring = self.getGridString()
            templist = tempstring.split('\n')
            temprow = templist[len(templist)-gridy-1]
            tempchar = temprow[gridx-1]
            if tempchar == self.active_symbol:
                return True
            else:
                return False
        else:
            return None
