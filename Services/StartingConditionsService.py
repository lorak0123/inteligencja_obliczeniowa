from typing import Type

from Models.Point import Point, Magazine, Client
from Models.Demand import Demand
from Models.Vehicle import Vehicle
import numpy as np

from visualizer.map_visualizer import draw_point_map

MAX_DEMAND = 200
NUMBER_OF_MAGAZINES = 5
VEHICLE_CAPACITY = [1000, 1500, 2000]
NUMBER_OF_POINTS = 10


def GeneratePoints(pointNumber: int):
    points: Point = []
    for i in range(pointNumber-NUMBER_OF_MAGAZINES):
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
                magazines[np.random.randint(0, len(magazines))],
                VEHICLE_CAPACITY[np.random.randint(0, 3)],
                False
            )
        )
    cat_vehicle = np.random.randint(0, number_of_vehicles)
    vehicles[cat_vehicle].is_cat_driver = True
    return vehicles


def generate_starting_conditions():
    clients = [generate_point(False) for _ in range(NUMBER_OF_POINTS-NUMBER_OF_MAGAZINES)]
    magazines = [generate_point(True) for _ in range(NUMBER_OF_MAGAZINES)]
    # points = GeneratePoints(NUMBER_OF_POINTS)
    # magazines = list(filter(lambda x: x.isMagazine == True, points))
    vehicles = generate_vehicles(magazines)
    [vehicles[0].move(Point(point.x_coordinate, point.y_coordinate)) for point in clients]
    return [*clients, *magazines, *vehicles]

# print(GenerateDemand())
# demands =[]
# for i in range(10000):
#     demands.append(GenerateDemand())
# lens = [0,0,0]
# for i in demands:
#     for j in range(3):
#         if(i[j]>0):
#             lens[j]+=1
#
# print(lens[0],lens[1],lens[2])

# p = GeneratePoints(30)
# for i in p:
#     print(i)


if __name__ == '__main__':
    points: list[Type[Point]] = generate_starting_conditions()


    [print(item) for item in points]
    draw_point_map(points)
