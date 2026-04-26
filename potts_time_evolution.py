import numpy as np
import matplotlib.pyplot as plt

from potts_mcmc import init_lattice, metropolis_step, energy_per_spin


def simulate_time_evolution(L, q, T, n_steps, mode="cold", J=1.0):
    latt = init_lattice(L, q, mode)
    energies = []

    for step in range(n_steps):
        metropolis_step(latt, T, q, J)

        if step % (L * L) == 0:
            energies.append(energy_per_spin(latt, J))

    return np.array(energies)


def plot_time_evolution(results, q, L, savepath):
    plt.figure(figsize=(10, 6))

    for label, energies in results.items():
        plt.plot(energies, label=label)

    plt.axhline(-2.0, color="black", linestyle="--", label="Low-T limit (-2)")
    plt.axhline(-2.0 / q, color="red", linestyle="--", label=f"High-T limit (-2/{q})")

    plt.xlabel("Measurement step")
    plt.ylabel("Energy per spin E/N")
    plt.title(f"Potts model q={q}, L={L}")
    plt.legend()
    plt.savefig(savepath, bbox_inches="tight")
    plt.close()


def run_time_evolution(output_dir="results"):
    L = 20
    steps = 600000

    for q in [2, 10]:
        T_low = 0.5
        T_high = 20.0

        results = {
            f"Cold start, T={T_low}": simulate_time_evolution(L, q, T_low, steps, "cold"),
            f"Hot start, T={T_low}": simulate_time_evolution(L, q, T_low, steps, "hot"),
            f"Cold start, T={T_high}": simulate_time_evolution(L, q, T_high, steps, "cold"),
            f"Hot start, T={T_high}": simulate_time_evolution(L, q, T_high, steps, "hot"),
        }

        plot_time_evolution(
            results,
            q=q,
            L=L,
            savepath=f"{output_dir}/time_evolution_q{q}.pdf",
        )