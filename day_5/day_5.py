import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read().rstrip()

lines = [line for line in PUZZLE_INPUT.split("\n") if line]

num_stack = (len(lines[0]) // 4) + 1

STACKS = {n + 1: [] for n in range(num_stack)}
moves = []

for l in lines:
    if "[" in l:
        cons = [l[i : i + 3] for i in range(0, len(l), 4)]
        for i, c in enumerate(cons):
            if c.strip():
                STACKS[i + 1].insert(0, c[1])
    if l.startswith("move"):
        v = l.replace("move ", "").replace("from ", "").replace("to ", "")
        nums = [int(x) for x in v.split(" ")]
        moves.append(nums)

stacks = copy.deepcopy(STACKS)

for mo in moves:
    num, frm, to = mo
    for i in range(num):
        o = stacks[frm].pop(~0)
        stacks[to].append(o)

result = ""
for n, v in stacks.items():
    result += v[~0]

# Part 1 = LBLVVTVLP
print(f"answer = {result}")

stacks = copy.deepcopy(STACKS)

for mo in moves:
    num, frm, to = mo
    st = []
    for i in range(num):
        st.append(stacks[frm].pop(~0))
    while st:
        o = st.pop(~0)
        stacks[to].append(o)

result = ""
for n, v in stacks.items():
    result += v[~0]

# Part 2 = TPFFBDRJD
print(f"answer = {result}")
