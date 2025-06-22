#This python script will generate a random n x n grid with a set vacancy probability and check if it percolates (that
#is, it will check if there is a sequence of "simple" moves from any open cell in the bottom row to any open cell
#in the top row). Then, it will take the CLOSED grid and perform Conway's Game of Life on it.

#I don't think that there will be any interesting results here, but I'd like to just test it first

#First step is to copy paste the relevant code from the Percolation.py script and the GameOfLife.py script.


##### Imports #####
import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation

##### Percolation ##### 

def BFS_with_path(grid):
    '''
    Documentation of this function can be found in the file called "Percolation.py". This is a so called "breadth-first search" algorithm.
    '''
    n = grid.shape[0]
    visited = np.zeros_like(grid, dtype=bool)
    queue = []
    came_from = {}

    # Direction vectors: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Start from all open grid in the bottom row
    for j in range(n):
        if grid[n-1, j] == 0:
            queue.append((n-1, j))
            visited[n-1, j] = True
            came_from[(n-1, j)] = None  # Starting points

    while queue:
        i, j = queue.pop(0)

        # Check if we've reached the top row
        if i == 0:
            # Reconstruct path
            path = []
            current = (i, j)
            while current is not None:
                path.append(current)
                current = came_from[current]
            return True, path

        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n:
                if grid[ni, nj] == 0 and not visited[ni, nj]:
                    visited[ni, nj] = True
                    queue.append((ni, nj))
                    came_from[(ni, nj)] = (i, j)

    return False, []


#Okay let's actually use the code now
#Set up parameters and grid
percolates = False
n = int(input("What is your desired grid size (n by n)? "))
p = float(input("What is your desired vacancy probability? (0,1] "))
num_tries = 1

while not percolates:
    #Generate grids and check for percolation until we find one.
    grid = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            grid[i][j] = 0 if random.random() < p else 1

    # Run BFS with path tracking
    percolates, path = BFS_with_path(grid)
    num_tries +=1
    print(f'Graph did not percolate. Moving to attempt number {num_tries}') #Purely for my own entertainment :)

print(f"Percolating grid found on attempt number {num_tries}. Visulaizing now.")
#Only move on to visualization if we have a plot that percolates
# Plot with gridlines
fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(grid, cmap='binary', origin='upper')

# Draw gridlines
ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
ax.tick_params(which='both', bottom=False, left=False, labelbottom=False, labelleft=False)

#Title and show
plt.title("Percolating Graph")
plt.show()


##### Game of Life #####


def Updategrid(grid):
    '''
    This function will update the current graph according to the following rules
    1. Any live cell with fewer than 2 live neighbors dies
    2. Any live cell with two or three neighbors lives unchanged
    3. Any live cell with more than three neighbors dies
    4. Any dead cell with exactly three live neighbors becomes alive

    TODO: Update this to the correct syntax. The current syntax is from the PyGame code I wrote a while back.
    '''

    updated_grid = np.zeros((grid.shape[0],grid.shape[1])) #Create a blank canvas for our updated grid

    for row,col in np.ndindex(grid.shape):
        alive = np.sum(grid[row-1:row+2,col-1:col+2])-grid[row,col] #Calculate how many neighbors we have

        if grid[row,col] == 1: #If the cell is occupied
            if alive<2 or alive >3: #And if the cell meets the dying criterion (1 and 3)
                updated_grid[row,col] == 0 #Kill the cell

            elif 2<= alive <=3: #If the cell is occupied and meets the criterion for surviving (2)
                updated_grid[row,col]=1 #Keep it alive

        else: #If the cell is unoccupied
            if alive==3: #If the cell has exactly three neighbors
                updated_grid[row,col]=1 #Bring that cell to life (4)

    return updated_grid


iterations = 100 #Calculate 100 time steps into the future
counter = 0 #Keep track of how many timesteps we have done

while counter < iterations:
    #Perform the game of life.
    print(f"Running. Iteration number {counter}")
    updated = Updategrid(grid) #update the percolating grid
    counter +=1


#Sanity check
fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(updated, cmap='binary', origin='upper')

# Draw gridlines
ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
ax.tick_params(which='both', bottom=False, left=False, labelbottom=False, labelleft=False)

#Title and show
plt.title(f"Percolating Graph after {iterations} iterations of the Game of Life")
plt.show()
