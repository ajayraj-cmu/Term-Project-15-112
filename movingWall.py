class MovingWall:
    def __init__(self, row, col, cellHeight, cellWidth, direction, cutout):
        self._location = (row * cellHeight + cellHeight / 2, col * cellWidth + cellWidth / 2)
        self._row = row
        self._col = col
        self._oldRow = row
        self._oldCol = col
        self._direction = direction
        self._cutout = cutout
        self._width = cellWidth // 2
        self._hitCool = 4
        self._lastHit = 0

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, newLocation):
        self._location = newLocation

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, newRow):
        self._oldRow = self._row
        self._row = newRow

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, newCol):
        self._oldCol = self._col
        self._col = newCol

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, newDirection):
        self._direction = newDirection

    @property
    def cutout(self):
        return self._cutout

    @cutout.setter
    def cutout(self, newCutout):
        self._cutout = newCutout

    @property
    def width(self):
        return self._width

    @property
    def hitCool(self):
        return self._hitCool

    @property
    def lastHit(self):
        return self._lastHit

    @lastHit.setter
    def lastHit(self, time):
        self._lastHit = time

    def getPosition(self):
        return self._row, self._col

    def getPreviousPosition(self):
        return self._oldRow, self._oldCol

    def updateLocation(self, dy, dx):
        y, x = self._location
        self._location = (y + dy, x + dx)
