import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

SHAPES = [
    (((0,0), (1,0), (2,0), (3,0)), 3),
    (((1,0), (0,1),(1,1),(2,1),(1,2)), 2),
    (((0,0), (1,0),(2,0),(2,1),(2,2)),2),
    (((0,0), (0,1),(0,2),(0,3)), 0),
    (((0,0),(1,0),(0,1),(1,1)), 1)
]

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

def print_(pos, shape):
    print()
    s = set()
    for p in shape:
        np = (pos[0] + p[0], pos[1] + p[1])
        s.add(np)
    for r in range(result + 5, -1, -1):
        row = []
        for c in range(7):
            if (c,r) in s:
                row.append('@')
            elif (c,r) in filled:
                row.append('#')
            else:
                row.append('.')
        print("".join(row))

result = 0

curr_shape = 0
filled = set()
for c in range(7):
    filled.add((c, 0))
down = False
hit = False
pos = (2, 4)
num_shape = 0

while num_shape < 2022:
    for l in lines[0]:
        shape, cmax = SHAPES[curr_shape]
        if l == '<':
            pos = (max(pos[0]-1, 0),pos[1])
            for pt in shape:
                npt = (pos[0] + pt[0], pos[1] + pt[1])
                if npt in filled:
                    pos = (pos[0]+1, pos[1])
                    break
        else:
            pos = (min(pos[0]+1, 6-cmax),pos[1])
            for pt in shape:
                npt = (pos[0] + pt[0], pos[1] + pt[1])
                if npt in filled:
                    pos = (pos[0]-1, pos[1])
                    break
#        print_(pos, shape)
#        print(result)
#        input()

        pos = (pos[0], pos[1]-1)
        for pt in shape:
            npt = (pos[0] + pt[0], pos[1] + pt[1])
            if npt in filled:
                hit = True
                break
        if hit:
            pos = (pos[0], pos[1]+1)
            for pt in shape:
                npt = (pos[0] + pt[0], pos[1] + pt[1])
                filled.add(npt)
                result = max(result, npt[1])
            curr_shape = (curr_shape + 1) % (len(SHAPES))
            pos = (2, result + 4)
            hit = False
            num_shape += 1
            #print_(123, [])
            print(num_shape, result)
            if num_shape >= 2022:
                break
            #input()

best = 0
for f in filled:
   best = max(best, f[1])

print(best)

# Part 1 = 
print(f"answer = {result}")

result = 0

# Part 2 = 
print(f"answer = {result}")
