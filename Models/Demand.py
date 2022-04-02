import numpy as np


class Demand:
    def __init__(self, uranium: int, tuna: int, orange: int):
        self.uranium = uranium
        self.tuna = tuna
        self.orange = orange

    @classmethod
    def random_demand(cls, max_demand = 200) -> 'Demand':
        demands = []
        while np.sum(demands) < 100:
            for i in range(3):
                demand = np.random.randint(0, max_demand)
                if (np.random.randint(0,
                                      100) > 74):  # pozwala dostroić liczbę przypadków z jednym, dwoma, lub trzeba produktami
                    demand = int(demand / 3)
                if np.sum(demands) + demand > 200 or len(demands) == 3:
                    break
                demands.append(demand)
            if np.sum(demands) + demand > max_demand or len(demands) == 3:
                break
        demands = [i * (-1) if np.random.choice([True, False]) else i for i in demands]
        while len(demands) < 3:
            demands.append(0)
        np.random.shuffle(demands)

        return cls(demands[0], demands[1], demands[2])

    def __str__(self):
        return "{},{},{}".format(self.uranium, self.tuna, self.orange)