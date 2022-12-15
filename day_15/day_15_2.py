import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

result = 0
sensors = {}

for l in lines:
    l = l.replace("Sensor at x=",'').replace(": closest beacon is at x=", " ")
    l = l.replace(" y=", "")
    parts = l.split(" ")
    x, y = parts[0].split(",")
    bx, by = parts[1].split(",")
    sensors[(int(x), int(y))] = (int(bx), int(by))

empty = set()
beacons = set(sensors.values())
print(1)
target = 2000000
min_ = 100000000000
max_ = 0

md = {} 

for s, b in sensors.items():
    dc = abs(s[0] - b[0])
    dr = abs(s[1] - b[1])
    md[s] = dc + dr

for r in range(0,4000000):
    c =0
    while c <= 4000000:
        inrange = False
        for s, b in sensors.items():
            m = md[s]
            # is c,r in range of sensor?
            mdr = m - abs(s[1] - r)
            if mdr <= 0:
                continue
            cmin = s[0] - mdr
            cmax = s[0] + mdr
            #print(r, c, m, mdr, cmin, cmax, s)
            if cmin <= c < cmax:
                c = cmax + 1
                inrange = True
                #print('foung')
                break
            if (c, r) in sensors or (c, r) in beacons:
                c += 1
                inrange = True
        if not inrange:
            assert False, 4000000*c + r

        




def print_grid():
    for r in range(-2, 23):
        row = []
        for c in range(-2, 26):
            if (c,r) in sensors:
                row.append("S")
            elif (c,r) in beacons:
                row.append("B")
            elif (c,r) in empty:
                row.append("#")
            else:
                row.append(".")
        print("".join(row))
print(2)


# Part 2 = 
print(f"answer = {result}")
