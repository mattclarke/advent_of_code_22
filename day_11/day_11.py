import copy
import sys


MONKEYS = [
    [[64], lambda x: x * 7, 13, 1, 3],
    [[60, 84, 84, 65], lambda x: x + 7, 19, 2, 7],
    [[52, 67, 74, 88, 51, 61], lambda x: x * 3, 5, 5, 7],
    [[67, 72], lambda x: x + 3, 2, 1, 2],
    [[80, 79, 58, 77, 68, 74, 98, 64], lambda x: x * x, 17, 6, 0],
    [[62, 53, 61, 89, 86], lambda x: x + 8, 11, 4, 6],
    [[86, 89, 82], lambda x: x + 2, 7, 3, 0],
    [[92, 81, 70, 96, 69, 84, 83], lambda x: x + 4, 3, 4, 5],
]

monkeys = copy.deepcopy(MONKEYS)
result = [0 for _ in MONKEYS]

for foo in range(20):
    for i, m in enumerate(monkeys):
        items = m[0]
        func = m[1]
        test = m[2]
        for item in items:
            result[i] += 1
            worry = func(item)
            worry //= 3
            if worry % test == 0:
                monkeys[m[3]][0].append(worry)
            else:
                monkeys[m[4]][0].append(worry)
        items.clear()

result.sort()

# Part 1 = 55216
print(f"answer = {result[~0] * result[~1]}")

monkeys = copy.deepcopy(MONKEYS)
result = [0 for _ in MONKEYS]

lcm = 1
for m in monkeys:
    lcm *= m[2]

for foo in range(10000):
    for i, m in enumerate(monkeys):
        items = m[0]
        func = m[1]
        test = m[2]
        for item in items:
            result[i] += 1
            worry = func(item)
            worry %= lcm
            if worry % test == 0:
                monkeys[m[3]][0].append(worry)
            else:
                monkeys[m[4]][0].append(worry)
        items.clear()

result.sort()

# Part 2 = 12848882750
print(f"answer = {result[~0] * result[~1]}")

