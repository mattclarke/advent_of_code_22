import copy
import sys

from heapq import heappush, heappop

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

CAN_OPEN = set()

for n,v in VALVES.items():
    if v[0] != 0:
        CAN_OPEN.add(n)

DISTS = {}

for o in CAN_OPEN:
    q = [(o, 0)]
    seen = {o}
    while q:
        curr, d = q.pop(0)
        if d > len(VALVES):
            break
        if curr != o:
            key = (curr, o)
            best = DISTS.get(key, 1000000)
            if d < best:
                DISTS[key] = d
            else:
                continue
        for nxt in VALVES[curr][1]:
            q.append((nxt, d + 1))

result = 0
q = []
heappush(q, (0, 1, 'AA',  []))
seen = set()
best = {}

while q:
    press, minute, curr, state = heappop(q)
    if minute >= 30 or set(state) == CAN_OPEN:
        result = min(result, press)
        if (set(state) == CAN_OPEN):
            print(result, len(q), set(state) == CAN_OPEN, state)
        continue
    if (press, minute, curr, frozenset(state)) in seen:
        continue
    foo = best.get(frozenset(state), 0)
    if press > foo:
        continue
    best[frozenset(state)] = press
    seen.add((press, minute, curr, frozenset(state)))
    if curr not in state:
        nstate = copy.copy(state)
        nstate.append(curr)
        npress = press - (VALVES[curr][0] * (30 - minute))
        heappush(q, (npress, minute+1, curr, nstate))
    for npos in CAN_OPEN:
        if npos in state or npos == curr:
            continue
        heappush(q, (press, minute + DISTS[(curr, npos)], npos, copy.copy(state)))

print(result)
