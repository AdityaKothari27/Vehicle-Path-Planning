import Model
import pygame
from pygame.locals import *
from time import sleep
import argparse

class Screen: 

    def __init__(self, L, antHill, food, elementSize=30, borderSize=1, margin=40):
        # Initialize attributes of the Screen object
        self.L = L
        self.antHill = antHill
        self.food = food
        self.elementSize = elementSize
        self.borderSize = borderSize
        self.margin = margin
        self.ScreenLength = L * (self.elementSize + self.borderSize) + 2 * self.margin
        self.XText = self.margin / 2     
        self.YText = self.margin / 4
        self.SXText = 0     
        self.SYText = 0
        self.window = None 

        # Create basic and inner rectangles for cells
        self.basicRect = pygame.Surface((self.elementSize + 2 * self.borderSize, self.elementSize + 2 * self.borderSize))
        self.basicRect.fill(Color("black"))
        self.innerRect = pygame.Surface((self.elementSize, self.elementSize))
        self.innerRect.fill(Color("white"))
        self.basicRect.blit(self.innerRect, (self.borderSize, self.borderSize))

        # Initialize Pygame
        pygame.init()     
        self.opened = False     

        # Initialize font for text rendering
        self.font = pygame.font.Font(pygame.font.get_default_font(), 14)     

    # Method for drawing text on the screen
    def drawText(self, text, X, Y, SX, SY):
        pygame.draw.rect(self.window, Color("white"), (X, Y, SX, SY))     
        self.window.blit(self.font.render(text, True, Color("black")), (X, Y))     
        return self.font.size(text)                                           

    # Method for initializing the screen
    def startScreen(self):
        self.window = pygame.display.set_mode((self.ScreenLength, self.ScreenLength)) 
        pygame.display.set_caption("Ants GUI")
        self.window.fill(Color("white")) 

        # Draw cells on the screen
        X = self.margin     
        for i in range(self.L):     
            for j in range(self.L):     
                coords = self.getPygameCornerOfCell(i, j)     
                self.window.blit(self.basicRect, coords)     

        # Draw ant hill and food sources
        antHillCoords = self.getPygameCornerOfCell(self.antHill[0], self.antHill[1])     
        self.changeInnerRectColor("brown")     
        self.window.blit(self.basicRect, antHillCoords)     

        foodCoords = self.getPygameCornerOfCell(self.food[0], self.food[1])     
        self.changeInnerRectColor("green")
        self.window.blit(self.basicRect, foodCoords)

        pygame.display.update()     
        self.opened = True     

    # Method for calculating the corner position of a cell
    def getPygameCornerOfCell(self, cellX, cellY):
        PosX = cellX * (self.elementSize + self.borderSize) + self.margin
        PosY = self.L - cellY - 1
        PosY = PosY * (self.elementSize + self.borderSize) + self.margin
        return (PosX, PosY)

    # Method for changing the color of the inner rectangle of a cell
    def changeInnerRectColor(self, color="white"):
        if isinstance(color, tuple):
            if(color[0] > 255): color = (255, color[1], color[2])
            if(color[1] > 255): color = (color[0], 255, color[2])
            if(color[2] > 255): color = (color[0], color[1], 255)
            if(color[0] < 0): color = (0, color[1], color[2])
            if(color[1] < 0): color = (color[0], 0, color[2])
            if(color[2] < 0): color = (color[0], color[1], 0)
            self.innerRect.fill(Color(color[0], color[1], color[2], 255))
        else:
            self.innerRect.fill(Color(color))
        self.basicRect.blit(self.innerRect, (self.borderSize, self.borderSize))

    # Method for updating the score displayed on the screen
    def updateScore(self, score):
        pos = self.drawText("Round trip(s) : {}".format(score), self.XText, self.YText, self.SXText, self.SYText)
        self.SXText = pos[0]
        self.SYText = pos[1]

    # Method for updating the pheromone levels displayed on the screen
    def updatePheromones(self, pheromones):
        for i in range(len(pheromones)):     
            for j in range(len(pheromones)):     
                if not ((i == self.antHill[0] and j == self.antHill[1]) or (i == self.food[0] and j == self.food[1])):     
                    cellCoords = self.getPygameCornerOfCell(i, j)     
                    rgb = 255 - round(pheromones[i][j])     
                    self.changeInnerRectColor((rgb, rgb, rgb))     
                    self.window.blit(self.basicRect, cellCoords)     

    # Method for updating the ants displayed on the screen
    def updateAnts(self, ants):
        for i in range(len(ants)):     
            for j in range(len(ants)):     
                if not ((i == self.antHill[0] and j == self.antHill[1]) or (i == self.food[0] and j == self.food[1])):     
                    cellCoords = self.getPygameCornerOfCell(i, j)     
                    rgb = 255 - round(ants[i][j]) * 10     
                    self.changeInnerRectColor((rgb, rgb, rgb))     
                    self.window.blit(self.basicRect, cellCoords)     

    # Method for handling events in the Pygame window
    def listen(self):
        for event in pygame.event.get():                                                    
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):     
                self.opened = False
                pygame.quit()                                                                    

# Function for checking if a value is positive
def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("argument needs to be positive")
    return ivalue

# Function for checking if a value is between 0 and 1
def check_0_1(value):
    fvalue = float(value)
    if fvalue < 0 or fvalue > 1:
        raise argparse.ArgumentTypeError("argument needs to be between 0 and 1")
    return fvalue

# Parse command-line arguments
parser = argparse.ArgumentParser("Console.py", description="Runs a simulation of the algorithm and displays the resulted path.")
parser.add_argument("--width", help="Side size of the world. (Default: 10)", type=check_positive)
parser.add_argument("-s", "--scouts", help="Number of scout ants. (Default: width)", type=check_positive)
parser.add_argument("-w", "--workers", help="Number of worker ants. (Default: 10*width)", type=check_positive)
parser.add_argument("-r", "--rate", help="Pheromones decrease rate between 0 and 1. (Default: 0.7)", type=check_0_1)
args = parser.parse_args()

# Set default values for width, scout ants, worker ants, and pheromone decrease rate
if args.width:
    width = args.width
else:
    width = 10

if args.scouts:
    scoutAnts = args.scouts
else:
    scoutAnts = width

if args.workers:
    workerAnts = args.workers
else:
    workerAnts = 10 * width

if(args.rate):
    decreaseRate = args.rate
else:
    decreaseRate = 0.7

# Create a world object with specified parameters
world = Model.World(width, scoutAnts, workerAnts, decreaseRate)

# Create a screen object with world parameters
screen = Screen(world.width, world.anthill, world.food)

# Start the simulation screen
screen.startScreen()

# Main loop for the simulation
while screen.opened:
    # Run one iteration of the simulation
    world.loop()                                    
    # Update the ants displayed on the screen
    screen.updateAnts(world.antsNumberPerCell())    
    # Update the score displayed on the screen
    screen.updateScore(world.broughtFood)        
    # Update the Pygame display
    pygame.display.update()                        
    # Listen for events in the Pygame window
    screen.listen()                                
    # Introduce a slight delay to control the simulation speed
    sleep(0.016)                                    