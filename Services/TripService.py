from Models.point import Point
from Models.demand import Demand
from Models.vehicle import Vehicle
import numpy as np
import math

def CalculateDistanceBetweenTwoPoints(point1: Point, point2: Point):
    return math.dist([point1.xCoordinate,point1.yCoordinate],
                     [point2.xCoordinate,point2.yCoordinate])

def CalculateTotalTripDistance(points: list[Point]):
    pass

def CreateRandomTrip(vehicle: Vehicle, points: list[Point]):
    pass
