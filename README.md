# advent_of_code_22
https://adventofcode.com/2022

## Day 1
- Part 1: loop through the data to find the maximum.
- Part 2: keep all the sums for each elves, sort then sum the highest three.

## Day 2
- Part 1: loop through and compare the "hands".
- Part 2: similar but second column is the desired result.

Initially I did it "long hand" but went back and refactored to make it more compact.

## Day 3
- Part 1: loop, split and use a set to find the item that appears in both.
- Part 2: similar but compare three elves to find the common item.

## Day 4
- Part 1: convert to ints and see if the whole range is contained.
- Part 2: similar but see if either of the ends of one range are enclosed by the other range.

## Day 5
- Part 1: the hard part was extracting the data for the crates, it would have been quicker to copy that information by hand.
- Part 2: same but use an additional stack to keep the crate order.

## Day 6
- Part 1: use a queue to keep the last four characters in, then convert to a set. If the length of the set is 4 then we have the answer.
- Part 2: same but the length is 14 rather than 4.

## Day 7
- Part 1: use a stack and sum the file sizes. When popping out of the directory add that directory's size to the enclosing directory. DON'T FORGET TO POP THE STACK AT THE END!
- Part 2: filter to get directories of suitable size then find the smallest.

## Day 8
- Part 1: loop through the rows and columns (forward and reverse) and add the trees that can be seen from outside to a set.
- Part 2: for each tree in the set, go in each direction until reaches edge or hits a tree that cannot be seen over. After each direction multiple the score.

## Day 9
- Part 1: move the head and if the tail is not adjecent move it towards the head. Store tail's position in a set.
- Part 2: create a list of the ten knots, move the first one and then update the others based on the preceeding knot. Store the last knot's position in a set.

## Day 10
- Part 1: started by not reading the instructions correctly! If it is an add command then it "execute" during the next cycle, so store the value to be added and do the addition next turn.
- Part 2: if the current pixel is within one of the value in the register the pixel is on. Requires some modulo to get the lines.

## Day 11
- Part 1: implement the algorithm as described. I typed the puzzle data in by hand rather than parse it!
- Part 2: need to keep the worry smallish otherwise the maths starts to get slow (e.g. taking the modulus of a big number takes a long time). I guessed (after a few attempts) that the solution was to modulo the worry by the LCM of all the monkeys' divisors. Not entirely sure why that works...

UPDATE:

We don't care about the worry value as such, we only care how it responds to having a modulo applied. 

For addition:
 - `(x + a) % y` = `((x % y) + (a % y)) % y`

For multiplication:
 - `(x * a) % y` = `((x % y) * (a % y)) % y`

Examples:
```
(30 + 8) % 19 = 0 and ((30 % 19) + (8 % 19)) % 19 = 0
(35 + 8) % 19 = 5 and ((35 % 19) + (8 % 19)) % 19 = 5

(38 * 4) % 19 = 0 and ((38 % 19) * (4 % 19)) % 19 = 0
(20 * 4) % 19 = 4 and ((20 % 19) * (4 % 19)) % 19 = 4

(45 * 45) % 19 = 11 and ((45 % 19) * (45 % 19)) % 19 = 11
```
As there are multiple divisors we need to use the LCM as it is the lowest value that is valid for all the divisors.
```
Consider 17 and 19:
  17 * 19 = 323

  500 % 17 = 7
  500 % 323 = 177 => 177 % 17 = 7

  500 % 19 = 6
  500 % 323 = 177 => 177 % 19 = 6
```

## Day 12
- Part 1: used a BFS to find the route.
- Part 2: same but with multiple starting points.

## Day 13
- Part 1: created a recursive comparison function. Recursive to handle lists within lists.
- Part 2: used the function from part 1 with `functools.cmp_to_key` to order the signals.

## Day 14
- Part 1: reasonably straightforward to implement the algorithm using sets. Stop the simulation when sand exceeds either the horizontal or vertical bounds.
- Part 2: same as part 1 except the addition of an infinite floor. Stop when sand is added to the sand origin.

## Day 15
- Part 1: for each sensor, mark all empty coordinates that are within the Manhatten distance and on the specified row 
- Part 2: for each row and column, see if it reachable from a sensor. If it is reachable from a sensor, then jump forward to the next column that cannot be reached from that sensor (checking each column would take forever!). If not reachable then we are done. 

## Day 16
- Part 1: used a heapq to prioritise the most promising solutions.
- Part 2: took many many hours. Rewrote part 1 to try to optimise the solutions. Reduced the nodes down to only those that can be opened and calculated the distance to all other nodes. Lots of ifs, so was a bit buggy. Getting the right answer the first time took ~10 minutes, but with some pruning managed to get it down to ~70 seconds (pypy). Would like to make it a bit neater!

UPDATE: realised that there was **no reason to do both in parallel**: I can do all my moves first then switch to the elephant. This only requires a small modification to the solution to part 1 to switch to the elephant when there is no more options in range for me. Much less confusing logic. Also added tracking of best values to speed it up. Takes less than 20 seconds to run.

Note: it doesn't work for the example because I can open all the valves before changing to the elephant.

## Day 17
- Part 1: implement the "game" - took me a while to do this!
- Part 2: target to big to simulate, but after the simulation settles down the height increase per shape repeats. The repetition allows the answer to be derived mathematically, see the code for details.

An alternative would have been to record the top ~30 rows after each rock and see when a repeat occurs.

## Day 18
- Part 1: for each rock check all the sides to see if there is air next to it.
- Part 2: surround the area with 'water' and for any cube that touches water fill that one. Repeat until water has got every where it can, then count the rock sides that touch water.

## Day 19
- Part 1: use a heapq to queue all the "choices" and then work through them. Using a number of tricks to skip branches, such as bailing if the same state has been achieving in a quicker time, don't build more robots than we need, etc. Still pretty slow at ~6 minutes with pypy.
- Part 2: adjusted to new rules. Takes ~15 minutes to complete. Will try to speed it up.

Update:
- replacing the "score" with `minutes` rather than `r_geo` brings the times down to ~175s and ~700s. Using `minutes` is almost the same as doing a DFS? 
- Using a regular deque instead of a heapq reduces the times down to ~52 seconds and ~270 seconds.
- Using `appendleft` when building a geode robot reduces the times a little (~47s and ~230s). Internet tip!
- Last minute will produce the same number of geodes as the previous minute, so can just add `r_geode` and exit (~35s and 130s). Internet tip!
- Throw away any materials we cannot spend in the remaining time. This reduces the number of different states, so we are more likely to hit the cache for major speed increases (~14s and ~40s!). Internet tip!

## Day 20
- Part 1: implemented the algorithm using a linked list because a) it is easier than doing the wrap-around maths and b) I suspected it would be needed for part 2.
- Part 2: the stepsize is huge, but as the list is circular we can use the modulo to reduce it. Took a while for me to realise I needed to take the modulo of the number of nodes - 1 because we have detached the original node!

## Day 21
- Part 1: implement the algorithm as described.
- Part 2: apply the modifications and then binary search for the correct value. Initially, I did it by hand because I am lazy!

## Day 22
- Part 1: implement the instructions. To make it easier to deal with the wrapping I padded the rows to the same length, so the map is rectangular.
- Part 2: the hard bit is working out how the faces join together and how that affects the row, column and direction when moving faces. I spent a lot of time looking at a cube with numbers written on it! Not sure how to make the solution general.

## Day 23
- Part 1: implement the algorithm. I had to do two passes, one to find the positions where two or more elves wanted to move to and one to do the moves if allowed. Can the duplication be reduced?
- Part 2: same thing, but count the elves that don't move and when that number equals the total number of elves return the round number.

Update:
- refactored to reduce the duplication by using a defaultdict. Simplies part 2 too.
