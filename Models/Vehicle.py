from enum import Enum

from Models.Point import Point, Client
from Models.Demand import Demand
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

    def move(self, point: Point):
        self.x_coordinate = point.x_coordinate
        self.y_coordinate = point.y_coordinate
        self.directions.append(Point(self.x_coordinate, self.y_coordinate))

    def go_to_next_client(self, points: list[Client]):
        not_done = list(filter(lambda client: client.not_done, points))

        if len(not_done) == 0:
            raise Exception('No more clients')

        actual = Point(self.x_coordinate, self.y_coordinate)
        nearest_point = not_done[0]
        nearest_distance = actual.calculate_distance(not_done[0])

        for i in range(1, len(not_done)):
            distance = actual.calculate_distance(not_done[i])
            if distance < nearest_distance:
                nearest_point = not_done[i]
                nearest_distance = distance

        self.x_coordinate = nearest_point.x_coordinate
        self.y_coordinate = nearest_point.y_coordinate
        self.directions.append(Point(self.x_coordinate, self.y_coordinate))

        nearest_point.demand = Demand(0, 0, 0)
