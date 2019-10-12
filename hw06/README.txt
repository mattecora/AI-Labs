################################################################################
#                                  Homework 6                                  #
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
    > Input initial state: 1 0 2 4 5 7 3 8 9 6 11 12 13 10 14 15

- Input the maximum time limit for unsolvable states (in seconds):
    > Input time limit: 30

- Decide the heuristic to be used (1: misplaced tiles, 2: Manhattan distance):
    > Heuristic to use (1/2)? 2

- If the initial state is solvable, then results are shown:
    > Moves: ['R', 'D', 'L', 'D', 'D', 'R', 'R']
    > Number of nodes expanded: 7
    > Time taken (seconds): 0.0010252
    > Memory used (bytes): 8192

- If the initial state is not solvable, an error message is shown:
    > Solution not found.

## How it works ##

The solution for the assignment is similar to the one proposed for the previous 
homeworks, the only difference being the implementation of the search algorithm 
(in this case, the A* Search is used). This is implemented in the solve_astar() 
method of the Puzzle class, which allows to use two possible heuristics for the 
estimation of a node's cost:

- h1(), which counts the number of misplaced tiles;
- h2(), which computes the Manhattan distance of a misplaced tile to its final 
expected position.

The selection between the two version is performed through an integer variable, 
stored in the Puzzle object, set to 1 when the first heuristic has to be used 
and to any other value when the second heuristic has to be used (default). In 
both cases, the search method performs the following actions:

- It initializes a number of parameters, such as the number of expanded nodes, 
the start time, the start memory, the search frontier (initially, a single node 
corresponding to the initial state) and a list of visited states;
- It runs a loop until the time difference with the start time is less then the 
set time limit and the search frontier is not empty;
- At each iteration, it pops a node from the front of the frontier and checks 
whether it is a goal, in which case it returns the path to the node, the number 
of expansions, the elapsed time and the used memory;
- If the node is not a goal and its state has not already been visited, it is 
expanded and its successors are pushed into the frontier sorted by the value of 
f(n) = g(n) + h(n); this operation is performed through the insort() function 
of the bisect library, which results to be much faster than sorting the frontier
each time a node is inserted.

To take into account the value of the heuristic function, the Node class has 
been expanded with the introduction of an additional field, called hval. The two
heuristics are computed as follows:

- h1() performs a sum over a list, created using the list comprehension syntax, 
which contains 0 for all tiles already in their final position and 1 for all 
currently misplaced tiles;
- h2() loops over the values from 0 to the dimension of the puzzle; for each 
element, it retrieves its position into the given state and computes its final 
position, summing to the returned value the Manhattan distance between the two 
locations.

The other methods are implemented as in the previous assignment.