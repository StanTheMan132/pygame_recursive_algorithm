#----------IMPORTS----------
import pygame
import sys
import random

#----------VARIABLES----------

# Define colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)

# Define screen size
size = (1000,1000)

# Define amount  of rows and collumnns 
collumn_size = 25
row_size = 25
# Calculate pixel height and with of row and collumn
row_height = size[1] / row_size 
collumn_width = size[0] / collumn_size 

# Define the stack to keep track of previous cells
stack = []

# Define the update count, the update count defines the update speed, the higher the update count the faster the maze gets solved
update_count = 120 


#----------CLASSES----------

# Cell classs, each cell in the grid is a Cell object 
class Cell():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False

    def fill_cell(self, color, screen):
        # Fill the cell with a certain color, 
        # Find top left corner
        x0 = self.x * collumn_width 
        y0 = self.y * row_height
        # create a square from the top left to the bottom right, slight offset for the grid lines
        square = pygame.Rect(x0+2,y0+2,collumn_width-4,row_height-4)
        # Draw the rectagle, but screen doenst get redrawn yet. This has to be done from the calling function
        pygame.draw.rect(screen, color, square)

    def remove_border(self, x_old, y_old, screen):
        # Remove the border between this cel and the cel before it
        print('removing border from cell %d : %d ' % (self.x, self.y))
        print('previous cel was %d : %d ' % (x_old, y_old))
        # Calculate the top left corner in pixels
        top_left = (self.x*collumn_width, self.y*row_height)

        # If the Y is the same then the previous cell must be to the left or right
        if y_old == self.y:

            if self.x < x_old:
                # Remove right border
                print('Removing right border')
                top_right = top_left[0]+collumn_width
                bottom = top_left[1]+row_height
                pygame.draw.line(screen, WHITE, (top_right, top_left[1]), (top_right, bottom),2)

            if self.x > x_old:
                print('Removing left border')
                # Remove left border
                bottom_left = (top_left[0], top_left[1] + row_height) 
                pygame.draw.line(screen, WHITE, (top_left[0], top_left[1]),(bottom_left[0], bottom_left[1]),2)

        elif self.y > y_old:
            # Remove top border
            print('Removing top border')
            top_right = top_left[0] + collumn_width
            pygame.draw.line(screen, WHITE, (top_left[0], top_left[1]), (top_right, top_left[1]),2)

        else:
            print('Removing bottom border')
            # Remove bottom border
            bottom_left = (top_left[0],top_left[1]+row_height)
            bottom_right = (top_left[0]+collumn_width,top_left[1]+row_height)
            pygame.draw.line(screen, WHITE, (bottom_left[0], bottom_left[1]), (bottom_right[0],bottom_right[1]),2)

def drawGrid(screen):
    # Draw the grid on the screen

    # Set the background color
    screen.fill(WHITE)

    # Draw rows 
    for i in range(0, row_size):
        start = (i * row_height) + row_height
        length = collumn_size * collumn_width
        pygame.draw.line(screen, BLACK, [0,start],[length,start],2)
    # Draw collums
    for i in range(0,collumn_size):
        start = (i * collumn_width) + collumn_width 
        length = row_size * row_height
        pygame.draw.line(screen, BLACK, [start,0],[start, length],2)


def cell_and_direction_to_new_cell(direction, x, y):
    # Find the index of a new cell given a current cel and direction from that cell

    if direction == 'up':
        newX = x
        newY = y - 1
    if direction == 'right':
        newX = x + 1
        newY = y 

    if direction == 'down':
        newX = x
        newY = y + 1

    if direction == 'left':
        newX = x - 1
        newY = y

    return newX, newY

def validateNewLocation(x,y):
# Validate that the new location is valid, ie not off the grid of a allready visited cell

    # Cell is off the grid
    if not  0 <= x <= row_size-1:
        # Location is invalid 
        return False 
    elif not 0 <= y <= collumn_size-1:
        # Location is invalid 
        return False

    # Cell has allready been visited
    elif cells[x][y].visited == True:
        return False
    # Cell is valid
    else:
        return True


def getNewXY(col, row): 
    # Find a new cell to go to

    #All posible directions a cell can go
    directions = ['up','right','down','left']
    # Keep track of if a valid pair of row and collumn has been found
    foundValidPair = False

    # Keep going until valid pair is found
    while foundValidPair == False:
        # choose a random direction
        direction = random.choice(directions)
        # convert the position of the current cell and a direction to the index of a new cell 
        newCol, newRow = cell_and_direction_to_new_cell(direction, col, row)
        # Check if the new pair is valid
        isValid = validateNewLocation(newCol, newRow)
        if isValid:
            foundValidPair = True
        else:
            # Take the direction away from the directions list, this way this direction cant be chosen again
            directions.remove(direction)
            # If the direction list is empty there is no valid way to go. Break out of the loop
            if directions == []:
                break
                 
    if foundValidPair:
        # If a valid pair was found return the new cell
        return newCol, newRow
    else:
        # No valid pair was found to return false
        return False 



def updateCell(x,y,screen, clock):
    # Set the current cell as visited
    cells[x][y].visited = True

    # Get Col and Row of a randomly chosen neighbouring cell
    newCell = getNewXY(x,y)

    if newCell:
        # A new cell could be found so set the new coardinates and append it to the stack
        newCol, newRow = newCell
        newCellObj =  cells[newCol][newRow]
        # Remove the border between this and the new cell
        newCellObj.remove_border(x,y,screen)
        # Color the cell red
        newCellObj.fill_cell(RED, screen)
        # append the current cell to the stack
        stack.append((x,y))

    else:
        # No valid new cell found so reverse one cell
        newCol, newRow =  stack.pop()
        currentCellObj = cells[x][y]
        newCellObj =  cells[newCol][newRow]
        # Color the cell black
        newCellObj.fill_cell(GREEN,screen)
        currentCellObj.fill_cell(GREEN,screen)

        # If the stack is empty generation is done
        if stack == []:
            print('done')
            return None

    # Tick the clock
    clock.tick(update_count)
    # Update the display
    pygame.display.flip()
    # Recursively update the new cell
    updateCell(newCol, newRow, screen,clock)


#----------MAIN----------
def main():
    # Make al the cell objects
    global cells
    cells = []
    for i in range(0, collumn_size):
        cells.append([])
        for j in range(0, row_size):
            cells[i].append(Cell(i,j))

    # Update recursion limit
    sys.setrecursionlimit(2000)
    # Initialize pygame
    pygame.init()
    clock = pygame.time.Clock()
    # Initialize screen
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Maze")

    # Draw a grid on the screen
    drawGrid(screen)
    clock.tick(update_count)
    pygame.display.flip()

    # Start at 0,0 and recursively go through all cells
    updateCell(0,0,screen,clock)

    # Once it has gone through all cells color every cell white
    for i in cells:
        for j in i:
            j.fill_cell(WHITE, screen)
    clock.tick(10)
    pygame.display.flip()

    while True:
        # Leave the display up
        pass
    

if __name__ == "__main__":
    main()
