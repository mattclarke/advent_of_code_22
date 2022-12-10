import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

result = 0

X =1
Q = None
cycle = 1
finish = False
busy = False
add = 0

while lines or Q is not None:
    if cycle in  [20, 60, 100, 140, 180, 220]:
        result += cycle * X
    if lines and Q is None:
        l = lines.pop(0)
        if l != 'noop':
            op, val = l.split(' ')
            Q = int(val)
            cycle += 1
            continue
    if Q is not None:
        X += Q
        Q = None
    cycle += 1
    

# Part 1 = 13860 
print(f"answer = {result}")

result = 0

# Part 2 = 
print(f"answer = {result}")
