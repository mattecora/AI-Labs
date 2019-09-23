################################################################################
#                                  Homework 4                                  #
#                CS 411 - Artificial Intelligence I - Fall 2019                #
#                           Matteo Corain 650088272                            #
################################################################################

## Requirements ##

- Python3 interpreter (tested on Python 3.7.4, Windows OS)
- psutil package (can be installed using pip)

## How to run ##

- Run script puzzle.py using the Python interpreter:
    > python puzzle.py

- Input the initial state as a space-separated integer list:
    > Input initial state: 1 0 2 4 5 7 3 8 9 6 11 12 13 10 14 15

- If the initial state is solvable, then results are shown:
    > Moves: ['R', 'D', 'L', 'D', 'D', 'R', 'R']
    > Number of nodes expanded: 361
    > Time taken (seconds): 0.0246656
    > Memory used (bytes): 14831616

- If the initial state is not solvable, an error message is shown:
    > Solution not found.

## How it works ##

The solution for the assignment is based on the function bfs_search(), which 
implements a breadth-first search technique for the solution of the 15-puzzle. 
Nodes of the search tree are represented by the Node class, which includes the 
following fields:

- The path in the tree that leads to the node (we may store only the parent, 
but it is easier to retrieve the complete path when we get a solution);
- The state of the environment in that node, represented as a list of sixteen 
integer elements;
- The action that has been taken to reach that node;
- The depth of the node in the search tree;
- The cost of the path that reaches that node (in this case, it is equal to the 
depth: each move counts as a single increment in the path cost).

The search function takes as arguments the initial state of the puzzle, parsed 
from the command line using the parse_state() function, and the maximum amount 
of time for which the algorithm may run. It initializes a frontier list with a 
new node corresponding to the root of the search tree, having:

- As path, an empty list;
- As state, the initial state;
- As action, a null value;
- As depth, zero;
- As cost, zero.

After that, the function initializes a list of visited states, the counter of 
expanded nodes and the start time of the algorithm; then, it loops until the 
frontier is not empty and the difference between the start time and the current 
time is lower than the given limit. At each iteration:

- It pops the first node in the frontier;
- It checks whether the extracted node is a goal via the goal_test() function, 
which compares the state of the node with the expected one;
- If the node state is a goal, it returns the sequence of nodes that allow to 
reach the solution (stored in the path attribute of the Node class) appending 
to it the current node, the number of expansions and the time difference with 
the start of the algorithm;
- If the node state is not a goal, it proceeds to extend the frontier list by 
adding at the end the nodes generated from the expansion of the current node, 
which are obtained through the expand() function; finally, it inserts the node 
state into the visited list and increments the number of expanded nodes.

The expand() function receives as parameters a node and the list of visited 
states and returns a list of nodes that are reachable via the given node. Those 
are generated starting from the list of actions and of the corresponding final 
states that can be taken from the given node, computed via get_successors(). In 
particular, for each action, the function checks whether its associated final 
state has already been visited; if not, it appends to the successors list a new 
node, characterized by:

- A path that is the current node's path, plus the current node;
- A state that is the final state as computed by get_successors();
- An action that is a possible action as computed by get_successors();
- A depth that is the current node's depth, plus one;
- A cost that is the current node's cost, plus one.

The get_successors() function takes as parameter the current state and generates 
a list of all the possible actions that can be taken from it and the respective 
final states. It performs the following actions:

- It searches the row and column position of the 0 in the current state;
- It checks whether the empty spot is in the first column; if not, then it adds 
the "left" action to the possible ones and computes the respective final state;
- It checks whether the empty spot is in the first row; if not, then it adds 
the "up" action to the possible ones and computes the respective final state;
- It checks whether the empty spot is in the last column; if not, then it adds 
the "right" action to the possible ones and computes the respective final state;
- It checks whether the empty spot is in the last row; if not, then it adds the 
"down" action to the possible ones and computes the respective final state.