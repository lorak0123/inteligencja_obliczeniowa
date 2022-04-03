from typing import Type

from matplotlib import pyplot as plt

from Models.point import Point, Client, Magazine
from Models.vehicle import Vehicle, ColorCapacityMapper

plt.style.use('fivethirtyeight')

COLOR_MAP = {ColorCapacityMapper.READ: '#FF0000',
             ColorCapacityMapper.GREEN: '#32CD32',
             ColorCapacityMapper.BLUE: '#1E90FF'}


def draw_point_map(points: list[Type[Point]]):
    clients: Client = list(filter(lambda point: isinstance(point, Client), points))
    magazines: Magazine = list(filter(lambda point: isinstance(point, Magazine), points))
    vehicles: Vehicle = list(filter(lambda point: isinstance(point, Vehicle), points))

    for i, vehicle in enumerate(vehicles):
        plt.plot([point.x_coordinate for point in vehicle.directions],
                 [point.y_coordinate for point in vehicle.directions],
                 # c=COLOR_MAP[vehicle.color],
                 label=f'Trasa pojazd {i}',
                 linewidth=2,
                 alpha=0.5)

    plt.scatter(x=[point.x_coordinate for point in magazines],
                y=[point.y_coordinate for point in magazines],
                c='#FF7F50',
                marker='x',
                s=70,
                label="Magazyny")

    plt.scatter(x=[point.x_coordinate for point in vehicles],
                y=[point.y_coordinate for point in vehicles],
                marker='^',
                color=[COLOR_MAP[point.color] for point in vehicles],
                s=100,
                label="Pojazdy")

    plt.scatter(x=[point.x_coordinate for point in clients],
                y=[point.y_coordinate for point in clients],
                c='#000000',
                label="Klienci")

    plt.legend()

    plt.show()
