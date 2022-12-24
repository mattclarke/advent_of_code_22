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
    for c,ch in enumerate(l):
        if ch in ['#', '.']:
            row.append(ch)
        elif ch in ['>','<','v','^']:
            row.append('.')
            WINDS.append((r,c, ch))
        else:
            assert False
    GRID.append(row)

START = (0, GRID[0].index('.'))
END = (len(GRID) - 1, GRID[~0].index('.'))

def show(grid, winds, pos):
    w = defaultdict(lambda: [])
    for r,c,d in winds:
        w[(r,c)].append(d)

    for r, row in enumerate(grid):
        l = []
        for c, ch in enumerate(row):
            if (r,c) == pos:
                l.append('E')
            elif (r,c) in w:
                if len(w[(r,c)]) == 1:
                    l.append(w[(r,c)][0])
                else:
                    l.append(str(len(w[r,c])))
            else:
                l.append(ch)
        print(''.join(l))
    print()

#show(GRID, WINDS, START)
winds = WINDS
wind_squares = set([(r,c) for r,c,_ in winds])
WIND_CACHE = {}

def update_winds(winds):
    cached = WIND_CACHE.get(tuple(winds))
    if cached:
        return cached
    nwinds = []
    squares = set()
    for i, (r,c,d) in enumerate(winds):
        if d == '>':
            c += 1
            if c == len(GRID[0]) - 1:
               c = 1
        elif d == '<':
            c -= 1
            if c == 0:
               c = len(GRID[0]) - 2
        elif d == '^':
            r -= 1
            if r == 0:
               r = len(GRID) - 2
        elif d == 'v':
            r += 1
            if r == len(GRID) - 1:
               r = 1
        nwinds.append((r,c,d))
        squares.add((r,c))
    WIND_CACHE[tuple(winds)] = (nwinds, squares)
    return nwinds, squares

D = [(1, 0),(0, -1), (0, 1), (-1,0)]  
pos = START
q = [((END[0] - pos[0] + END[1] - pos[1], 0), 0, pos, copy.deepcopy(winds))] 
result = 100000000000000000
SEEN = set()

def calc_score(pos):
   return (END[0] - npos[0] + END[1] - npos[1])

while q:
    #print(len(q), len(SEEN))
    score, minute, pos, winds = heappop(q)
    if minute >= result:
        continue
    if (minute, pos, frozenset(winds)) in SEEN:
        continue
    SEEN.add((minute, pos, frozenset(winds)))
    #print(score, minute, pos, winds)
    #show(GRID, winds, pos)
    #input()
    winds, wind_squares = update_winds(winds)
    home = False
    for dr, dc in D:
        npos = (pos[0]+dr, pos[1]+dc)
        if npos[0] < 0 or npos[0] > len(GRID) or npos[1] < 0 or npos[1] > len(GRID[0]):
            continue
        if npos == END:
            home = True
            break
        elif npos in wind_squares:
            continue
        elif GRID[npos[0]][npos[1]] == '.':
            if minute + 1 >= result:
                continue
            heappush(q, ((calc_score(npos), -minute), minute + 1, npos, copy.deepcopy(winds)))
    if home:
        result = min(result, minute +1)
        print(result, len(q))
        continue
    # wait
    if pos in wind_squares:
        # cannot stay put
        continue
    heappush(q, ((calc_score(pos), -minute), minute + 1, pos, copy.deepcopy(winds)))

    

# Part 1 = 
print(f"answer = {result}")

result = 0

# Part 2 = 
print(f"answer = {result}")
