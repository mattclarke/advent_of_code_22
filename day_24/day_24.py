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

for r, l in enumerate(lines):
    row = []
    for c, ch in enumerate(l):
        if ch in ["#", "."]:
            row.append(ch)
        elif ch in [">", "<", "v", "^"]:
            row.append(".")
            WINDS.append((r, c, ch))
        else:
            assert False
    GRID.append(row)

START = (0, GRID[0].index("."))
END = (len(GRID) - 1, GRID[~0].index("."))


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
            if c == len(GRID[0]) - 1:
                c = 1
        elif d == "<":
            c -= 1
            if c == 0:
                c = len(GRID[0]) - 2
        elif d == "^":
            r -= 1
            if r == 0:
                r = len(GRID) - 2
        elif d == "v":
            r += 1
            if r == len(GRID) - 1:
                r = 1
        nwinds.append((r, c, d))
        squares.add((r, c))
    winds = nwinds
    if squares in WIND_SEEN:
        break
    WIND_CACHE[t] = squares


D = [(1, 0), (0, -1), (0, 1), (-1, 0)]


def calc_manhatten(pos, tgt):
    if tgt == END:
        return tgt[0] - pos[0] + tgt[1] - pos[1]
    else:
        return pos[0] - tgt[0] + pos[1] - tgt[1]


def solve(start, end, minute):
    result = 100000000000000000
    q = [((calc_manhatten(start, end), minute), minute, start)]
    SEEN = set()
    while q:
        score, minute, pos = heappop(q)
        md = calc_manhatten(pos, end)
        if md == 1:
            # Once we are within one can go straight to the exit.
            if minute + 1 < result:
                if minute + 1 < result:
                    result = minute + 1
            continue
        if minute >= result:
            continue
        if minute + md >= result:
            continue
        if (pos, minute) in SEEN:
            continue
        SEEN.add((pos, minute))

        wind_squares = WIND_CACHE[(minute + 1) % len(WIND_CACHE)]
        for dr, dc in D:
            npos = (pos[0] + dr, pos[1] + dc)
            if npos[0] < 0 or npos[0] > len(GRID) - 1:
                continue
            elif npos in wind_squares:
                continue
            elif GRID[npos[0]][npos[1]] == ".":
                if minute + 1 >= result:
                    continue
                heappush(q, ((calc_manhatten(npos, end), -minute), minute + 1, npos))
        # wait
        if pos in wind_squares:
            # cannot stay put
            continue
        heappush(q, ((calc_manhatten(pos, end), -minute), minute + 1, pos))
    return result


minute = solve(START, END, 0)

# Part 1 = 242
print(f"answer = {minute}")

minute = solve(END, START, minute)
minute = solve(START, END, minute)

# Part 2 = 720
print(f"answer = {minute}")
