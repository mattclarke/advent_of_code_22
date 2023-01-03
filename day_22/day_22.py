import copy
import sys


FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(FILE) as f:
    PUZZLE_INPUT = f.read()

lines = [line for line in PUZZLE_INPUT.split("\n") if line]

GRID = []
START = None
PUZZLE = ""
max_ = 0
for r, l in enumerate(lines):
    if l[0] in [".", " ", "#"]:
        max_ = max(max_, len(l))

for r, l in enumerate(lines):
    if l:
        PUZZLE = l
        row = []
        for c, ch in enumerate(l):
            if START is None and ch == ".":
                START = (r, c)
            row.append(ch)
        while len(row) < max_:
            row.append(" ")
        GRID.append(row)
    else:
        pass
GRID.pop()
sofar = []
temp = []
for ch in PUZZLE:
    if ch == "R" or ch == "L" or ch == " ":
        temp.append(int("".join(sofar)))
        if ch != " ":
            temp.append(ch)
        sofar = []
    else:
        sofar.append(ch)
temp.append(int("".join(sofar)))
PUZZLE = temp


def show(g, pos=None):
    for r, row in enumerate(g):
        l = []
        for c, ch in enumerate(row):
            if pos and pos == (r, c):
                l.append("p")
            else:
                l.append(ch)
        print("".join(l).rstrip())
    print("")


TURN_R = ((0, 1), (1, 0), (0, -1), (-1, 0))

puzzle = copy.copy(PUZZLE)
heading = 0
pos = START

while puzzle:
    # show(GRID, pos)
    dist = puzzle.pop(0)
    rot = puzzle.pop(0) if puzzle else ""
    for _ in range(dist):
        # show(GRID, pos)
        npos = (pos[0] + TURN_R[heading][0], pos[1] + TURN_R[heading][1])
        try:
            if GRID[npos[0]][npos[1]] == "#":
                break
        except:
            pass

        if TURN_R[heading] == (0, 1):
            if npos[1] >= len(GRID[npos[0]]) or GRID[npos[0]][npos[1]] == " ":
                t = (npos[0], 0)
                while True:
                    if GRID[t[0]][t[1]] == ".":
                        npos = t
                        break
                    elif GRID[t[0]][t[1]] == "#":
                        npos = pos
                        break
                    else:
                        t = (t[0], t[1] + 1)
        elif TURN_R[heading] == (0, -1):
            if npos[0] < 0 or GRID[npos[0]][npos[1]] == " ":
                t = (npos[0], len(GRID[npos[0]]) - 1)
                while True:
                    if GRID[t[0]][t[1]] == ".":
                        npos = t
                        break
                    elif GRID[t[0]][t[1]] == "#":
                        npos = pos
                        break
                    else:
                        t = (t[0], (t[1] - 1) % len(GRID[0]))
        elif TURN_R[heading] == (1, 0):
            if npos[0] >= len(GRID) or GRID[npos[0]][npos[1]] == " ":
                t = (0, npos[1])
                while True:
                    if GRID[t[0]][t[1]] == ".":
                        npos = t
                        break
                    elif GRID[t[0]][t[1]] == "#":
                        npos = pos
                        break
                    else:
                        t = (t[0] + 1, t[1])
        elif TURN_R[heading] == (-1, 0):
            if npos[0] < 0 or GRID[npos[0]][npos[1]] == " ":
                t = (len(GRID) - 1, npos[1])
                while True:
                    if t[1] >= len(GRID[t[0]]):
                        t = (t[0] - 1, t[1])
                        continue

                    if GRID[t[0]][t[1]] == ".":
                        npos = t
                        break
                    elif GRID[t[0]][t[1]] == "#":
                        npos = pos
                        break
                    else:
                        t = (t[0] - 1, t[1])

        pos = npos
        assert pos[0] >= 0 and pos[1] >= 0, (pos, dist, rot, heading)
    if rot == "R":
        heading = (heading + 1) % 4
    elif rot == "L":
        heading = (heading - 1) % 4

result = 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + heading

# Part 1 = 109094
print(f"answer = {result}")

FACES = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
FACE_COORDS = {}

size, width, height = (
    (len(GRID) // 4, 3, 4) if len(GRID) > len(GRID[0]) else (len(GRID[0]) // 4, 4, 3)
)

faces = []
face = 1
for h in range(height):
    for w in range(width):
        if GRID[size * h][size * w] == " ":
            continue
        faces.append((h, w))
        FACE_COORDS[face] = (size * h, size * w)
        for r in range(size * h, size * h + size):
            row = []
            for c in range(size * w, size * w + size):
                row.append(GRID[r][c])
            FACES[face].append(row)
        face += 1

# Convert the mapping to a common  net, namely:
#
#  A
# BCD
#  E
#  F
#
# 1 = rotation clockwise

MAP_STD = {
    # U, R, D, L
    "a": [("f", 0), ("d", 1), ("c", 0), ("b", -1)],
    "b": [("a", 1), ("c", 0), ("e", -1), ("f", 2)],
    "c": [("a", 0), ("d", 0), ("e", 0), ("b", 0)],
    "d": [("a", -1), ("f", 2), ("e", 1), ("c", 0)],
    "e": [("c", 0), ("d", -1), ("f", 0), ("b", 1)],
    "f": [("e", 0), ("d", 2), ("a", 0), ("b", 2)],
}

mapping = {}
q = [("a", 0, 0)]
seen = {0}

while q:
    s, f, r = q.pop(0)
    mapping[s] = (f, r)
    curr_face = faces[f]
    for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        try:
            idx = faces.index((curr_face[0] + dr, curr_face[1] + dc))
        except ValueError:
            continue
        if idx in seen:
            continue
        seen.add(idx)
        if (dr, dc) == (1, 0):
            # Down
            foo = (2 + r) % 4
            ns, rot = MAP_STD[s][foo]
            # TODO: this is a hack to make sure we don't do 3 rotations
            # 3 rotations == -1 rotation
            # not very robust - rotate through a list and use mod?
            nr = r + rot
            nr = -1 if nr == 3 else nr
            q.append((ns, idx, nr))
        if (dr, dc) == (0, 1):
            # Right
            foo = (1 + r) % 4
            ns, rot = MAP_STD[s][foo]
            nr = r + rot
            nr = -1 if nr == 3 else nr
            q.append((ns, idx, nr))
        if (dr, dc) == (0, -1):
            # Left
            foo = (3 + r) % 4
            ns, rot = MAP_STD[s][foo]
            nr = r + rot
            nr = -1 if nr == 3 else nr
            q.append((ns, idx, nr))

print(mapping)


def print_face(face, pos):
    for r, row in enumerate(face):
        tmp = []
        for c, ch in enumerate(row):
            if (r, c) == pos:
                tmp.append("P")
            else:
                tmp.append(ch)
        print("".join(tmp))
    print()


def rotate_face(face, num_rots):
    if num_rots == 0:
        return copy.deepcopy(face)
    elif num_rots == 1:
        nface = []
        for i in range(len(face[0])):
            row = []
            for j in range(len(face) - 1, -1, -1):
                row.append(face[j][i])
            nface.append(row)
    elif num_rots == -1:
        nface = []
        for i in range(len(face[0]) - 1, -1, -1):
            row = []
            for j in range(len(face)):
                row.append(face[j][i])
            nface.append(row)
    elif abs(num_rots) == 2:
        nface = []
        for r in face:
            row = list(reversed(r))
            nface.insert(0, row)

    return nface


NET = {}

for name, (face, rot) in mapping.items():
    NET[name] = rotate_face(FACES[face + 1], rot)

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


JOINS = {
    # up, right, down, left
    "a": (
        ("f", lambda r, c: (size - 1, c), UP),
        ("d", lambda r, c: (0, size - r - 1), DOWN),
        ("c", lambda r, c: (0, c), DOWN),
        ("b", lambda r, c: (0, r), DOWN),
    ),
    "b": (
        ("a", lambda r, c: (c, 0), RIGHT),
        ("c", lambda r, c: (r, 0), RIGHT),
        ("e", lambda r, c: (size - c - 1, 0), RIGHT),
        ("f", lambda r, c: (size - r - 1, 0), RIGHT),
    ),
    "c": (
        ("a", lambda r, c: (size - 1, c), UP),
        ("d", lambda r, c: (r, 0), RIGHT),
        ("e", lambda r, c: (0, c), DOWN),
        ("b", lambda r, c: (r, size - 1), LEFT),
    ),
    "d": (
        ("a", lambda r, c: (size - c - 1, size - 1), LEFT),
        ("f", lambda r, c: (size - r - 1, size - 1), LEFT),
        ("e", lambda r, c: (c, size - 1), LEFT),
        ("c", lambda r, c: (r, size - 1), LEFT),
    ),
    "e": (
        ("c", lambda r, c: (size - 1, c), UP),
        ("d", lambda r, c: (size - 1, r), UP),
        ("f", lambda r, c: (0, c), DOWN),
        ("b", lambda r, c: (size - 1, size - r - 1), UP),
    ),
    "f": (
        ("e", lambda r, c: (size - 1, c), UP),
        ("d", lambda r, c: (size - r - 1, size - 1), LEFT),
        ("a", lambda r, c: (0, c), DOWN),
        ("b", lambda r, c: (size - r - 1, 0), RIGHT),
    ),
}

puzzle = copy.copy(PUZZLE)
heading = RIGHT
curr_face = "a"
pos = (0, 0)

while puzzle:
    dist = puzzle.pop(0)
    rot = puzzle.pop(0) if puzzle else ""
    for _ in range(dist):
        if heading == UP:
            npos = (pos[0] - 1, pos[1])
            if npos[0] >= 0:
                if NET[curr_face][npos[0]][npos[1]] == "#":
                    break
            else:
                # Change face
                f, conv, nd = JOINS[curr_face][0]
                npos = conv(*pos)
                if NET[f][npos[0]][npos[1]] == "#":
                    break
                curr_face = f
                heading = nd
        elif heading == RIGHT:
            npos = (pos[0], pos[1] + 1)
            if npos[1] < size:
                if NET[curr_face][npos[0]][npos[1]] == "#":
                    break
            else:
                # Change face
                f, conv, nd = JOINS[curr_face][1]
                npos = conv(*pos)
                if NET[f][npos[0]][npos[1]] == "#":
                    break
                curr_face = f
                heading = nd
        elif heading == DOWN:
            npos = (pos[0] + 1, pos[1])
            if npos[0] < size:
                if NET[curr_face][npos[0]][npos[1]] == "#":
                    break
            else:
                # Change face
                f, conv, nd = JOINS[curr_face][2]
                npos = conv(*pos)
                if NET[f][npos[0]][npos[1]] == "#":
                    break
                curr_face = f
                heading = nd
        elif heading == LEFT:
            npos = (pos[0], pos[1] - 1)
            if npos[1] >= 0:
                if NET[curr_face][npos[0]][npos[1]] == "#":
                    break
            else:
                # Change face
                f, conv, nd = JOINS[curr_face][3]
                npos = conv(*pos)
                if NET[f][npos[0]][npos[1]] == "#":
                    break
                curr_face = f
                heading = nd
        pos = npos
    if rot == "R":
        heading = (heading + 1) % 4
    elif rot == "L":
        heading = (heading - 1) % 4

# Convert back to "real" space
curr_face, rotate = mapping[curr_face]
curr_face += 1  # because faces start from 1 (for now)

if rotate == 2:
    pos = (size - pos[0], size - pos[1])
elif rotate == 1:
    pass
elif rotate == -1:
    pass

result = (
    1000 * (FACE_COORDS[curr_face][0] + pos[0] + 1)
    + 4 * (FACE_COORDS[curr_face][1] + pos[1] + 1)
    + [3, 0, 1, 2][heading]
)

# Part 2 = 53324
print(f"answer = {result}")
