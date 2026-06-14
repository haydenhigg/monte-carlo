from monte_carlo import MonteCarlo, Normal, ChiSquare, StudentT
from statistics import stdev

mc = MonteCarlo(Normal()(3))

mc.simulate(100_000)

# print(mc.proportion(lambda x: abs(x) > 3))
print(mc.visualize(domain=(-5, 5)))
