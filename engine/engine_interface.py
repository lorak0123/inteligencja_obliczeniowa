import abc
from typing import Type

from Models.point import Client, Magazine, Point
from Models.vehicle import Vehicle


class EngineInterface(metaclass=abc.ABCMeta):
    def __init__(self, points: list[Type[Point]]):
        self.clients: list[Client] = list(filter(lambda point: isinstance(point, Client), points))
        self.magazines: list[Magazine] = list(filter(lambda point: isinstance(point, Magazine), points))
        self.vehicles: list[Vehicle] = list(filter(lambda point: isinstance(point, Vehicle), points))

    @abc.abstractmethod
    def compute(self) -> list[Type[Point]]:
        raise NotImplementedError
