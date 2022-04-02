from enum import Enum
from Models.point import Point
from Models.demand import Demand
from Models.utils import ToStrMixin


class ColorCapacityMapper(Enum):
    READ = 1000
    GREEN = 1500
    BLUE = 2000

    @property
    def __dict__(self):
        return self.name


class Vehicle(Point, ToStrMixin):
    def __init__(self, demand: Demand, point: Point, color: ColorCapacityMapper, is_cat_driver: bool):
        super().__init__(**point.__dict__)
        self.demand = demand
        self.capacity = color.value
        self.is_cat_driver = is_cat_driver
        self.color = color
        self.directions = [Point(self.x_coordinate, self.y_coordinate)]
        self.total_distance = 0

    def move(self, point: Point):
        self.total_distance += Point(self.x_coordinate, self.y_coordinate).calculate_distance(point)
        self.x_coordinate = point.x_coordinate
        self.y_coordinate = point.y_coordinate
        self.directions.append(Point(self.x_coordinate, self.y_coordinate))

