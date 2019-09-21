from time import time
from psutil import Process

class Node:
    def __init__(self, path, state, action, depth, cost):
        self.path = path
        self.state = state
        self.action = action
        self.depth = depth
        self.cost = cost

def parse_state(input_string):
    return [int(input_string.strip().split(" ")[i]) for i in range(16)]

def goal_test(node):
    return node.state[0:15] == sorted(node.state[0:15])

def bfs_search(initial_state, time_limit):
    # Initialize the frontier with the initial state
    frontier = [Node([], initial_state, None, 0, 0)]

    # Initialize an empty list of visited states
    visited = []

    # Initialize additional parameters
    start_time = time()
    expansions = 0

    while time() - start_time < time_limit:
        # If the frontier is empty, then we have no solution
        if len(frontier) == 0:
            return False, False, False
        
        # Get a node from the front
        node = frontier.pop(0)

        # Check if the goal has been reached
        if goal_test(node):
            return node, time() - start_time, expansions
        
        # Otherwise, expand the node and add all to the frontier
        frontier.extend(expand(node, visited))

        # Mark the current state as already visited
        visited.append(node.state)

        # Increment number of expanded nodes
        expansions = expansions + 1
    
    return False, False, False

def expand(node, visited):
    # Initialize empty successors list
    successors = []

    # Compute possible actions and states
    actions, states = successor_function(node.state)

    for i in range(len(actions)):
        # If the state has already been visited, discard
        if any([states[i] == other for other in visited]):
            continue

        # Otherwise, create new node
        successors.append(Node(node.path + [node], states[i], actions[i], node.depth + 1, node.cost + 1))

    return successors

def successor_function(state):
    actions = []
    states = []
    
    # Identify the position of 0
    for i in range(16):
        if state[i] == 0:
            row = i // 4
            col = i % 4
            break
    
    # Not in the first col, we can do L
    if col != 0:
        actions.append("L")
        new_state = list(state)

        # Move left one col
        new_state[row * 4 + col] = new_state[row * 4 + col - 1]
        new_state[row * 4 + col - 1] = 0

        states.append(new_state)
    
    # Not in the first row, we can do U
    if row != 0:
        actions.append("U")
        new_state = list(state)

        # Move down one row
        new_state[row * 4 + col] = new_state[(row - 1) * 4 + col]
        new_state[(row - 1) * 4 + col] = 0

        states.append(new_state)
    
    # Not in the last col, we can do R
    if col != 3:
        actions.append("R")
        new_state = list(state)

        # Move right one col
        new_state[row * 4 + col] = new_state[row * 4 + col + 1]
        new_state[row * 4 + col + 1] = 0

        states.append(new_state)
    
    # Not in the last row, we can do D
    if row != 3:
        actions.append("D")
        new_state = list(state)

        # Move down one row
        new_state[row * 4 + col] = new_state[(row + 1) * 4 + col]
        new_state[(row + 1) * 4 + col] = 0

        states.append(new_state)

    return actions, states

# Ask the user for the initial state
initial_state = parse_state(input("Input initial state: "))

# Run the algorithm
node, elap_time, expansions = bfs_search(initial_state, 30)

# Print results
if node != False:
    print("Moves: {}".format([n.action for n in node.path[1:] + [node]]))
    print("Number of nodes expanded: {}".format(expansions))
    print("Time taken (seconds): {}".format(elap_time))
    print("Memory used (bytes): {}".format(Process().memory_info().rss))
else:
    print("Solution not found.")