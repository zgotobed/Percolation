import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

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
            return True, []
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n:
                if grid[ni, nj] == 0 and not visited[ni, nj]:
                    visited[ni, nj] = True
                    queue.append((ni, nj))
                    came_from[(ni, nj)] = (i, j)

    return False, []

# --- Parameters ---
grid_sizes = [10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]      # Grid sizes to sweep
ps = np.linspace(0, 1, 50)               # Vacancy probabilities
n_reps = 100                             # Trials per configuration

# --- Storage for results ---
results = np.zeros((len(grid_sizes), len(ps)))  # percolation probability

# --- Run simulations ---
for i, n in enumerate(tqdm(grid_sizes, desc="Grid sizes")):
    for j, p in enumerate(tqdm(ps, desc=f"p sweep (n={n})", leave=False)):
        outcomes = []
        for _ in range(n_reps):
            grid = (np.random.rand(n, n) >= p).astype(int)
            percolates, _ = BFS_with_path(grid)
            outcomes.append(1 if percolates else 0)
        results[i, j] = np.mean(outcomes)

# --- Plot heatmap ---
plt.figure(figsize=(10, 6))
im = plt.imshow(results, aspect='auto', origin='lower', 
                extent=[ps[0], ps[-1], grid_sizes[0], grid_sizes[-1]],
                cmap='viridis')

plt.colorbar(im, label='Percolation Probability')
plt.xlabel('Site Vacancy Probability p')
plt.ylabel('Grid Size n')
plt.title('Percolation Probability Heatmap\n(vs. Grid Size and Site Vacancy)')
plt.tight_layout()
plt.show()
