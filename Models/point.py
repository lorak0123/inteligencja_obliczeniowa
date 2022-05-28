import math

from Models.demand import Demand
from Models.utils import ToStrMixin


class Point(ToStrMixin):
    def __init__(self, x_coordinate: float, y_coordinate: float):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

    def calculate_distance(self, point: 'Point') -> float:
        return math.sqrt((point.x_coordinate - self.x_coordinate)**2 + (point.y_coordinate - self.y_coordinate)**2)


class Client(Point):
    def __init__(self, x_coordinate: float, y_coordinate: float, demand: Demand):
        super().__init__(x_coordinate, y_coordinate)
        self.demand = demand
        self.start_demand = demand

    @property
    def is_done(self) -> bool:
        if self.demand.tuna == 0 and self.demand.orange == 0 and self.demand.uranium == 0:
            return True

    @property
    def not_done(self) -> bool:
        return not self.is_done


class Magazine(Point):
    def __init__(self, x_coordinate: float, y_coordinate: float):
        super().__init__(x_coordinate, y_coordinate)
