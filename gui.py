import tkinter as tk
import random
from tkinter import messagebox 

class VacuumCleanerGUI:

    def __init__(self, environment, agent):
        self.env = environment
        self.agent = agent
        self.size = environment.size

        self.root = tk.Tk()
        self.root.title("Vacuum Cleaner World")
        self.canvas = tk.Canvas(self.root, width=self.size * 50, height=self.size * 50)
        self.canvas.pack()

        self.time_steps = 10
        self.update_interval = 500  
        self.rectangles = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.evaluator = Evaluator(environment, agent)  # Initialize the Evaluator

        self.draw_environment()
        self.run_simulation()

        self.root.mainloop()

    def draw_environment(self):
        """Draws the initial environment on the canvas."""
        for i in range(self.size):
            for j in range(self.size):
                x1, y1 = i * 50, j * 50
                x2, y2 = x1 + 50, y1 + 50
                if self.env.grid[i][j]['is_wall']:
                    color = 'black'
                else:
                    color = 'white'
                self.rectangles[i][j] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def update_environment(self):
        """Updates the environment after each action of the agent."""
        for i in range(self.size):
            for j in range(self.size):
                if self.env.grid[i][j]['is_wall']:
                    color = 'black'
                elif self.agent.x == i and self.agent.y == j:
                    color = 'blue'  # Agent's position
                elif self.env.grid[i][j]['dirt'] > 0:
                    color = 'brown'  # Dirt
                else:
                    color = 'white'  # Clean space
                self.canvas.itemconfig(self.rectangles[i][j], fill=color)

    def run_simulation(self):
        """Runs the simulation step by step."""
        if self.agent.energy > 0 and self.time_steps > 0:
            dirt, is_wall = self.agent.perceive()

            if dirt > 0:
                self.agent.suck()
            else:
                self.agent.move(random.choice(["north", "south", "east", "west"]))

            self.env.increase_dirt()
            self.update_environment()

            self.time_steps -= 1
            self.root.after(self.update_interval, self.run_simulation)
        else:
            self.end_simulation()
        
    def end_simulation(self):
        """End of simulation, evaluate performance and show results."""
        total_dirt, remaining_energy = self.evaluator.evaluate_performance()  # Get the evaluation
        messagebox.showinfo("Simulation Complete",
                            f"Total dirt left: {total_dirt}\nRemaining energy: {remaining_energy}")
        
# Evaluator class
class Evaluator:
    def __init__(self, environment, agent):
        self.env = environment
        self.agent = agent

    def evaluate_performance(self):
        """Calculates the total dirt left and remaining energy after the simulation."""
        total_dirt = sum(cell['dirt'] for row in self.env.grid for cell in row if not cell['is_wall'])
        remaining_energy = self.agent.energy
        return total_dirt, remaining_energy