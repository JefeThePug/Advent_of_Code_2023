"""
--- Part Two ---

The parabolic reflector dish deforms, but not in a way that focuses the beam. To do that, you'll need to move the 
rocks to the edges of the platform. Fortunately, a button on the side of the control panel labeled "spin cycle" 
attempts to do just that!

Each cycle tilts the platform four times so that the rounded rocks roll north, then west, then south, then east. 
After each tilt, the rounded rocks roll as far as they can before the platform tilts in the next direction. After 
one cycle, the platform will have finished rolling the rounded rocks in those four directions in that order.

Here's what happens in the example above after each of the first few cycles:
    After 1 cycle:            After 2 cycles:           After 3 cycles:
    .....#....                .....#....                .....#....
    ....#...O#                ....#...O#                ....#...O#
    ...OO##...                .....##...                .....##...
    .OO#......                ..O#......                ..O#......
    .....OOO#.                .....OOO#.                .....OOO#.
    .O#...O#.#                .O#...O#.#                .O#...O#.#
    ....O#....                ....O#...O                ....O#...O
    ......OOOO                .......OOO                .......OOO
    #...O###..                #..OO###..                #...O###.O
    #..OO#....                #.OOO#...O                #.OOO#...O
This process should work if you leave it running long enough, but you're still worried about the north support 
beams. To make sure they'll survive for a while, you need to calculate the total load on the north support beams 
after 1000000000 cycles.

In the above example, after 1000000000 cycles, the total load on the north support beams is 64.

Run the spin cycle for 1000000000 cycles. Afterward, what is the total load on the north support beams?

"""

import numpy as np


def calculate(grid):
    weights = np.array([[n]*grid.shape[1] for n in range(grid.shape[0], 0, -1)])
    return np.sum(np.where(grid == "O", weights, 0))
    
def shift_up(grid):
    for c in range(grid.shape[1]):
        rocks = np.where(grid[:, c] == "O")[0]
        for r in rocks:
            p = r - 1
            while p >= 0 and grid[p, c] == ".":
                grid[p, c], grid[p + 1, c] = grid[p + 1, c], grid[p, c]
                p -= 1
    return grid


with open("input.txt") as f:
    grid = np.array([list(line.strip()) for line in f])

spin_cycles = 1000000000
visited = {}
visited[grid.tobytes()] = 0

for i in range(1, spin_cycles + 1):
    for j in range(4):
        grid = shift_up(grid)
        grid = np.rot90(grid, k=3)
        
    if seen := visited.get(grid.tobytes(), None):
        period = i - seen
        cycle_pos = (spin_cycles - seen)%period
        billion = seen + cycle_pos
        bytes_arr = list(visited.keys())[billion]
        final = np.frombuffer(bytes_arr, dtype="<U1").reshape(grid.shape)
        break
    visited[grid.tobytes()] = i
    
print(calculate(final))

# total load is 112452
