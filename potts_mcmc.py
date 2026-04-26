import math
import numpy as np

rng = np.random.default_rng(12345)


def init_lattice(L, q, mode="hot"):
    if mode == "cold":
        return np.zeros((L, L), dtype=np.int16)
    if mode == "hot":
        return rng.integers(0, q, size=(L, L), dtype=np.int16)
    raise ValueError("mode must be 'hot' or 'cold'")


def total_energy(latt, J=1.0):
    right_eq = latt == np.roll(latt, -1, axis=1)
    down_eq = latt == np.roll(latt, -1, axis=0)
    return float(-J * (np.count_nonzero(right_eq) + np.count_nonzero(down_eq)))


def energy_per_spin(latt, J=1.0):
    return total_energy(latt, J) / latt.size


def metropolis_step(latt, T, q, J=1.0):
    L = latt.shape[0]
    beta = 1.0 / T

    i = rng.integers(0, L)
    j = rng.integers(0, L)

    old = int(latt[i, j])
    r = rng.integers(0, q - 1)
    new = r if r < old else r + 1

    up = int(latt[(i - 1) % L, j])
    down = int(latt[(i + 1) % L, j])
    left = int(latt[i, (j - 1) % L])
    right = int(latt[i, (j + 1) % L])

    n_old = int(old == up) + int(old == down) + int(old == left) + int(old == right)
    n_new = int(new == up) + int(new == down) + int(new == left) + int(new == right)

    dE = -J * (n_new - n_old)

    if dE <= 0 or rng.random() < math.exp(-beta * dE):
        latt[i, j] = new


def metropolis_sweep(latt, T, q, J=1.0):
    for _ in range(latt.size):
        metropolis_step(latt, T, q, J)