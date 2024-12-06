class Enemy:
    def __init__(self, row, col, cellHeight, cellWidth):
        self._location = (row * cellHeight + cellHeight / 2, col * cellWidth + cellWidth / 2)
        self._row = row
        self._col = col
        self._oldRow = row
        self._oldCol = col
        self._direction = "right"
        self._isAttacking = False
        self._attackCool = 0.5
        self._lastAttackTime = 0

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, newLocation):
        self._location = newLocation

    def updateLocation(self, dy, dx):
        y, x = self._location
        self._location = (y + dy, x + dx)

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
    def isAttacking(self):
        return self._isAttacking

    @isAttacking.setter
    def isAttacking(self, state):
        self._isAttacking = state

    @property
    def attackCool(self):
        return self._attackCool

    @property
    def lastAttackTime(self):
        return self._lastAttackTime

    @lastAttackTime.setter
    def lastAttackTime(self, time):
        self._lastAttackTime = time

    def canAttack(self, currentTime):
        return not self._isAttacking or (currentTime - self._lastAttackTime >= self._attackCool)

    def getPosition(self):
        return self._row, self._col

    def getPreviousPosition(self):
        return self._oldRow, self._oldCol
