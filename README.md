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
