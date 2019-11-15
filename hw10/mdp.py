from math import inf
from sys import argv

import matplotlib.pyplot as plt

class Square:
    def __init__(self, category, reward):
        self.category = category
        self.reward = reward
    
    def __repr__(self):
        return f"{self.category} ({self.reward})"

class MDP:
    def __init__(self, size, walls, terms, reward, tprobs, gamma, epsilon):
        self.size = size
        self.gamma = gamma
        self.epsilon = epsilon

        # Create board
        self.board = {}
        for i in range(size[0]):
            for j in range(size[1]):
                # Check if cell is a wall
                if (i, j) in walls:
                    self.board[(i, j)] = Square("wall", 0)
                
                # Check if cell is a terminal state
                elif (i, j) in terms:
                    self.board[(i, j)] = Square("terminal", terms[(i, j)])
                
                # Cell is a regular state
                else:
                    self.board[(i, j)] = Square("regular", reward)
        
        # Create transition model
        self.tmodel = {
            "up": {"up": tprobs[0], "down": tprobs[3], "left": tprobs[1], "right": tprobs[2]},
            "down": {"up": tprobs[3], "down": tprobs[0], "left": tprobs[2], "right": tprobs[1]},
            "left": {"up": tprobs[2], "down": tprobs[1], "left": tprobs[0], "right": tprobs[3]},
            "right": {"up": tprobs[1], "down": tprobs[2], "left": tprobs[3], "right": tprobs[0]}
        }

    @classmethod
    def from_file(cls, filename):
        try:
            with open(filename) as f:
                for line in f:
                    # Skip comment lines
                    if line[0] == "#":
                        continue

                    # Split the line on :
                    tokens = line.split(":")

                    # Parse size
                    if tokens[0].strip() == "size":
                        size = (int(tokens[1].strip().split(" ")[0]), int(tokens[1].strip().split(" ")[1]))
                    
                    # Parse walls
                    elif tokens[0].strip() == "walls":
                        walls = []
                        for wall in tokens[1].strip().split(","):
                            walls.append((int(wall.strip().split(" ")[0]) - 1, int(wall.strip().split(" ")[1]) - 1))
                    
                    # Parse terminal states
                    elif tokens[0].strip() == "terminal_states":
                        terminal_states = {}
                        for ts in tokens[1].strip().split(","):
                            terminal_states[(int(ts.strip().split(" ")[0]) - 1, int(ts.strip().split(" ")[1]) - 1)] = float(ts.strip().split(" ")[2])
                    
                    # Parse reward
                    elif tokens[0].strip() == "reward":
                        reward = float(tokens[1].strip())
                    
                    # Parse transition probabilities
                    elif tokens[0].strip() == "transition_probabilities":
                        transition_probabilities = (
                            float(tokens[1].strip().split(" ")[0]), float(tokens[1].strip().split(" ")[1]),
                            float(tokens[1].strip().split(" ")[2]), float(tokens[1].strip().split(" ")[3])
                        )
                    
                    # Parse discount rate
                    elif tokens[0].strip() == "discount_rate":
                        discount_rate = float(tokens[1].strip())
                    
                    # Parse epsilon
                    elif tokens[0].strip() == "epsilon":
                        epsilon = float(tokens[1].strip())

            return cls(size, walls, terminal_states, reward, transition_probabilities, discount_rate, epsilon)
        except Exception:
            return None
    
    def move(self, state, action):
        if action == "up" and state[1] + 1 < self.size[1] and self.board[(state[0], state[1] + 1)].category != "wall":
            return (state[0], state[1] + 1)
        elif action == "down" and state[1] - 1 >= 0 and self.board[(state[0], state[1] - 1)].category != "wall":
            return (state[0], state[1] - 1)
        elif action == "left" and state[0] - 1 >= 0 and self.board[(state[0] - 1, state[1])].category != "wall":
            return (state[0] - 1, state[1])
        elif action == "right" and state[0] + 1 < self.size[0] and self.board[(state[0] + 1, state[1])].category != "wall":
            return (state[0] + 1, state[1])
        else:
            return state
    
    def value_iteration(self):
        U = {}
        Up = {}
        delta = inf
        models = []

        # Initialize dictionaries
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                U[(i, j)] = 0
                Up[(i, j)] = 0

        # Start value iteration loop
        while delta > self.epsilon * (1 - self.gamma) / self.gamma:
            U = dict(Up)
            delta = 0

            for s in self.board:
                # Check if s is a wall state
                if self.board[s].category == "wall":
                    Up[s] = 0
                
                # Check if s is a terminal state
                elif self.board[s].category == "terminal":
                    Up[s] = self.board[s].reward
                
                # Compute U'[s] for regular states
                else:
                    Up[s] = self.board[s].reward + self.gamma * max([
                        sum([self.tmodel[a][ap] * U[self.move(s, ap)] for ap in ["up", "down", "left", "right"]])
                        for a in ["up", "down", "left", "right"]
                    ])

                # Update delta
                if abs(Up[s] - U[s]) > delta:
                    delta = abs(Up[s] - U[s])

            # Append returned model
            models.append(dict(Up))
        
        # Define the actual policy
        policy = {}
        for s in Up:
            # Exclude if terminal or wall state
            if self.board[s].category != "regular":
                continue

            # Search for the best action for each state
            best_act, best_val = None, 0
            for a in ["up", "down", "left", "right"]:
                v = sum([self.tmodel[a][ap] * Up[self.move(s, ap)] for ap in ["up", "down", "left", "right"]])
                if v > best_val:
                    best_act = a
                    best_val = v

            # Add the best action to the policy
            policy[s] = best_act
    
        return policy, models

    def policy_iteration(self):
        pass

    def plot(self, policy, models, states):
        # Plot value iteration curves
        plt.figure()
        for s in states:
            plt.plot([models[i][s] for i in range(len(models))])
        
        # Show grid, title and legend
        plt.grid()
        plt.title("Value iteration curves")
        plt.legend(states)

        # Plot board (adequately adjusting indices)
        plt.figure()
        plt.imshow([[models[-1][(j, self.size[1] - 1 - i)] for j in range(self.size[0])] for i in range(self.size[1])])
        
        # Add annotations to the states
        for i in range(self.size[1]):
            for j in range(self.size[0]):
                # Regular state, print value and policy
                if self.board[(j, self.size[1] - 1 - i)].category == "regular":
                    plt.text(j, i, f"{round(models[-1][(j, self.size[1] - 1 - i)], 4)}\n{policy[(j, self.size[1] - 1 - i)]}", ha="center", va="center", color="w")
                
                # Terminal state, print value
                elif self.board[(j, self.size[1] - 1 - i)].category == "terminal":
                    plt.text(j, i, f"{round(models[-1][(j, self.size[1] - 1 - i)], 4)}\nterminal", ha="center", va="center", color="w")
                
                # Wall state
                elif self.board[(j, self.size[1] - 1 - i)].category == "wall":
                    plt.text(j, i, "wall", ha="center", va="center", color="w")

        # Adjust axes and show title
        plt.yticks(range(self.size[1]), reversed(range(1, self.size[1] + 1)))
        plt.xticks(range(self.size[0]), range(1, self.size[0] + 1))
        plt.axis([-0.5, self.size[0] - 0.5, self.size[1] - 0.5, -0.5])
        plt.title("Value iteration optimal policy")

        # Show plots
        plt.show()

if __name__ == "__main__":
    # Create the MDP
    mdp = MDP.from_file(argv[1])

    # Compute the policy through value iteration
    policy, models = mdp.value_iteration()

    # Parse states to print value iteration curves
    states = []
    for i in range(2, len(argv)):
        states.append((int(argv[i].split(",")[0]) - 1, int(argv[i].split(",")[1]) - 1))

    # Plot the results
    mdp.plot(policy, models, states)