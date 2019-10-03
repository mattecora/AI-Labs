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
    def __init__(self, size, initial_state, time_limit, use_recursion):
        self.size = size
        self.initial_state = initial_state
        self.time_limit = time_limit
        self.use_recursion = use_recursion
    
    @classmethod
    def from_console(cls):
        try:
            size = int(input("Input puzzle dimension: "))
            input_string = input("Input initial state: ")
            initial_state = [int(input_string.strip().split(" ")[i]) for i in range(size ** 2)]
            time_limit = float(input("Input time limit: "))
            use_recursion = input("Use recursion (Y/n)? ") != 'n'
            return cls(size, initial_state, time_limit, use_recursion)
        except Exception:
            print("Invalid input.")
    
    def solve_ids(self):
        # Initialize parameters
        limit = 0
        result = False
        expansions = 0
        start_time = time()
        start_mem = Process().memory_info().rss

        while time() - start_time < self.time_limit:
            # Run a depth-limited search
            if self.use_recursion:
                result, partial_exp = self.solve_dls_rec(Node([], self.initial_state, None, 0, 0), 0, limit, [])
            else:
                result, partial_exp = self.solve_dls_iter(limit)
            
            # Update number of expansions
            expansions = expansions + partial_exp

            # Check results
            if result != False:
                return result, expansions, time() - start_time, Process().memory_info().rss - start_mem
            
            # Increase the depth limit
            limit = limit + 1

        return False, False, False, False
    
    def solve_dls_rec(self, node, expansions, depth_limit, visited):
        # Check goal fulfillment
        if self.goal_test(node):
            return node.path[1:] + [node], expansions
        
        # Check maximum depth
        if node.depth >= depth_limit:
            return False, expansions
        
        # Check if not already visited
        if any([node.state == other for other in visited]):
            return False, expansions
        
        # Mark the current state as already visited
        visited.append(node.state)

        # Increment number of expanded nodes
        expansions = expansions + 1

        # Loop through possible states
        for successor in self.expand(node):
            result, expansions = self.solve_dls_rec(successor, expansions, depth_limit, visited)
            if result != False:
                return result, expansions
        
        return False, expansions
    
    def solve_dls_iter(self, depth_limit):
        # Initialize parameters
        expansions = 0

        # Initialize the frontier with the initial state
        frontier = [Node([], self.initial_state, None, 0, 0)]

        # Initialize an empty list of visited states
        visited = []

        while len(frontier) > 0:
            # Get a node from the front
            node = frontier.pop(0)

            # Check if the goal has been reached
            if self.goal_test(node):
                return node.path[1:] + [node], expansions
            
            # Check that the state has not already been visited
            if not any([node.state == other for other in visited]) and node.depth < depth_limit:
                # Mark the current state as already visited
                visited.append(node.state)

                # Increment number of expanded nodes
                expansions = expansions + 1

                # Otherwise, expand the node and add all to the frontier
                frontier = self.expand(node) + frontier
        
        return False, expansions
    
    def goal_test(self, node):
        # Check if it is a list of ordered integers, terminated by 0
        return node.state == list(range(1, self.size ** 2)) + [0]

    def expand(self, node):
        # Compute possible actions and states
        actions, states = self.get_successors(node.state)

        # Create successor nodes
        successors = [Node(node.path + [node], states[i], actions[i], node.depth + 1, node.cost + 1) for i in range(len(actions))]

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
    path, expansions, elap_time, delta_mem = puzzle.solve_ids()

    # Print results
    if path != False:
        print("Moves: {}".format([n.action for n in path]))
        print("Number of nodes expanded: {}".format(expansions))
        print("Time taken (seconds): {:.6}".format(elap_time))
        print("Memory used (bytes): {}".format(delta_mem))
    else:
        print("Solution not found.")