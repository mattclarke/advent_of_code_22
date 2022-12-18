import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

CUBES = set()

for l in lines:
    coords = tuple([int(x) for x in l.split(",")])
    CUBES.add(coords)

result = 0
min_x = 10000000000
max_x = 0
min_y = 10000000000
max_y = 0
min_z = 10000000000
max_z = 0

for cube in CUBES:
    for x, y, z in [
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    ]:
        if (cube[0] + x, cube[1] + y, cube[2] + z) not in CUBES:
            result += 1
        # For part 2
        min_x = min(min_x, cube[0] + x)
        max_x = max(max_x, cube[0] + x)
        min_y = min(min_y, cube[1] + y)
        max_y = max(max_y, cube[1] + y)
        min_z = min(min_z, cube[2] + z)
        max_z = max(max_z, cube[2] + z)

# Part 1 = 4636
print(f"answer = {result}")

WATER = set()
result = 0

for x in [min_x, max_x]:
    for y in range(min_y, max_y):
        for z in range(min_z, max_z):
            WATER.add((x, y, z))
            if (x, y, z) in CUBES:
                assert FALSE

for y in [min_y, max_y]:
    for x in range(min_x, max_x):
        for z in range(min_z, max_z):
            WATER.add((x, y, z))
            if (x, y, z) in CUBES:
                assert FALSE

for z in [min_z, max_z]:
    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            WATER.add((x, y, z))
            if (x, y, z) in CUBES:
                assert FALSE


def show(x):
    for y in range(min_y, max_y + 1):
        row = []
        for z in range(min_z, max_z + 1):
            if (x, y, z) in CUBES:
                row.append("#")
            elif (x, y, z) in WATER:
                row.append("~")
            else:
                row.append(" ")
        print("".join(row))
    print("")


# Flood the area until water had reached everywhere it can
while True:
    prev = len(WATER)
    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            for z in range(min_z, max_z):
                if (x, y, z) in CUBES or (x, y, z) in WATER:
                    continue
                for dx, dy, dz in [
                    (1, 0, 0),
                    (-1, 0, 0),
                    (0, 1, 0),
                    (0, -1, 0),
                    (0, 0, 1),
                    (0, 0, -1),
                ]:
                    if (x + dx, y + dy, z + dz) in WATER:
                        WATER.add((x, y, z))
                        continue
    if len(WATER) == prev:
        break

for cube in CUBES:
    for x, y, z in [
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    ]:
        if (cube[0] + x, cube[1] + y, cube[2] + z) in WATER:
            result += 1

# Part 2 = 2572
print(f"answer = {result}")
