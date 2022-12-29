import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

str_to_num = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
num_to_str = {2: "2", 1: "1", 0: "0", -1: "-", -2: "="}
fives = [5**x for x in range(20)]
maxs = []

for f in fives:
    if not maxs:
        maxs.append(2 * f)
        continue
    a = maxs[~0] + 2 * f
    maxs.append(a)


def to_dec(s):
    result = 0
    for i, c in enumerate(reversed(s)):
        result += fives[i] * str_to_num[c]
    return result


total = 0
for l in lines:
    total += to_dec(l)

print("input =", total)


def to_snafu(target):
    def _find(target, index):
        if index == 0:
            return num_to_str[target]
        is_neg = True if target < 0 else False
        f = fives[index]
        if maxs[index - 1] < abs(target) <= maxs[index]:
            if maxs[index - 1] < abs(target) <= f + maxs[index - 1]:
                result = "-" if is_neg else "1"
                target -= f * -1 if is_neg else f * 1
                return result + _find(target, index - 1)
            else:
                result = "=" if is_neg else "2"
                target -= f * -2 if is_neg else f * 2
                return result + _find(target, index - 1)
        return "0" + _find(target, index - 1)

    start = None
    for i, (mn, mx) in enumerate(zip(maxs[:-1], maxs[1:])):
        if mn < target <= mx:
            start = i + 1
            break
    return _find(target, start)


result = to_snafu(total)

assert to_dec(result) == total

# Part 1 = 2-121-=10=200==2==21
print(f"answer = {result}")


def to_snafu(target):
    """Internet solution"""
    result = ""
    carry = 0
    while target != 0:
        target, m = divmod(target, 5)
        m += carry
        if m > 2:
            result = num_to_str[m - 5] + result
            carry = 1
        else:
            result = num_to_str[m] + result
            carry = 0
    return result

print(to_snafu(38))
