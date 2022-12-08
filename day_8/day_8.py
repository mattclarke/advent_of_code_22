import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

TREES = []
SEEN = set()

for l in lines:
    row = []
    for c in l:
        row.append(int(c))
    TREES.append(row)

cols = [-1 for _ in range(len(TREES[0]))]

for r, row in enumerate(TREES):
    height = -1
    for c, t in enumerate(row):
        if t > height:
            height = t
            SEEN.add((r, c))
    height = -1
    for c, t in enumerate(reversed(row)):
        if t > height:
            height = t
            SEEN.add((r, len(cols) - c - 1))
    for c, t in enumerate(row):
        if t > cols[c]:
            cols[c] = t
            SEEN.add((r, c))

cols = [-1 for _ in range(len(TREES[0]))]
for r, row in enumerate(reversed(TREES)):
    for c, t in enumerate(row):
        if t > cols[c]:
            cols[c] = t
            SEEN.add((len(TREES) - r - 1, c))

# Part 1 = 1647
print(f"answer = {len(SEEN)}")

result = 0

for s in SEEN:
    rmax = TREES[s[0]][s[1]]
    total = 1

    score = 0
    for r in range(s[0], 0, -1):
        if TREES[r - 1][s[1]] >= rmax:
            score += 1
            break
        score += 1
    total *= score

    score = 0
    for r in range(s[0] + 1, len(TREES)):
        if TREES[r][s[1]] >= rmax:
            score += 1
            break
        score += 1
    total *= score

    score = 0
    for c in range(s[1], 0, -1):
        if TREES[s[0]][c - 1] >= rmax:
            score += 1
            break
        score += 1
    total *= score

    score = 0
    for c in range(s[1] + 1, len(TREES[0])):
        if TREES[s[0]][c] >= rmax:
            score += 1
            break
        score += 1
    total *= score

    result = max(total, result)

# Part 2 = 392080
print(f"answer = {result}")
