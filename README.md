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

Update: 
- I realised that there was **no reason to do both in parallel**: I can do all my moves first then switch to the elephant. This only requires a small modification to the solution to part 1 to switch to the elephant when there are no more options in range for me. Much less confusing logic. Also added tracking of best values to speed it up. Takes less than 20 seconds to run.

Note: it doesn't work for the example because I can open all the valves before changing to the elephant.

- Interleaved the moves of me and the elephant, so now it works for the example too.

- Neatest internet solution seems to be to use DP, and for part 2 split the 'available' valves in two (one for the elephant and one for me) and run the code for part 1 twice for all combinations to get the highest score.

Update July 2023:
- Rerunning part 1 but for 26 minutes using DP gives us a cache of possible valve states against total pressure. If we keep this cache and select the entries with the best pressure for a particular set of valves then we can find the best pair of unique valve sets which gives us our answer!
- Currently doesn't work for the example...

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
- Replacing the "score" with `minutes` rather than `r_geo` brings the times down to ~175s and ~700s. Using `minutes` is almost the same as doing a DFS? 
- Using a regular deque instead of a heapq reduces the times down to ~52 seconds and ~270 seconds.
- Using `appendleft` when building a geode robot reduces the times a little (~47s and ~230s). Internet tip!
- Last minute will produce the same number of geodes as the previous minute, so can just add `r_geode` and exit (~35s and 130s). Internet tip!
- Throw away any materials we cannot spend in the remaining time. This reduces the number of different states, so we are more likely to hit the cache for major speed increases (~14s and ~40s!). Internet tip!

Update July 2023:
- watched this video https://youtu.be/5rb0vvJ7NCY before trying to implement this in Elixir
- Initial working version with cache takes 993s (16.5 minutes) for part 1.
- Only building the maximum required number of robots (e.g. if the most ore required for a build is 4 then we only need 4 ore robots) brings it down to 99s.
- Skip the final round as it will produce the same number of geodes as the previous round = 46s.
- Throw away materials we don't need to reduce the number of cache states = 22s.
- Calculate the upper bound for a branch and if it cannot exceed the best score so far then don't explore it = 9s.
- If we can build X on a turn then don't wait and then build it next turn as that cannot produce a better result = 4s.
- In the video, he then removes the cache as the number of cache misses is the bottleneck but this makes it slower for my version (Elixir vs Rust issue?). His cache hits were ~5% but mine are ~10-30% which is probably because I throw away unrequired materials.
- Part 2 takes 5s. It's a newer computer than the one used in December, so PyPy3's times now are 8s and 18s for comparison.


## Day 20
- Part 1: implemented the algorithm using a linked list because a) it is easier than doing the wrap-around maths and b) I suspected it would be needed for part 2.
- Part 2: the stepsize is huge, but as the list is circular we can use the modulo to reduce it. Took a while for me to realise I needed to take the modulo of the number of nodes - 1 because we have detached the original node!

Pro tip:
- Use a deque as the linked list and `queue.append(queue.popleft())` to rotate the list.
- Rotating the item we are interested in to the front makes the maths easier.
- Note: it is slower than a real linked list but quicker to implement!

## Day 21
- Part 1: implement the algorithm as described.
- Part 2: apply the modifications and then binary search for the correct value. Initially, I did it by hand because I am lazy!

## Day 22
- Part 1: implement the instructions. To make it easier to deal with the wrapping I padded the rows to the same length, so the map is rectangular.
- Part 2: the hard bit is working out how the faces join together and how that affects the row, column and direction when moving faces. I spent a lot of time looking at a cube with numbers written on it! Not sure how to make the solution general.

Update:
- Part 2 is now general! Read on Reddit that it was possible to map any net shape to a common net (I chose the standard cross shape), so then it is only necessary to solve for that shape. There is some complication in mapping a net to a common net but it is okay. 

## Day 23
- Part 1: implement the algorithm. I had to do two passes, one to find the positions where two or more elves wanted to move to and one to do the moves if allowed. Can the duplication be reduced?
- Part 2: same thing, but count the elves that don't move and when that number equals the total number of elves return the round number.

Update:
- Refactored to reduce the duplication by using a defaultdict. Simplies part 2 too.

## Day 24
- Part 1: implemented the algorithm using heapq. Despite some branch trimming it is slow (~8 minutes).
- Part 2: basically runs the algorithm three times. Very slow at ~28 minutes!  

Update:
- Remove unnecessary copying brings part 1 down to <3 minutes and part 2 down to <11 minutes.
- STUPID! Nothing wrong with my solution concept but continually creating frozenset is incredibly slow. Removing that from what goes into SEEN (as it turns out not to be required!) brings it down to ~30s!
- Creating the wind cache beforehand and indexing it by the minute modulo the cache length brings it down to ~3 seconds (because it removes the excessive tuple creation I was using when creating the cache). Hat-tip to JP for the idea of creating the cache first and using the minute as the key!
- heapq is unnecessary, using a standard deque-based BFS is actually faster at ~1 second.

Update 2024:
- Added a solution based on an APL solution I saw. Basically it done as a variation of Conway's game of life:
  - From each possible position we could currently be at, we populate the compass directions and the current position.
  - We then kill all the position where the winds are.
  - Repeat until the end position is occupied.

## Day 25
- Part 1: converting numbers to and from a weird base 5. Took me a while to work out how to convert back to decimal.
- Part 2: no part 2!

Update:
- Internet example shows that it can be done in a more "traditional" way. Normally converting from a decimal to another base can be done like so:
```
result = []

while target != 0:
    target, d = divmod(target, 5)
    # insert as we are starting with the least significant
    result.insert(0, d)

```
- However, for this task the digits can only range from -2 to 2. Therefore, if the modulo is greater than 2 it can be brought back into range by subtracting -5. When this happens we "carry" one to the next digit:
```
decimal is 38
divmod by 5 gives 7 and a remainder of 3
3 is greater than 2 so we subtract 5 giving -2 and a carry

divmod by 5 of 7 gives 1 and a remainder of 2
but as there was a carry the remainder becomes 3
3 is greater than 2 so we subtract 5 giving -2 and a carry

finally, divmod by 5 of 1 gives 0 and a remainder of 1
add the carry gives 2, so the final answer is '2, -2, -2'
```
