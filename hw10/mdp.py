import sys
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
        if action == "up" and state[1] + 1 < self.size[1]:
            return (state[0], state[1] + 1)
        elif action == "down" and state[1] - 1 >= 0:
            return (state[0], state[1] - 1)
        elif action == "left" and state[0] - 1 >= 0:
            return (state[0] - 1, state[1])
        elif action == "right" and state[0] + 1 < self.size[0]:
            return (state[0] + 1, state[1])
        else:
            return state
    
    def value_iteration(self):
        U = {}
        Up = {}
        delta = 100
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
    
        return models

    def policy_iteration(self):
        pass

def plot_iter(models, states):
    plt.figure()

    for s in states:
        plt.plot([models[i][s] for i in range(len(models))])
    
    plt.grid()
    plt.title("Value iteration curves")
    plt.legend(states)
    plt.show()

if __name__ == "__main__":
    mdp = MDP.from_file(sys.argv[1])
    models = mdp.value_iteration()
    
    plot_iter(models, [(0,0), (2,2), (3,3)])