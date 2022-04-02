from Models.Point import Point
from Models.Demand import Demand
from Models.utils import ToStrMixin

COLORS = ['R', 'G', 'B']
VEHICLE_CAPACITY = [1000, 1500, 2000]


class Vehicle(Point, ToStrMixin):
    def __init__(self, demand: Demand, point: Point, capacity: int, is_cat_driver: bool):
        super().__init__(**point.__dict__)
        self.demand = demand
        self.capacity = capacity
        self.is_cat_driver = is_cat_driver
        self.color = COLORS[VEHICLE_CAPACITY.index(self.capacity)]

