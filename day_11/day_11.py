import copy
import sys
import queue


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

MONKEYS = [
    [[79,98], lambda x: x * 19, 23, 2, 3],
    [[54,65,75,74], lambda x: x +6, 19, 2, 0],
    [[79,60,97], lambda x: x * x, 13, 1, 3],
    [[74], lambda x: x + 3, 17, 0, 1],
    ]

#MONKEYS = [
#    [[64], lambda x: x * 7, 13, 1, 3],
#    [[60,84,84,65], lambda x: x +7, 19, 2, 7],
#    [[52,67,74,88,51,61], lambda x: x * 3, 5, 5, 7],
#    [[67,72], lambda x: x + 3, 2, 1, 2],
#    [[80,79,58,77,68,74,98,64], lambda x: x * x, 17, 6, 0],
#    [[62,53,61,89,86], lambda x: x +8, 11, 4, 6],
#    [[86,89,82], lambda x: x +2, 7, 3, 0],
#    [[92,81,70,96,69,84,83], lambda x: x +4, 3, 4, 5],
#    ]

result = [0 for _ in MONKEYS]

monkeys = copy.deepcopy(MONKEYS)

for foo in range(10000):
    print(foo)
    for i, m in enumerate(monkeys):
        items = m[0]
        func = m[1]
        test = m[2]
        for item in items:
            result[i] += 1
            worry = func(item)
            #worry //= 3
            if worry % test == 0:
                monkeys[m[3]][0].append(worry)
                worry //= test
            else:
                monkeys[m[4]][0].append(worry)
        items.clear()

    print(result)

result.sort()
print(result)


# Part 1 = 
print(f"answer = {result[~0] * result[~1]}")

result = 0

# Part 2 = 
print(f"answer = {result}")
