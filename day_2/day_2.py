with open("input.txt") as f:
    PUZZLE_INPUT = f.read()

#PUZZLE_INPUT = """
#A Y
#B X
#C Z
#"""

lines = [line.strip().split(" ") for line in PUZZLE_INPUT.split("\n") if line] 

VALUES = {
    "X": 1,
    "Y": 2,
    "Z": 3
}

L = 0
D = 3
W = 6

RESULTS = {
    "A": {"X": D, "Y": W, "Z": L}, 
    "B": {"X": L, "Y": D, "Z": W}, 
    "C": {"X": W, "Y": L, "Z": D}, 
}

score = 0
for opp, resp in lines:
    score += VALUES[resp]
    score += RESULTS[opp][resp]

# Part 1 = 13221
print(f"answer = {score}")

OUTCOME = {
    "X": L,
    "Y": D,
    "Z": W
}

RESPONSE = {
    "A": {"X": 3, "Y": 1, "Z": 2}, 
    "B": {"X": 1, "Y": 2, "Z": 3}, 
    "C": {"X": 2, "Y": 3, "Z": 1}, 
}

score = 0
for opp, resp in lines:
    score += OUTCOME[resp]
    score += RESPONSE[opp][resp]

# Part 2 = 13131 
print(f"answer = {score}")

