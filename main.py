import os
import numpy as np

from potts_time_evolution import run_time_evolution
from potts_temperature_scan import run_scan, plot_scan, plot_comparison


def main():
    os.makedirs("results", exist_ok=True)

    run_time_evolution(output_dir="results")

    L = 24
    sweeps_eq = 400
    sweeps_meas = 1200
    thin = 5
    block_size = 50

    T_q2 = np.linspace(0.5, 1.8, 27)
    T_q10 = np.linspace(0.45, 0.95, 26)

    print("\n=== q=2 scan ===")
    T2, e2, se2, log2 = run_scan(
        L=L,
        q=2,
        temps=T_q2,
        sweeps_eq=sweeps_eq,
        sweeps_meas=sweeps_meas,
        thin=thin,
        block_size=block_size,
    )

    np.savetxt(
        "results/energy_vs_T_q2.csv",
        np.c_[T2, e2, se2],
        delimiter=",",
        header="T,<E>/N,SE",
        comments="",
    )

    np.savetxt(
        "results/log_q2.csv",
        log2,
        delimiter=",",
        header="T,<E>/N,SE,n_samples,block_size,n_blocks,runtime",
        comments="",
    )

    plot_scan(
        T2,
        e2,
        se2,
        q=2,
        savepath="results/energy_vs_T_q2.pdf",
    )

    print("\n=== q=10 scan ===")
    T10, e10, se10, log10 = run_scan(
        L=L,
        q=10,
        temps=T_q10,
        sweeps_eq=sweeps_eq,
        sweeps_meas=sweeps_meas,
        thin=thin,
        block_size=block_size,
    )

    np.savetxt(
        "results/energy_vs_T_q10.csv",
        np.c_[T10, e10, se10],
        delimiter=",",
        header="T,<E>/N,SE",
        comments="",
    )

    np.savetxt(
        "results/log_q10.csv",
        log10,
        delimiter=",",
        header="T,<E>/N,SE,n_samples,block_size,n_blocks,runtime",
        comments="",
    )

    plot_scan(
        T10,
        e10,
        se10,
        q=10,
        savepath="results/energy_vs_T_q10.pdf",
    )

    plot_comparison(
        T2,
        e2,
        se2,
        T10,
        e10,
        se10,
        savepath="results/energy_vs_T_comparison.pdf",
    )


if __name__ == "__main__":
    main()