import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

MOVES = []

for l in lines:
    d, n = l.split()
    MOVES.append((d, int(n)))


def move_head(h_pos):
    if d == "U":
        h_pos = (h_pos[0], h_pos[1] + 1)
    elif d == "D":
        h_pos = (h_pos[0], h_pos[1] - 1)
    elif d == "R":
        h_pos = (h_pos[0] + 1, h_pos[1])
    elif d == "L":
        h_pos = (h_pos[0] - 1, h_pos[1])
    return h_pos


def follow(h_pos, t_pos):
    # If adjacent then don't move tail
    if abs(h_pos[0] - t_pos[0]) <= 1 and abs(h_pos[1] - t_pos[1]) <= 1:
        return t_pos
    if t_pos[0] < h_pos[0]:
        t_pos = (t_pos[0] + 1, t_pos[1])
    elif t_pos[0] > h_pos[0]:
        t_pos = (t_pos[0] - 1, t_pos[1])
    if t_pos[1] < h_pos[1]:
        t_pos = (t_pos[0], t_pos[1] + 1)
    elif t_pos[1] > h_pos[1]:
        t_pos = (t_pos[0], t_pos[1] - 1)
    return t_pos


SEEN = set()
h_pos = (0, 0)
t_pos = (0, 0)

for mv in MOVES:
    d, amt = mv
    for _ in range(amt):
        h_pos = move_head(h_pos)
        t_pos = follow(h_pos, t_pos)
        SEEN.add(t_pos)

# Part 1 = 6030
print(f"answer = {len(SEEN)}")

SEEN = set()
knots = [(0, 0) for _ in range(10)]

for mv in MOVES:
    d, amt = mv
    for _ in range(amt):
        knots[0] = move_head(knots[0])
        for k in range(1, len(knots)):
            knots[k] = follow(knots[k - 1], knots[k])
        SEEN.add(knots[~0])

# Part 2 = 2545
print(f"answer = {len(SEEN)}")
