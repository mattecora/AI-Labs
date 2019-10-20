################################################################################
#                                  Homework 7                                  #
#                CS 411 - Artificial Intelligence I - Fall 2019                #
#                           Matteo Corain 650088272                            #
################################################################################

## Requirements ##

- Python3 interpreter (tested on Python 3.7.4, Windows OS)
- psutil package (can be installed using pip)

## How to run ##

- Run script puzzle.py using the Python interpreter:
    > python puzzle.py

- Input the size of the puzzle (length of the side, N for a NxN puzzle):
    > Input puzzle dimension: 4 (15-puzzle)

- Input the initial state as a space-separated integer list:
    > Input initial state: 5 2 4 8 10 0 3 14 13 6 11 12 1 15 9 7

- Input the maximum time limit for unsolvable states (in seconds):
    > Input time limit: 30

- Decide the heuristic to be used (1: misplaced tiles, 2: Manhattan distance):
    > Heuristic to use (1/2)? 2

- If the initial state is solvable, then results are shown:
    > Moves: ['R', 'D', 'D', 'L', 'L', 'U', 'R', 'D', 'R', 'R', 
              'U', 'U', 'L', 'L', 'D', 'R', 'R', 'U', 'U', 'L', 
              'L', 'D', 'L', 'D', 'R', 'R', 'D', 'L', 'U', 'U', 
              'L', 'U', 'R', 'R', 'D', 'D', 'R', 'D']
    > Number of nodes expanded: 528926
    > Time taken (seconds): 19.7194
    > Memory used (bytes): 69632

- If the initial state is not solvable, an error message is shown:
    > Solution not found.

## How it works ##

The solution for the assignment is similar to the one proposed for the previous 
homeworks, extending the iterative deepening approach using as cutoff the f 
value as considered in A*. Initially, the cutoff is set to the f value of the 
initial state; then, for each unsuccessful call to the depth-limited search, it 
is updated with the minimum value that is greater than the current cutoff. For 
this reason, the value of the next limit is initially set to inf and updated 
whenever we are expanding a node whose f value is greater than the cutoff. Also 
in this case, both the misplaced tiles and the Manhattan distance heuristic 
functions can be used.

Compared to the previous assignments, some optimizations have been implemented 
to support the solution of more complex initial states as the ones provided as 
the last test cases. The main change to improve the overall efficiency has been 
to save visited states in the form of hashable tuples in a hash set, instead of 
in the form of lists stored in a list; in this way, the check for determining 
whether a state has been visited can be reduced to a O(1) "in" operation, great 
improvement over the previous O(n) search.

An additional improvement has been to reduce the number of index() operations, 
which are particularly expensive when performed many times during the search, 
by caching their results whenever possible.