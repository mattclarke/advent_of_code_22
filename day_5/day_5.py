import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read().rstrip()

lines = [line for line in PUZZLE_INPUT.split("\n") if line]

num_stack = (len(lines[0]) // 4) + 1

stacks = { n + 1: [] for n in range(num_stack)}
moves = []

for l in lines:
    if '[' in l:
        cons = []
        cnt = 0
        foo = ""
        for i, ch in enumerate(l):
            if cnt == 3:
                cons.append(foo)
                cnt = 0
                foo = ''
                continue
            foo += ch
            cnt += 1
        cons.append(foo)

        i = 1
        for c in cons:
            if c.strip():
                stacks[i].insert(0, c[1])
            i += 1
    if l.startswith('move'):
        v = l.replace('move ', '').replace('from ', '').replace('to ', '')
        nums = [int(x) for x in v.split(' ')]
        moves.append(nums)

stacks_1 = copy.deepcopy(stacks)

for mo in moves:
    num, fro, to = mo
    for i in range(num):
        o = stacks_1[fro].pop(~0)
        stacks_1[to].append(o)

result = ""
for n,v in stacks_1.items():
    result += v[~0]

# Part 1 = LBLVVTVLP
print(f"answer = {result}")

for mo in moves:
    num, fro, to = mo
    st = []
    for i in range(num):
        st.append(stacks[fro].pop(~0))
    while st:
        o = st.pop(~0)
        stacks[to].append(o)

result = ""
for n,v in stacks.items():
    result += v[~0]

# Part 2 = TPFFBDRJD
print(f"answer = {result}")
