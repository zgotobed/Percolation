import numpy as np
import matplotlib.pyplot as plt
import random

def BFS_with_path(grid):
    '''
    General concept:
    -Start at a cell in the bottom row
    -Check to see if the cells to the left, right, up, and down are open
    -If so, priority is given to moving straight up, put the moves L,R, and D (if applicable) into a queue
    -After moving straight up, we repeat the process and add other moves further down the queue
    -Repeat this along one path until we get stuck (the only accpeted move is the opposite of the move we just did)
    -Go back to the most recent entry in the queue and repeat. Work backwards through the queue
    -If all surrounding cells have been visited then we need to toss that cell from the queue, since we have already explored all possible options

    Edge cases:
    -D is not an acceptable move on the first repitition
    -Handle when the current cell is on the edge of the board
    -Queue removal when a cell is surrounded by cells that have already been visited
    '''
    n = grid.shape[0]
    visited = np.zeros_like(grid, dtype=bool)
    queue = []
    came_from = {}

    # Direction vectors: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Start from all open cells in the bottom row
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

#The goal here is to run BFS for varying values of P and then make a plot which has probability of percolating on the 
#y axis and the probability value on the x axis

probs = np.linspace(0,1,100)

n_reps = 1000 #number of reps for statistics
n = 50 #size of the grids to test on
grids = np.zeros((n_reps, n, n))
p =0.6

PercolateCheck = np.zeros(n_reps) # A list which stores whether or not a graph percolates
#Now let's create 100 random grids at some fixed p value and check whether or not the percolate

for grid_number in range(n_reps):
    grid = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            grid[i][j] = 0 if random.random() < p else 1
    grids[grid_number] = grid #Store the nth grid in the nth position in the grids array

for grid_number in range(len(grids)):
    #Check each grid for percolation
    percolates, path = BFS_with_path(grids[grid_number])
    if percolates:
        PercolateCheck[grid_number] = 1 #If the grid percolates then let's make sure to mark that down
    else:
        PercolateCheck[grid_number] = 0

yes_percolate = np.count_nonzero(PercolateCheck == 1)
no_percolate = n_reps - yes_percolate

percolation_probability = yes_percolate/n_reps

print(f"The probability that a graph percolates at size {n}x{n} is {percolation_probability}")