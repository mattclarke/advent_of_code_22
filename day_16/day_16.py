import copy
import sys

from heapq import heappush, heappop

FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

result = 0

VALVES = {}

[
    "Valve",
    "AA",
    "has",
    "flow",
    "rate=0;",
    "tunnels",
    "lead",
    "to",
    "valves",
    "DD,",
    "II,",
    "BB",
]

for l in lines:
    l = l.split()
    v = l[1]
    r = int(l[4].replace(";", "")[5:])
    t = [x.replace(",", "") for x in l[9:]]
    VALVES[v] = (r, t)

CAN_OPEN = set()

for n, v in VALVES.items():
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
heappush(q, (0, 0, 1, "AA", [], 0))
best = {}


while q:
    press, toadd, minute, curr, state, dist = heappop(q)
    if dist > 0:
        heappush(q, (press, toadd, minute + 1, curr, state, dist - 1))
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

# Part 1 = 1488
print(f"answer = {-result}")

result = 0
q = []
heappush(q, (0, 1, "AA", "AA", [], 0, 0))
best = {}
length = 26
test = ["JJ", "DD", "HH", "BB", "CC", "EE"]

while q:
    press, minute, me, elep, state, mdist, edist = heappop(q)
    nstate = copy.copy(state)
    foo = best.get((minute, tuple(state)), 0)
    if press > foo:
        continue
    best[(minute, tuple(state))] = press
    moptions = []
    if mdist == 0:
        if me != "AA":
            nstate.append(me)
        for npos in CAN_OPEN:
            if npos in nstate or npos == elep:
                continue
            dist = DISTS[(me, npos)]
            if dist >= length - minute:
                continue
            moptions.append(
                (
                    VALVES[npos][0] * (length - minute - dist),
                    VALVES[npos][0],
                    dist,
                    npos,
                )
            )
        moptions.sort()
    eoptions = []
    if edist == 0:
        if elep != "AA":
            nstate.append(elep)
        for npos in CAN_OPEN:
            if npos in nstate or npos == me:
                continue
            dist = DISTS[(elep, npos)]
            if dist >= length - minute:
                continue
            eoptions.append(
                (
                    VALVES[npos][0] * (length - minute - dist),
                    VALVES[npos][0],
                    dist,
                    npos,
                )
            )
        eoptions.sort()
    if minute <= length:
        add = 0
        for s in nstate:
            add -= VALVES[s][0]
        press += add
        result = min(result, press)
    else:
        continue
    if mdist > 0 and edist > 0:
        heappush(q, (press, minute + 1, me, elep, nstate, mdist - 1, edist - 1))
        continue
    if moptions and not eoptions:
        for _, score, dist, tgt in moptions:
            if tgt == elep:
                continue
            heappush(
                q, (press, minute + 1, tgt, elep, copy.copy(nstate), dist, edist - 1)
            )
    elif eoptions and not moptions:
        for _, score, dist, tgt in eoptions:
            if tgt == me:
                continue
            heappush(
                q, (press, minute + 1, me, tgt, copy.copy(nstate), mdist - 1, dist)
            )
    elif len(moptions) == 1 and len(eoptions) == 1 and moptions[0] == eoptions[0]:
        _, s1, d1, t1 = moptions[0]
        _, s2, d2, t2 = eoptions[0]
        if d1 <= d2:
            heappush(q, (press, minute + 1, t1, elep, copy.copy(nstate), d1, edist))
        else:
            heappush(q, (press, minute + 1, me, t2, copy.copy(nstate), mdist, d2))
    elif moptions and eoptions:
        for _, s1, d1, t1 in moptions:
            if t1 == elep:
                continue
            for _, s2, d2, t2 in eoptions:
                if t1 == t2 or t2 == me:
                    continue
                heappush(q, (press, minute + 1, t1, t2, copy.copy(nstate), d1, d2))
    else:
        heappush(
            q, (press, minute + 1, me, elep, copy.copy(nstate), mdist - 1, edist - 1)
        )


# Part 2 = 2111
print(f"answer = {-result}")
