with open("input.txt") as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

result = 0

for l in lines:
    f, s = l.split(",")
    f1, f2 = f.split("-")
    f1, f2 = int(f1), int(f2)
    s1, s2 = s.split("-")
    s1, s2 = int(s1), int(s2)
    if f1 <= s1 and f2 >= s2:
        result += 1
    elif s1 <= f1 and s2 >= f2:
        result += 1

# Part 1 = 518
print(f"answer = {result}")

result = 0

for l in lines:
    f, s = l.split(",")
    f1, f2 = f.split("-")
    f1, f2 = int(f1), int(f2)
    s1, s2 = s.split("-")
    s1, s2 = int(s1), int(s2)
    if f1 <= s1 and f2 >= s1:
        result += 1
    elif f1 <= s2 and f2 >= s2:
        result += 1
    elif s1 <= f1 and s2 >= f1:
        result += 1
    elif s1 <= f2 and s2 >= f2:
        result += 1

# Part 2 = 909
print(f"answer = {result}")
