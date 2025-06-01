import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from numba import njit, int32, boolean

# --- Optimized BFS function with numba ---
@njit(boolean(int32[:, :]))
def BFS_numba(grid):
    n = grid.shape[0]
    visited = np.zeros((n, n), dtype=boolean)

    queue = np.empty((n * n, 2), dtype=int32)  # Preallocate queue
    head = 0
    tail = 0

    # Initialize queue with bottom row
    for j in range(n):
        if grid[n - 1, j] == 0:
            queue[tail, 0] = n - 1
            queue[tail, 1] = j
            tail += 1
            visited[n - 1, j] = True

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while head < tail:
        i, j = queue[head]
        head += 1
        if i == 0:
            return True

        for d in directions:
            ni, nj = i + d[0], j + d[1]
            if 0 <= ni < n and 0 <= nj < n:
                if grid[ni, nj] == 0 and not visited[ni, nj]:
                    visited[ni, nj] = True
                    queue[tail, 0] = ni
                    queue[tail, 1] = nj
                    tail += 1

    return False

# --- Parameters ---
grid_sizes = [10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
ps = np.linspace(0, 1, 50)
n_reps = 100

results = np.zeros((len(grid_sizes), len(ps)))

# --- Run simulations ---
for i, n in enumerate(tqdm(grid_sizes, desc="Grid sizes")):
    for j, p in enumerate(tqdm(ps, desc=f"p sweep (n={n})", leave=False)):
        count = 0
        for _ in range(n_reps):
            grid = (np.random.rand(n, n) >= p).astype(np.int32)
            if BFS_numba(grid):
                count += 1
        results[i, j] = count / n_reps

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
