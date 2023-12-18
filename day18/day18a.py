"""
--- Day 18: Lavaduct Lagoon ---

Thanks to your efforts, the machine parts factory is one of the first factories up and running since the 
lavafall came back. However, to catch up with the large backlog of parts requests, the factory will also need a 
large supply of lava for a while; the Elves already started creating a large lagoon nearby for this purpose.

However, they aren't sure the lagoon will be big enough; they've asked you to take a look at the dig plan 
(your puzzle input). For example:
    R 6 (#70c710)
    D 5 (#0dc571)
    L 2 (#5713f0)
    D 2 (#d2c081)
    R 2 (#59c680)
    D 2 (#411b91)
    L 5 (#8ceee2)
    U 2 (#caa173)
    L 1 (#1b58a2)
    U 2 (#caa171)
    R 2 (#7807d2)
    U 3 (#a77fa3)
    L 2 (#015232)
    U 2 (#7a21e3)
The digger starts in a 1 meter cube hole in the ground. They then dig the specified number of meters up (U), 
down (D), left (L), or right (R), clearing full 1 meter cubes as they go. The directions are given as seen from 
above, so if "up" were north, then "right" would be east, and so on. Each trench is also listed with the color 
that the edge of the trench should be painted as an RGB hexadecimal color code.

When viewed from above, the above example dig plan would result in the following loop of trench (#) having been 
dug out from otherwise ground-level terrain (.) [A] At this point, the trench could contain 38 cubic meters of 
lava. However, this is just the edge of the lagoon; the next step is to dig out the interior so that it is one 
meter deep as well [B]:
    [A]  #######      [B]  #######
         #.....#           #######
         ###...#           #######
         ..#...#           ..#####
         ..#...#           ..#####
         ###.###           #######
         #...#..           #####..
         ##..###           #######
         .#....#           .######
         .######           .######
Now, the lagoon can contain a much more respectable 62 cubic meters of lava. While the interior is dug out, 
the edges are also painted according to the color codes in the dig plan.

The Elves are concerned the lagoon won't be large enough; if they follow their dig plan, 
how many cubic meters of lava could it hold?

"""

from typing import Tuple
    
def shoelace(corners: Tuple[int, int]) -> int:
    ys, xs = zip(*corners)
    n = len(xs)
    area = 0.5 * abs(sum(xs[i] * ys[(i + 1) % n] - xs[(i + 1) % n] * ys[i] for i in range(n)))
    return int(area)
    
with open("input.txt") as f:
    instructions = [line.split()[:2] for line in f]

DIRS = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
corners = []
steps = 0
y, x = 0, 0

for d, n in instructions:
    n = int(n)
    y, x = y + DIRS[d][0] * n, x + DIRS[d][1] * n
    corners.append((y, x))
    steps += n

picks = (steps + 2) // 2
    
print(shoelace(corners) + picks)

# capacity is 36807m³
