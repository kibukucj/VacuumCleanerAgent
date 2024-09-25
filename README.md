# Vacuum Cleaner World Simulation

## Project Overview

This project simulates how a vacuum cleaner (the "agent") operates in a 10x10 grid environment. The primary goal of the agent is to clean dirt from rooms while conserving as much energy as possible. The simulation introduces several challenges, such as random accumulation of dirt and walls that the agent must avoid. The agent is evaluated based on how efficiently it cleans the environment while minimizing energy consumption.

## Features

- **10x10 Grid Environment**: The environment is a 10x10 maze. (A 8x8 maze surrounding by walls.)Each cell is either a wall or a room. The walls are always clean and the agent cannot pass through the wall.
- **Agent Movement**: The agent can move in four directions (north, south, east, west) to clean the environment. Each move costs 1 point of energy.
- **Sucking Dirt**: The agent can suck dirt from the grid, but this action costs 2 points of energy.
- **Energy Management**: The agent’s performance is based on the balance between cleaning effectiveness and energy conservation.
- **Time Steps**: The simulation runs for a set number of time steps, after which the performance is evaluated.

### Simulation Goals:
- **Cleaning Efficiency**: Clean as many dirty cells as possible within the given time steps.
- **Energy Optimization**: Minimize energy usage while achieving maximum cleaning.

## Path Planning Algorithm (Recent Update)
In this version, the agent is equipped with a path-planning algorithm that allows it to:
- **Identify Nearest Dirt**: The agent scans the environment to locate the nearest dirty cell.
- **Move Efficiently**: Using Manhattan distance, the agent moves step-by-step toward the nearest dirt to clean it, reducing random movement and conserving energy.
- **Energy Conservation**: The agent remains idle when no dirt is nearby consuming no energy.

## Evaluation
At the end of the simulation, the following metrics are displayed:
- **Total Dirt Remaining**: How much dirt is left in the environment.
- **Energy Remaining**: How much energy the agent has after the simulation.

## How to Run the Simulation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd vacuum-cleaner-simulation

2. Run the simulation:
   python vacuumcleaner.py

## Requirements 
    -Python 3.x
    

