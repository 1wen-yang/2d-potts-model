import time
import numpy as np
import matplotlib.pyplot as plt

from potts_mcmc import init_lattice, metropolis_sweep, energy_per_spin


def blocking_average(data, block_size):
    n = len(data)
    n_blocks = n // block_size

    if n_blocks < 2:
        raise ValueError("not enough data for multiple blocks")

    data = data[:n_blocks * block_size]
    blocks = data.reshape(n_blocks, block_size)
    block_means = blocks.mean(axis=1)

    mean = block_means.mean()
    se = block_means.std(ddof=1) / np.sqrt(n_blocks)

    return mean, se, block_means


def run_scan(
    L=24,
    q=2,
    temps=None,
    sweeps_eq=400,
    sweeps_meas=1200,
    thin=5,
    block_size=50,
    start_mode="hot",
    J=1.0,
    verbose=True,
):
    if temps is None:
        temps = np.linspace(0.5, 2.0, 31) if q == 2 else np.linspace(0.45, 0.95, 26)

    e_means = []
    e_errs = []
    log_rows = []

    latt = init_lattice(L, q, mode=start_mode)

    for T in temps:
        t0 = time.time()

        for _ in range(sweeps_eq):
            metropolis_sweep(latt, T, q, J=J)

        samples = []

        for s in range(sweeps_meas):
            metropolis_sweep(latt, T, q, J=J)

            if (s + 1) % thin == 0:
                samples.append(energy_per_spin(latt, J=J))

        samples = np.asarray(samples, dtype=float)
        mean, se, _ = blocking_average(samples, block_size=block_size)

        e_means.append(mean)
        e_errs.append(se)

        n_samples = samples.size
        n_blocks = n_samples // block_size
        runtime = time.time() - t0

        log_rows.append([T, mean, se, n_samples, block_size, n_blocks, runtime])

        if verbose:
            print(
                f"T={T:6.4f} | <E>/N = {mean: .6f} ± {se:.6f} "
                f"| n={n_samples}, block={block_size}, nb={n_blocks} "
                f"| {runtime:.2f}s"
            )

    return (
        np.array(temps),
        np.array(e_means),
        np.array(e_errs),
        np.array(log_rows),
    )


def plot_scan(T, e, se, q, savepath):
    plt.figure(figsize=(6, 4))

    plt.errorbar(T, e, yerr=se, fmt="o-", lw=1, ms=4, label=f"q={q}")

    plt.axhline(-2.0, ls=":", color="gray", lw=1)
    plt.axhline(-2.0 / q, ls=":", color="gray", lw=1)

    plt.xlabel("Temperature T")
    plt.ylabel("<E>/N")
    plt.title(f"Potts model: <E>/N vs T (q={q})")
    plt.grid(alpha=0.3)
    plt.legend()

    plt.savefig(savepath, bbox_inches="tight")
    plt.close()


def plot_comparison(T2, e2, se2, T10, e10, se10, savepath):
    Tc_q2 = 1.0 / np.log(1.0 + np.sqrt(2.0))
    Tc_q10 = 1.0 / np.log(1.0 + np.sqrt(10.0))

    plt.figure(figsize=(6, 4))

    plt.errorbar(T2, e2, yerr=se2, fmt="o-", ms=4, label="q=2")
    plt.errorbar(T10, e10, yerr=se10, fmt="s-", ms=4, label="q=10")

    plt.axhline(-2.0, ls=":", color="gray", lw=1)
    plt.axhline(-1.0, ls=":", color="gray", lw=1)
    plt.axhline(-0.2, ls=":", color="gray", lw=1)

    plt.axvline(Tc_q2, color="blue", linestyle="--", lw=1, label=f"Tc(q=2)={Tc_q2:.3f}")
    plt.axvline(Tc_q10, color="red", linestyle="--", lw=1, label=f"Tc(q=10)={Tc_q10:.3f}")

    plt.xlabel("Temperature T")
    plt.ylabel("<E>/N")
    plt.title("Potts model: <E>/N vs T (q=2 vs q=10)")
    plt.grid(alpha=0.3)
    plt.legend()

    plt.savefig(savepath, bbox_inches="tight")
    plt.close()