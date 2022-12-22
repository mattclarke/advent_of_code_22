import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line for line in PUZZLE_INPUT.split("\n") if line]

GRID = []
START = None
PUZZLE = ''
max_ = 0
for r, l in enumerate(lines):
    max_ = max(max_, len(l))

for r, l in enumerate(lines):
    if l:
        PUZZLE = l
        row = []
        for c, ch in enumerate(l):
            if START is None and ch == '.':
                START = (r, c)
            row.append(ch)
        while len(row) < max_:
            row.append(' ')
        GRID.append(row)
    else:
        pass
GRID.pop()
sofar = []
temp = []
for ch in PUZZLE:
    if ch == 'R' or ch == 'L' or ch == ' ':
        temp.append(int(''.join(sofar)))
        if ch != ' ':
            temp.append(ch)
        sofar = []
    else:
        sofar.append(ch)
temp.append(int(''.join(sofar)))
PUZZLE = temp


def show(g, pos=None):
    for r, row in enumerate(g):
        l = []
        for c, ch in enumerate(row):
            if pos and pos == (r, c):
                l.append('p')
            else:
                l.append(ch)
        print(''.join(l).rstrip())
    print('')


TURN_R = ((0, 1), (1, 0), (0, -1), (-1, 0))

puzzle = copy.copy(PUZZLE)
heading = 0
pos = START

while puzzle:
    #show(GRID, pos)
    dist = puzzle.pop(0)
    rot = puzzle.pop(0) if puzzle else ''
    for _ in range(dist):
        #show(GRID, pos)
        npos = (pos[0] + TURN_R[heading][0], pos[1] + TURN_R[heading][1])
        try:
            if GRID[npos[0]][npos[1]] == '#':
                break
        except:
            pass
     
        if TURN_R[heading] == (0,1):
            if npos[1] >= len(GRID[npos[0]]) or GRID[npos[0]][npos[1]] == ' ':
                t = (npos[0], 0)
                while True:
                    if GRID[t[0]][t[1]] == '.':
                        npos = t
                        break
                    elif GRID[t[0]][t[1]] == '#':
                        npos = pos
                        break
                    else:
                        t = (t[0], t[1]+1)
        elif TURN_R[heading] == (0,-1):
            if npos[0] < 0 or GRID[npos[0]][npos[1]] == ' ':
                t = (npos[0], len(GRID[npos[0]]) - 1)
                while True:    
                    if GRID[t[0]][t[1]] == '.':
                        npos = t
                        break
                    elif GRID[t[0]][t[1]] == '#':
                        npos = pos
                        break
                    else:
                        t = (t[0], (t[1]-1) % len(GRID[0]))
        elif TURN_R[heading] == (1,0):
            if npos[0] >= len(GRID) or GRID[npos[0]][npos[1]] == ' ':
                t = (0, npos[1])
                while True:
                    if GRID[t[0]][t[1]] == '.':
                        npos = t
                        break
                    elif GRID[t[0]][t[1]] == '#':
                        npos = pos
                        break
                    else:
                        t = (t[0]+1, t[1])
        elif TURN_R[heading] == (-1, 0):
            if npos[0] < 0 or GRID[npos[0]][npos[1]] == ' ':
                t = (len(GRID)-1, npos[1])
                while True:
                    if t[1] >= len(GRID[t[0]]):
                        t = (t[0]-1, t[1])
                        continue
                        
                    if GRID[t[0]][t[1]] == '.':
                        npos = t
                        break
                    elif GRID[t[0]][t[1]] == '#':
                        npos = pos
                        break
                    else:
                        t = (t[0]-1, t[1])
               
        pos = npos
        assert pos[0] >= 0 and pos[1] >= 0, (pos, dist, rot, heading)
    if rot == 'R':
        heading = (heading + 1) % 4
    elif rot == 'L':
        heading = (heading - 1) % 4
    #show(GRID, pos)

print(pos, heading)
result = 1000*(pos[0] + 1) + 4*(pos[1] + 1) + heading

# Part 1 = 109094
print(f"answer = {result}")

result = 0

# Part 2 = 
print(f"answer = {result}")
