import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

result = 0

X = 1
Q = 0 
cycle = 1
image = []

while lines or Q:
    if cycle in [20, 60, 100, 140, 180, 220]:
        result += cycle * X
    if (cycle - 1) % 40 in [X - 1, X, X + 1]:
        image.append("#")
    else:
        image.append(" ")
    cycle += 1
    if lines and not Q:
        l = lines.pop(0)
        if l != "noop":
            op, val = l.split(" ")
            Q = int(val)
            continue
    if Q:
        X += Q
        Q = 0


# Part 1 = 13860
print(f"answer = {result}")

for i, x in enumerate(image):
    print(x, end="")
    if (i + 1) % 40 == 0:
        print("")

# Read the answer off the screen
# Part 2 = RZHFGJCB
