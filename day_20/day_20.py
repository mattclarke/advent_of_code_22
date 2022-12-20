import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

ORIG = []

class Node:
   def __init__(self, value):
       self.value = value
       self.nx = None
       self.pr = None

ORIG_ORDER = []

HEAD = Node(123)
CURR = HEAD
ZERO = None

result = 0

for i, l in enumerate(lines):
    ORIG.append(int(l))
    n = Node(int(l))
    ORIG_ORDER.append(n)
    CURR.nx = n
    n.pr = CURR
    CURR = n
    if int(l) == 0:
        ZERO = n
CURR.nx = HEAD.nx
HEAD.nx.pr = CURR

curr = HEAD.nx



for i in range(len(ORIG_ORDER)):
    steps = ORIG_ORDER[i].value
    if steps == 0:
        continue
    np = ORIG_ORDER[i]
    # detach current
    np.pr.nx = np.nx
    np.nx.pr = np.pr
    
    tp = np
    if steps > 0:
        for _ in range(steps):
            tp = tp.nx
        tp.nx.pr = ORIG_ORDER[i]
        ORIG_ORDER[i].nx = tp.nx
        ORIG_ORDER[i].pr = tp

        tp.nx = ORIG_ORDER[i]
    else:
        steps = abs(steps)
        for _ in range(steps):
            tp = tp.pr
        tp.pr.nx = ORIG_ORDER[i]
        ORIG_ORDER[i].pr = tp.pr
        ORIG_ORDER[i].nx = tp
        tp.pr = ORIG_ORDER[i]
    
    p = HEAD.nx
    vals = []
    for j in range(len(ORIG_ORDER)):
        vals.append(str(p.value))
        p = p.nx
    #print(",".join(vals))
   
print("=============")
curr = ZERO.nx
results = []
for x in range(1, 3001):
    if x % 1000 == 0:
        results.append(curr.value)
    curr = curr.nx

# Part 1 = 
print(f"answer = {sum(results)}")

result = 0

# Part 2 = 
print(f"answer = {result}")
