from Models.Demand import Demand
class Point:
    def __init__(self, xCoordinate: float, yCoordinate: float, demand: Demand, isMagazine: bool):
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
        self.demand = demand
        self.isMagazine = isMagazine

    def __str__(self):
        return "{},{},{},{}".format(self.xCoordinate,self.yCoordinate,self.demand,self.isMagazine)