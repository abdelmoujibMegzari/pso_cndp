# Particle Swarm Optimization for Critical Node Detection Problem (CNDP)

This repository is part of a research project focused on solving the Critical Node Detection Problem (CNDP) using Particle Swarm Optimization (PSO). The project employs a star topology and a custom dynamic topology for the PSO approach. Additionally, the project implements existing greedy and Variable Neighborhood Search (VNS) solutions for comparative analysis.

## Project Structure

- `main_pso_star.py`: Entry point for running the PSO algorithm with a star topology.
- `main_pso_dynamic.py`: Entry point for running the PSO algorithm with a dynamic topology.
- `main_greedy.py`: Entry point for running the greedy algorithm solution.
- `main_vns.py`: Entry point for running the VNS solution.
- `pso/`: Contains the implementation of the PSO algorithm.
- `greedy_CNDP.py`: Contains the implementation of the greedy solution.
- `vns.py`: Contains the implementation of the VNS solution.
- `graphDataSet/`: Directory containing data sets used in the algorithms. Dataset proposed by Mario Ventresca accessible in [https://engineering.purdue.edu/~mventresca/index.php?cnd]
- `GraphTest.py`: Contains tests for graph functionalities used in algorithms.
- `Results/`: Directory containing the results of the running the algorithms on graphDataSet graphs as described in the the thesis.

## Getting Started

### Prerequisites

Ensure you have Python installed on your machine (Python 3.x is recommended).

### Installation

1. Clone the repository:

```bash
git clone https://github.com/abdelmoujibMegzari/pso_cndp.git
```

2. Navigate to the cloned directory:

```bash
cd pso_cndp
```

### Usage

To run any of the solutions, use one of the following commands:
each command will guide you and ask for input data set to run the algorithm.

- For PSO with star topology:

```bash
python main_pso_star.py
```

- For PSO with dynamic topology:

```bash
python main_pso_dynamic.py
```

- For the greedy solution:

```bash
python main_greedy.py
```

- For the VNS solution:

```bash
python main_vns.py
```

## License

This project is licensed under the GPL-3.0 license - see the LICENSE file for details.
