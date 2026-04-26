# Potts Model MCMC Simulation

This project implements a Markov Chain Monte Carlo simulation of the 2D q-state Potts model using the Metropolis algorithm.

## Overview

The Potts model is a lattice-based statistical physics model where each site takes one of q discrete states. Neighboring sites prefer to have the same state.

This project studies:

- Energy evolution over time (thermalization)
- Equilibrium energy using MCMC sampling
- Phase transitions via temperature scan
- Differences between q = 2 and q = 10

---

## Project Structure

```
potts-model/
├── main.py
├── potts_mcmc.py
├── potts_time_evolution.py
├── potts_temperature_scan.py
├── results/
├── requirements.txt
└── README.md
```

---

## File Description

**main.py**  
Entry point. Runs all experiments.

**potts_mcmc.py**  
Core implementation of the Potts model and Metropolis algorithm.

**potts_time_evolution.py**  
Simulates energy evolution over time.

**potts_temperature_scan.py**  
Performs temperature scans and computes average energy with error estimation.

---

## Requirements

```
numpy
matplotlib
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## Run

```
python main.py
```

All results will be saved in the `results/` folder.

---

## Output

### Time evolution

- `results/time_evolution_q2.pdf`
- `results/time_evolution_q10.pdf`

### Temperature scan

- `results/energy_vs_T_q2.pdf`
- `results/energy_vs_T_q10.pdf`

### Comparison

- `results/energy_vs_T_comparison.pdf`

---

## Data

- `results/energy_vs_T_q2.csv`
- `results/energy_vs_T_q10.csv`

Format:

```
T, <E>/N, SE
```

---

## Method

Energy:

```
E = -J * sum delta(s_i, s_j)
```

Sampling method:

Metropolis algorithm:

1. Propose a new state  
2. Compute ΔE  
3. Accept if ΔE ≤ 0 or with probability exp(-ΔE / T)

---

## Expected Behavior

At low temperature, energy approaches -2.  
At high temperature, energy approaches -2/q.

Critical temperature:

```
Tc = 1 / log(1 + sqrt(q))
```

For q = 2: continuous transition  
For q = 10: first-order transition  

---

## Author

Yiwen Yang