with open("input.txt") as f:
    PUZZLE_INPUT = f.read()

maximum = 0
current = 0
for line in PUZZLE_INPUT.split("\n"):
    line = line.strip()
    if not line:
        maximum = max(current, maximum)
        current = 0
        continue
    current += int(line)

# Part 1 = 67633
print(f"answer = {maximum}")

elves = []

current = 0
for line in PUZZLE_INPUT.split("\n"):
    line = line.strip()
    if not line:
        elves.append(current)
        current = 0
        continue
    current += int(line)

elves.sort()

# Part 2 = 199628 
print(f"answer = {sum(elves[~2:])}")

