# FinQuantOpt
Optimizing Financial Assets Low risk High gain

FinQuantOpt is a research project that explores how quantum computing can be used to solve portfolio optimization problems in finance. The goal is to find the best way to allocate assets in a portfolio while considering constraints like risk and return. Instead of using traditional methods, this project uses quantum algorithms—specifically the Variational Quantum Eigensolver (VQE)—to tackle these challenges.

The project is organized into several folders that separate the different parts of the system. There are scripts that run the main optimization process, tools for analyzing results, and templates for building new financial problems. The main script, called `sbo_steps1to3.py`, performs three key steps: it converts a financial problem into a format that a quantum computer can understand, builds and optimizes a quantum circuit to solve it, and then runs that circuit using either a simulator or real quantum hardware. An optional fourth step uses classical methods to refine the solution further.

To run an experiment, users configure settings in a file called `doe.py`. This file lets them choose which portfolio to optimize, what kind of quantum circuit to use, which optimizer to apply, and whether to run the experiment on a simulator or a real quantum device. The system supports different portfolio sizes, from small sets of 31 assets to larger ones with over 150.

Once the experiment is running, users can monitor its progress using a built-in visualization tool. This shows how the quantum algorithm is performing over time and helps identify whether the solution is improving. After the run is complete, results are saved in files that include the optimized parameters, performance metrics, and even the quantum circuit itself, which can be deployed to hardware.

The project also includes tutorials and examples to help users learn how to build their own portfolio problems. These are not meant to be run directly but serve as building blocks for creating new experiments. Users can generate their own financial models using tools like GUROBI and plug them into the system by updating the configuration file.

FinQuantOpt is designed for researchers, students, and developers who want to explore how quantum computing might offer advantages in financial optimization. It provides a hands-on way to test ideas, compare classical and quantum solutions, and experiment with different quantum circuit designs. Whether you're interested in benchmarking performance or scaling up to more complex problems, this project offers a flexible and educational platform for quantum finance exploration.
