import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

MONKEYS = {}
result = 0

for l in lines:
    parts = l.replace(':', '').split(' ')
    if len(parts) == 2:
        MONKEYS[parts[0]] = (int(parts[1]),)
    else:
        MONKEYS[parts[0]] = (parts[1], parts[2], parts[3])

SHOUTED = {}
root = False

while not root:
    for mn, mv in MONKEYS.items():
        if len(mv) == 1:
            SHOUTED[mn] = mv[0]
        else:
           if mv[0] in SHOUTED and mv[2] in SHOUTED:
                if mv[1] == '+':
                    SHOUTED[mn] = SHOUTED[mv[0]] + SHOUTED[mv[2]]
                elif mv[1] == '-':
                    SHOUTED[mn] = SHOUTED[mv[0]] - SHOUTED[mv[2]]
                elif mv[1] == '*':
                    SHOUTED[mn] = SHOUTED[mv[0]] * SHOUTED[mv[2]]
                elif mv[1] == '/':
                    SHOUTED[mn] = SHOUTED[mv[0]] // SHOUTED[mv[2]]
                else:
                    assert False
                if mn == 'root':
                    root = True
                    break

# Part 1 = 85616733059734
print(f"answer = {SHOUTED['root']}")

SHOUTED = {}
humn = 3560324848168
root = False

while not root:
    for mn, mv in MONKEYS.items():
        if mn == 'root':
            if mv[0] in SHOUTED and mv[2] in SHOUTED:
                if SHOUTED[mv[0]] == SHOUTED[mv[2]]:
                    root = True
                    break
                else:
                    SHOUTED = {}
                    humn += 1
        elif mn == 'humn':
            SHOUTED[mn] = humn
        elif len(mv) == 1:
            SHOUTED[mn] = mv[0]
        else:
           if mv[0] in SHOUTED and mv[2] in SHOUTED:
                if mv[1] == '+':
                    SHOUTED[mn] = SHOUTED[mv[0]] + SHOUTED[mv[2]]
                elif mv[1] == '-':
                    SHOUTED[mn] = SHOUTED[mv[0]] - SHOUTED[mv[2]]
                elif mv[1] == '*':
                    SHOUTED[mn] = SHOUTED[mv[0]] * SHOUTED[mv[2]]
                elif mv[1] == '/':
                    SHOUTED[mn] = SHOUTED[mv[0]] // SHOUTED[mv[2]]
                else:
                    assert False
                if mn == 'root':
                    root = True
                    break

# Part 2 = 3560324848168
print(f"answer = {humn}")
