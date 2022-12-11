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

