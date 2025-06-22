#This python script will generate a random n x n grid with a set vacancy probability and check if it percolates (that
#is, it will check if there is a sequence of "simple" moves from any open cell in the bottom row to any open cell
#in the top row). Then, it will take the CLOSED grid and perform Conway's Game of Life on it.

#I don't think that there will be any interesting results here, but I'd like to just test it first

#First step is to copy paste the relevant code from the Percolation.py script and the GameOfLife.py script.



##### Percolation ##### 

import numpy as np
import matplotlib.pyplot as plt
import random

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
# Set up parameters and grid
n = int(input("What is your desired grid size (n by n)? "))
p = float(input("What is your desired vacancy probability? (between 0 and 1 inclusive) "))

grid = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        grid[i][j] = 0 if random.random() < p else 1

# Run BFS with path tracking
percolates, path = BFS_with_path(grid)
print("Percolates?", percolates)

# Plot with gridlines and blue path highlights
fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(grid, cmap='binary', origin='upper')

# Draw gridlines
ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
ax.tick_params(which='both', bottom=False, left=False, labelbottom=False, labelleft=False)

# Highlight percolation path in blue
if percolates:
    for (i, j) in path:
        rect = plt.Rectangle((j - 0.5, i - 0.5), 1, 1, color='blue', alpha=0.6)
        ax.add_patch(rect)

    plt.title("Percolates! Path Highlighted in Blue")
else:
    plt.title("Does Not Percolate")

plt.show()



#Game of life, now. I think I'm just gonna rewrite it from scratch using the PyGame code I wrote as a skeleton.

def Updategrid(grid,size):
    '''
    This function will update the current graph according to the following rules
    1. Any live cell with fewer than 2 live neighbors dies
    2. Any live cell with two or three neighbors lives unchanged
    3. Any live cell with more than three neighbors dies
    4. Any dead cell with exactly three live neighbors becomes alive

    TODO: Update this to the correct syntax. The current syntax is from the PyGame code I wrote a while back.
    '''

    updated_grid = np.zeros((grid.shape[0],grid.shape[1]))

    for row,col in np.ndindex(grid.shape):
        alive = np.sum(grid[row-1:row+2,col-1:col+2])-grid[row,col]
        color = color_bg if grid[row,col] == 0 else color_alive_next

        if grid[row,col] == 1:
            if alive<2 or alive >3:
                if with_progress:
                    color = color_die_next

            elif 2<= alive <=3:
                updated_grid[row,col]=1
                if with_progress:
                    color = color_alive_next

        else:
            if alive==3:
                updated_grid[row,col]=1
                if with_progress:
                    color = color_alive_next