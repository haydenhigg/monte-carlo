from abc import ABC, abstractmethod
from typing import Hashable, Callable
from random import gauss, random
from math import sqrt, inf

class Sampler(ABC):
    @abstractmethod
    def sample(self) -> Hashable:
        pass

class Function(Sampler):
    def __init__(self, function: Callable[[], Hashable]):
        self.function = function

    def sample(self) -> Hashable:
        return self.function()

class Mixture(Sampler):
    def __init__(self, a: Sampler, b: Sampler, function: Callable[[Hashable, Hashable], Hashable]):
        self.a = a
        self.b = b
        self.function = function

    def sample(self) -> Hashable:
        return self.function(self.a.sample(), self.b.sample())

class Normal(Sampler):
    def __init__(self, mean: float = 0, std_dev: float = 1):
        self.mean = mean
        self.std_dev = std_dev

    def sample(self) -> Hashable:
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

    def simulate(self, n: int = 1e3):
        for _ in range(int(n)):
            self.results.append(self.sampler.sample())

    def frequencies(self) -> dict[Hashable, float]:
        counts = {}
        total_count = 0

        for result in self.results:
            if result in counts:
                counts[result] += 1
            else:
                counts[result] = 1

            total_count += 1

        return {k: v / total_count for k, v in counts.items()}

    def proportion(self, filter: Callable[Hashable, bool] = lambda _: True) -> float:
        return sum([v for k, v in self.frequencies().items() if filter(k)])

    def buckets(self, n: int, low: float, high: float) -> tuple[list[float], float]:
        bucket_width = (high - low) / n
        buckets = [0 for _ in range(n)]

        for k, v in self.frequencies().items():
            i = int((k - low) // bucket_width)

            if i >= 0 and i <= n - 1:
                buckets[i] += v

        max_bucket = -inf

        for bucket in buckets:
            if bucket > max_bucket:
                max_bucket = bucket

        return ([bucket / max_bucket for bucket in buckets], bucket_width)

    def histogram(
        self,
        width: int = 79,
        height: int = 23
    ) -> str:
        # calculate buckets
        min_displayable = 0.125 / height

        low = min(self.results)
        high = max(self.results)

        buckets, bucket_width = self.buckets(width, low, high)

        while buckets[0] < min_displayable or buckets[-1] < min_displayable:
            while buckets and buckets[0] < min_displayable:
                buckets.pop(0)
                low += bucket_width

            while buckets and buckets[-1] < min_displayable:
                buckets.pop()
                high -= bucket_width

            buckets, bucket_width = self.buckets(width, low, high)

        # build histogram visualization
        histogram = [height * bucket for bucket in buckets]
        lines = ['' for _ in range(height)]

        for iy in range(height):
            y = height - iy
            over_zero = False

            for i, bar in enumerate(histogram):
                if not over_zero and low + bucket_width * (i + 0.5) >= 0:
                    over_zero = True
                    lines[iy] += '|'

                if bar >= y:
                    lines[iy] += '\u2588'
                elif bar + 0.125 >= y:
                    lines[iy] += '\u2587'
                elif bar + 0.25 >= y:
                    lines[iy] += '\u2586'
                elif bar + 0.375 >= y:
                    lines[iy] += '\u2585'
                elif bar + 0.5 >= y:
                    lines[iy] += '\u2584'
                elif bar + 0.625 >= y:
                    lines[iy] += '\u2583'
                elif bar + 0.75 >= y:
                    lines[iy] += '\u2582'
                elif bar + 0.875 >= y:
                    lines[iy] += '\u2581'
                else:
                    lines[iy] += ' '

        return '\n'.join(lines)
