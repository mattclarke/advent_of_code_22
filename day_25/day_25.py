import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

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
        val = 0
        if c == "2":
            val = 2
        elif c == "1":
            val = 1
        elif c == "0":
            val = 0
        elif c == "-":
            val = -1
        elif c == "=":
            val = -2
        else:
            assert False
        result += fives[i] * val
    return result


total = 0
for l in lines:
    total += to_dec(l)

print("input =", total)


def find_first_digit(target):
    is_neg = True if target < 0 else False
    target = abs(target)
    for i, f in enumerate(fives):
        if maxs[i - 1] < target <= maxs[i]:
            if maxs[i - 1] < target <= f + maxs[i - 1]:
                return (-1, f, i) if is_neg else (1, f, i)
            else:
                return (-2, f, i) if is_neg else (2, f, i)
    assert False


def find_digit(target, i):
    is_neg = True if target < 0 else False
    target = abs(target)
    f = fives[i]
    if maxs[i - 1] < target <= maxs[i]:
        if maxs[i - 1] < target <= f + maxs[i - 1]:
            return (-1, f, i) if is_neg else (1, f, i)
        else:
            return (-2, f, i) if is_neg else (2, f, i)
    return 0, f, i


target = total
so_far = []
num, f, i = find_first_digit(target)
so_far.append(num)
target -= num * f
i -= 1

while i > 0:
    num, f, i = find_digit(target, i)
    so_far.append(num)
    target -= num * f
    i -= 1
so_far.append(target)

result = ""
for x in so_far:
    if x == 2:
        result += "2"
    elif x == 1:
        result += "1"
    elif x == 0:
        result += "0"
    elif x == -1:
        result += "-"
    elif x == -2:
        result += "="
    else:
        assert False

assert to_dec(result) == total

# def find_digit(target, base):
#    max_f = 0
#    for i, f5 in enumerate(fives):
#        if target < f5:
#            max_f = i-1
#
#    mu =[-2, -1, 0, 1, 2]:
#    for i in range(len(mu)-1):
#        low = fives[max_f] * mu[i]
#        hgh = fives[max_f] * mu[i+1]
#        mid = fives[max_f] * mu[i+1]
#        for x in range(max_f):
#            low += fives[x] * -2
#            hgh += fives[x] * -2
#            mid =
#
#
#    for i, f5 in enumerate(fives):
#       mx = f5 * 2
#       mxm = f5 * 2
#       mn = f5
#       for x in range(i):
#           mx += fives[x] * 2
#           mxm += fives[x] * -2
#           mn += fives[x] * -2
#       if mn <= total <= mx:
#           print(f5, mn, mx, mxm)
#           if total >= mxm:
#               print('starts with a two')
#           else:
#               print('starts with a one')
#
# Part 1 = 2-121-=10=200==2==21
print(f"answer = {result}")
