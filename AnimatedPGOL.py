import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation

def BFS_with_path(grid):
    n = grid.shape[0]
    visited = np.zeros_like(grid, dtype=bool)
    queue = []
    came_from = {}

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for j in range(n):
        if grid[n-1, j] == 0:
            queue.append((n-1, j))
            visited[n-1, j] = True
            came_from[(n-1, j)] = None

    while queue:
        i, j = queue.pop(0)
        if i == 0:
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

def Updategrid(grid):
    updated_grid = np.zeros_like(grid)
    n = grid.shape[0]

    for row in range(n):
        for col in range(n):
            # Get 3x3 neighborhood and avoid out-of-bounds
            neighbors = grid[max(0, row-1):min(n, row+2), max(0, col-1):min(n, col+2)]
            alive = np.sum(neighbors) - grid[row, col]

            if grid[row, col] == 1:
                if alive < 2 or alive > 3:
                    updated_grid[row, col] = 0
                else:
                    updated_grid[row, col] = 1
            else:
                if alive == 3:
                    updated_grid[row, col] = 1

    return updated_grid

# --- Percolation and Initial Grid Setup ---
percolates = False
n = int(input("What is your desired grid size (n by n)? "))
p = float(input("What is your desired vacancy probability? (0,1] "))
num_tries = 1

while not percolates:
    grid = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            grid[i][j] = 0 if random.random() < p else 1
    percolates, path = BFS_with_path(grid)
    num_tries += 1
    print(f'Graph did not percolate. Moving to attempt number {num_tries}')

print(f"Percolating grid found on attempt number {num_tries}. Visualizing now.")

# Plot with gridlines
fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(grid, cmap='binary', origin='upper')

# Draw gridlines
ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
ax.tick_params(which='both', bottom=False, left=False, labelbottom=False, labelleft=False)

#Title and show
plt.title("Percolating Graph (STILL FRAME = 0. CLOSE TO ANIMATE.)")
plt.show()


# --- Game of Life Animation Setup ---
fig, ax = plt.subplots(figsize=(8, 8))
im = ax.imshow(grid, cmap='binary', origin='upper', animated=True)

# Draw gridlines
ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
ax.tick_params(which='both', bottom=False, left=False, labelbottom=False, labelleft=False)

iterations = 100

def animate(frame):
    global grid
    grid = Updategrid(grid)
    im.set_array(grid)
    ax.set_title(f"Game of Life on percolating {n}x{n} grid")
    return [im]

ani = animation.FuncAnimation(fig, animate, frames=iterations, interval=200, blit=True, repeat=False)
plt.show()

