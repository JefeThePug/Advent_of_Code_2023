"""
--- Day 17: Clumsy Crucible ---

The lava starts flowing rapidly once the Lava Production Facility is operational. As you leave, the reindeer 
offers you a parachute, allowing you to quickly reach Gear Island.

As you descend, your bird's-eye view of Gear Island reveals why you had trouble finding anyone on your way up: 
half of Gear Island is empty, but the half below you is a giant factory city!

You land near the gradually-filling pool of lava at the base of your new lavafall. Lavaducts will eventually 
carry the lava throughout the city, but to make use of it immediately, Elves are loading it into large crucibles 
on wheels.

The crucibles are top-heavy and pushed by hand. Unfortunately, the crucibles become very difficult to steer at 
high speeds, and so it can be hard to go in a straight line for very long.

To get Desert Island the machine parts it needs as soon as possible, you'll need to find the best way to get the 
crucible from the lava pool to the machine parts factory. To do this, you need to minimize heat loss while 
choosing a route that doesn't require the crucible to go in a straight line for too long.

Fortunately, the Elves here have a map (your puzzle input) that uses traffic patterns, ambient temperature, and 
hundreds of other parameters to calculate exactly how much heat loss can be expected for a crucible entering any 
particular city block. For example:
    2413432311323
    3215453535623
    3255245654254
    3446585845452
    4546657867536
    1438598798454
    4457876987766
    3637877979653
    4654967986887
    4564679986453
    1224686865563
    2546548887735
    4322674655533
Each city block is marked by a single digit that represents the amount of heat loss if the crucible enters that 
block. The starting point, the lava pool, is the top-left city block; the destination, the machine parts factory, 
is the bottom-right city block. (Because you already start in the top-left block, you don't incur that block's 
heat loss unless you leave that block and then return to it.)

Because it is difficult to keep the top-heavy crucible going in a straight line for very long, it can move at 
most three blocks in a single direction before it must turn 90 degrees left or right. The crucible also can't 
reverse direction; after entering each city block, it may only turn left, continue straight, or turn right.
One way to minimize heat loss is this path:
    2>>34^>>>1323
    32v>>>35v5623
    32552456v>>54
    3446585845v52
    4546657867v>6
    14385987984v4
    44578769877v6
    36378779796v>
    465496798688v
    456467998645v
    12246868655<v
    25465488877v5
    43226746555v>
This path never moves more than three consecutive blocks in the same direction and incurs a heat loss of only 102.

Directing the crucible from the lava pool to the machine parts factory, but not moving more than three consecutive 
blocks in the same direction, what is the least heat loss it can incur?

"""

import numpy as np

from collections import namedtuple
from heapq import heappop, heappush


DIRECTIONS = [(-1, 0), (0, -1), (0, 1), (1, 0)]
MAX = 4

def check_straight(d1pos, d2pos, s):
    if np.array_equal(d1pos, -np.array(d2pos)): return None
    if np.array_equal(d1pos, d2pos): return s + 1
    return 1

def valid_coordinates(row, col, grid):
    return 0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]

def dijkstra(grid, start):
    Node = namedtuple("Node", "heat, pos, d_pos, straight")
    
    q = [Node(0, start, (0, 0), 1)]
    heats = np.full((*grid.shape, 4, MAX + 1), np.iinfo(np.int64).max)

    while q:
        heat, (y, x), dpos, straight = heappop(q)

        for a, b in DIRECTIONS:
            pos = y + a, x + b
            if not valid_coordinates(*pos, grid): continue
            
            _straight = check_straight(dpos, (a, b), straight)
            if not _straight or _straight == MAX: continue
                
            _heat = heat + grid[pos]
            
            if _heat < heats[(i := pos + (a + 2*max(b, 0), _straight))]:
                heats[i] = _heat
                new_element = Node(_heat, pos, (a, b), _straight)
                heappush(q, new_element)

    return heats[-1, -1].min()


with open("input.txt") as f:
    grid = np.array([[int(i) for i in line.strip()] for line in f])

print(dijkstra(grid, (0, 0)))
    
# least heat loss is 665
