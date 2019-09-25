from time import time
from psutil import Process

class Node:
    def __init__(self, path, state, action, depth, cost):
        self.path = path
        self.state = state
        self.action = action
        self.depth = depth
        self.cost = cost

class Puzzle:
    def __init__(self, size, initial_state, time_limit):
        self.size = size
        self.initial_state = initial_state
        self.time_limit = time_limit
    
    @classmethod
    def from_console(cls):
        try:
            size = int(input("Input puzzle dimension: "))
            input_string = input("Input initial state: ")
            initial_state = [int(input_string.strip().split(" ")[i]) for i in range(16)]
            time_limit = float(input("Input time limit: "))
            return cls(size, initial_state, time_limit)
        except Exception:
            print("Invalid input.")
            return False

    def solve_bfs(self):
        # Initialize parameters
        expansions = 0
        start_time = time()
        start_mem = Process().memory_info().rss

        # Initialize the frontier with the initial state
        frontier = [Node([], self.initial_state, None, 0, 0)]

        # Initialize an empty list of visited states
        visited = []

        while len(frontier) > 0 and time() - start_time < self.time_limit:
            # Get a node from the front
            node = frontier.pop(0)

            # Check if the goal has been reached
            if self.goal_test(node):
                return node.path[1:] + [node], expansions, time() - start_time, Process().memory_info().rss - start_mem
            
            if not any([node.state == other for other in visited]):
                # Mark the current state as already visited
                visited.append(node.state)

                # Otherwise, expand the node and add all to the frontier
                frontier.extend(self.expand(node))

                # Increment number of expanded nodes
                expansions = expansions + 1
        
        return False, False, False, False

    def goal_test(self, node):
        return node.state == list(range(1, self.size ** 2)) + [0]

    def expand(self, node):
        # Compute possible actions and states
        actions, states = self.get_successors(node.state)

        # Create new nodes
        successors = [Node(node.path + [node], states[i], actions[i], node.depth + 1, node.cost + 1) for i in range(len(actions))]

        return successors

    def get_successors(self, state):
        actions = []
        states = []
        
        # Identify the position of 0
        for i in range(self.size ** 2):
            if state[i] == 0:
                row = i // self.size
                col = i % self.size
                break
        
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

# Instantiate solver
puzzle = Puzzle.from_console()

# Run the solver
path, expansions, elap_time, delta_mem = puzzle.solve_bfs()

# Print results
if path != False:
    print("Moves: {}".format([n.action for n in path]))
    print("Number of nodes expanded: {}".format(expansions))
    print("Time taken (seconds): {:.6}".format(elap_time))
    print("Memory used (bytes): {}".format(delta_mem))
else:
    print("Solution not found.")