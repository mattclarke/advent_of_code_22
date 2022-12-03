with open("input.txt") as f:
    PUZZLE_INPUT = f.read()

# PUZZLE_INPUT = """
# vJrwpWtwJgWrhcsFMMfFFhFp
# jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
# PmmdzqPrVvPwwTWBwg
# wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
# ttgJtRGJQctTZtZT
# CrZsJsPPZsGzwwsLwLmpwMDw
# """

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]


def score(ch):
    if ch.islower():
        return ord(ch) - 96
    else:
        return ord(ch) - 65 + 27


result = 0

for l in lines:
    front = l[0 : len(l) // 2]
    back = l[len(l) // 2 :]
    same = set(front).intersection(set(back))
    result += score(same.pop())

# Part 1 = 8018
print(f"answer = {result}")

result = 0

group = []

for i, l in enumerate(lines):
    group.append(l)
    if len(group) == 3:
        a = set(group[0]).intersection(set(group[1])).intersection(set(group[2]))
        result += score(a.pop())
        group.clear()

# Part 2 = 2518
print(f"answer = {result}")
