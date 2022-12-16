import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

result = 0

VALVES = {}

['Valve', 'AA', 'has', 'flow', 'rate=0;', 'tunnels', 'lead', 'to', 'valves', 'DD,', 'II,', 'BB']

for l in lines:
    l = l.split()
    v = l[1]
    r = int(l[4].replace(';','')[5:])
    t = [x.replace(',','') for x in l[9:]]
    VALVES[v] = (r, t)

current = 'AA'
vopen = {}

def solve():
    def _solve(current, states, minutes):
        if minutes == 30:
            return True, states
        curr = VALVES[current]

        pass
    _solve('AA', {}, 0)

import heapq as hq
q = []

hq.heappush(q, (0, 1, 'AA', []))
result = 0
seen = set()
best = {}

while q:
    #press, minute, curr, state = hq.heappop(q)
    press, minute, curr, state = q.pop(0)
    if (press, minute, curr, frozenset(state)) in seen:
        continue
    seen.add((press, minute, curr, frozenset(state)))
    foo = best.get(frozenset(state), 0)
    if press > foo:
        continue
    best[frozenset(state)] = press
    if minute == 30:
        result = min(result, press)
        print(press, result, state)
        continue
    if curr not in state and VALVES[curr][0]:
        nstate = copy.copy(state)
        nstate.append(curr)
        npress = press - (VALVES[curr][0] * (30 - minute)) 
        hq.heappush(q, (npress, (minute + 1), curr, nstate))
    targets = VALVES[curr][1]
    for t in targets:
        hq.heappush(q, (press, (minute + 1), t, copy.copy(state)))


# Part 1 = 
print(f"answer = {result}")

result = 0

# Part 2 = 
print(f"answer = {result}")
