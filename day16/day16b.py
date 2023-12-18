"""
--- Part Two ---

As you try to work out what might be wrong, the reindeer tugs on your shirt and leads you to a nearby control 
panel. There, a collection of buttons lets you align the contraption so that the beam enters from any edge tile 
and heading away from that edge. (You can choose either of two directions for the beam if it starts on a corner; 
for instance, if the beam starts in the bottom-right corner, it can start heading either left or upward.)

So, the beam could start on any tile in the top row (heading downward), any tile in the bottom row (heading 
upward), any tile in the leftmost column (heading right), or any tile in the rightmost column (heading left). 
To produce lava, you need to find the configuration that energizes as many tiles as possible.

In the above example, this can be achieved by starting the beam in the fourth tile from the left in the top row:
    .|<2<\....        .#####....
    |v-v\^....        .#.#.#....
    .v.v.|->>>        .#.#.#####
    .v.v.v^.|.        .#.#.##...
    .v.v.v^...        .#.#.##...
    .v.v.v^..\        .#.#.##...
    .v.v/2\\..        .#.#####..
    <-2-/vv|..        ########..
    .|<<<2-|.\        .#######..
    .v//.|.v..        .#...#.#..
Using this configuration, 51 tiles are energized.

Find the initial beam configuration that energizes the largest number of tiles; 
how many tiles are energized in that configuration?

"""
    
import numpy as np

def rotate(grid: np.ndarray) -> np.ndarray:
    grid = np.where(grid == "|", "*", grid)
    grid = np.where(grid == "-", "|", grid)
    grid = np.where(grid == "*", "-", grid)
    grid = np.where(grid == "/", "*", grid)
    grid = np.where(grid == "\\", "/", grid)
    grid = np.where(grid == "*", "\\", grid)
    return np.rot90(grid)
    
def follow_line(y: int, x: int, d: int, r: int) -> None:
    if (y not in range(instruct.shape[0]) 
            or x not in range(instruct.shape[1])):
        return
    output[y, x] = "#"
    mark = instruct[y, x]
    
    if mark == "|" and d == 0:
        instruct[y, x] = "‖"
        follow_line(y - 1, x, -1, 0)
        follow_line(y + 1, x, 1, 0)
    elif mark == "-" and r == 0:
        instruct[y, x] = "="
        follow_line(y, x - 1, 0, -1)
        follow_line(y, x + 1, 0, 1)
    elif mark == "/":
        follow_line(y - r, x - d, -r, -d)
    elif mark == "\\":
        follow_line(y + r, x + d, r, d)
    elif mark in "‖=": # prevent infinite loop
        return
    else: # . or ignored splitter
        follow_line(y + d, x + r, d, r)

with open("input.txt") as f:
    instruct = np.array([list(line.strip()) for line in f])

most = 0

for _ in range(4):
    for i in range(instruct.shape[0]):
        output = np.zeros_like(instruct)
        follow_line(i, 0, 0, 1)
        x = np.count_nonzero(output == "#")
        most = max(most, x)
        instruct = np.where(instruct == "‖", "|", instruct)
        instruct = np.where(instruct == "=", "-", instruct)
    instruct = rotate(instruct)
        
print(most)

# 7572
