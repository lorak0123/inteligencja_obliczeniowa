from Models.Point import Point
from Models.Demand import Demand

COLORS = ['R','G','B']
VEHICLE_CAPACITY = [1000, 1500, 2000]
class Vehicle:
    def __init__(self, demand: Demand, point: Point, capacity: int, isCatDriver: bool):
        self.demand = demand
        self.point = point
        self.capacity = capacity
        self.isCatDriver = isCatDriver
        self.color = COLORS[VEHICLE_CAPACITY.index(self.capacity)]

    def __str__(self):
        return '{},{},{},{},{}'.format(self.demand,self.point,self.capacity,self.isCatDriver,self.color)
