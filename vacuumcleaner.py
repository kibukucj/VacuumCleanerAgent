import random

# Environment class
class Environment:
    def __init__(self, size=10, dirt_probability=0.01, seed=1):
        self.size = size
        self.grid = [[{'is_wall': False, 'dirt': 0} for _ in range(size)] for _ in range(size)]
        self.dirt_probability = dirt_probability
        random.seed(seed)
        self.place_walls()

"""Explanation of the __init__ function:
        size=10: This defines the environment as a 10x10 grid (you can adjust the size).
        dirt_probability=0.01: Each room has a 1% chance of accumulating 1 unit of dirt in each time step.
        grid: A 2D list (10x10) where each cell has two properties:
        is_wall: Boolean to indicate if the cell is a wall.
        dirt: How much dirt is in the cell (starting at 0).
        place_walls(): Places walls around the grid’s borders (the outer edges).
"""

    def place_walls(self):
        for i in range(self.size):
            self.grid[0][i]['is_wall'] = True
            self.grid[self.size-1][i]['is_wall'] = True
            self.grid[i][0]['is_wall'] = True
            self.grid[i][self.size-1]['is_wall'] = True

"""Explanation of place_walls:
        This method surrounds the grid with walls (outermost rows and columns) by setting is_wall = True for the boundary cells.
        For example, if the environment is 10x10, this method marks the cells at the first and last row and column as walls.
"""

    def increase_dirt(self):
        for row in self.grid:
            for cell in row:
                if not cell['is_wall']:
                    if random.random() < self.dirt_probability:
                        cell['dirt'] += 1

    def print_environment(self):
        for row in self.grid:
            print(' '.join(['#' if cell['is_wall'] else str(cell['dirt']) for cell in row]))

"""Explanation of increase_dirt():
        This method iterates over the grid and, for each non-wall room, adds dirt with a 1% probability (based on dirt_probability).
        It uses random.random() to generate a random number between 0 and 1, and if this number is less than 0.01, it increases the dirt in that room.
"""

# Agent class
class Agent:
    def __init__(self, environment):
        self.env = environment
        self.x = 1  # Initial position
        self.y = 1
        self.energy = 100

"""Explanation of __init__():
        self.env: The agent interacts with the environment.
        self.x and self.y: These represent the agent's current position on the grid. It starts at position (1, 1) (just inside the top-left corner).
        self.energy: The agent has an initial energy of 100. It uses energy to move and clean.
"""

    def perceive(self):
        return self.env.grid[self.x][self.y]['dirt'], self.env.grid[self.x][self.y]['is_wall']

""" Explanation of perceive():
        This function allows the agent to sense its current environment.
        It returns two things:
        The amount of dirt in the current room (self.env.grid[self.x][self.y]['dirt']).
        Whether the current position is a wall (self.env.grid[self.x][self.y]['is_wall']).
"""

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

"""Explanation of move():
        The agent can move in four directions (north, south, east, west).
        Before moving, it checks if there is a wall in that direction.
        Each move costs 1 unit of energy (self.energy -= 1).
"""

    def suck(self):
        if self.env.grid[self.x][self.y]['dirt'] > 0:
            self.env.grid[self.x][self.y]['dirt'] -= 1
            self.energy -= 2

"""Explanation of suck():
        This method allows the agent to clean the room it’s in.
        If the room has dirt, it decreases the dirt by 1 and reduces the agent’s energy by 2 (self.energy -= 2).
"""

    def idle(self):
        pass

"""Explanation of idle():
        This method does nothing (the agent stays idle).
        Idle doesn't consume any energy.
"""

# Evaluator class
class Evaluator:
    def __init__(self, environment, agent, time_steps):
        self.env = environment
        self.agent = agent
        self.time_steps = time_steps

"""Explanation of __init__():
        self.env: This is the environment where the agent operates.
        self.agent: This is the agent that we are evaluating.
        self.time_steps: The number of time steps (or rounds) in the simulation.
"""

    def run_simulation(self):
        for _ in range(self.time_steps):
            dirt, is_wall = self.agent.perceive()

            if dirt > 0:
                self.agent.suck()
            else:
                self.agent.move(random.choice(["north", "south", "east", "west"]))

            self.env.increase_dirt()
            self.env.print_environment()
            print(f"Agent's position: ({self.agent.x}, {self.agent.y}), Energy: {self.agent.energy}")

"""Explanation of run_simulation():
        This is the main simulation loop that runs for a given number of time steps.
        For each time step:
        The agent perceives its environment (dirt and walls).
        If there’s dirt in the current room, it sucks.
        Otherwise, it randomly moves in one of four directions.
        The environment increases dirt probabilistically in all rooms (increase_dirt()).
        The environment is printed after each time step along with the agent's position and remaining energy.
"""

    def evaluate_performance(self):
        total_dirt = sum(cell['dirt'] for row in self.env.grid for cell in row if not cell['is_wall'])
        print(f"Total dirt left: {total_dirt}, Energy remaining: {self.agent.energy}")

"""Explanation of evaluate_performance():
        After the simulation, this method evaluates the agent’s performance.
        It calculates the total dirt left in all rooms and the remaining energy of the agent, which are the two key performance measures.
"""

# Main function to run the simulation
if __name__ == "__main__":
    env = Environment()
    agent = Agent(env)
    evaluator = Evaluator(env, agent, time_steps=10)

    evaluator.run_simulation()
    evaluator.evaluate_performance()

"""
        env = Environment(): Creates the environment (10x10 grid).
        agent = Agent(env): Initializes the agent in the environment.
        evaluator = Evaluator(env, agent, time_steps=10): Sets up the simulation for 10 time steps.
        evaluator.run_simulation(): Runs the agent's actions in the environment.
        evaluator.evaluate_performance(): Outputs the final performance of the agent (total dirt and energy remaining).
"""
