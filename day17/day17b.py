"""
--- Part Two ---

The crucibles of lava simply aren't large enough to provide an adequate supply of lava to the machine parts 
factory. Instead, the Elves are going to upgrade to ultra crucibles.

Ultra crucibles are even more difficult to steer than normal crucibles. Not only do they have trouble going in a 
straight line, but they also have trouble turning!

Once an ultra crucible starts moving in a direction, it needs to move a minimum of four blocks in that direction 
before it can turn (or even before it can stop at the end). However, it will eventually start to get wobbly: an 
ultra crucible can move a maximum of ten consecutive blocks without turning.

In the above example, an ultra crucible could follow this path to minimize heat loss:
    2>>>>>>>>1323
    32154535v5623
    32552456v4254
    34465858v5452
    45466578v>>>>
    143859879845v
    445787698776v
    363787797965v
    465496798688v
    456467998645v
    122468686556v
    254654888773v
    432267465553v
In the above example, an ultra crucible would incur the minimum possible heat loss of 94.

Here's another example [A] Sadly, an ultra crucible would need to take an unfortunate path like this one [B]:
    [A]  111111111111        [B]  1>>>>>>>1111
         999999999991             9999999v9991
         999999999991             9999999v9991
         999999999991             9999999v9991
         999999999991             9999999v>>>>
This route causes the ultra crucible to incur the minimum possible heat loss of 71.

Directing the ultra crucible from the lava pool to the machine parts factory, 
what is the least heat loss it can incur?

"""

import numpy as np

from collections import namedtuple
from heapq import heappop, heappush


DIRECTIONS = [(-1, 0), (0, -1), (0, 1), (1, 0)]
MAX = 11

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
            if straight < 4 and _straight == 1 and dpos != (0,0): continue
            if (not _straight or _straight == MAX): continue
                
            _heat = heat + grid[pos]
            
            if _heat < heats[(i := pos + (a + 2*max(b, 0), _straight))]:
                heats[i] = _heat
                new_element = Node(_heat, pos, (a, b), _straight)
                heappush(q, new_element)
    return heats[-1, -1].min()


with open("input.txt") as f:
    grid = np.array([[int(i) for i in line.strip()] for line in f])

print(dijkstra(grid, (0, 0)))
    
# least heat loss is 809
