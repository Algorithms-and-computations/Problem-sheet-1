import random
from numba import jit, prange
import numpy as np
import matplotlib.pyplot as plt

# Compiled and parallelised
@jit(nopython=True, parallel=True)
def calculate_pi(N):
    hits = 0

    for i in prange(N):
        x = random.random()  # Between 0.0 and 1.0
        y = random.random()  # Between 0.0 and 1.0
        if x**2 + y**2 < 1:
            hits += 4

    return hits / N


N = 123456
N_trials = 12345

samples = np.array([calculate_pi(N) for _ in range(N_trials)])

# samples = np.empty((N_trials))

# for i in range(N_trials):
#     samples[i] = calculate_pi(N)

best_estimate = np.mean(samples)
print("Best pi estimate = %.10f" % best_estimate)

variance = np.var(samples)

# See notes
expected_variance = np.pi * (4 - np.pi) / N
print("Variance = %.10f, (expected %.10f)" % (variance, expected_variance))

plt.hist(samples, bins=50, color='blue', edgecolor='black')
plt.title("pi samples")
plt.xlabel("sample")
plt.ylabel("frequency")
plt.show()
