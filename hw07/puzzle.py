from math import inf
from time import time
from psutil import Process

class Node:
    def __init__(self, path, state, action, depth, cost, hval):
        self.path = path
        self.state = state
        self.action = action
        self.depth = depth
        self.cost = cost
        self.hval = hval

    def __lt__(self, other):
        return (self.cost + self.hval) < (other.cost + other.hval)

class Puzzle:
    def __init__(self, size, initial_state, time_limit, heuristic):
        self.size = size
        self.initial_state = initial_state
        self.time_limit = time_limit
        self.heuristic = heuristic
        self.solution = list(range(1, self.size ** 2)) + [0]
    
    @classmethod
    def from_console(cls):
        try:
            size = int(input("Input puzzle dimension: "))
            input_string = input("Input initial state: ")
            initial_state = [int(input_string.strip().split(" ")[i]) for i in range(size ** 2)]
            time_limit = float(input("Input time limit: "))
            heuristic = int(input("Heuristic to use (1/2)? "))
            return cls(size, initial_state, time_limit, heuristic)
        except Exception:
            print("Invalid input.")
    
    def h1(self, state):
        return sum([1 if state[i] != self.solution[i] else 0 for i in range(self.size ** 2)])

    def h2(self, state):
        h = 0

        for i in range(self.size ** 2):
            row, col = state.index(i) // self.size, state.index(i) % self.size
            exp_row, exp_col = self.solution.index(i) // self.size, self.solution.index(i) % self.size
            h = h + abs(row - exp_row) + abs(col - exp_col)
        return h

    def solve_ida(self):
        # Initialize parameters
        limit = self.h1(self.initial_state) if self.heuristic == 1 else self.h2(self.initial_state)
        result = False
        expansions = 0
        start_time = time()
        start_mem = Process().memory_info().rss

        while time() - start_time < self.time_limit:
            # Run a depth-limited A* search
            result, partial_exp, limit = self.solve_dla(limit, start_time)
            
            # Update number of expansions
            expansions = expansions + partial_exp

            # Check results
            if result != False:
                return result, expansions, time() - start_time, Process().memory_info().rss - start_mem

        return False, False, False, False

    def solve_dla(self, f_limit, start_time):
        # Initialize parameters
        expansions = 0
        next_limit = inf

        # Initialize the frontier with the initial state
        frontier = [Node([], self.initial_state, None, 0, 0, 
            self.h1(self.initial_state) if self.heuristic == 1 else self.h2(self.initial_state))]

        # Initialize an empty list of visited states
        visited = []

        while len(frontier) > 0 and time() - start_time < self.time_limit:
            # Get a node from the front
            node = frontier.pop(0)

            # Check if the goal has been reached
            if self.goal_test(node):
                return node.path[1:] + [node], expansions, next_limit
            
            # Check if the f-value exceeds the cutoff
            if node.cost + node.hval > f_limit:
                # Update the next limit (smallest of the f-values exceeding cutoff)
                next_limit = min(next_limit, node.cost + node.hval)
            
            # Otherwise, check that the state has not already been visited
            elif not any([node.state == other for other in visited]):
                # Mark the current state as already visited
                visited.append(node.state)

                # Increment number of expanded nodes
                expansions = expansions + 1

                # Otherwise, expand the node and add all to the frontier (depth-first)
                frontier = self.expand(node) + frontier
        
        return False, expansions, next_limit
    
    def goal_test(self, node):
        # Check if it is a list of ordered integers, terminated by 0
        return node.state == self.solution

    def expand(self, node):
        # Compute possible actions and states
        actions, states = self.get_successors(node.state)

        # Create successor nodes
        successors = [Node(node.path + [node], states[i], actions[i], node.depth + 1, node.cost + 1,
            self.h1(states[i]) if self.heuristic == 1 else self.h2(states[i])) for i in range(len(actions))]

        return successors

    def get_successors(self, state):
        actions = []
        states = []
        
        # Identify the position of 0
        row, col = state.index(0) // self.size, state.index(0) % self.size
        
        # Not in the first col, we can do L
        if col != 0:
            actions.append("L")
            new_state = list(state)

            # Move left one col
            new_state[row * self.size + col] = new_state[row * self.size + col - 1]
            new_state[row * self.size + col - 1] = 0

            states.append(new_state)
        
        # Not in the first row, we can do U
        if row != 0:
            actions.append("U")
            new_state = list(state)

            # Move down one row
            new_state[row * self.size + col] = new_state[(row - 1) * self.size + col]
            new_state[(row - 1) * self.size + col] = 0

            states.append(new_state)
        
        # Not in the last col, we can do R
        if col != self.size - 1:
            actions.append("R")
            new_state = list(state)

            # Move right one col
            new_state[row * self.size + col] = new_state[row * self.size + col + 1]
            new_state[row * self.size + col + 1] = 0

            states.append(new_state)
        
        # Not in the last row, we can do D
        if row != self.size - 1:
            actions.append("D")
            new_state = list(state)

            # Move down one row
            new_state[row * self.size + col] = new_state[(row + 1) * self.size + col]
            new_state[(row + 1) * self.size + col] = 0

            states.append(new_state)

        return actions, states

if __name__ == "__main__":
    # Instantiate solver
    puzzle = Puzzle.from_console()
    if puzzle is None:
        exit()

    # Run the solver
    path, expansions, elap_time, delta_mem = puzzle.solve_ida()

    # Print results
    if path != False:
        print("Moves: {}".format([n.action for n in path]))
        print("Number of nodes expanded: {}".format(expansions))
        print("Time taken (seconds): {:.6}".format(elap_time))
        print("Memory used (bytes): {}".format(delta_mem))
    else:
        print("Solution not found.")