import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

GRID = []
START = None
P2 = []

for r, l in enumerate(lines):
    row = []
    for c, ch in enumerate(l):
        if ch == "S":
            START = (r, c)
            P2.append((0, START))
        if ch == "E":
            END = (r, c)
        if ch == "a":
            P2.append((0, (r, c)))
        row.append(ch)
    GRID.append(row)


def solve(queue):
    best = set()

    while queue:
        cnt, pos = queue.pop(0)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            npos = (pos[0] + dr, pos[1] + dc)
            cl = GRID[pos[0]][pos[1]]
            if (
                npos[0] < 0
                or npos[0] == len(GRID)
                or npos[1] < 0
                or npos[1] == len(GRID[0])
            ):
                continue
            if npos in best:
                continue
            nl = GRID[npos[0]][npos[1]]
            if nl == "a" and cl == "S":
                queue.append((cnt + 1, npos))
                continue
            elif nl == "E" and cl == "z":
                return cnt + 1
            elif nl == "E":
                continue
            elif ord(nl) - ord(cl) <= 1:
                best.add(npos)
                queue.append((cnt + 1, npos))
    assert False


# Part 1 = 380
print(f"answer = {solve([(0, START)])}")

# Part 2 = 375
print(f"answer = {solve(P2[:])}")
