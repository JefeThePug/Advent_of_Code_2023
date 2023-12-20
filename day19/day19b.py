"""
--- Part Two ---

Even with your help, the sorting process still isn't fast enough.

One of the Elves comes up with a new plan: rather than sort parts individually through all of these workflows, 
maybe you can figure out in advance which combinations of ratings will be accepted or rejected.

Each of the four ratings (x, m, a, s) can have an integer value ranging from a minimum of 1 to a maximum of 4000. 
Of all possible distinct combinations of ratings, your job is to figure out which ones will be accepted.

In the above example, there are 167409079868000 distinct combinations of ratings that will be accepted.

Consider only your list of workflows; the list of part ratings that the Elves wanted you to sort is no longer 
relevant. How many distinct combinations of ratings will be accepted by the Elves' workflows?

"""

from math import prod
from typing import Dict, Tuple, List
    
class Workflows:
    def __init__(self, lines: List[str]):
        self.workflows = {}
        for w in lines:
            self.add_workflow(w)
    
    def add_workflow(self, s: str) -> None:
        name, rules = s[:-1].split("{")
        rules = rules.split(",")
        steps = [(c[0], c[1], int(c[2:]), goal) for r in rules[:-1] for c, goal in [r.split(":")]]
        self.workflows[name] = (steps, rules.pop())


    def count(self, ranges: Dict[str, Tuple[int, int]], wf: str = "in") -> int:
        if wf == "R":
            return 0
        if wf == "A":
            return prod(u - l + 1 for l, u in ranges.values())
        
        total = 0
        rules, els = self.workflows[wf]
        
        for xmas, op, n, goal in rules:
            l, u = ranges[xmas]
            if op == "<":
                a, b = (l, min(n - 1, u)), (max(n, l), u)
            else:
                a, b = (max(n + 1, l), u), (l, min(n, u))
            if range(a[0], a[1] + 1):
                total += self.count(ranges | {xmas: a}, goal)
            if range(b[0], b[1] + 1):
                ranges |= {xmas: b}
            else: 
                break
        else:
            total += self.count(ranges, els)
        
        return total
                         
    
with open("input.txt") as f:
    paths, _ = f.read().strip().split("\n\n")
    
wf = Workflows(paths.splitlines())
items = {c: (1, 4000) for c in "xmas"}

print(wf.count(items))
    
# total is 
