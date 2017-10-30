import pygame, sys
from pygame.locals import *
import random
import Configuration as config
import json

# Number of frames per second
FPS = 10

###Sets size of grid
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 10

# Check to see if the width and height are multiples of the cell size.
assert WINDOWWIDTH % CELLSIZE == 0, "Window widthpi must be a multiple of cell size"
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size"

# Determine number of cells in horizonatl and vertical plane
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)  # number of cells wide
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)  # Number of cells high

# CONFIGURATION = config.Configuration(48, 64, [(1, 2), (2, 3), (2, 2)])

# set up the colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGRAY = (40, 40, 40)
GREEN = (0, 255, 0)

# Draws the grid lines
def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


# Colours the cells green for life and white for no life
def colourGrid(item, lifeDict):
    x = item[0]
    y = item[1]
    y = y * CELLSIZE  # translates array into grid size
    x = x * CELLSIZE  # translates array into grid size
    if lifeDict[item] == 0:
        pygame.draw.rect(DISPLAYSURF, WHITE, (x, y, CELLSIZE, CELLSIZE))
    if lifeDict[item] == 1:
        pygame.draw.rect(DISPLAYSURF, GREEN, (x, y, CELLSIZE, CELLSIZE))
    return None


def readConfigurationFromFile():
    configString = open('configuration.txt', 'r').read();
    configuration = config.Configuration(configString)
    return configuration;


def writeConfigurationToFile():
    file = open('configuration.txt', 'w');
    con = config.Configuration(CELLWIDTH, CELLHEIGHT, [(5, 7), (2, 8), (8, 4)]);
    conJson = con.toJSON();
    file.write(conJson);


# Creates an dictionary of all the cells
# Sets all cells as dead (0)
def blankGrid():
    gridDict = {}
    # creates dictionary for all cells
    for y in range(CELLHEIGHT):
        for x in range(CELLWIDTH):
            gridDict[x, y] = 0  # Sets cells as dead
    return gridDict


# Assigns a 0 or a 1 to all cells
def startingGridRandom(lifeDict):
    for item in lifeDict:
        lifeDict[item] = random.randint(0, 1)
    return lifeDict


# Determines how many alive neighbours there are around each cell
def getNeighbours(item, lifeDict):
    neighbours = 0
    for x in range(-1, 2):
        for y in range(-1, 2):
            checkCell = (item[0] + x, item[1] + y)
            result_value = None;

            if checkCell[0] == CELLWIDTH and 0 <= checkCell[1] < CELLHEIGHT:
                result_value = lifeDict[0, checkCell[1]]

            if checkCell[0] < 0 and 0 <= checkCell[1] < CELLHEIGHT:
                result_value = lifeDict[CELLWIDTH - 1, checkCell[1]]
            if checkCell[1] == CELLHEIGHT and 0 <= checkCell[0] < CELLWIDTH:
                result_value = lifeDict[checkCell[0], 0]
            if checkCell[1] < 0 and 0 <= checkCell[0] < CELLWIDTH:
                result_value = lifeDict[checkCell[0], CELLHEIGHT - 1]

            if result_value is None and checkCell[0] >= 0 and checkCell[1] >= 0 and checkCell[0] < CELLWIDTH and checkCell[1] < CELLHEIGHT:
                result_value = lifeDict[checkCell]

            if result_value == 1:
                if x == 0 and y == 0:  # negate the central cell
                    neighbours += 0
                else:
                    neighbours += 1

    return neighbours


# determines the next generation by running a 'tick'
def tick(lifeDict):
    newTick = {}
    for item in lifeDict:
        # get number of neighbours for that item
        numberNeighbours = getNeighbours(item, lifeDict)
        if lifeDict[item] == 1:  # For those cells already alive
            if numberNeighbours < 2:  # kill under-population
                newTick[item] = 0
            elif numberNeighbours > 3:  # kill over-population
                newTick[item] = 0
            else:
                newTick[item] = 1  # keep status quo (life)
        elif lifeDict[item] == 0:
            if numberNeighbours == 3:  # cell reproduces
                newTick[item] = 1
            else:
                newTick[item] = 0  # keep status quo (death)
    return newTick


# main function
def main():
    pygame.init()
    global DISPLAYSURF
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Game of Life')

    DISPLAYSURF.fill(WHITE)

    lifeDict = blankGrid()  # creates library and Populates to match blank grid
    config = readConfigurationFromFile();

    list = config.startCellsList;

    for cell in list:
        lifeDict[(cell[0], cell[1])] = 1
    #lifeDict = startingGridRandom(lifeDict)  # Assign random life

    # Colours the live cells, blanks the dead
    for item in lifeDict:
        colourGrid(item, lifeDict)

    drawGrid()
    pygame.display.update()

    while True:  # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # runs a tick
        lifeDict = tick(lifeDict)

        # Colours the live cells, blanks the dead
        for item in lifeDict:
            colourGrid(item, lifeDict)

        drawGrid()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()
