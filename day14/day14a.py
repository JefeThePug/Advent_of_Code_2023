"""
--- Day 14: Parabolic Reflector Dish ---

You reach the place where all of the mirrors were pointing: a massive parabolic reflector dish attached to the 
side of another large mountain.

The dish is made up of many small mirrors, but while the mirrors themselves are roughly in the shape of a 
parabolic reflector dish, each individual mirror seems to be pointing in slightly the wrong direction. If the 
dish is meant to focus light, all it's doing right now is sending it in a vague direction.

This system must be what provides the energy for the lava! If you focus the reflector dish, maybe you can go 
where it's pointing and use the light to fix the lava production.

Upon closer inspection, the individual mirrors each appear to be connected via an elaborate system of ropes and 
pulleys to a large metal platform below the dish. The platform is covered in large rocks of various shapes. 
Depending on their position, the weight of the rocks deforms the platform, and the shape of the platform controls 
which ropes move and ultimately the focus of the dish.

In short: if you move the rocks, you can focus the dish. The platform even has a control panel on the side that 
lets you tilt it in one of four directions! The rounded rocks (O) will roll when the platform is tilted, while 
the cube-shaped rocks (#) will stay in place. You note the positions of all of the empty spaces (.) and rocks 
(your puzzle input). For example (A) Start by tilting the lever so all of the rocks will slide north as far as 
they will go (B):
    (A)  O....#....      (B)  OOOO.#.O..
         O.OO#....#           OO..#....#
         .....##...           OO..O##..O
         OO.#O....O           O..#.OO...
         .O.....O#.           ........#.
         O.#..O.#.#           ..#....#.#
         ..O..#O..O           ..O..#.O.O
         .......O..           ..O.......
         #....###..           #....###..
         #OO..#....           #....#....    
You notice that the support beams along the north side of the platform are damaged; to ensure the platform 
doesn't collapse, you should calculate the total load on the north support beams.

The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock to the south 
edge of the platform, including the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.) So, the 
amount of load caused by each rock in each row is as follows:
    OOOO.#.O.. 10
    OO..#....#  9
    OO..O##..O  8
    O..#.OO...  7
    ........#.  6
    ..#....#.#  5
    ..O..#.O.O  4
    ..O.......  3
    #....###..  2
    #....#....  1
The total load is the sum of the load caused by all of the rounded rocks. In this example, the total load is 136.

Tilt the platform so that the rounded rocks all roll north. 
Afterward, what is the total load on the north support beams?

"""

from typing import Tuple

class Rock:
    def __init__(self, pos: Tuple[int], space: str):
        self.y, self.x = pos
        self.rolling = space == "O"
        self.mark = space
        
    def move(self) -> None:
        if self.rolling:
            self.y -= 1


with open("input.txt") as f:
    layout = f.read().strip()

height = 1 + layout.count("\n")
width = layout.find("\n")

grid = [["."]*width for i in range(height)]
rocks = []

for y, line in enumerate(layout.split("\n")):
    for x, space in enumerate(line):
        if space in "O#":
            rocks.append(Rock((y, x), space))

for rock in rocks:
    while rock.rolling and rock.y-1 >= 0 and grid[rock.y-1][rock.x] == ".":
        rock.move()
    grid[rock.y][rock.x] = rock.mark
    
print(sum((height-i)*line.count("O") for i, line in enumerate(grid)))
    
# total is 109345
