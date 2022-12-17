import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

SHAPES = [
    (((0, 0), (1, 0), (2, 0), (3, 0)), 3),
    (((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)), 2),
    (((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)), 2),
    (((0, 0), (0, 1), (0, 2), (0, 3)), 0),
    (((0, 0), (1, 0), (0, 1), (1, 1)), 1),
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
            if (c, r) in s:
                row.append("@")
            elif (c, r) in filled:
                row.append("#")
            else:
                row.append(".")
        print("".join(row))


filled = set()
for c in range(7):
    filled.add((c, 0))

curr_shape = 0
hit = False
pos = (2, 4)
num_shapes = 0
target = 2022
result = 0

while num_shapes < target:
    for i, l in enumerate(lines[0]):
        shape, cmax = SHAPES[curr_shape]
        if l == "<":
            pos = (max(pos[0] - 1, 0), pos[1])
            for pt in shape:
                npt = (pos[0] + pt[0], pos[1] + pt[1])
                if npt in filled:
                    pos = (pos[0] + 1, pos[1])
                    break
        else:
            pos = (min(pos[0] + 1, 6 - cmax), pos[1])
            for pt in shape:
                npt = (pos[0] + pt[0], pos[1] + pt[1])
                if npt in filled:
                    pos = (pos[0] - 1, pos[1])
                    break
        pos = (pos[0], pos[1] - 1)
        for pt in shape:
            npt = (pos[0] + pt[0], pos[1] + pt[1])
            if npt in filled:
                hit = True
                break
        if hit:
            pos = (pos[0], pos[1] + 1)
            for pt in shape:
                npt = (pos[0] + pt[0], pos[1] + pt[1])
                filled.add(npt)
                result = max(result, npt[1])

            curr_shape = (curr_shape + 1) % (len(SHAPES))
            pos = (2, result + 4)
            hit = False
            num_shapes += 1

            if num_shapes >= target:
                break


# Part 1 = 3098
print(f"answer = {result}")

filled = set()
for c in range(7):
    filled.add((c, 0))

curr_shape = 0
hit = False
pos = (2, 4)
num_shapes = 0
prev_res = 0
result = 0

# Stores the pattern to look for
pattern = []

# Tracks the current pattern
tracker = []

# The shape numbers where the pattern is repeated
repeats = []

# The height as each shape stops moving
heights = []

# Something large enough to find the period
target = 6000

while num_shapes < target:
    for i, l in enumerate(lines[0]):
        # 2500 as it takes a little while for the repetition to start
        if result != prev_res and num_shapes >= 2500:
            if len(pattern) < 10:
                pattern.append(result - prev_res)
                if len(pattern) == 10:
                    repeats.append(num_shapes - 1)
            elif len(tracker) < 10:
                tracker.append(result - prev_res)
            else:
                tracker.pop(0)
                tracker.append(result - prev_res)
                if tracker == pattern:
                    repeats.append(num_shapes - 1)
        prev_res = result
        shape, cmax = SHAPES[curr_shape]
        if l == "<":
            pos = (max(pos[0] - 1, 0), pos[1])
            for pt in shape:
                npt = (pos[0] + pt[0], pos[1] + pt[1])
                if npt in filled:
                    pos = (pos[0] + 1, pos[1])
                    break
        else:
            pos = (min(pos[0] + 1, 6 - cmax), pos[1])
            for pt in shape:
                npt = (pos[0] + pt[0], pos[1] + pt[1])
                if npt in filled:
                    pos = (pos[0] - 1, pos[1])
                    break
        pos = (pos[0], pos[1] - 1)
        for pt in shape:
            npt = (pos[0] + pt[0], pos[1] + pt[1])
            if npt in filled:
                hit = True
                break
        if hit:
            pos = (pos[0], pos[1] + 1)
            for pt in shape:
                npt = (pos[0] + pt[0], pos[1] + pt[1])
                filled.add(npt)
                result = max(result, npt[1])
            heights.append(result)

            curr_shape = (curr_shape + 1) % (len(SHAPES))
            pos = (2, result + 4)
            hit = False
            num_shapes += 1

            if num_shapes >= target:
                break
# The target number of blocks is too big to simulate
# but if we run it for a bit we can see that the rate of change
# of the height repeats in a sequence.
# We can obtain the period of the repeats and how the height changes
# per period.
period = repeats[1] - repeats[0]
height_change = heights[repeats[1]] - heights[repeats[0]]

target = 1000000000000
# We can start at the being of the first period
target -= repeats[0]
# Calculate the number of times the period fits inside the target
factor = target // period
result = heights[repeats[0]] + factor * height_change
# Calculate the remainder and find the number of results
# from the start of the period to that, and add to the total
leftover = target % period
result += heights[repeats[0] + leftover - 1] - heights[repeats[0]]


# Part 2 = 1525364431487
print(f"answer = {result}")
