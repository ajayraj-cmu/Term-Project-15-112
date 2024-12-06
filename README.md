# Term-Project-15-112
Project Description:

The project will be presented in the shape of a fully functional 3-D raycasted maze using the CMU’s 2-D graphics engine (CMU Graphics). The maze itself will be casted before the player who will be playing from the first person point of view as if they were inside the physical maze itself. The player will be provided a menu screen with a sequence of rules that include the following in summation: they must survive the maze by avoiding losing their initial 1000 HP to the oncoming autonomously moving enemies and oscillating walls throughout the maze while also trying defeat a minimum of 20 enemies in which they can then scour for the false wall/portal within the maze to escape. The longer that the player remains within the maze, the larger the difficulty (such that every 15s there will be a wave in which the number of enemies are increased, the hit damage and radius increases, and the overall speed of the walls and enemies increases as well). In order to defeat the enemies, the player can utilize the drawing feature to draw the prompted shape on the actual enemies within a certain margin of error and they can also weave through the walls. 

The maze itself is created using a DFS algorithm that I designed which randomizes every time but still makes it a solvable maze which means that the user cannot memorize the path. Likewise, the enemies are equipped with pathfinding so no matter where a player runs, the enemies will follow and they will get increasingly faster as the time goes on. The moving walls will likewise increase in speed, and the flashing light animations make it harder to see as the game goes on so it is better to beat the game earlier on. The ray casting was made using the DDA algorithm, the pathfinding, was inspired by a more primitive version of A*, and the pattern detection was done using Dynamic Time Warping Detection.


Run Instructions:
*Editor: It is highly recommended that this game is run on the VS Code editor and that the latest version of python be downloaded for the best run-time experience.

*Downloading Files: Ensure to download and place into your main source folder the code-base filesthat are purely in python. This includes: main.py, enemy.py, movingWall.py, leaderBoard.py). Ensure to also download the pngs included in this repositiory with the exact same file name and of the type png and ensure that you drag and drop these files directly into your vs code editor/palce them within the active src folder that your are coding with.

*Additional Downloads: 
*Ensure to have the following modules/libraries imported (within main.py):
-Math (built into python)
-Time (buil in)
-Copy (built in)
-Random (built in)
-CMU Graphics (you can visit https://academy.cs.cmu.edu/desktop or pip install cmu-graphics)
-PIL (built in via some editors but you can also pip via pip install pillow or for windows pip install Pillow)
-Import the three other object classes (enemy.py, movingWall.py, and leaderBoard.py)

Shortcut Commands:
*Arrow Keys: These keys will display movement when trying to navigate throughout the entirety of maze (forward key is for forward movement, left key is for turning left, and the right key is for turning right from a first person point of view).
