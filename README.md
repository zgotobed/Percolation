# Percolation
 Implementation of percolation in python. Description of the files below


# AnimatedPGOL
Animated version of Conway's game of life performed on an n x n percolating grid. Just a fun little side project

# GameofLife
I learned how to use PyGame to make an interactive version of CGOL

# PercolatingGOL
Non-animated version of AnimatedPGOL. This file simply shows you the start and end result

# Percolation
This file takes an n x n grid with site vacancy probability p and checks to see if a single graph percolates

# PercoaltionThreshold
This file does a 2D sweep over grid size (n x n) and site vacancy probability and produces a heat map of the so called
"percolation threshold". This heat map tells you for 100 iterations (fixed in code, although you can change if you want)
, what is the probability that my grid will percolate? Numba is used to GREATLY speed up performance.