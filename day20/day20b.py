"""
--- Part Two ---

The final machine responsible for moving the sand down to Island Island has a module attached named rx. 
The machine turns on when a single low pulse is sent to rx.

Reset all modules to their default states. Waiting for all pulses to be fully handled after each button press, 
what is the fewest number of button presses required to deliver a single low pulse to the module named rx?

"""

import re

from typing import List, Tuple, Dict
from math import lcm


class Module:
    def __init__(self, kind: str, name: str, dest: str):
        self.name = name
        self.relay = dest.split(", ")
        self.mem = 0 if kind == "%" else {}
        self.kind = kind
        
    def send(self, o: str, pulse: int) -> List[Tuple[str, int, str]]:
        if self.kind == "&":
            self.mem[o] = pulse
            sending = int(sum(self.mem.values()) != len(self.mem))
            return [(self.name, sending, i) for i in self.relay]
        elif not pulse:
            self.mem = not self.mem
            return [(self.name, int(self.mem), i) for i in self.relay]
        return []


def begin(initial: List[str], modules: Dict[str, Module]) -> int:
    c = 0
    trigger, = [name for name, m in modules.items() if "rx" in m.relay]
    requirements = {name: None for name, m in modules.items() if trigger in m.relay}
    
    while not all(requirements.values()):
        c += 1
        queue = [("O", 0, d) for d in initial]

        while queue:
            orig, pulse, dest = queue.pop(0)
            if orig in requirements and requirements[orig] is None and pulse == 1:
                requirements[orig] = c
            if dest in modules:
                queue.extend(modules[dest].send(orig, pulse))
                
    return lcm(*requirements.values())
    

initial = []
modules = {}
            
with open("input2.txt") as f:
    for x in f.readlines():
        kind, name, dest = re.match(r"([%&]?)(\w+) -> (.*)", x).groups()
        if name == "broadcaster":
            initial = dest.split(", ")
            continue
        modules[name] = Module(kind, name, dest)
            
for name, module in modules.items():
    for r in module.relay:
        if r in modules and modules[r].kind == "&":
            modules[r].mem[name] = False

print(begin(initial, modules))
    
# minimum is 247702167614647
