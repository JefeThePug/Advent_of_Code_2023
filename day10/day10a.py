"""
--- Day 10: Pipe Maze ---

You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal island. This 
island is surprisingly cold and there definitely aren't any thermals to glide on, so you leave your hang glider 
behind.

You wander around for a while, but you don't find any people or animals. However, you do occasionally find 
signposts labeled "Hot Springs" pointing in a seemingly consistent direction; maybe you can find someone at the 
hot springs and ask them where the desert-machine parts are made.

The landscape here is alien; even the flowers and trees are made of metal. As you stop to admire some metal 
grass, you notice something metallic scurry away in your peripheral vision and jump into a big pipe! It didn't 
look like any animal you've ever seen; if you want a better look, you'll need to get ahead of it.

Scanning the area, you discover that the entire field you're standing on is densely packed with pipes; it was 
hard to tell at first because they're the same metallic silver color as the "ground". You make a quick sketch of 
all of the surface pipes you can see (your puzzle input).

The pipes are arranged in a two-dimensional grid of tiles:
    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape 
the pipe has. Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the 
animal is one large, continuous loop.

For example, here is a square loop of pipe:
    .....
    .F-7.
    .|.|.
    .L-J.
    .....
If the animal had entered this loop in the northwest corner, the sketch would instead look like this:
    .....
    .S-7.
    .|.|.
    .L-J.
    .....
In the above diagram, the S tile is still an F: you can tell because of how the adjacent pipes connect to it.

Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows above loop:
    -L|F7
    7S-7|
    L|7||
    -L-J|
    L|-JF
In the above diagram, you can still figure out which pipes form the main loop: they're the ones connected to S, 
pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to 
its two neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to 
connect back to those two pipes).

Here is a sketch that has a slightly more complex main loop and one with extra, non-main pipe tiles also shown:
    ..F7.     7-F7-
    .FJ|.     .FJ|7
    SJ.L7     SJLL7
    |F--J     |F--J
    LJ...     LJ.LJ
If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the 
starting position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. 
Instead, you need to find the tile that would take the longest number of steps along the loop to reach from the 
starting point - regardless of which way around the loop the animal went.

In the first example with the square loop, you can count the distance each tile in the loop is from the starting 
point like this:
    .....     .....
    .S-7.     .012.
    .|.|.     .1.3.
    .L-J.     .234.
    .....     .....
In this example, the farthest point from the start is 4 steps away.

Here's the more complex loop again with the distances for each tile on that loop:
    ..F7.     ..45.
    .FJ|.     .236.
    SJ.L7     01.78
    |F--J     14567
    LJ...     23...

Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting 
position to the point farthest from the starting position?

"""

import numpy as np

from collections import deque
from typing import Tuple

SHAPES = {"NS": "|", "EW": "-", "EN": "L", "NW": "J", "SW": ">", "ES": "F"}
OFFSETS = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}
CONNECTS = {"N": "|LJ", "S": "|>F", "E": "-LF", "W": "-J>"}
JOINS = {"N": "|>F", "S": "|LJ", "E": "-J>", "W": "-LF"}

def replace_s(y: int, x:int) -> None:
    paths = sorted(d for d, off in OFFSETS.items() if grid[y + off[0], x + off[1]] in JOINS[d])
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
    
with open("input.txt") as f:
    txt = f.read().replace("7", ">").replace("\n","")
    size = int(len(txt)**0.5)

grid = np.array(list(txt), dtype=np.dtype('<U4')).reshape((size, size))
start = divmod(txt.find("S"), size)

replace_s(*start)
get_path(start)

str_to_int = np.vectorize(lambda x: int(x) if x.isdigit() else np.nan)
grid = str_to_int(grid)

print(np.nanmax(grid).astype(int))
    
#total steps is 6951
