import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

result = 0
stack = []

for l in lines:
    for i, c in enumerate(l):
        if len(stack) < 4:
            stack.append(c)
        else:
            s = set(stack)
            if len(s) == 4:
                result = i
                break
            stack.pop(0)
            stack.append(c)

# Part 1 = 1275
print(f"answer = {result}")

result = 0
stack = []

for l in lines:
    for i, c in enumerate(l):
        if len(stack) < 14:
            stack.append(c)
        else:
            s = set(stack)
            if len(s) == 14:
                result = i
                break
            stack.pop(0)
            stack.append(c)

for l in lines:
    pass

# Part 2 = 3605
print(f"answer = {result}")
