"""
--- Part Two ---

The galaxies are much older (and thus much farther apart) than the researcher initially estimated.

Now, instead of the expansion you did before, make each empty row or column one million times larger. That is, 
each empty row should be replaced with 1000000 empty rows, and each empty column should be replaced with 1000000 
empty columns.

(In the example above, if each empty row or column were merely 10 times larger, the sum of the shortest paths 
between every pair of galaxies would be 1030. If each empty row or column were merely 100 times larger, the sum 
of the shortest paths between every pair of galaxies would be 8410. However, your universe will need to expand 
far beyond these values.)

Starting with the same initial image, expand the universe according to these new rules, then find the length of 
the shortest path between every pair of galaxies. What is the sum of these lengths?

"""

import numpy as np

from itertools import combinations
from typing import Tuple

def get_dist(exp_c: int, exp_r: int, s: Tuple[int], e: Tuple[int]) -> int:
    multiplier = 1000000
    sy, sx = s
    ey, ex = e
    base_x = abs(sx - ex)
    base_y = abs(sy - ey)
    a = sum(exp in range(*sorted([sy, ey])) for exp in exp_r) * (multiplier - 1)
    b = sum(exp in range(*sorted([sx, ex])) for exp in exp_c) * (multiplier - 1)
    return base_x + base_y + a + b
    
with open("input.txt") as f:
    txt = [*map(str.strip, f.readlines())]
    shape = len(txt), len(txt[0])
    
grid = np.array([*map(list,txt)]).reshape(shape)
galaxies = [tuple(i) for i in np.argwhere(grid == '#')]
exp_r = np.where(~np.any(grid == '#', axis=1))[0]
exp_c = np.where(~np.any(grid == '#', axis=0))[0]

print(sum(get_dist(exp_c, exp_r, s, e) for s, e in combinations(galaxies, 2)))
            
# sum is 382979724122
