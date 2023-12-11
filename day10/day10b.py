"""
--- Part Two ---

You quickly reach the farthest point of the loop, but the animal never emerges. Maybe its nest is within the 
area enclosed by the loop?

To determine whether it's even worth taking the time to search for such a nest, you should calculate how many 
tiles are contained within the loop. For example:
    ...........       ...........
    .S-------7.       .S-------7.
    .|F-----7|.       .|F-----7|.
    .||.....||.       .||OOOOO||.
    .||.....||.   ->  .||OOOOO||.
    .|L-7.F-J|.       .|L-7OF-J|.
    .|..|.|..|.       .|II|O|II|.
    .L--J.L--J.       .L--JOL--J.
    ...........       .....O.....
The above loop encloses merely four tiles - the two pairs of . in the southwest and southeast (marked I). 
The middle . tiles (marked O) are not in the loop. Here is the same loop again with those regions marked:

In fact, there doesn't even need to be a full tile path to the outside for tiles to count as outside the loop - 
squeezing between pipes is also allowed! Here, I is still within the loop and O is still outside the loop:
    ..........
    .S------7.
    .|F----7|.
    .||OOOO||.
    .||OOOO||.
    .|L-7F-J|.
    .|II||II|.
    .L--JL--J.
    ..........
In both of the above examples, 4 tiles are enclosed by the loop.
Here's a larger example:
    .F----7F7F7F7F-7....        OF----7F7F7F7F-7OOOO
    .|F--7||||||||FJ....        O|F--7||||||||FJOOOO
    .||.FJ||||||||L7....        O||OFJ||||||||L7OOOO
    FJL7L7LJLJ||LJ.L-7..        FJL7L7LJLJ||LJIL-7OO
    L--J.L7...LJS7F-7L7.   ->   L--JOL7IIILJS7F-7L7O
    ....F-J..F7FJ|L7L7L7        OOOOF-JIIF7FJ|L7L7L7
    ....L7.F7||L7|.L7L7|        OOOOL7IF7||L7|IL7L7|
    .....|FJLJ|FJ|F7|.LJ        OOOOO|FJLJ|FJ|F7|OLJ
    ....FJL-7.||.||||...        OOOOFJL-7O||O||||OOO
    ....L---J.LJ.LJLJ...        OOOOL---JOLJOLJLJOOO
The above sketch has many random bits of ground, some of which are in the loop (I) and some of which are 
outside it (O). In this larger example, 8 tiles are enclosed by the loop.

Any tile that isn't part of the main loop can count as being enclosed by the loop. Here's another example with 
many bits of junk pipe lying around that aren't connected to the main loop at all:
    FF7FSF7F7F7F7F7F---7        FF7FSF7F7F7F7F7F---7
    L|LJ||||||||||||F--J        L|LJ||||||||||||F--J
    FL-7LJLJ||||||LJL-77        FL-7LJLJ||||||LJL-77
    F--JF--7||LJLJ7F7FJ-        F--JF--7||LJLJIF7FJ-
    L---JF-JLJ.||-FJLJJ7   ->   L---JF-JLJIIIIFJLJJ7
    |F|F-JF---7F7-L7L|7|        |F|F-JF---7IIIL7L|7|
    |FFJF7L7F-JF7|JL---7        |FFJF7L7F-JF7IIL---7
    7-L-JL7||F7|L7F-7F7|        7-L-JL7||F7|L7F-7F7|
    L.L7LFJ|||||FJL7||LJ        L.L7LFJ|||||FJL7||LJ
    L7JLJL-JLJLJL--JLJ.L        L7JLJL-JLJLJL--JLJ.L
In this last example, 10 tiles (marked I) are enclosed by the loop.

Figure out whether you have time to search for the nest by calculating the area within the loop. 
How many tiles are enclosed by the loop?

"""

import numpy as np

from collections import deque
from typing import Tuple

SHAPES = {"NS": "|", "EW": "-", "EN": "L", "NW": "J", "SW": ">", "ES": "F"}
OFFSETS = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}
OFFSETS_B = [*OFFSETS.values()] + [(-1, -1), (-1, 1), (1, -1), (1, 1)]
CONNECTS = {"N": "|LJ", "S": "|>F", "E": "-LF", "W": "-J>"}
JOINS = {"N": "|>F", "S": "|LJ", "E": "-J>", "W": "-LF"}

def replace_s(y: int, x:int) -> None:
    paths = sorted(d for d, off in OFFSETS.items() if grid[y + 2*off[0], x + 2*off[1]] in JOINS[d])
    grid[y, x] = SHAPES["".join(paths)]
    
def get_path(s: Tuple[int]) -> None:
    q = deque([(*s, 0, grid[s])])
    grid[s] = 0
    while q:
        y, x, n, shape = q.pop()
        for d, spot in OFFSETS.items():
            if shape not in CONNECTS[d]: continue
            ny, nx = y + spot[0], x + spot[1]
            if grid[ny, nx] in JOINS[d]:
                q.appendleft((ny, nx, n + 1, grid[ny, nx]))
                grid[ny, nx] = n + 1

def get_start(s: str) -> Tuple[int]:
    for row_index, row in enumerate(grid):
        for col_index in range(len(row) - 2):
            if all(row[col_index + i] == s for i in range(3)):
                return (row_index, col_index)
                
def perimeter(s: Tuple[int]) -> None:
    q = deque([s])
    grid[s] = "@"
    while q:
        y, x = q.pop()
        for off_y, off_x in OFFSETS_B:
            ny, nx = y + off_y, x + off_x
            if grid[ny, nx] == " ":
                q.appendleft((ny, nx))
                grid[ny, nx] = "@"
    
with open("input2.txt") as f:
    txt = f.read().replace("7", ">").strip().split("\n")
    txt = ["-".join(list(line)) for line in txt]
    size = len(txt[0])
    txt = ("|"*size).join(txt)

grid = np.array(list(txt), dtype=np.dtype('<U4')).reshape((size, size))
start = divmod(txt.find("S"), size)
replace_s(*start)

get_path(start)
path_walls = np.vectorize(lambda x: f"@" if x.isdigit() else " ")
grid = path_walls(grid)

perimeter(get_start(" "))
count_blanks = np.vectorize(lambda x: "*" if x.isspace() else " ")
grid = count_blanks(grid)

evens = np.arange(0, grid.shape[0], 2)
grid = grid[evens][:, evens]

print(np.count_nonzero(grid == "*"))
    
#total enclosed tiles is 563
