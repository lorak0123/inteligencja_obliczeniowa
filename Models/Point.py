from Models.Demand import Demand
from Models.utils import ToStrMixin


class Point(ToStrMixin):
    def __init__(self, x_coordinate: float, y_coordinate: float):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate


class Client(Point, ToStrMixin):
    def __init__(self, x_coordinate: float, y_coordinate: float, demand: Demand):
        super().__init__(x_coordinate, y_coordinate)
        self.demand = demand


class Magazine(Point, ToStrMixin):
    def __init__(self, x_coordinate: float, y_coordinate: float):
        super().__init__(x_coordinate, y_coordinate)
