import random
from typing import Type

from Models.Point import Point, Magazine, Client
from Models.Demand import Demand
from Models.Vehicle import Vehicle, ColorCapacityMapper
import numpy as np

from visualizer.map_visualizer import draw_point_map

MAX_DEMAND = 200
NUMBER_OF_MAGAZINES = 5
VEHICLE_CAPACITY = [1000, 1500, 2000]
NUMBER_OF_POINTS = 100


def generate_points(point_number: int):
    points: Point = []
    for i in range(point_number-NUMBER_OF_MAGAZINES):
        points.append(generate_point(False))
    for i in range(NUMBER_OF_MAGAZINES):
        points.append(generate_point(True))
    return points


def generate_point(is_magazine: bool):
    if is_magazine:
        return Magazine(
            np.random.random() * 100,
            np.random.random() * 100,
        )
    else:
        return Client(
            np.random.random() * 100,
            np.random.random() * 100,
            Demand.random_demand(MAX_DEMAND)
        )


def generate_vehicles(magazines: list[Magazine]):
    number_of_vehicles = np.random.randint(3, 7)
    vehicles = []
    for i in range(number_of_vehicles):
        demand = Demand(0, 0, 0)
        vehicles.append(
            Vehicle(
                demand,
                random.choice(magazines),
                random.choice([color for color in ColorCapacityMapper]),
                False
            )
        )
    cat_vehicle = np.random.randint(0, number_of_vehicles)
    vehicles[cat_vehicle].is_cat_driver = True
    return vehicles


def generate_starting_conditions(number_of_points: int, number_of_magazines: int):
    clients = [generate_point(False) for _ in range(number_of_points-number_of_magazines)]
    magazines = [generate_point(True) for _ in range(number_of_magazines)]
    # points = GeneratePoints(NUMBER_OF_POINTS)
    # magazines = list(filter(lambda x: x.isMagazine == True, points))
    vehicles = generate_vehicles(magazines)
    try:
        while True:
            vehicles[0].go_to_next_client(clients)
    except Exception:
        pass

    return [*clients, *magazines, *vehicles]


if __name__ == '__main__':
    points: list[Type[Point]] = generate_starting_conditions(NUMBER_OF_POINTS, NUMBER_OF_MAGAZINES)

    [print(item) for item in points]
    draw_point_map(points)
