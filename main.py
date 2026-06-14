from monte_carlo import MonteCarlo, StudentT
from random import random
from math import sqrt

mc = MonteCarlo(StudentT(4))

mc.simulate(1e6)

print(mc.proportion(lambda x: x < 1.190))
