import copy
import sys

from heapq import heappush, heappop

FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line.strip() for line in PUZZLE_INPUT.split("\n") if line]

BLUEPRINTS = {}

result = 0

for i, l in enumerate(lines):
    parts = l.split()
    ore = (int(parts[6]), 0, 0)
    clay = (int(parts[12]), 0, 0)
    obs = (int(parts[18]), int(parts[21]), 0)
    geode = (int(parts[27]), 0, int(parts[30]))
    BLUEPRINTS[i+1] = (ore, clay, obs, geode) 

RESULTS = {}



for num, bp in BLUEPRINTS.items():
    q = [(-1,1, (1, 0, 0, 0), (0,0,0,0), set())]
    BEST = {}
    result = 0
    max_ore = max(bp[0][0], bp[1][0], bp[2][0], bp[3][0])
    max_cla = max(bp[0][1], bp[1][1], bp[2][1], bp[3][1])
    max_obs = max(bp[0][2], bp[1][2], bp[2][2], bp[3][2])

    while q:
        score, minute, (r_ore, r_cla, r_obs, r_geo), (ore, cla, obs, geo), ignore = heappop(q)

        if minute > 32:
            result = max(result, geo)
            print(result)
            continue

        if (minute, (r_ore, r_cla, r_obs, r_geo), (ore, cla, obs, geo)) in BEST:
            continue
        BEST[(minute, (r_ore, r_cla, r_obs, r_geo), (ore, cla, obs, geo))] = 0

        can_build = set()
        for rp, rtype in zip(bp, ['ore', 'cla', 'obs', 'geo']):
            if ore >= rp[0] and cla >= rp[1] and obs >= rp[2]:
                can_build.add(rtype)

        ore += r_ore
        cla += r_cla
        obs += r_obs
        geo += r_geo

        #print(minute, r_ore, r_cla, r_obs, r_geo, ore, cla, obs, geo, can_build)
        #print(len(q))
        minute += 1
        #input()

        if not can_build:
            heappush(q, (-(r_geo), minute, (r_ore, r_cla, r_obs, r_geo), (ore, cla, obs, geo), set()))
            continue

        if can_build == ignore:
            heappush(q, (-(r_geo), minute, (r_ore, r_cla, r_obs, r_geo), (ore, cla, obs, geo), ignore))
        
        for rtype in can_build:
            if rtype == 'ore':
                if r_ore == max_ore:
                    # don't build more than we need!
                    continue
                if r_obs > 0:
                   # once we are building obs it is too late to build more
                   continue
                o, c, ob = bp[0]
                heappush(q, (-(r_geo), minute, (r_ore+1, r_cla, r_obs, r_geo), (ore-o, cla-c, obs-ob, geo), set()))
            elif rtype == 'cla':
                if r_cla == max_cla:
                    # don't build more than we need!
                    continue
                o, c, ob = bp[1]
                heappush(q, (-(r_geo), minute, (r_ore, r_cla+1, r_obs, r_geo), (ore-o, cla-c, obs-ob, geo), set()))
            elif rtype == 'obs':
                if r_obs == max_obs:
                    # don't build more than we need!
                    continue
                o, c, ob = bp[2]
                heappush(q, (-(r_geo), minute, (r_ore, r_cla, r_obs+1, r_geo), (ore-o, cla-c, obs-ob, geo), set()))
            elif rtype == 'geo':
                o, c, ob = bp[3]
                heappush(q, (-(r_geo), minute, (r_ore, r_cla, r_obs, r_geo+1), (ore-o, cla-c, obs-ob, geo), set()))
            else:
                assert False

        # If can build anything then must build something
        if len(can_build) == 4:
            continue
        else:
            # Don't forget we can not build too
            heappush(q, (-(r_geo), minute, (r_ore, r_cla, r_obs, r_geo), (ore, cla, obs, geo), can_build))

    RESULTS[num] = result
    print(num, result)
    break
print(RESULTS)
result = 0
for k, v in RESULTS.items():
    result += k * v

# Part 1 = 1616
print(f"answer = {result}")

result = 0

# Part 2 = 8990 
print(f"answer = {result}")
