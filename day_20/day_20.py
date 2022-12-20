import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]


class Node:
    def __init__(self, value):
        self.value = value
        self.nx = None
        self.pr = None


def solve(factor, num_times):
    for _ in range(num_times):
        for i in range(len(ORIG_ORDER)):
            steps = ORIG_ORDER[i].value * factor
            if steps == 0:
                continue
            np = ORIG_ORDER[i]
            # detach current
            np.pr.nx = np.nx
            np.nx.pr = np.pr

            tp = np
            if steps > 0:
                steps = steps % (len(ORIG_ORDER) - 1)
                for _ in range(steps):
                    tp = tp.nx
                tp.nx.pr = ORIG_ORDER[i]
                ORIG_ORDER[i].nx = tp.nx
                ORIG_ORDER[i].pr = tp

                tp.nx = ORIG_ORDER[i]
            else:
                steps = abs(steps)
                steps = steps % (len(ORIG_ORDER) - 1)
                for _ in range(steps):
                    tp = tp.pr
                tp.pr.nx = ORIG_ORDER[i]
                ORIG_ORDER[i].pr = tp.pr
                ORIG_ORDER[i].nx = tp
                tp.pr = ORIG_ORDER[i]

    curr = ZERO.nx
    results = []
    for x in range(1, 3001):
        if x % 1000 == 0:
            results.append(curr.value * factor)
        curr = curr.nx
    return sum(results)


ORIG_ORDER = []
HEAD = Node("HEAD")
CURR = HEAD
ZERO = None

for i, l in enumerate(lines):
    num = int(l)
    n = Node(num)
    ORIG_ORDER.append(n)
    CURR.nx = n
    n.pr = CURR
    CURR = n
    if num == 0:
        ZERO = n
CURR.nx = HEAD.nx
HEAD.nx.pr = CURR

# Part 1 = 7713
print(f"answer = {solve(1, 1)}")

ORIG_ORDER = []
HEAD = Node("HEAD")
CURR = HEAD
ZERO = None

for i, l in enumerate(lines):
    num = int(l)
    n = Node(num)
    ORIG_ORDER.append(n)
    CURR.nx = n
    n.pr = CURR
    CURR = n
    if num == 0:
        ZERO = n
CURR.nx = HEAD.nx
HEAD.nx.pr = CURR

# Part 2 = 1664569352803
print(f"answer = {solve(811589153, 10)}")
