"""
--- Part Two ---

Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: 
one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. 
For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?

"""

from string import ascii_lowercase as letters

def get_num(s: str) -> int:
    return int(f"{s[0]}{s[-1]}") if s else 0

def numberize(s: str) -> str:
    replacements = {
        "one": "o1e", "two": "t2o", "three": "t3e", "four": "f4r", "five": "f5e", 
        "six": "s6x", "seven": "s7n", "eight": "e8t", "nine": "n9e", "zero": "z0o"}
    for old, new in replacements.items():
        s = s.replace(old, new)
    return s

def get_calibration_sum(s: str) -> int:
    return sum(get_num(numberize(line).strip(letters)) for line in s.split("\n"))
    
with open("input.txt") as f:
    print(get_calibration_sum(f.read()))
    
#sum is 54824
