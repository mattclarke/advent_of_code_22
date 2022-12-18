import copy
import sys

from heapq import heappush, heappop

FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

result = 0

VALVES = {}

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
    for score, dist, tgt in options:
        nstate = copy.copy(state)
        nstate.append(tgt)
        heappush(q, (press, score, minute + 1, tgt, nstate, dist))

# Part 1 = 1488
print(f"answer = {-result}")


result = 0
q = []
heappush(q, (0, 0, 1, "AA", [], 0, False))
best = {}


while q:
    press, toadd, minute, curr, state, dist, is_elep = heappop(q)
    # Guessed that by the time we have 4 valves open, the best
    # arrangment is the optimal configuration.
    # Saves a lot of time as we can skip many configurations.
    if len(state) > 4:
        mn = 30 + minute if is_elep else minute
        if press > best.get((mn, frozenset(state)), 0):
            continue
        best[(mn, frozenset(state))] = press
    if dist > 0:
        heappush(
            q, (press, toadd, minute + 1, curr, copy.copy(state), dist - 1, is_elep)
        )
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
        if dist >= 26 - minute:
            continue
        options.append((VALVES[npos][0] * (26 - minute - dist), dist, npos))
    for score, dist, tgt in options:
        nstate = copy.copy(state)
        nstate.append(tgt)
        heappush(q, (press, score, minute + 1, tgt, nstate, dist, is_elep))
    if not options and not is_elep:
        # Switch to elephant: set location back to "AA" and time back to
        # minute 1 and carry on.
        nstate = copy.copy(state)
        heappush(q, (press, 0, 1, "AA", nstate, 0, True))


# Part 2 = 2111
print(f"answer = {-result}")

assert False, "delete this line to run the original solution to part 2"

result = 0
q = []
heappush(q, (0, 1, "AA", "AA", [], 0, 0))
best = {}
length = 26

while q:
    press, minute, me, elep, state, mdist, edist = heappop(q)
    nstate = copy.copy(state)
    # Guessed that by the time we have 4 valves open, the best
    # arrangment is the optimal configuration.
    # Saves a lot of time as we can skip many configurations.
    if len(state) > 4:
        if press > best.get((minute, frozenset(state)), 0):
            continue
        best[(minute, frozenset(state))] = press
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
                    dist,
                    npos,
                )
            )
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
                    dist,
                    npos,
                )
            )
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
        for dist, tgt in moptions:
            if tgt == elep:
                continue
            heappush(
                q, (press, minute + 1, tgt, elep, copy.copy(nstate), dist, edist - 1)
            )
    elif eoptions and not moptions:
        for dist, tgt in eoptions:
            if tgt == me:
                continue
            heappush(
                q, (press, minute + 1, me, tgt, copy.copy(nstate), mdist - 1, dist)
            )
    elif len(moptions) == 1 and len(eoptions) == 1 and moptions[0] == eoptions[0]:
        # Only one node left for both, so send the one closest
        d1, t1 = moptions[0]
        d2, t2 = eoptions[0]
        if d1 <= d2:
            heappush(q, (press, minute + 1, t1, elep, copy.copy(nstate), d1, edist))
        else:
            heappush(q, (press, minute + 1, me, t2, copy.copy(nstate), mdist, d2))
    elif moptions and eoptions:
        for d1, t1 in moptions:
            if t1 == elep:
                continue
            for d2, t2 in eoptions:
                if t1 == t2 or t2 == me:
                    continue
                heappush(q, (press, minute + 1, t1, t2, copy.copy(nstate), d1, d2))
    else:
        # No nodes within reach within the remaining time
        heappush(
            q, (press, minute + 1, me, elep, copy.copy(nstate), mdist - 1, edist - 1)
        )


# Part 2 = 2111
print(f"answer = {-result}")
