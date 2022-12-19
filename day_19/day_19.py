import copy
import sys

from heapq import heappush, heappop

FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

BLUEPRINTS = {}

result = 0
['Blueprint', '1:', 'Each', 'ore', 'robot', 'costs', '4', 'ore.', 'Each', 'clay', 'robot', 'costs', '2', 'ore.', 'Each', 'obsidian', 'robot', 'costs', '3', 'ore', 'and', '14', 'clay.', 'Each', 'geode', 'robot', 'costs', '2', 'ore', 'and', '7', 'obsidian.']

for i, l in enumerate(lines):
    parts = l.split()
    ore = (int(parts[6]), 0, 0)
    clay = (int(parts[12]), 0, 0)
    obs = (int(parts[18]), int(parts[21]), 0)
    geode = (int(parts[27]), 0, int(parts[30]))
    BLUEPRINTS[i+1] = (ore, clay, obs, geode) 

RESULTS = {}

for num, bp in BLUEPRINTS.items():
    q = [(-1,1, (1, 0, 0, 0), (0,0,0,0), [0],[])]
    BEST = {}
    result = 0

    while q:
        score, minute, (r_ore, r_clay, r_obs, r_geode), (ore, clay, obs, geode), state, ignore = heappop(q)
        if minute > 24:
            result = max(result, geode)
            continue
        best = BEST.get(minute, [0])
        if len(best) >= len(state) and state[minute -1] < best[minute-1]:
            continue
        BEST[minute] = copy.copy(state)
        can_build = []
        for rp, rtype in zip(bp, ['ore', 'clay', 'obs', 'geode']):
            if ore >= rp[0] and clay >= rp[1] and obs >= rp[2]:
                can_build.append(rtype)
        if 'geode' in can_build:
            can_build = ['geode']
        if 'obs' in can_build:
            can_build = ['obs']

        ore += r_ore
        clay += r_clay
        obs += r_obs
        geode += r_geode

        nstate = copy.copy(state)
        nstate.append(geode)
        
        if can_build and can_build != ignore:
            for rtype in can_build:
                if rtype == 'ore':
                    o, c, ob = bp[0]
                    heappush(q, (-(r_ore + r_clay + r_obs + 2*r_geode), minute + 1, (r_ore +1, r_clay, r_obs, r_geode), (ore-o, clay-c, obs-ob, geode), copy.copy(nstate), []))
                elif rtype == 'clay':
                    o, c, ob = bp[1]
                    heappush(q, (-(r_ore + r_clay + r_obs + 2*r_geode), minute + 1, (r_ore, r_clay+1, r_obs, r_geode), (ore-o, clay-c, obs-ob, geode), copy.copy(nstate),[]))
                elif rtype == 'obs':
                    o, c, ob = bp[2]
                    heappush(q, (-(r_ore + r_clay + r_obs + 2*r_geode), minute + 1, (r_ore, r_clay, r_obs+1, r_geode), (ore-o, clay-c, obs-ob, geode), copy.copy(nstate),[]))
                elif rtype == 'geode':
                    o, c, ob = bp[3]
                    heappush(q, (-(r_ore + r_clay + r_obs + 2*r_geode), minute + 1, (r_ore, r_clay, r_obs, r_geode+1), (ore-o, clay-c, obs-ob, geode), copy.copy(nstate),[]))
                else:
                    assert False
        heappush(q, (-(r_ore + r_clay + r_obs + 2*r_geode), minute + 1, (r_ore, r_clay, r_obs, r_geode), (ore, clay, obs, geode), copy.copy(nstate), can_build))

    RESULTS[num] = result
    print(num, result)
print(RESULTS)
result = 0
for k, v in RESULTS.items():
    result += k * v
# Part 1 = 
print(f"answer = {result}")

result = 0

# Part 2 = 
print(f"answer = {result}")
