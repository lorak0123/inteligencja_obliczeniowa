from Models.Point import Point
from Models.Demand import Demand
from Models.Vehicle import Vehicle
import numpy as np


MAX_DEMAND = 200
NUMBER_OF_MAGAZINES = 5
VEHICLE_CAPACITY = [1000, 1500, 2000]
NUMBER_OF_POINTS = 10

def GeneratePoints(pointNumber: int):
    points: Point = []
    for i in range(pointNumber-NUMBER_OF_MAGAZINES):
        points.append(GeneratePoint(False))
    for i in range(NUMBER_OF_MAGAZINES):
        points.append(GeneratePoint(True))
    return points

def GeneratePoint(isMagazine:bool):
    demands = GenerateDemand()
    return Point(
        np.random.random() * 100,
        np.random.random() * 100,
        Demand(
            demands[0],
            demands[1],
            demands[2],
        ),
        isMagazine
    )

def GenerateDemand():
    demands = []
    while np.sum(demands) <100:
        for i in range(3):
            demand = np.random.randint(0, MAX_DEMAND)
            if(np.random.randint(0, 100) > 74): #pozwala dostroić liczbę przypadków z jednym, dwoma, lub trzeba produktami
                demand = int(demand/3)
            if(np.sum(demands) + demand > 200 or len(demands) == 3):
                break
            demands.append(demand)
        if (np.sum(demands) + demand > MAX_DEMAND or len(demands) == 3):
            break
    demands = [i * (-1) if np.random.choice([True, False]) else i for i in demands]
    while len(demands)<3:
        demands.append(0)
    np.random.shuffle(demands)
    return demands

def GenerateVehicles(magazines : list[Point]):
    numberOfVehicles = np.random.randint(3,7)
    vehicles = []
    for i in range(numberOfVehicles):
        demand = Demand(0, 0, 0)
        vehicles.append(
            Vehicle(
                demand,
                magazines[np.random.randint(0,len(magazines))],
                VEHICLE_CAPACITY[np.random.randint(0,3)],
                False
            )
        )
    catVehicle = np.random.randint(0,numberOfVehicles)
    vehicles[catVehicle].isCatDriver = True
    return vehicles

def GenerateStartingConditions():
    points = GeneratePoints(NUMBER_OF_POINTS)
    magazines = list(filter(lambda x: x.isMagazine == True, points))
    vehicles = GenerateVehicles(magazines)
    return points, vehicles

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

p,v = GenerateStartingConditions()
for i in v:
    print(i)
