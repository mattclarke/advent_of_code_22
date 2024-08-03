import copy
import sys

from collections import defaultdict, deque
from heapq import heappush, heappop

FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

GRID = []
WINDS = []

lines = lines[1:-1]

for r, l in enumerate(lines):
    row = []
    l = l.replace("#", "")
    for c, ch in enumerate(l):
        if ch == ".":
            row.append(ch)
        elif ch in [">", "<", "v", "^"]:
            row.append(".")
            WINDS.append((r, c, ch))
        else:
            assert False
    GRID.append(row)

START = (0, 0)
END = (len(GRID) - 1, len(GRID[~0]) - 1)


def show(grid, winds, pos):
    w = defaultdict(lambda: [])
    for r, c, d in winds:
        w[(r, c)].append(d)

    for r, row in enumerate(grid):
        l = []
        for c, ch in enumerate(row):
            if (r, c) == pos:
                l.append("E")
            elif (r, c) in w:
                if len(w[(r, c)]) == 1:
                    l.append(w[(r, c)][0])
                else:
                    l.append(str(len(w[r, c])))
            else:
                l.append(ch)
        print("".join(l))
    print()


# Prebuild the wind cache
winds = WINDS
WIND_CACHE = {}
WIND_SEEN = set()
t = 0

while True:
    if t == 0:
        squares = set()
        for r, c, d in winds:
            if d in {">", "<", "v", "^"}:
                squares.add((r, c))
        WIND_CACHE[t] = squares
        WIND_SEEN.add(frozenset(squares))
    t += 1
    squares = set()
    nwinds = []
    for i, (r, c, d) in enumerate(winds):
        if d == ">":
            c += 1
            if c == len(GRID[0]):
                c = 0
        elif d == "<":
            c -= 1
            if c == -1:
                c = len(GRID[0]) - 1
        elif d == "^":
            r -= 1
            if r == -1:
                r = len(GRID) - 1
        elif d == "v":
            r += 1
            if r == len(GRID):
                r = 0
        nwinds.append((r, c, d))
        squares.add((r, c))
    winds = nwinds
    if squares in WIND_SEEN:
        break
    WIND_CACHE[t] = squares


D = [(1, 0), (0, -1), (0, 1), (-1, 0)]


def solve(start, end, minute):
    result = 100000000000000000
    q = deque([(minute, start)])
    SEEN = set()
    while q:
        minute, pos = q.popleft()
        if pos == end:
            result = min(result, minute)
            continue
        if minute >= result:
            continue
        if (pos, minute) in SEEN:
            continue
        SEEN.add((pos, minute))

        wind_squares = WIND_CACHE[(minute + 1) % len(WIND_CACHE)]
        for dr, dc in D:
            npos = (pos[0] + dr, pos[1] + dc)
            if npos[0] < 0 or npos[0] > END[0] or npos[1] < 0 or npos[1] > END[1]:
                continue
            elif npos in wind_squares:
                continue
            elif GRID[npos[0]][npos[1]] == ".":
                if minute + 1 >= result:
                    continue
                q.append((minute + 1, npos))
        # wait
        if pos in wind_squares:
            # cannot stay put
            continue
        q.append((minute + 1, pos))
    return result + 1


minute = solve(START, END, 0)

# Part 1 = 242
print(f"answer = {minute}")

minute = solve(END, START, minute)
minute = solve(START, END, minute)

# Part 2 = 720
print(f"answer = {minute}")


# # Solving it in a game of life style
# # Based on a solution I saw in APL
def solve_new(start, end, minute):
    curr_grid = defaultdict(lambda: False)

    while curr_grid[end] != True:
        wind_squares = WIND_CACHE[(minute + 1) % len(WIND_CACHE)]
        next_grid = defaultdict(lambda: False)

        if start not in wind_squares:
            next_grid[start] = True
        for r in range(END[0] + 1):
            for c in range(END[1] + 1):
                if not curr_grid[(r, c)]:
                    continue
                for d in [(0, 0), (1, 0), (0, -1), (0, 1), (-1, 0)]:
                    npos = (r + d[0], c + d[1])
                    if (
                        npos[0] < 0
                        or npos[0] > END[0]
                        or npos[1] < 0
                        or npos[1] > END[1]
                    ):
                        continue
                    elif npos in wind_squares:
                        continue
                    else:
                        next_grid[npos] = True
        curr_grid = next_grid
        minute += 1
    return minute + 1


minute = solve_new(START, END, 0)
print(f"answer = {minute}")

minute = solve_new(START, END, solve_new(END, START, minute - 1) - 1)
print(f"answer = {minute}")
