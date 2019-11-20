################################################################################
#                                  Homework 10                                 #
#                CS 411 - Artificial Intelligence I - Fall 2019                #
#                           Matteo Corain 650088272                            #
################################################################################

## Requirements ##

- Python3 interpreter (tested on Python 3.8.0, Windows OS)
- matplotlib package (for drawing graphs, can be installed using pip)

## How to run ##

Run script mdp.py using the Python interpreter:
    > python mdp.py [mdp_input_file] [mode] [states]

Options:
    - mdp_input_file: path to the file containing the MDP description. Input 
      files have to be structured as the given ones.
    - mode: either -v (value iteration) or -p (policy iteration).
    - states: list of states (space-separated) whose value curves should be 
      plotted, in the x,y format (e.g. 1,1).

## How it works ##

The Markov decision problem is represented by means of the MDP class, whose 
constructor takes as arguments:

- The size of the game board, as a tuple (sizeX, sizeY);
- The locations of walls, as a list of tuples [(x, y)];
- The locations of terminal states, as a dictionary {(x, y) -> value};
- The reward for non-terminal states;
- The transition probabilities, as a list [probabilities of going straight, 
  slipping left, right, and back];
- The discount rate gamma;
- The tolerance value epsilon.

These parameters are used to construct two internal data structures, namely:

- board: it is a dictionary that maps each location (x, y) to a Square object; 
  those are characterized by the type of the considered cell (either "wall", 
  "terminal" or "regular") and by their associated reward (for wall states, 
  this is conventionally set to zero);
- tmodel: it is a dictionary that maps each action ("up", "down", "left", 
  "right") on a sub-dictionary, mapping each possible outcome of the selected 
  action on its probability.

Input parameters can be are parsed from a file structured similar to the given 
examples by means of the static method from_file() of the MDP class, which 
takes as parameter the name of the file that contains the description of the 
problem to be considered.

The value iteration procedure is implemented in the value_iteration() method of 
the MDP class. This performs the following actions:

- It initializes the U' dictionary by setting the initial value of each square 
  to its associated reward for terminal states and to 0 for others;
- It copies the value dictionary U' computed at the previous iteration on the 
  previous value dictionary U and resets the value of delta;
- It starts the value iteration loop, which terminates when the value of delta 
  (initially infinite) falls below the threshold defined by epsilon;
- For each regular state, it updates its value by means of the value iteration 
  formula, consequently updating the value of delta;
- It pushes the obtained model U' into the models list and prints it to console;
- When the value iteration loops terminates, it uses the last computed model to
  define the actual policy, by selecting for each regular state the action that 
  yields the best expected value;
- Finally, it prints and returns the overall policy, in addition to the list of 
  models computed for each iteration.

The policy iteration algorithm is instead implemented in the policy_iteration() 
method of the MDP class. This performs the following actions:

- It initializes the U' dictionary, contextually defining an initial random 
  policy for each regular state (by means of the choice function of Python's 
  random library);
- It starts the policy iteration loop, which terminates when the boolean flag 
  unchanged becomes True (there is no change in the policy in two subsequent 
  iterations of the loop);
- It iteratively evaluates the policy by running a loop similar to the value 
  iteration one, in which the value is computed based on the result of the 
  defined policy (i.e. there is no max operator);
- It updates the policy by checking, for each state, if there exists an action 
  that yields an expected value that is greater than the expected value of the 
  action currently in the policy; if that is the case, unchanged flag becomes 
  False (policy has changed in this iteration);
- It stores the computed model into the models list and prints the policy as 
  computed at the end of each iteration;
- Finally, it returns the overall policy and the list of models computed for 
  each iteration.

For better visualization, the results of both the methods can be passed to the 
plot() method offered by the MDP class, which takes as an additional argument 
a list of states for which we want to show the corresponding value curve (in 
this case, they are parsed from the command line). This performs the following 
actions:

- If the given states list is not empty, it creates a new Matplotlib figure and 
  plots, for each of the given states, the corresponding value curve by listing 
  all the values of the considered state in the successive iterations;
- It creates a second Matplotlib figure, in which the imshow() method offered 
  by the library is exploited to plot a grid of cells, whose color depends on 
  the value of the considered location in the final model; the input matrix for 
  this method is created starting from the last dictionary in the models list, 
  by opportunely adapting the x and y indices where necessary; cells are also 
  labeled with their value and the associated policy action.