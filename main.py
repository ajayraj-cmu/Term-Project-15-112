from cmu_graphics import *
from math import *
import copy
import random
from PIL import Image, ImageOps
import time
from enemy import Enemy
from movingWall import MovingWall
from leaderBoard import bestScores

#DFS BackTracking Algorithm  
def generateMaze(width, height):
    row=[1 for i in range(width)]
    maze = [copy.copy(row) for j in range(height)]

    def carvingPath(y, x):
        maze[y][x] = 0
        possibleDirections = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(possibleDirections)
        
        for dx, dy in possibleDirections:
            newXPos = x + dx
            newYPos = y + dy
            if (0 <= newXPos < width and 0 <= newYPos < height and maze[newYPos][newXPos] == 1):
                maze[y + dy // 2][x + dx // 2] = 0
                carvingPath(newYPos, newXPos)
    
    carvingPath(1, 1)
    
    maze[1][1] = 0
    maze[1][2] = 0
    maze[2][1] = 0

    maze[width-1][height-1]=0
    maze[width-2][height-1]=0
    maze[width-1][height-2]=0
    return maze
 #Calculations inspired by: https://stackoverflow.com/questions/77464377/solution-of-maze

#Places enemies on 2-D board for maze
def generateEnemies(app, maze, numOfEnemies):
    counter=numOfEnemies
    while counter>0:
        row=random.randint(0, app.mazeHeight-1)
        col=random.randint(0, app.mazeWidth-1)
        if maze[row][col]==0 and enemyNeighbours(app, maze, row, col)==False:
            maze[row][col]=2
            counter-=1

    return maze

#Checks to see valid enemy placements (distanced)
def enemyNeighbours(app, maze, row, col):
    if maze[row][col]!=0:
        return False
    directions=[(1,1), (0,1), (1,0), (-1,1), (1,-1), (-1,-1), (0,-1), (-1,0)]
    for drow, dcol in directions:
        for i in range(1):
            if 0<=row+i*drow<app.rows and 0<=col+i*dcol<app.cols and maze[row+i*drow][col+i*dcol]==2:
                return True
    return False

#Checks to see valid wall placements (distanced)
def neighbourWalls(app, maze, row, col):
    if maze[row][col]!=0:
        return False
    directions=[(0,1), (1,0),(0,-1), (-1,0)]
    for drow, dcol in directions:
        for i in range(1):
            if 0<=row+i*drow<app.rows and 0<=col+i*dcol<app.cols and (maze[row+i*drow][col+i*dcol]==1):
                return True
    return False

#Places enemies on 2-D board for maze
def placeMovingWalls(app, maze, numOfWalls):
    counter=numOfWalls
    while counter>0:
        row=random.randint(0, app.mazeHeight-1)
        col=random.randint(0, app.mazeWidth-1)
        if maze[row][col]==0 and neighbourWalls(app, maze, row, col)==False:
            maze[row][col]=3
            counter-=1
    return maze

#Checks to see valid moving wall placements (distanced)
def movingWallDirection(app, row,col):
    if 0<=row<app.rows and 0<=col+1<app.cols and app.maze[row][col+1]!=1:
        return "side+"
    elif 0<=row<app.rows and 0<=col-1<app.cols and app.maze[row][col-1]!=1:
        return "side-"
    if 0<=row+1<app.rows and 0<=col<app.cols and app.maze[row+1][col]!=1:
        return "up+"
    elif 0<=row-1<app.rows and 0<=col<app.cols and app.maze[row-1][col]!=1:
        return "up-"
    
def onAppStart(app):
    app.currentScreen = 'start'  
    resetApp(app)

def resetApp(app):
    #Game Stat Vars
    app.win = False
    app.hit = False
    app.timer = 0 #Also referenced as the score
    app.health = 1000
    app.killCount = 0
    app.finalScore = 0
    app.isPaused = False
    app.scoresList=[]
    

    #End Game
    app.endGame = False
    app.gameStarted = False  

    #Shape-Drawing Variables
    app.pattern = []
    app.xValues = []
    app.yValues = []
    app.isValid = False
    app.shapes = ['Square', 'Triangle', 'Circle']
    app.currentShape = random.choice(app.shapes)
    app.message = f"Draw a {app.currentShape}"

    #Maze
    app.mazeWidth = 10
    app.mazeHeight = 10
    app.maze = generateMaze(app.mazeWidth, app.mazeHeight)
    app.time=0
    app.stepsPerSecond=220

    
    #Board vars
    app.rows = len(app.maze)
    app.cols = len(app.maze[0])
    app.boardLeft = 0
    app.boardTop = 0
    app.boardWidth = 400
    app.boardHeight = 400
    app.cellWidth=app.boardWidth/app.cols
    app.cellHeight=app.boardHeight/app.rows

    #Enemies and Moving Walls
    app.enemies=[]
    app.numOfEnemies=app.rows*(2)
    app.numOfMovingWalls=app.rows
    app.directionIncrement=5
    app.maze=generateEnemies(app, app.maze, app.numOfEnemies)
    app.maze=placeMovingWalls(app, app.maze, app.numOfMovingWalls)

    #Player vars
    app.playerX=int(1/app.cols * 400)+1/2*app.cellWidth
    app.playerY=int(1/app.rows * 400)+1/2*app.cellHeight
    app.playerAngle=pi/2
    app.step=3
    app.dx=0
    app.dy=0
    app.playerRadius=3.5
    app.currentRow=int(app.playerY//app.cellHeight)
    app.currentCol=int(app.playerX//app.cellWidth)

    #Storing Enemy Info
    app.enemies = []
    for row in range(len(app.maze)):
        for col in range(len(app.maze[0])):
            if app.maze[row][col] == 2 and (row,col) != (app.playerX//app.cols, app.playerY//app.rows):
                app.enemies.append(Enemy(row, col, app.cellHeight, app.cellWidth))


            
    #Storing Moving Wall Info
    app.movingWalls = []
    for row in range(len(app.maze)):
        for col in range(len(app.maze[0])):
            if (app.maze[row][col] == 3 and 
                (row, col) != (app.playerX//app.cols, app.playerY//app.rows)):
                direction = movingWallDirection(app, row, col)
                cutout = random.choice([0, 1])
                app.movingWalls.append(
                    MovingWall(row, col, app.cellHeight, app.cellWidth, direction, cutout)
                )


    #Raycasting Variables:
    app.FOV=pi/3

    #All Textures and Images:

    #Cover Screen: Made Usign GPT Image Gen.
    app.coverScreen=CMUImage(Image.open("newCoverScreen.png").resize((400,400)))

    #Created using GPT Image Generation
    app.wall=Image.open("wall.png").resize((400, 400))

    #Created using GPT Image Generation
    app.enemy="cmu://872300/35360434/Screenshot+2024-12-01+at+11.14.48AM.png"

    #Created using GPT Image Generation
    app.enemy=CMUImage(Image.open("enemy.png").resize((400,400)))

    #Created using GPT Image Generation
    app.endScreen=CMUImage(Image.open("endOfGame.png").resize((400,400)))

    #Created using GPT Image Generation
    app.wallTwo=Image.open("wallTwo.png").resize((400, 400))

    #Created using GPT Image Generation
    app.winScreen=CMUImage(Image.open("winScreen.png").resize((400,400)))


def drawStartScreen(app):
    drawImage(app.coverScreen, 0, 0, width=400, height=400)
    drawRect(125, 250, 150, 40, fill=gradient('red', 'blue', 'orange', 'purple', start='left'), 
            border='black', borderWidth=5)
    drawRect(127, 252, 146, 36, fill=None, border='yellow', borderWidth=1)  # Glow effect
    drawLabel('Start', 200, 270, fill='yellow', size=30, bold=True)

def drawMenuScreen(app):
    drawRect(0, 0, 400, 400, fill=gradient('purple', 'blue', 'pink', start='left'))
    drawRect(50, 30, 300, 60, fill=gradient('purple', 'blue'), align='center')
    drawLabel('MAZE RUNNER', 200, 60, size=35, bold=True, fill='yellow')
    drawRect(50, 120, 300, 200, fill=gradient('blue', 'purple', start='top'))
    drawLabel('MISSION OBJECTIVES:', 200, 140, size=20, bold=True, fill='yellow')
    y = 180
    rules = [
        '1) Kill 20+ enemies & find portal (false wall)',
        '2) Avoid enemies & moving walls',
        '3) Draw shapes to defeat enemies',
        '4)The lower the points for a win, the better'
    ]
    for rule in rules:
        drawRect(25, y-15, 350, 30, fill='blue')
        drawLabel(rule, 200, y, fill='white', size=16, bold=True)
        y += 40
    drawRect(100, 330, 200, 50, 
            fill=gradient('purple', 'blue', 'pink', start='left'),
            border='white', borderWidth=2)
    drawLabel('Start Game', 200, 355, size=25, bold=True, fill='cyan')

def drawGameScreen(app):
    if app.hit == False:
        drawRect(0, 0, 400, 400, fill=gradient('purple', 'blue', 'pink', start='left'))
    else:
        drawRect(0, 0, 400, 400, fill="red")
    castFullMaze(app)
    #Draw Pattern for killing enemies
    for i in range(1, len(app.pattern)):
        currX, currY = app.pattern[i]
        lastX, lastY = app.pattern[i - 1]
        drawLine(lastX, lastY, currX, currY, fill='cyan', lineWidth=10)
    drawRect(0, 0, 400, 50, fill='black', opacity=70)
    drawLabel(f'HP: {app.health}', 50, 25, fill="yellow", size=18, bold=True)
    drawLabel(f'Score: {app.timer}', 150, 15, fill="white", size=18, bold=True)
    drawLabel(f'Kills: {app.killCount}', 150, 35, fill="white", size=18, bold=True)
    drawLabel(app.message, 300, 25, fill='orange', size=18, bold=True)
    drawRect(20, 60, 60, 30, fill='white', opacity=80)
    drawLabel('PAUSE', 50, 75, fill='black', bold=True, size=16)

def drawEndScreen(app):
    if app.win == False:
        drawImage(app.endScreen, 0, 0, width=400, height=400)
        drawLabel('Game Over', 200, 125, size=30, fill='white')
        drawLabel(f'Your Score Was: {app.finalScore}', 200, 200, size=25, fill='yellow')
        top_scores = sorted(set(app.scoresList), reverse=True)[:3]
        for i in range(3):
            score = top_scores[i] if i < len(top_scores) else None
            drawLabel(f"Top {i + 1} Score: {score if score is not None else 'None'}", 200, 230 + (i * 30), size=20, fill='white')
        drawRect(150, 320, 100, 40, fill='gray')
        drawLabel('Restart', 200, 340, fill='white')
    else:
        drawImage(app.winScreen, 0, 0, width=400, height=400)
        drawLabel('Congrats You Won', 200, 125, size=30, fill='yellow')
        drawLabel(f'Your Score Was: {app.finalScore}', 200, 200, size=25, fill='yellow')
        top_scores = sorted(set(app.scoresList), reverse=True)[:3]
        for i in range(3):
            score = top_scores[i] if i < len(top_scores) else None
            drawLabel(f"Top {i + 1} Score: {score if score is not None else 'None'}", 200, 230 + (i * 30), size=20, fill='white')
        drawRect(150, 320, 100, 40, fill='gray')
        drawLabel('Restart', 200, 340, fill='white')


def redrawAll(app):
    if app.endGame:
        drawEndScreen(app)
    elif app.currentScreen == 'start':
        drawStartScreen(app)
    elif app.currentScreen == 'menu':
        drawMenuScreen(app)
    elif app.currentScreen == 'game':
        drawGameScreen(app)
        if app.isPaused:
            drawRect(0, 0, 400, 400, fill='black', opacity=50)
            drawLabel('PAUSED', 200, 200, size=40, fill='white', bold=True)
            drawLabel('Click anywhere to resume', 200, 250, size=20, fill='white')
def onMousePress(app, mouseX, mouseY):
    if app.endGame:
        if (150 <= mouseX <= 250 and 320 <= mouseY <= 360): 
            app.currentScreen = 'start'
            resetApp(app)
    elif app.currentScreen == 'start':
        if (125 <= mouseX <= 275 and 250 <= mouseY <= 290):
            app.currentScreen = 'menu'
    elif app.currentScreen == 'menu':
        if (100 <= mouseX <= 300 and 330 <= mouseY <= 380):
            app.currentScreen = 'game'
            app.gameStarted = True  
    elif app.currentScreen == 'game':
        if (20 <= mouseX <= 80 and 60 <= mouseY <= 90):
            app.isPaused = not app.isPaused
        elif app.isPaused:
            app.isPaused = False  


#Used for tracing
def onMouseDrag(app, mouseX, mouseY):
    app.yValues.append(mouseY)
    app.xValues.append(mouseX)
    app.pattern.append((mouseX, mouseY))

#Checks if any enemies are killed
def onMouseRelease(app, mouseX, mouseY):
    checkValid(app)
    app.xValues = []
    app.yValues = []
    if app.isValid:
        app.currentShape = random.choice(app.shapes)
        app.message = f"Success. Draw a {app.currentShape}"
 
    enemiesToRemove = []
    for enemy in app.enemies:
        enemyNumber = 0
        # Access location property correctly
        enemyY, enemyX = enemy.location  # Correctly use the location property
        dx = enemyX - app.playerX
        dy = enemyY - app.playerY
        distanceToEnemy = sqrt(dx**2 + dy**2)
        angleToEnemy = (atan2(dy, dx) - app.playerAngle) % (2 * pi)
        if angleToEnemy > pi:
            angleToEnemy -= 2 * pi  
        if abs(angleToEnemy) < app.FOV / 2:
            enemyScreenX = app.boardWidth / 2 + (angleToEnemy / (app.FOV / 2)) * (app.boardWidth / 2)
            if distanceToEnemy == 0:
                enemySize = app.height
            else:
                enemySize = (app.height * 8) / distanceToEnemy   
            enemyLeft = enemyScreenX - enemySize / 2
            enemyTop = (app.height - enemySize) / 2
            leftBound = enemyLeft - 10
            rightBound = enemyLeft + enemySize + 10
            upperBound = enemyTop - 10
            lowerBound = enemySize + enemyTop + 10
            eliminateEnemy = False
            for x, y in app.pattern:
                if leftBound <= x <= rightBound and upperBound <= y <= lowerBound:
                    eliminateEnemy = True
                    break      
            if eliminateEnemy and app.isValid:
                enemiesToRemove.append(enemy)   
    for enemy in enemiesToRemove:
        if enemy in app.enemies: 
            removeRow = enemy.row  # Access row property
            removeCol = enemy.col  # Access col property
            app.maze[removeRow][removeCol] = 0
            app.enemies.remove(enemy)
            app.killCount += 1
        counter = 1
        while counter > 0:
            row = random.randint(0, app.rows - 1)
            col = random.randint(0, app.cols - 1)
            if app.maze[row][col] == 0 and enemyNeighbours(app, app.maze, row, col) == False and (row, col) != (enemy.row, enemy.row):
                app.maze[row][col] = 2
                app.enemies.append(Enemy(row, col, app.cellHeight, app.cellWidth))  # Use the updated Enemy class
                counter -= 1
    app.pattern = []
    app.isValid = False

#Checks if valid pattern is drawn
def checkValid(app):
    app.isValid=False
    if len(app.pattern) == 0:
        app.isValid = False
        app.message = f"Not a valid {app.currentShape}"
        return
    tempPattern = copy.copy(app.pattern)
    leftX = min(app.xValues)
    rightX = max(app.xValues)
    minY = min(app.yValues)
    maxY = max(app.yValues)
    width = rightX - leftX
    height = maxY - minY
    # To make the epsilon relative to the size of the shape (after trial-testing)
    epsilon = min(height, width) * 0.4
    if width == 0 or height == 0:
        app.isValid = False
        app.message = f'Not a Valid {app.currentShape}!'
        return
    if app.currentShape == 'Square':
        sampleShape = generateSampleSquare(app, width, leftX, minY, 150)
    elif app.currentShape == 'Triangle':
        sampleShape = generateSampleTriangle(app, width, height, leftX, minY, 150)
    elif app.currentShape == 'Circle':
        radius = width / 2
        centerX = (leftX + rightX) / 2
        centerY = (minY + maxY) / 2
        if radius == 0:
            app.isValid = False
            app.message = "Not a Valid Circle!"
            return
        sampleShape = generateSampleCircle(app, radius, centerX, centerY, 150)
    app.isValid = True
    for (trueX, trueY) in sampleShape:
        closePoint = False
        for (drawX, drawY) in tempPattern:
            if dist((trueX, trueY), (drawX, drawY)) <= epsilon:
                closePoint = True
                break
        if not closePoint:
            app.isValid = False
            break
    distances = []
    for (trueX, trueY) in sampleShape:
        minDistance = 1000
        for (drawX, drawY) in tempPattern:
            distance = dist((trueX, trueY), (drawX, drawY))
            if distance < minDistance:
                minDistance = distance
        distances.append(minDistance)
    averageDistanceCurrent = sum(distances) / len(distances)
    accurateShape = True
    for shape in ['Square', 'Triangle', 'Circle']:
        if shape != app.currentShape:
            if shape == 'Square':
                sampleShape = generateSampleSquare(app, width, leftX, minY, 150)
            elif shape == 'Triangle':
                sampleShape = generateSampleTriangle(app, width, height, leftX, minY, 150)
            elif shape == 'Circle':
                radius = width / 2
                centerX = (leftX + rightX) / 2
                centerY = (minY + maxY) / 2
                sampleShape = generateSampleCircle(app, radius, centerX, centerY, 150)
            distances = []
            for (trueX, trueY) in sampleShape:
                minDistance = 1000
                for (drawX, drawY) in tempPattern:
                    distance = dist((trueX, trueY), (drawX, drawY))
                    if distance < minDistance:
                        minDistance = distance
                distances.append(minDistance)
            averageDistanceOther = sum(distances) / len(distances)
            if averageDistanceCurrent >= averageDistanceOther:
                accurateShape = False
                break
    app.isValid = accurateShape
    if app.isValid:
        app.message = f"Valid {app.currentShape}!"
    else:
        app.message = f"Not a Valid {app.currentShape}!"

#Creates basis square to compare drawn pattern to
def generateSampleSquare(app, sideLength, leftX, minY, numPoints):
    points = []
    halfSideLength = sideLength / 2
    centerX, centerY = leftX + halfSideLength, minY + halfSideLength 
    sideLengthPoints = numPoints // 4  
    leftX=centerX - halfSideLength
    constantY=centerY - halfSideLength 
    for i in range(sideLengthPoints):
        x = leftX + (i / sideLengthPoints) * sideLength
        y = constantY
        points.append((x, y))
    constantX=centerX + halfSideLength 
    topY=centerY - halfSideLength
    for i in range(sideLengthPoints):
        x = constantX
        y =topY+ (i / sideLengthPoints) * sideLength
        points.append((x, y))
    constantY=centerY + halfSideLength
    rightX=centerX + halfSideLength
    for i in range(sideLengthPoints):
        x = rightX - (i / sideLengthPoints) * sideLength
        y = constantY 
        points.append((x, y))
    constantX=centerX
    bottomY=centerY + halfSideLength
    for i in range(sideLengthPoints):
        x = constantX - halfSideLength 
        y = bottomY - (i / sideLengthPoints) * sideLength
        points.append((x, y))
    return points

#Creates basis triangle to compare drawn pattern to
def generateSampleTriangle(app, width, height, leftX, minY, numPoints):
    points = []
    pointsPerSide = numPoints // 3
    for i in range(pointsPerSide):
        x = leftX + (i / pointsPerSide) * width
        y = minY + height
        points.append((x, y))
    topX = leftX + width / 2
    for i in range(pointsPerSide):
        x = leftX + width - (i / pointsPerSide) * (width / 2)
        y = minY + height - (i / pointsPerSide) * height
        points.append((x, y))
    for i in range(pointsPerSide):
        x = leftX + (i / pointsPerSide) * (width / 2)
        y = minY + height - (i / pointsPerSide) * height
        points.append((x, y))
    return points

#Creates basis circle to compare drawn pattern to
def generateSampleCircle(app, radius, centerX, centerY, numPoints):
    points = []
    for i in range(numPoints):
        angle = (i/numPoints)*(2 * pi)
        x = centerX + radius * cos(angle)
        y = centerY + radius * sin(angle)
        points.append((x, y))
    return points


def onStep(app):
    if app.currentScreen == 'game' and app.gameStarted and not app.isPaused:
        if app.health <= 0 or app.win:
            app.finalScore = app.timer  
            if app.win==True:
                bestScoreInstance = bestScores(app.finalScore)  
                app.scoresList = bestScoreInstance.bestThreeScores()  
            app.endGame = True
        else:
            app.time+=1
            if app.time%5==0:
                pathFinding(app)
                movingWalls(app)
            if app.time%60==0:
                app.timer+=1
            if app.timer%15==0:
                app.stepsPerSecond+=10


def ColandRow(app, location):
    y, x = location  
    row = int(y // app.cellHeight)
    col = int(x // app.cellWidth)
    return (row, col)

#Initiates pathfinding for enemies towards the player in the maze
def pathFinding(app):
    hitOnce=False
    enemyRadius = 8
    playerRow = int(app.playerY // app.cellHeight)
    playerCol = int(app.playerX // app.cellWidth)
    minimumDistance = 10
    minDistanceToPlayer = 10
    enemySpeed = 0.5

    for enemy in app.enemies:
        app.directionIncrement = 5
        enemyY, enemyX = enemy.location
        currentRow, currentCol = ColandRow(app, (enemyY, enemyX))
        directions = ["right", "left", "up", "down"]
        bestDistance = float('inf')
        bestDirection = None
        targetX, targetY = enemyX, enemyY
        currentDistanceToPlayer = calculateDistance(enemyX, enemyY, app.playerX, app.playerY)
        bestDirection = None
        bestMove = None
        distanceToPlayer = currentDistanceToPlayer

        for direction in directions:
            newX, newY = enemyX, enemyY
            if direction == "right":
                newX += app.directionIncrement
            elif direction == "left":
                newX -= app.directionIncrement
            elif direction == "down":
                newY += app.directionIncrement
            elif direction == "up":
                newY -= app.directionIncrement

            newRow, newCol = ColandRow(app, (newY, newX))
            if not (0 <= newCol < app.cols and 0 <= newRow < app.rows):
                continue

            wallCollision = False
            for yBound, xBound in [
                (newY - app.mazeWidth / 2, newX - app.mazeWidth / 2),
                (newY + app.mazeWidth / 2, newX - app.mazeWidth / 2),
                (newY - app.mazeWidth / 2, newX + app.mazeWidth / 2),
                (newY + app.mazeWidth / 2, newX + app.mazeWidth / 2)
            ]:
                checkRow = int(yBound // app.cellHeight) % app.rows
                checkCol = int(xBound // app.cellWidth) % app.cols
                if app.maze[checkRow][checkCol] == 1:
                    wallCollision = True
                    break
            if wallCollision:
                continue

            tooClose = False
            for other in app.enemies:
                if other != enemy:
                    otherY, otherX = other.location
                    distanceToOtherEnemy = calculateDistance(newX, newY, otherX, otherY)
                    if distanceToOtherEnemy < minimumDistance:
                        tooClose = True
                        break

            distanceToPlayer = calculateDistance(newX, newY, app.playerX, app.playerY)
            if distanceToPlayer < minDistanceToPlayer:
                continue

            if not tooClose:
                distance = calculateDistance(newX, newY, app.playerX, app.playerY)
                if distance < bestDistance:
                    bestDistance = distance
                    bestDirection = direction
                    bestMove = (newX, newY)

        if bestMove is None:
            bestMove = (enemyX, enemyY)
            directions = ["right", "left", "up", "down"]
            bestDirection = random.choice(directions)
            enemy.direction = bestDirection
            if bestDirection == "right":
                bestMove = (enemyX + app.directionIncrement, enemyY)
            elif bestDirection == "left":
                bestMove = (enemyX - app.directionIncrement, enemyY)
            elif bestDirection == "down":
                bestMove = (enemyX, enemyY + app.directionIncrement)
            elif bestDirection == "up":
                bestMove = (enemyX, enemyY - app.directionIncrement)

        # Calculate damage when the player is too close
        if distanceToPlayer < enemyRadius:
            currentTime = time.time()
            if enemy.canAttack(currentTime):
                app.health -= 20
                enemy.lastAttackTime = currentTime
                enemy.isAttacking = True
                hitOnce=True  # Player is hit

        enemy.updateLocation(
            (bestMove[1] - enemyY) * enemySpeed,
            (bestMove[0] - enemyX) * enemySpeed
        )

    if app.health <= 0:
        app.endGame = True
    if hitOnce==True:
        app.hit=True
    else:
        app.hit=False

def calculateDistance(currentX, currentY, playerX, playerY):
    return sqrt((playerX-currentX)**2 + (playerY-currentY)**2)

#Moves walls across corridors
def movingWalls(app):
    hitOnce=False
    wallSpeed = 0.3
    playerX, playerY = app.playerX, app.playerY
    playerRadius = app.cellWidth / 4
    
    for wall in app.movingWalls:
        y, x = wall.location
        direction = wall.direction
        moveDistance = 8
        wallRadius = app.cellWidth / 4
        targetY, targetX = y, x
        distance = ((playerX - x) ** 2 + (playerY - y) ** 2) ** 0.5
        
        if distance <= 5:
            app.health -= 5
            currentTime = time.time()
            if currentTime - wall.lastHit >= 4:
                app.health -= 5
                wall.lastHit = currentTime
                hitOnce=True

        if direction == "side+":
            targetX += moveDistance
        elif direction == "side-":
            targetX -= moveDistance
        elif direction == "up+":
            targetY += moveDistance
        elif direction == "up-":
            targetY -= moveDistance

        wallCollision = False
        points = [
            (targetY, targetX - wallRadius),
            (targetY, targetX + wallRadius),
            (targetY - wallRadius, targetX),
            (targetY + wallRadius, targetX)
        ]
        
        for checkY, checkX in points:
            checkRow = int(checkY // app.cellHeight)
            checkCol = int(checkX // app.cellWidth)
            if 0 <= checkRow < app.rows and 0 <= checkCol < app.cols:
                if app.maze[checkRow][checkCol] == 1:
                    wallCollision = True
                    break

        if not wallCollision:
            wall.location = (
                y + (targetY - y) * wallSpeed,
                x + (targetX - x) * wallSpeed
            )
        else:
            if direction == "side+":
                wall.direction = "side-"
            elif direction == "side-":
                wall.direction = "side+"
            elif direction == "up+":
                wall.direction = "up-"
            elif direction == "up-":
                wall.direction = "up+"

        newRow, newCol = ColandRow(app, (targetX, targetY))
        wall.row = newRow
        wall.col = newCol

    if app.health <= 0:
        app.endGame = True

    if hitOnce==True:
        app.hit=True

#Checks for valid wall movement
def checkWallsinDirection(app, direction, row, col):
    if direction=="side+":
        if 0<=row<app.rows and 0<=col+1<app.cols and app.maze[row][col+1]!=1:
            return True
        else:
            return False
    elif direction=="side-":
        if 0<=row<app.rows and 0<=col-1<app.cols and app.maze[row][col-1]!=1:
            return True
        else:
            return False
    elif direction=="up+":
        if 0<=row+1<app.rows and 0<=col<app.cols and app.maze[row+1][col]!=1:
            return True
        else:
            return False
    elif direction=="up-":
        if 0<=row-1<app.rows and 0<=col<app.cols and app.maze[row-1][col]!=1:
            return True
        else:
            return False

#Only utilized mathematical explanation (base-level) from this video: https://www.youtube.com/watch?v=NbSee-XM7WA&t=444s
#Also inspired by DDA Algorithm
def castFullMaze(app):
    renderQueue = []  

    rayCount =230
    rayAngleIncrement = app.FOV / rayCount

    for i in range(rayCount):
        currentRayAngle = (app.playerAngle - app.FOV / 2 + i * rayAngleIncrement) % (2 * pi)
        rayXComp = cos(currentRayAngle)
        rayYComp = sin(currentRayAngle)

        currentMazeLocationRow = app.playerY // app.cellHeight
        currentMazeLocationCol = app.playerX // app.cellWidth

        currentRow = int(currentMazeLocationRow)
        currentCol = int(currentMazeLocationCol)

        playerPosX = app.playerX
        playerPosY = app.playerY

        while True:
            if (currentCol < 0 or currentCol >= app.cols or
                currentRow < 0 or currentRow >= app.rows or
                app.maze[currentRow][currentCol] == 1):     
                
                distanceToWall = sqrt((playerPosX - app.playerX)**2 + (playerPosY - app.playerY)**2)
                newDistance = distanceToWall * cos((currentRayAngle - app.playerAngle) % (2 * pi))  #Fisheye distortion
                if newDistance==0:
                    newDistance=0.001
                wallHeight = (app.height * 15) / newDistance

                color="Blue"
                if (playerPosX//app.cellWidth==app.cols-1 or playerPosX//app.cellWidth==app.cols-2) or (playerPosY//app.cellHeight==app.rows-1 or playerPosY//app.cellHeight==app.rows-2):
                    color="Red"
                     

                #GPT gave me logic to add my existing elements to a renderQue (to make smoother rendering)
                renderQueue.append({
                    "type": "wall",
                    "distance": newDistance,
                    "sliceIndex": i,
                    "topOfWall": (app.height - wallHeight) / 2,
                    "sliceWidth": app.boardWidth / rayCount,
                    "wallHeight": wallHeight,
                    "color": color
                })
                break

            # Advance ray
            if rayXComp > 0:
                nextGridLineDist = app.cellWidth * (currentCol + 1) - playerPosX
                mazeStepX = 1
                rayXDistance = nextGridLineDist / rayXComp
            elif rayXComp < 0:
                nextGridLineDist = playerPosX - app.cellWidth * currentCol
                mazeStepX = -1
                rayXDistance = nextGridLineDist / -rayXComp
            else:
                rayXDistance = float('inf')

            if rayYComp > 0:
                nextGridLineDist = app.cellHeight * (currentRow + 1) - playerPosY
                mazeStepY = 1
                rayYDistance = nextGridLineDist / rayYComp
            elif rayYComp < 0:
                nextGridLineDist = playerPosY - app.cellHeight * currentRow
                mazeStepY = -1
                rayYDistance = nextGridLineDist / -rayYComp
            else:
                rayYDistance = float('inf')

            if rayXDistance < rayYDistance:
                currentCol += mazeStepX
                playerPosX += rayXDistance * rayXComp
                playerPosY += rayXDistance * rayYComp
            else:
                currentRow += mazeStepY
                playerPosX += rayYDistance * rayXComp
                playerPosY += rayYDistance * rayYComp

    for enemy in app.enemies:
       enemyY, enemyX = enemy.location
       dx = enemyX - app.playerX
       dy = enemyY - app.playerY
       distanceToEnemy = sqrt(dx**2 + dy**2)
       angleToEnemy = (atan2(dy, dx) - app.playerAngle) % (2 * pi)
       
       if angleToEnemy > pi:
           angleToEnemy -= 2 * pi

       if abs(angleToEnemy) < app.FOV / 2:
           enemyScreenX = app.boardWidth / 2 + (angleToEnemy / (app.FOV / 2)) * (app.boardWidth / 2)
           enemySize = app.height if distanceToEnemy == 0 else (app.height * (app.rows)) / distanceToEnemy
           enemyLeft = enemyScreenX - enemySize / 2
           enemyTop = (app.height - enemySize) / 2
           
           renderQueue.append({
               "type": "enemy",
               "distance": distanceToEnemy,
               "left": enemyLeft,
               "top": enemyTop,
               "size": enemySize
           })
    for wall in app.movingWalls:
        wallY, wallX = wall.location
        dx = wallX - app.playerX
        dy = wallY - app.playerY
        distanceToWall = sqrt(dx**2 + dy**2)
        angleToWall = (atan2(dy, dx) - app.playerAngle) % (2 * pi)
        
        if angleToWall > pi:
            angleToWall -= 2 * pi
            
        if abs(angleToWall) < app.FOV / 2:
            wallScreenX = app.boardWidth / 2 + (angleToWall / (app.FOV / 2)) * (app.boardWidth / 2)
            wallSize = (app.mazeWidth) + (app.height * app.rows) / max(distanceToWall, 1e-5)
            wallLeft = wallScreenX - wallSize / 2
            wallTop = (app.height - wallSize) / 2
            
            renderQueue.append({
                "type": "movingWall",
                "distance": distanceToWall,
                "left": wallLeft,
                "top": wallTop,
                "size": wallSize,
                "cutout": wall.cutout
            })
    renderQueue.sort(key=lambda item: item["distance"], reverse=True)
    #I designed overall logic, GPT have me logic to use renderQue (and to also render closer objects first in the maze)
    for item in renderQueue:
        if item["type"] == "wall":
            if item["color"]!="red":
                croppedImage=app.wallTwo.crop((int(item["sliceIndex"] * item["sliceWidth"]),item["topOfWall"], int(item["sliceIndex"] * item["sliceWidth"])+item["sliceWidth"], item["topOfWall"]+item["wallHeight"]))
                borderedImage=CMUImage(ImageOps.expand(croppedImage,border=(0,3,0,3), fill="Gold"))
                drawImage(borderedImage, int(item["sliceIndex"] * item["sliceWidth"]), item["topOfWall"])
            else:
               drawRect(int(item["sliceIndex"] * item["sliceWidth"]), item["topOfWall"], item["sliceWidth"], item["wallHeight"], fill="red")
        elif item["type"] == "enemy":
            drawImage(app.enemy,item["left"], item["top"], width=item["size"], height=item["size"])
        elif item["type"] == "movingWall":
            cutout = item["cutout"]  
            wall = app.wall.resize((400, 400))
            width, height = wall.size
            halfWidth = width // 2
            wallSize = item["size"]
            if cutout == 1:
                leftHalf = wall.crop((0, 0, halfWidth, height))
                leftHalf = CMUImage(leftHalf)
                drawImage(leftHalf, item["left"] - 30, item["top"], width=wallSize*2, height=wallSize*1.2)
            elif cutout == 0:
                rightHalf = wall.crop((halfWidth, 0, width, height))
                rightHalf = CMUImage(rightHalf)
                drawImage(rightHalf, item["left"] + 30, item["top"], width=wallSize*2, height=wallSize*1.2)
#Allows for full player movement
def onKeyHold(app, keys):
    if 'right' in keys:
        app.playerAngle += 0.1
        app.playerAngle = app.playerAngle % (2 * pi)  
    if 'left' in keys:
        app.playerAngle -= 0.1
        app.playerAngle = app.playerAngle % (2 * pi)  
    if 'up' in keys:
        if validMovementCheck(app, app.playerX, app.playerY): 
            moveX = app.step * cos(app.playerAngle)
            moveY = app.step * sin(app.playerAngle)
            app.playerX += moveX
            app.playerY += moveY

#Checks for valid player movement
def validMovementCheck(app, startX, startY): 
    canMove = True
    rayXComp = cos(app.playerAngle)
    rayYComp = sin(app.playerAngle)
    currentMazeLocationRow = app.playerY//app.cellHeight
    currentMazeLocationCol = app.playerX//app.cellWidth
    currentRow = int(currentMazeLocationRow)
    currentCol = int(currentMazeLocationCol)
    playerPosX = app.playerX
    playerPosY = app.playerY
    while True:
        if (int(currentCol) < 0 or int(currentCol) >= app.cols or
            int(currentRow) < 0 or int(currentRow) >= app.rows or
            app.maze[int(currentRow)][int(currentCol)] == 1):
            wallDist = sqrt((playerPosX-startX)**2 + (playerPosY-startY)**2)
            if wallDist <= app.playerRadius * 4:
                canMove = False
                if ((playerPosX//app.cellWidth==app.cols-1 or playerPosX//app.cellWidth==app.cols-2) or (playerPosY//app.cellHeight==app.rows-1 or playerPosY//app.cellHeight==app.rows-2)) and app.killCount>=20:
                    app.endGame=True
                    app.win=True
                    app.currentScreen=='end'
            break  
        if rayXComp > 0:
            nextGridLineDist = app.cellWidth*(currentCol+1)-playerPosX
            mazeStepX = 1
            rayXDistance = nextGridLineDist/max(rayXComp, 1e-6)
        elif rayXComp < 0:
            nextGridLineDist = playerPosX-app.cellWidth*(currentCol)
            mazeStepX = -1
            rayXDistance = nextGridLineDist/max(-rayXComp, 1e-6)
        else:
            rayXDistance = float('inf')
            
        if rayYComp > 0:
            nextGridLineDist = app.cellHeight*(currentRow+1)-playerPosY
            mazeStepY = 1
            rayYDistance = nextGridLineDist/max(rayYComp, 1e-6)
        elif rayYComp < 0:
            nextGridLineDist = playerPosY-app.cellHeight*(currentRow)
            mazeStepY = -1
            rayYDistance = nextGridLineDist/max(-rayYComp, 1e-6)
        else:
            rayYDistance = float('inf')
            
        if rayXDistance < rayYDistance:
            currentCol += mazeStepX
            playerPosX += rayXDistance*rayXComp
            playerPosY += rayXDistance*rayYComp
        else:
            currentRow += mazeStepY
            playerPosX += rayYDistance*rayXComp
            playerPosY += rayYDistance*rayYComp        
    return canMove

def main():
    runApp()
main()