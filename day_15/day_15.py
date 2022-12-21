import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

result = 0
sensors = {}

for l in lines:
    l = l.replace("Sensor at x=", "").replace(": closest beacon is at x=", " ")
    l = l.replace(" y=", "")
    parts = l.split(" ")
    x, y = parts[0].split(",")
    bx, by = parts[1].split(",")
    sensors[(int(x), int(y))] = (int(bx), int(by))

empty = set()
beacons = set(sensors.values())

target = 2000000
min_ = 100000000000
max_ = 0

for s, b in sensors.items():
    if s:
        dc = abs(s[0] - b[0])
        dr = abs(s[1] - b[1])
        md = dc + dr
        if abs(s[1] - target) > md:
            continue

        for dr in range(-md - 1, md + 1):
            if s[1] + dr != target:
                continue
            for dc in range(-md - 1, md + 1):
                if abs(dr) + abs(dc) <= md:
                    if (s[0] + dc, s[1] + dr) not in sensors and (
                        s[0] + dc,
                        s[1] + dr,
                    ) not in beacons:
                        empty.add((s[0] + dc, s[1] + dr))
                        min_ = min(min_, s[0] + dc)
                        max_ = max(max_, s[0] + dc)


def print_grid():
    for r in range(-2, 23):
        row = []
        for c in range(-2, 26):
            if (c, r) in sensors:
                row.append("S")
            elif (c, r) in beacons:
                row.append("B")
            elif (c, r) in empty:
                row.append("#")
            else:
                row.append(".")
        print("".join(row))


result = 0
for c in range(min_ - 1, max_ + 1):
    if (c, target) in empty:
        result += 1

# Part 1 = 5403290
print(f"answer = {result}")

md = {}
result = None

for s, b in sensors.items():
    dc = abs(s[0] - b[0])
    dr = abs(s[1] - b[1])
    md[s] = dc + dr

for r in range(0, 4000000):
    c = 0
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
            if cmin <= c < cmax:
                c = cmax + 1
                inrange = True
                break
            if (c, r) in sensors or (c, r) in beacons:
                c += 1
                inrange = True
        if not inrange:
            result = 4000000 * c + r
            break
    if result:
        break


# Part 2 = 10291582906626
print(f"answer = {result}")
