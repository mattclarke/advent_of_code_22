import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

ELVES = set()
D = [(-1, 0), (1, 0), (-1, 0), (1, 0)]
D = ["n", "s", "w", "e"]

for r, l in enumerate(lines):
    for c, ch in enumerate(l):
        if ch == "#":
            ELVES.add((r, c))


def count_free(elves):
    minr = 100000
    maxr = 0
    minc = 100000
    maxc = 0
    for e in elves:
        minr = min(minr, e[0])
        minc = min(minc, e[1])
        maxr = max(maxr, e[0])
        maxc = max(maxc, e[1])
    count = 0
    for r in range(minr, maxr + 1, 1):
        row = []
        for c in range(minc, maxc + 1, 1):
            if (r, c) not in elves:
                count += 1
    return count


elves = copy.copy(ELVES)
d = copy.copy(D)
result_1 = 0
result_2 = 0
rnd = 0

while True:
    rnd += 1
    new_elves = set()
    dups = set()
    for e in elves:
        no_move = True
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if (e[0] + dr, e[1] + dc) in elves:
                    no_move = False
                    break
        if no_move:
            new_elves.add(e)
            continue

        for dd in d:
            if dd == "n":
                d1 = (e[0] - 1, e[1])
                d2 = (e[0] - 1, e[1] + 1)
                d3 = (e[0] - 1, e[1] - 1)
                if d1 not in elves and d2 not in elves and d3 not in elves:
                    if d1 not in new_elves:
                        new_elves.add(d1)
                    else:
                        dups.add(d1)
                    break
            elif dd == "s":
                d1 = (e[0] + 1, e[1])
                d2 = (e[0] + 1, e[1] + 1)
                d3 = (e[0] + 1, e[1] - 1)
                if d1 not in elves and d2 not in elves and d3 not in elves:
                    if d1 not in new_elves:
                        new_elves.add(d1)
                    else:
                        dups.add(d1)
                    break
            elif dd == "w":
                d1 = (e[0], e[1] - 1)
                d2 = (e[0] + 1, e[1] - 1)
                d3 = (e[0] - 1, e[1] - 1)
                if d1 not in elves and d2 not in elves and d3 not in elves:
                    if d1 not in new_elves:
                        new_elves.add(d1)
                    else:
                        dups.add(d1)
                    break
            elif dd == "e":
                d1 = (e[0], e[1] + 1)
                d2 = (e[0] + 1, e[1] + 1)
                d3 = (e[0] - 1, e[1] + 1)
                if d1 not in elves and d2 not in elves and d3 not in elves:
                    if d1 not in new_elves:
                        new_elves.add(d1)
                    else:
                        dups.add(d1)
                    break
    new_elves = set()
    counter = 0
    for e in elves:
        moved = False
        no_move = True
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if (e[0] + dr, e[1] + dc) in elves:
                    no_move = False
                    break
        if no_move:
            new_elves.add(e)
            counter += 1
            continue

        for dd in d:
            if dd == "n":
                d1 = (e[0] - 1, e[1])
                d2 = (e[0] - 1, e[1] + 1)
                d3 = (e[0] - 1, e[1] - 1)
                if d1 not in elves and d2 not in elves and d3 not in elves:
                    moved = True
                    if d1 in dups:
                        new_elves.add(e)
                    else:
                        new_elves.add(d1)
                        nobody_moved = False
                    break
            elif dd == "s":
                d1 = (e[0] + 1, e[1])
                d2 = (e[0] + 1, e[1] + 1)
                d3 = (e[0] + 1, e[1] - 1)
                if d1 not in elves and d2 not in elves and d3 not in elves:
                    moved = True
                    if d1 in dups:
                        new_elves.add(e)
                    else:
                        new_elves.add(d1)
                        nobody_moved = False
                    break
            elif dd == "w":
                d1 = (e[0], e[1] - 1)
                d2 = (e[0] + 1, e[1] - 1)
                d3 = (e[0] - 1, e[1] - 1)
                if d1 not in elves and d2 not in elves and d3 not in elves:
                    moved = True
                    if d1 in dups:
                        new_elves.add(e)
                    else:
                        new_elves.add(d1)
                        nobody_moved = False
                    break
            elif dd == "e":
                d1 = (e[0], e[1] + 1)
                d2 = (e[0] + 1, e[1] + 1)
                d3 = (e[0] - 1, e[1] + 1)
                if d1 not in elves and d2 not in elves and d3 not in elves:
                    moved = True
                    if d1 in dups:
                        new_elves.add(e)
                    else:
                        new_elves.add(d1)
                        nobody_moved = False
                    break
        if not moved:
            new_elves.add(e)
    if counter == len(elves):
        result_2 = rnd
        break
    if rnd == 10:
        result_1 = count_free(new_elves)
    elves = new_elves
    frt = d.pop(0)
    d.append(frt)

# Part 1 = 3877
print(f"answer = {result_1}")

# Part 2 = 982
print(f"answer = {result_2}")
