# VQE Portfolio Optimization - Quick Start Guide

## Repository Structure Overview

```
WISER_Optimization_VG/
├── _experiments/           # Main execution scripts
│   ├── sbo_steps1to3.py   # Main VQE execution script (EXECUTABLE)
│   ├── sbo_step4.py       # Post-processing/local search (EXECUTABLE)
│   ├── doe.py             # Experiment configurations
│   └── analysis*.ipynb    # Jupyter notebooks for analysis
├── _problems/              # Tutorial examples and building blocks
│   ├── constraint.py      # Base constraint classes (library code)
│   ├── quadratic_*.py     # Quadratic optimization examples
│   └── *.py               # Various optimization problem templates
├── src/
│   ├── step_1.py          # Problem mapping (LP file → quantum objective)
│   ├── experiment.py      # Experiment data structures
│   └── sbo/               # Core quantum optimization engine
├── data/
│   └── 1/
│       ├── 31bonds/       # 31-asset portfolio problems
│       ├── 109bonds/      # 109-asset portfolio problems
│       └── 155bonds/      # 155-asset portfolio problems
└── misc/                  # Additional utilities
```

## Key Files and What They Do

### Executable Scripts (What You Actually Run)

**`_experiments/sbo_steps1to3.py`** - Main execution script
- Runs the complete VQE portfolio optimization pipeline
- Steps 1-3: Problem mapping → Circuit optimization → Quantum execution
- **This is your primary entry point**

**`_experiments/sbo_step4.py`** - Post-processing
- Applies local search to improve quantum solutions
- Optional step for solution polishing

### Configuration Files

**`_experiments/doe.py`** - Design of Experiments
- Contains all experiment configurations
- Defines portfolio problems, ansatz settings, optimization parameters
- **Edit this to create new experiments**

### Core Logic (Don't Execute Directly)

**`src/step_1.py`** - Problem conversion utilities
- `problem_mapping()`: Converts LP files to quantum objective functions
- `model_to_obj()`: Handles constraint-to-penalty conversion
- `get_cplex_sol()`: Gets classical solution for comparison

**`src/experiment.py`** - Data structures for tracking results

**`src/sbo/`** - Quantum optimization engine (VQE/QAOA implementation)

**`_problems/`** - Tutorial examples and constraint infrastructure
- Contains base optimization problem classes (constraint.py, quadratic_constraint.py)
- Various optimization problem templates and examples
- **Good for learning but not directly executable**
- Used as building blocks by the main system

## How to Identify Executable Files

**Look for these patterns:**
```python
if __name__ == "__main__":
    # This indicates an executable script
    execute_multiple_runs(**doe['some_config'])
```

**Executable files typically:**
- Import from other modules but define main execution logic
- Have clear parameter configurations at the bottom
- Are located in `_experiments/` folder

**Library files typically:**
- Define classes and functions
- Have lots of `def` statements
- Are imported by executable files
- Located in `src/` folder

## Required Libraries

### Core Dependencies
```bash
pip install qiskit qiskit-aer qiskit-ibm-runtime
pip install docplex cplex  # For LP file handling
pip install numpy pandas scipy
pip install matplotlib seaborn  # For visualization
```

### IBM Quantum Access (Optional)
- For real quantum hardware: need IBM Quantum account
- For simulator only: no account needed

## Quick Start Workflow

### 1. Setup Environment
```bash
cd WISER_Optimization_VG
python -m venv vanguard
source vanguard/bin/activate  # Windows: vanguard\Scripts\activate
pip install -r requirements.txt  # if exists, or install manually
```

### 2. Run Basic Test
```bash
cd _experiments
python sbo_steps1to3.py
```

**What this does:**
- Loads 31-bond portfolio from `data/1/31bonds/docplex-bin-avgonly.lp`
- Runs VQE with TwoLocal ansatz (1 rep, bilinear entanglement)
- Uses AerSimulator (local quantum simulator)
- Saves results to `data/1/31bonds/test/exp0.pkl`

### 3. Monitor Progress
Use the monitoring tool to visualize:
```python
from vqe_monitor import VQEPortfolioMonitor
monitor = VQEPortfolioMonitor("path/to/data", experiment_id='test')
monitor.monitor_realtime()
```

### 4. Analyze Results
```bash
python sbo_step4.py  # Optional post-processing
```

## Experiment Configuration (doe.py)

### Key Parameters to Understand

```python
'1/31bonds/test': {
    'lp_file': f'{ROOT}/data/1/31bonds/docplex-bin-avgonly.lp',  # Portfolio data
    'experiment_id': 'test',                                      # Results folder name
    'num_exec': 1,                                               # Number of runs
    'ansatz': 'TwoLocal',                                        # Quantum circuit type
    'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},   # Circuit structure
    'theta_initial': 'piby3',                                    # Initial parameters
    'optimizer': 'nft',                                          # Classical optimizer
    'device': 'AerSimulator',                                    # Quantum backend
    'max_epoch': 1,                                              # Optimization epochs
    'alpha': 0.1,                                                # CVaR risk measure
    'shots': 2**13,                                              # Quantum measurements
    'theta_threshold': 0.06,                                     # Convergence threshold
}
```

### Common Configurations Available
- `'1/31bonds/test'` - Quick test (1 epoch, 1 execution)
- `'1/31bonds/TwoLocal2rep_piby3_AerSimulator_0.1'` - Standard simulator run
- `'1/109bonds/TwoLocal2rep_bilinear_piby3_fez_0.1'` - Real quantum hardware

## Creating Your Own Portfolio Problem

### Option 1: Use Existing Data Structure
1. Create your portfolio LP file in GUROBI format
2. Place it in `data/1/your_problem/`
3. Add configuration to `doe.py`:

```python
'1/your_problem/custom_test': {
    'lp_file': f'{ROOT}/data/1/your_problem/your_portfolio.lp',
    'experiment_id': 'custom_test',
    # ... copy other parameters from test config
}
```

4. Update `sbo_steps1to3.py` to use your config:
```python
execute_multiple_runs(**doe['1/your_problem/custom_test'], instance='', run_on_serverless=False)
```

### Option 2: Generate Portfolio Data with GUROBI
```python
import gurobipy as gp
# Create portfolio optimization model
# Export as LP file: model.write("your_portfolio.lp")
```

## Understanding the Output

### During Execution
- **Iteration logs**: Show optimizer progress (parameter updates, function evaluations)
- **Convergence info**: Objective function improvements over time

### Result Files
- **`exp0.pkl`**: Complete experiment results (parameters, solutions, timings)
- **`isa_ansatz.qpy`**: Optimized quantum circuit for hardware
- **Iteration files**: `experiment_id_0.pkl`, `experiment_id_1.pkl`, etc.

### Key Metrics to Track
- **Relative gap**: `(quantum_solution - classical_solution) / classical_solution`
- **Runtime**: Time to find solution
- **Function evaluations**: Number of quantum circuit evaluations
- **Convergence**: How quickly objective function improves

## Troubleshooting Common Issues

### ImportError: Cannot import cplex
```bash
pip install cplex  # Install CPLEX community edition
```

### KeyError in doe configuration
- Check experiment ID exists in `doe.py`
- Verify all required parameters are defined

### File not found errors
- Check LP file paths in `doe.py`
- Ensure data directory structure matches expectations

### Quantum backend errors
- For hardware: verify IBM Quantum account setup
- For simulator: ensure sufficient memory for problem size

## Next Steps for Development

### 1. Understand Baseline Performance
- Run existing 31-bond example
- Analyze results vs classical GUROBI solution
- Understand convergence behavior

### 2. Create Portfolio-Specific Problems
- Generate meaningful portfolio constraints
- Test different risk models
- Compare problem sizes (31 vs 109 vs 155 assets)

### 3. Optimize Quantum Approach
- Experiment with different ansatz types (TwoLocal vs BFCD)
- Tune hyperparameters (alpha, shots, circuit depth)
- Try different entanglement patterns

### 4. Scale and Validate
- Test on larger problems
- Compare performance vs classical methods
- Analyze quantum advantage scenarios

## File Execution Priority

**Start with these (in order):**
1. `_experiments/sbo_steps1to3.py` - Core VQE execution
2. `vqe_monitor.py` - Visualization tool  
3. `_experiments/sbo_step4.py` - Post-processing
4. Analysis notebooks in `_experiments/analysis*.ipynb`

**Modify these for customization:**
1. `_experiments/doe.py` - Experiment configurations
2. `src/step_1.py` - Problem mapping logic (advanced)

**Don't execute directly:**
- Anything in `src/sbo/` - Library code
- `src/experiment.py` - Data structures
- Constraint/optimization classes - Infrastructure
- **`_problems/` folder** - Tutorial examples and base classes (not executable, but useful for understanding)

This should give you a solid roadmap to navigate the codebase and start making meaningful contributions to the quantum portfolio optimization challenge!