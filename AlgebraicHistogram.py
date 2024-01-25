import random
import matplotlib.pyplot as plt


data = []
for i in range(100000):
    data.append(min(10, random.uniform(0,1) ** (-0.75)))
plt.hist(data, bins=200, density=True, label='histogram')
Nmax = 1000
U_init = 1
U_end = 10
UValues = []
PiValues = []
for i in range(Nmax):
    U = U_init + i * (U_end - U_init)/ Nmax
    UValues.append(U)
    PiValues.append(4.0 / 3.0 * U ** (-7/3))

plt.plot(UValues,PiValues, label='analytic')
plt.title('Distribution of $ O = ran(0,1) ** (-0.75)$')
plt.legend()
plt.xlabel('$U$ (random variable)')
plt.ylabel('$\pi(U)$ (probability)')
plt.savefig('AlgebraicEx3.png')
plt.show()
