import math
import random

from Models.utils import ToStrMixin


class Demand(ToStrMixin):
    def __init__(self, uranium: int, tuna: int, orange: int):
        self.uranium = uranium
        self.tuna = tuna
        self.orange = orange

    @classmethod
    def random_demand(cls, max_demand=200) -> 'Demand':
        demands = []
        while sum(demands) < 100:
            for i in range(3):
                demand = random.randint(0, max_demand)
                if random.randint(0, 100) > 74:  # pozwala dostroić liczbę przypadków z jednym, dwoma, lub trzeba produktami
                    demand = int(demand / 3)
                if sum(demands) + demand > 200 or len(demands) == 3:
                    break
                demands.append(demand)
            if sum(demands) + demand > max_demand or len(demands) == 3:
                break
        demands = [i * (-1) if random.choice([True, False]) else i for i in demands]
        while len(demands) < 3:
            demands.append(0)
        random.shuffle(demands)

        return cls(demands[0], demands[1], demands[2])

    @property
    def total(self) -> float:
        return self.orange + self.tuna + self.uranium

    @property
    def is_balance_positive(self) -> bool:
        return self.tuna >= 0 and self.orange >= 0 and self.uranium >= 0

    def can_satisfy(self, other: 'Demand', max_total: int = 0) -> bool:
        new = (self - other)
        return new.is_balance_positive and new.total <= max_total if max_total != 0 else True

    def __add__(self, other: 'Demand'):
        return Demand(uranium=self.uranium + other.uranium,
                      tuna=self.tuna + other.tuna,
                      orange=self.orange + other.orange)

    def __sub__(self, other: 'Demand'):
        return Demand(uranium=self.uranium - other.uranium,
                      tuna=self.tuna - other.tuna,
                      orange=self.orange - other.orange)

    def __lt__(self, other):
        self_sum = math.fabs(self.uranium) + math.fabs(self.tuna) + math.fabs(self.orange)
        other_sum = math.fabs(other.uranium) + math.fabs(other.tuna) + math.fabs(other.orange)

        return self_sum < other_sum

