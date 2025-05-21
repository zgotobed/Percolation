# The problem statement is as follows: 
# We model a percolation system using an n-by-n grid of sites. Each site is either open or blocked. 
# A full site is an open site that can be connected to an open site in the top row via a chain of 
# neighboring (left, right, up, down) open sites. We say the system percolates if there is a full site in the bottom 
# row. In other words, a system percolates if we fill all open sites connected to the top row and that process fills 
# some open site on the bottom row

# In a famous scientific problem, researchers are interested in the following question: if sites are independently 
# set to be open with probability p (and therefore blocked with probability 1 − p), what is the probability that the 
# system percolates? When p equals 0, the system does not percolate; when p equals 1, the system percolates. 
# When n is sufficiently large, there is a threshold value p* such that when p < p* a random n-by-n grid almost 
# never percolates, and when p > p*, a random n-by-n grid almost always percolates. No mathematical solution for 
# determining the percolation threshold p* has yet been derived.


# What is the first step? Let's first create an n by n grid which has each square being blocked w a probability p

import numpy as np
import random
import matplotlib.pyplot as plt

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

#Okay let's actually use the code now
# Set up parameters and grid
n = 100
p = 0.6
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
# TODO: Initialize all sites as blocked. Then, Repeat the following until the systme percolates:
#       - choose a site at random among all blocked sites
#       - open the site
#  The fraction of sites that are opened when the system percolates provides an estimate of the percolation threshold. 