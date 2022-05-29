import os
import random
from typing import Type

from Models.point import Point, Magazine, Client
from Models.demand import Demand
from Models.vehicle import Vehicle, ColorCapacityMapper

from visualizer.map_visualizer import draw_point_map


def generate_vehicles(magazines: list[Magazine]):
    number_of_vehicles = random.randint(3, 6)
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
    cat_vehicle = random.randint(0, number_of_vehicles - 1)
    vehicles[cat_vehicle].is_cat_driver = True
    return vehicles


def generate_starting_conditions(number_of_points: int, number_of_magazines: int) -> list[Type[Point]]:
    max_demand = int(os.environ['MAX_DEMAND'])
    map_size_x = int(os.environ['MAP_SIZE_X'])
    map_size_y = int(os.environ['MAP_SIZE_Y'])
    clients = [
        Client(
            random.random() * map_size_x,
            random.random() * map_size_y,
            Demand.random_demand(max_demand)
        ) for _ in range(number_of_points-number_of_magazines)
    ]
    magazines = [
        Magazine(
            random.random() * map_size_x,
            random.random() * map_size_y
        ) for _ in range(number_of_magazines)
    ]

    vehicles = generate_vehicles(magazines)

    return [*clients, *magazines, *vehicles]


if __name__ == '__main__':
    points: list[Type[Point]] = generate_starting_conditions(int(os.environ['NUMBER_OF_POINTS']),
                                                             int(os.environ['NUMBER_OF_MAGAZINES']))

    [print(item) for item in points]
    draw_point_map(points)

