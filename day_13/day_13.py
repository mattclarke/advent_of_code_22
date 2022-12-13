import copy
import functools
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]


def compare(first, second):
    first = first[:]
    second = second[:]
    if len(first) == 0 and len(second) > 0:
        return True
    elif len(first) > 0 and len(second) == 0:
        return False
    while first:
        if len(second) == 0:
            return False
        a = first.pop(0)
        b = second.pop(0)
        if isinstance(a, int) and isinstance(b, int):
            if a < b:
                return True
            elif a > b:
                return False
            continue
        elif isinstance(a, int):
            a = [a]
        elif isinstance(b, int):
            b = [b]
        result = compare(a, b)
        if result is not None:
            return result
    if len(second) > 0:
        return True
    # None represents no decision possible
    return None


results = []
i = 0
pair = 1
while i < len(lines):
    first = eval(lines[i])
    second = eval(lines[i + 1])

    result = compare(first, second)
    if result:
        results.append(pair)
    if result is None:
        print(first, second)
        assert False, "oops!"
    pair += 1
    i += 2

# Part 1 = 5503
print(f"answer = {sum(results)}")

packets = [[[2]], [[6]]]

for l in lines:
    packets.append(eval(l))


def cmp(a, b):
    return -1 if compare(a, b) else 1


packets.sort(key=functools.cmp_to_key(cmp))
result = (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)

# Part 2 = 20952
print(f"answer = {result}")
