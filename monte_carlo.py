from abc import ABC, abstractmethod
from typing import Any, Callable
from random import gauss, random
from math import sqrt

class Sampler(ABC):
    @abstractmethod
    def sample(self) -> Any:
        pass

class Function(Sampler):
    def __init__(self, function: Callable[[], Any]):
        self.function = function

    def sample(self) -> Any:
        return self.function()

class Mixture(Sampler):
    def __init__(self, a: Sampler, b: Sampler, function: Callable[[Any, Any], Any]):
        self.a = a
        self.b = b
        self.function = function

    def sample(self) -> Any:
        return self.function(self.a.sample(), self.b.sample())

class Normal(Sampler):
    def __init__(self, mean: float = 0, std_dev: float = 1):
        self.mean = mean
        self.std_dev = std_dev

    def sample(self) -> Any:
        return self.mean + gauss() * self.std_dev

class ChiSquare(Sampler):
    def __init__(self, df: int = 1):
        self.df = max(df, 1)

    def sample(self) -> float:
        ss = 0

        for _ in range(self.df):
            ss += gauss() ** 2

        return ss

class StudentT(Sampler):
    def __init__(self, df: int = 1):
       self.df = max(df, 1)
       self.normal = Normal()
       self.chi_square = ChiSquare(self.df)

    def sample(self) -> float:
        return self.normal.sample() / sqrt(self.chi_square.sample() / self.df)

class MonteCarlo:
    def __init__(self, sampler: Sampler = None):
        self.sampler = sampler or Function(random)
        self.results = []

    def simulate(self, n: int = 10_000):
        for _ in range(n):
            self.results.append(self.sampler.sample())

    def frequencies(self) -> dict[Any, float]:
        counts = {}
        total_count = 0

        for result in self.results:
            if result in counts:
                counts[result] += 1
            else:
                counts[result] = 1

            total_count += 1

        return {k: v / total_count for k, v in counts.items()}

    def proportion(self, filter: Callable[Any, bool] = lambda _: True) -> float:
        return sum([v for k, v in self.frequencies().items() if filter(k)])

    def visualize(
        self,
        width: int = 80,
        height: int = 20,
        domain: tuple[float, float] = None
    ) -> str:
        domain = domain or (min(self.results),  max(self.results))

        bucket_size = (domain[1] - domain[0]) / width
        buckets = [[domain[0] + bucket_size * i, 0] for i in range(width)]

        for k, v in self.frequencies().items():
            i = min(max((k - domain[0]) // bucket_size, 0), width - 1)
            buckets[int(i)][1] += v

        max_bucket = 0

        for bucket in buckets:
            if bucket[1] > max_bucket:
                max_bucket = bucket[1]

        histogram = [height * bucket[1] / max_bucket for bucket in buckets]
        lines = ['' for _ in range(height)]

        for iy in range(height):
            y = height - iy
            over_zero = False

            for i, bucket in enumerate(histogram):
                if not over_zero and buckets[i][0] >= 0:
                    over_zero = True
                    lines[iy] += '|'

                if bucket >= y:
                    lines[iy] += '\u2588'
                elif bucket + 0.125 >= y:
                    lines[iy] += '\u2587'
                elif bucket + 0.25 >= y:
                    lines[iy] += '\u2586'
                elif bucket + 0.375 >= y:
                    lines[iy] += '\u2585'
                elif bucket + 0.5 >= y:
                    lines[iy] += '\u2584'
                elif bucket + 0.625 >= y:
                    lines[iy] += '\u2583'
                elif bucket + 0.75 >= y:
                    lines[iy] += '\u2582'
                elif bucket + 0.875 >= y:
                    lines[iy] += '\u2581'
                else:
                    lines[iy] += ' '

        return '\n'.join(lines)
