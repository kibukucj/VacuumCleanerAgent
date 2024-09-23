import random
from gui import VacuumCleanerGUI

# Environment class
class Environment:
    def __init__(self, size=10, dirt_probability=0.01, seed=1):
        self.size = size
        self.grid = [[{'is_wall': False, 'dirt': 0} for _ in range(size)] for _ in range(size)]
        self.dirt_probability = dirt_probability
        random.seed(seed)
        self.place_walls()

    def place_walls(self):
        for i in range(self.size):
            self.grid[0][i]['is_wall'] = True
            self.grid[self.size-1][i]['is_wall'] = True
            self.grid[i][0]['is_wall'] = True
            self.grid[i][self.size-1]['is_wall'] = True

    def increase_dirt(self):
        for row in self.grid:
            for cell in row:
                if not cell['is_wall']:
                    if random.random() < self.dirt_probability:
                        cell['dirt'] += 1

    def print_environment(self):
        for row in self.grid:
            print(' '.join(['#' if cell['is_wall'] else str(cell['dirt']) for cell in row]))

# Agent class
class Agent:
    def __init__(self, environment):
        self.env = environment
        self.x = 1  # Initial position
        self.y = 1
        self.energy = 100

    def perceive(self):
        return self.env.grid[self.x][self.y]['dirt'], self.env.grid[self.x][self.y]['is_wall']

    def move(self, direction):
        if direction == "north" and not self.env.grid[self.x - 1][self.y]['is_wall']:
            self.x -= 1
        elif direction == "south" and not self.env.grid[self.x + 1][self.y]['is_wall']:
            self.x += 1
        elif direction == "east" and not self.env.grid[self.x][self.y + 1]['is_wall']:
            self.y += 1
        elif direction == "west" and not self.env.grid[self.x][self.y - 1]['is_wall']:
            self.y -= 1
        self.energy -= 1

    def suck(self):
        if self.env.grid[self.x][self.y]['dirt'] > 0:
            self.env.grid[self.x][self.y]['dirt'] -= 1
            self.energy -= 2

    def idle(self):
        pass

class Evaluator:
    def __init__(self, environment, agent):
        self.env = environment
        self.agent = agent

    def evaluate_performance(self):
        total_dirt = sum(cell['dirt'] for row in self.env.grid for cell in row if not cell['is_wall'])
        print(f"Total dirt left: {total_dirt}, Energy remaining: {self.agent.energy}")
        return total_dirt, self.agent.energy

# Main function to run the simulation
if __name__ == "__main__":
    env = Environment()
    agent = Agent(env)
    gui = VacuumCleanerGUI(env, agent)

