import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

ROCKS = set()
rmin = 10000000000
rmax = -1
cmin = 0
cmax = -1

for l in lines:
    parts = l.split(" -> ")
    parts = [(int(x.split(",")[0]), int(x.split(",")[1])) for x in parts]
    i = 0
    while i < len(parts) - 1:
        p1 = parts[i]
        p2 = parts[i + 1]
        rmin = min(rmin, p1[0], p2[0])
        rmax = max(rmax, p1[0], p2[0])
        cmin = min(cmin, p1[1], p2[1])
        cmax = max(cmax, p1[1], p2[1])
        if p1[0] != p2[0]:
            r1 = min(p1[0], p2[0])
            r2 = max(p1[0], p2[0])
            for r in range(r1, r2 + 1):
                ROCKS.add((r, p1[1]))
        elif p1[1] != p2[1]:
            r1 = min(p1[1], p2[1])
            r2 = max(p1[1], p2[1])
            for r in range(r1, r2 + 1):
                ROCKS.add((p1[0], r))
        else:
            assert False
        i += 1


def print_cave(sand=None):
    for r in range(cmin, cmax + 3):
        row = []
        for c in range(rmin - 5, rmax + 6):
            if (c, r) in ROCKS:
                row.append("#")
            elif sand and (c, r) in sand:
                row.append("o")
            else:
                row.append(".")
        print("".join(row))


USED = set(ROCKS)
sand = set()

s = (500, 0)
while True:
    if not (rmin <= s[0] <= rmax) or s[1] > cmax:
        break
    if (s[0], s[1] + 1) not in USED:
        s = (s[0], s[1] + 1)
    elif (s[0] - 1, s[1] + 1) not in USED:
        s = (s[0] - 1, s[1] + 1)
    elif (s[0] + 1, s[1] + 1) not in USED:
        s = (s[0] + 1, s[1] + 1)
    else:
        # Stopped
        sand.add(s)
        USED.add(s)
        s = (500, 0)

# Part 1 = 737
print(f"answer = {len(sand)}")

result = 0
USED = set(ROCKS)
sand = set()

s = (500, 0)
while True:
    if s[1] > cmax:
        sand.add(s)
        USED.add(s)
        s = (500, 0)
    elif (s[0], s[1] + 1) not in USED:
        s = (s[0], s[1] + 1)
    elif (s[0] - 1, s[1] + 1) not in USED:
        s = (s[0] - 1, s[1] + 1)
    elif (s[0] + 1, s[1] + 1) not in USED:
        s = (s[0] + 1, s[1] + 1)
    else:
        # Stopped
        sand.add(s)
        USED.add(s)
        if s == (500, 0):
            break
        s = (500, 0)

# Part 2 = 28145
print(f"answer = {len(sand)}")
