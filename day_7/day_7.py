import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

d = {"/": 0}
stack = ["/"]

in_ls = False
i = 0

while i < len(lines):
    if in_ls:
        if lines[i].startswith("$"):
            in_ls = False
    if lines[i] == "$ cd /":
        pass
    elif lines[i] == "$ cd ..":
        c = stack[~0]
        stack.pop(len(stack) - 1)
        d[stack[~0]] += d[c]
    elif lines[i].startswith("$ cd"):
        name = lines[i].replace("$ cd ", "")
        stack.append(stack[~0] + "/" + name)
        d[stack[~0]] = 0
    elif lines[i] == "$ ls":
        in_ls = True
    else:
        if in_ls:
            if not lines[i].startswith("dir"):
                s, n = lines[i].split(" ")
                d[stack[~0]] += int(s)
    i += 1

# Don't forget to pop the stack if it is not empty!
while stack:
    c = stack[~0]
    stack.pop(len(stack) - 1)
    if len(stack) > 0:
        d[stack[~0]] += d[c]

result = 0
for n, v in d.items():
    if v <= 100000:
        result += v

# Part 1 = 1297683
print(f"answer = {result}")

result = 100000000000000

target = 30000000 - (70000000 - d["/"])

for n, v in d.items():
    if v >= target:
        result = min(result, v)

# Part 2 = 5756764
print(f"answer = {result}")
