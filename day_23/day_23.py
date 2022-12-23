import copy
import sys

from collections import defaultdict


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

ELVES = set()
D = ["n", "s", "w", "e"]

for r, l in enumerate(lines):
    for c, ch in enumerate(l):
        if ch == "#":
            ELVES.add((r, c))


def count_free(elves):
    minr = min(e[0] for e in elves)
    maxr = max(e[0] for e in elves)
    minc = min(e[1] for e in elves)
    maxc = max(e[1] for e in elves)
    count = 0
    for r in range(minr, maxr + 1, 1):
        row = []
        for c in range(minc, maxc + 1, 1):
            if (r, c) not in elves:
                count += 1
    return count


elves = copy.copy(ELVES)
dir_ = copy.copy(D)

result_1 = 0
result_2 = 0
round_num = 0

while True:
    round_num += 1
    new_to_old = defaultdict(lambda: [])
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
            new_to_old[e].append(e)
            continue

        moved = False
        for dd in dir_:
            if dd == "n":
                d1 = (e[0] - 1, e[1])
                d2 = (e[0] - 1, e[1] + 1)
                d3 = (e[0] - 1, e[1] - 1)
                if d1 not in elves and d2 not in elves and d3 not in elves:
                    moved = True
                    new_to_old[d1].append(e)
                    break
            elif dd == "s":
                d1 = (e[0] + 1, e[1])
                d2 = (e[0] + 1, e[1] + 1)
                d3 = (e[0] + 1, e[1] - 1)
                if d1 not in elves and d2 not in elves and d3 not in elves:
                    moved = True
                    new_to_old[d1].append(e)
                    break
            elif dd == "w":
                d1 = (e[0], e[1] - 1)
                d2 = (e[0] + 1, e[1] - 1)
                d3 = (e[0] - 1, e[1] - 1)
                if d1 not in elves and d2 not in elves and d3 not in elves:
                    moved = True
                    new_to_old[d1].append(e)
                    break
            elif dd == "e":
                d1 = (e[0], e[1] + 1)
                d2 = (e[0] + 1, e[1] + 1)
                d3 = (e[0] - 1, e[1] + 1)
                if d1 not in elves and d2 not in elves and d3 not in elves:
                    moved = True
                    new_to_old[d1].append(e)
                    break
        if not moved:
            new_to_old[e].append(e)

    no_moves = True
    elves = set()
    for new, olds in new_to_old.items():
        if len(olds) == 1:
            # Only elf going to or staying at that position
            if new != olds[0]:
                no_moves = False
            elves.add(new)
        else:
            # 2+ elves going to the same square, so they all stay at their old positions
            elves.update(olds)
    if no_moves:
        result_2 = round_num
        break
    if round_num == 10:
        result_1 = count_free(elves)
    dir_.append(dir_.pop(0))

# Part 1 = 3877
print(f"answer = {result_1}")

# Part 2 = 982
print(f"answer = {result_2}")
