# monte-carlo

Trivially simple Monte Carlo simulations in Python

## example

```py
from monte_carlo import MonteCarlo, Normal

# Get 1e6 samples from the standard Normal distribution
mc = MonteCarlo(Normal())
mc.simulate(1e6)

# Print a histogram
print(mc.histogram())

# Print the probability that sample is below 0
p = mc.proportion(lambda x: x < 0)
print(f'{p * 100:.1f}%')
```

This results in the following output:

```
                                     ▄▆▇|▇█▃
                                   ▅████|███▅▁
                                 ▁██████|█████▅
                                 ███████|██████▅
                               ▁████████|███████▇
                              ▂█████████|████████▆
                             ▁██████████|█████████▆
                             ███████████|██████████▅
                            ████████████|███████████▄
                           ▆████████████|████████████▁
                          ▇█████████████|█████████████▂
                         ▆██████████████|██████████████▂
                        ▅███████████████|███████████████
                       ▅████████████████|████████████████
                      ▃█████████████████|█████████████████▁
                     ▄██████████████████|██████████████████▂
                    ▅███████████████████|███████████████████▂
                   ▇████████████████████|████████████████████▃
                 ▃██████████████████████|█████████████████████▆
               ▂▆███████████████████████|███████████████████████▄
             ▃▆█████████████████████████|█████████████████████████▄
          ▂▅▇███████████████████████████|███████████████████████████▆▃▁
▁▁▁▂▃▃▄▆▇███████████████████████████████|███████████████████████████████▆▅▄▃▂▂▁▁
50.0%
```

## documentation

### `Sampler`

This is the type that is expected when initializing a `MonteCarlo` instance.

`Sampler` is an abstract base class. Subclasses of `Sampler` can generate a sample by overriding the `.sample() -> Hashable` method.

Some basic `Sampler` classes are provided in this package:

- `Normal(mean: float = 0, std_dev: float = 1)`: Draw samples from a Gaussian distribution with the given parameters.
- `ChiSquare(df: int = 1)`: Draw samples from a chi-squared distribution with the given degrees of freedom.
- `StudentT(df: int = 1)`: Draw samples from a Student-T distribution with the given degrees of freedom.
- `Function(function: Callable[[], Hashable])`: Draw samples from `function()`.
- `Mixture(a: Sampler, b: Sampler, function: Callable[[Hashable, Hashable], Hashable])`: Draw samples from `function(a.sample(), b.sample())`. This is for composing multiple Samplers without creating a new `Sampler` subclass manually.

### `MonteCarlo`

This runs the trials and collects the results.

- `MonteCarlo(sampler: Sampler = None)`: Create a new MonteCarlo with a specified `Sampler`. If none is provided, the built-in `random` function will be used.

- `.simulate(n: int = 1e3)`: Run `n` trials and collect the results.
- `.frequencies() -> dict[Hashable, float]`: Calculate the frequency of each sample value.
- `.proportion(filter: Callable[[Hashable], bool] = lambda _: True) -> float`: Calculate the proportion of samples that satisfy a given condition. This is an empirical probability mass function (pmf).

***Note:** The following only work for numerical samples (e.g., `int`, `float`).*

- `.buckets(n: int, low: float, high: float) -> tuple[list[float], float]`: Split samples into `n` equal-width buckets between `low` and `high` (inclusive). Returns the buckets as well as the bucket width. Samples outside the domain `[low, high]` are ignored. All buckets are scaled so that the biggest bucket is 1.
- `.histogram(width: int = 79, height: int = 23, low: float = None, high: float = None) -> str`: Construct a string containing a simple, scaled histogram of the data.
