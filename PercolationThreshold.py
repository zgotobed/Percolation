import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm  # progress bar

def BFS_with_path(grid):
    """
    Perform BFS from all open cells in the bottom row to check for top-row connection.
    Return True and the path if percolation occurs, else False and empty path.
    """
    n = grid.shape[0]
    visited = np.zeros_like(grid, dtype=bool)
    queue = []
    came_from = {}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

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

# --- Simulation parameters ---
n = 100                   # Grid size
n_reps = 1000             # Number of trials per p
ps = np.linspace(0, 1, 50)
percolation_probs = []
percolation_stds = []

# --- Run simulation with progress bar ---
for p in tqdm(ps, desc="Running simulations"):
    outcomes = []
    for _ in range(n_reps):
        grid = (np.random.rand(n, n) >= p).astype(int)
        percolates, _ = BFS_with_path(grid)
        outcomes.append(1 if percolates else 0)
    mean = np.mean(outcomes)
    std = np.std(outcomes)
    percolation_probs.append(mean)
    percolation_stds.append(std)

# --- Plot results ---
plt.errorbar(ps, percolation_probs, yerr=percolation_stds, fmt='o-', color='blue',
             ecolor='gray', capsize=3, label='Percolation Probability ± Std Dev')
plt.axvline(x=ps[np.argmax(np.array(percolation_probs) > 0.5)], color='red', linestyle='--', label='Approx. Threshold')
plt.xlabel("Site Vacancy Probability p")
plt.ylabel("Percolation Probability")
plt.title(f"Percolation vs. Site Vacancy (Grid {n}x{n}, {n_reps} trials)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
