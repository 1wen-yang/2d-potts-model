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

## Model Description

We consider the Hamiltonian:

\[

E(\sigma) = -J \sum_{\langle i,j \rangle} \delta(s_i, s_j)

\]

where:

- \( s_i \in \{0, 1, ..., q-1\} \)

- nearest-neighbor interactions on a 2D lattice

- periodic boundary conditions

- \( J = 1 \)

### Energy per spin

\[

E/N = -\frac{1}{N} \sum_{\langle i,j \rangle} \delta(s_i, s_j)

\]

### Theoretical limits

- Low temperature: \( E/N \to -2 \)

- High temperature: \( E/N \to -2/q \)

### Critical temperature

\[

T_c(q) = \frac{1}{\ln(1 + \sqrt{q})}

\]

---

## Simulation Methods

### Metropolis Algorithm

- Random spin selection

- Random new state (excluding current)

- Accept with probability:

\[

P = \min(1, e^{-\Delta E / T})

\]

---

## Simulation Design

### Lattice

- Square lattice: \( L \times L \)

- Typical: \( L = 20 \) or \( L = 24 \)

- Periodic boundary conditions

### Experiments

#### 1. Time Evolution

- Steps: 600,000 updates

- Record once per sweep

- Compare:

  - hot start (random)

  - cold start (ordered)

Temperatures:

- Low: \( T = 0.5 \)

- High: \( T = 20.0 \)

---

#### 2. Temperature Scan

- q = 2: \( T \in [0.5, 1.8] \)

- q = 10: \( T \in [0.45, 0.95] \)

Per temperature:

- 400 sweeps equilibration

- 1200 sweeps measurement

- record every 5 sweeps (~240 samples)

---

### Statistical Treatment

To reduce correlation:

- Thinning (every 5 sweeps)

- Blocking method:

  - divide samples into blocks

  - compute block means

  - estimate standard error

---

## Results

### 1. Time Evolution

- Cold start stays near ground state at low T

- Hot start relaxes slowly

- Both converge to same equilibrium

### 2. Energy vs Temperature

- q = 2:

  - smooth transition (second-order)

- q = 10:

  - sharp drop near \( T_c \)

  - first-order behavior (rounded by finite size)

---

## Author

Yiwen Yang