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
heappush(q, (0, 0, 1, 'AA',  [], 0))
best = {}


while q:
    press, toadd, minute, curr, state, dist = heappop(q)
    if dist > 0:
        heappush(q, (press, toadd,  minute + 1, curr, state, dist - 1))
        continue
    if dist == 0:
        press = press - toadd
        result = min(result, press)
        toadd = 0
    options = []
    for npos in CAN_OPEN:
        if npos in state:
            continue
        dist = DISTS[(curr, npos)]
        if dist >= 30 - minute:
            continue
        options.append((VALVES[npos][0] * (30 - minute - dist), dist, npos))
    options.sort()
    for score, dist, tgt in options:
        nstate = copy.copy(state)
        nstate.append(tgt)
        heappush(q, (press, score, minute + 1, tgt, nstate, dist))

print(result)

result = 0
q = []
heappush(q, (0, 1, 'AA', 'AA', [], 10000, 0, 0, 0))
best = {}


while q:
    press, minute, me, elep, state, mdist, edist, madd, eadd = heappop(q)
#    print(minute, press, me, elep)
#    input()
    if mdist > 0 and edist > 0:
        heappush(q, (press, minute + 1, me, elep, state, mdist - 1, edist - 1, madd, eadd))
        continue
    moptions = []
    if mdist == 0:
        press = press - madd
        result = min(result, press)
        madd = 0
        for npos in CAN_OPEN:
            if npos in state:
                continue
            dist = DISTS[(me, npos)]
            if dist >= 30 - minute:
                continue
            moptions.append((VALVES[npos][0] * (30 - minute - dist), dist, npos))
        moptions.sort()
    eoptions = []
    if edist == 0:
        press = press - eadd
        result = min(result, press)
        eadd = 0
        for npos in CAN_OPEN:
            if npos in state:
                continue
            dist = DISTS[(elep, npos)]
            if dist >= 30 - minute:
                continue
            eoptions.append((VALVES[npos][0] * (30 - minute - dist), dist, npos))
        eoptions.sort()
    if moptions and not eoptions:
        for score, dist, tgt in moptions:
            nstate = copy.copy(state)
            nstate.append(tgt)
            heappush(q, (press, minute + 1, tgt, elep, nstate, dist, edist-1, score, eadd))
    elif eoptions and not moptions:
        for score, dist, tgt in eoptions:
            nstate = copy.copy(state)
            nstate.append(tgt)
            heappush(q, (press, minute + 1, me, tgt, nstate, mdist-1, dist, madd, score))
    else:
        for s1, d1, t1 in moptions:
            for s2, d2, t2 in eoptions:
                if t1 == t2:
                    continue
                nstate = copy.copy(state)
                nstate.append(t1)
                nstate.append(t2)
                heappush(q, (press, minute + 1, t1, t2, nstate, d1, d2, s1, s2))
print(result)
