import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

result = 0
CUBES = set()


for l in lines:
    coords = tuple([int(x) for x in l.split(',')])
    CUBES.add(coords)

for cube in CUBES:
    for x, y, z in [(1, 0,0), (-1, 0,0), (0, 1,0), (0, -1,0), (0,0,1), (0,0,-1)]:
        if (cube[0] + x, cube[1] + y, cube[2] + z) not in CUBES:
            result += 1

# Part 1 = 4636
print(f"answer = {result}")

result = 0

# Part 2 = 
print(f"answer = {result}")
