import math
import os
import numpy as np
from typing import Type
from copy import deepcopy
from Models.demand import Demand
from Models.exceptions import NoMoreClientsException
from Models.point import Point
from Models.vehicle import Vehicle
from engine.engine_interface import EngineInterface


class SingleVehicleEngine(EngineInterface):
    def go_to_next_magazine(self, vehicle: Vehicle):
        actual = Point(vehicle.x_coordinate, vehicle.y_coordinate)
        nearest_point = self.magazines[0]
        nearest_distance = actual.calculate_distance(nearest_point)

        for i in range(1, len(self.magazines)):
            distance = actual.calculate_distance(self.magazines[i])
            if distance < nearest_distance:
                nearest_point = self.magazines[i]
                nearest_distance = distance

        vehicle.move(nearest_point)
        max_demand = max([vehicle.capacity/5, int(os.environ['MAX_DEMAND'])])
        vehicle.demand = Demand(uranium=max_demand,
                                tuna=max_demand,
                                orange=max_demand)
        if vehicle.capacity >= 1500:
            self.global_demand_correction(vehicle)
        return nearest_distance, nearest_point

    def go_to_next_client(self, vehicle: Vehicle):
        not_done = list(filter(lambda client: client.not_done, self.clients))
        if len(not_done) == 0:
            raise NoMoreClientsException('No more clients')

        actual = Point(vehicle.x_coordinate, vehicle.y_coordinate)
        nearest_point = None
        nearest_2nd_point = None
        nearest_distance = None
        for i in range(len(not_done)):
            if vehicle.demand.can_satisfy(other=not_done[i].demand, max_total=vehicle.capacity):
                if nearest_point is None:
                    nearest_point = not_done[i]
                    nearest_distance = actual.calculate_distance(not_done[i])
                else:
                    distance = actual.calculate_distance(not_done[i])
                    if distance < nearest_distance:
                        nearest_2nd_point = nearest_point
                        nearest_point = not_done[i]
                        nearest_distance = distance

        if nearest_point is not None:
            if os.environ['FORTUNE_TELLER'] == 'True' and nearest_2nd_point is not None and len(not_done) > 3:
                dict ={}
                dict[nearest_point ] = self.see_the_future(deepcopy(vehicle), deepcopy(self.clients), deepcopy(nearest_point))
                dict[nearest_2nd_point] = self.see_the_future(deepcopy(vehicle), deepcopy(self.clients), deepcopy(nearest_2nd_point))
                dict = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1])}
                nearest_point = list(dict.keys())[0]
            vehicle.move(nearest_point)
            vehicle.demand -= nearest_point.demand
            nearest_point.demand = Demand(0, 0, 0)
        else:
            self.go_to_next_magazine(vehicle)

    def global_demand_correction(self, vehicle: Vehicle) -> list:
        not_done = list(filter(lambda client: client.not_done, self.clients))
        global_demand = Demand(uranium=0,
                                tuna=0,
                                orange=0)
        for i in not_done:
            global_demand += i.demand
        vehicle.demand.tuna += global_demand.tuna*(-1) if math.fabs(global_demand.tuna*(-1)) < vehicle.capacity/20 else np.sign(global_demand.tuna)*vehicle.capacity/20
        vehicle.demand.uranium += global_demand.uranium*(-1) if math.fabs(global_demand.uranium*(-1)) < vehicle.capacity/20 else np.sign(global_demand.uranium)*vehicle.capacity/20
        vehicle.demand.orange += global_demand.orange*(-1) if math.fabs(global_demand.orange*(-1)) < vehicle.capacity/20 else np.sign(global_demand.orange)*vehicle.capacity/20

    def see_the_future(self,  vehicle: Vehicle, points: list[Type[Point]], current_point: Point) -> bool:
        total_distance: int = 0
        not_done = list(filter(lambda client: client.not_done, points))
        for i in range(len(not_done)-3):
            dodanie, next_point=self.trip_forecast(vehicle, points, current_point)
            current_point = next_point
            total_distance += dodanie
        return total_distance

    def trip_forecast(self, vehicle: Vehicle, not_done: list[Type[Point]], actual: Point):
        not_done = list(filter(lambda client: client.not_done, not_done))

        if len(not_done) == 0:
            raise NoMoreClientsException('No more clients')
        nearest_point = None
        nearest_distance = None
        for i in range(len(not_done)):
            if vehicle.demand.can_satisfy(other=not_done[i].demand, max_total=vehicle.capacity):
                if nearest_point is None:
                    nearest_point = not_done[i]
                    nearest_distance = actual.calculate_distance(not_done[i])
                else:
                    distance = actual.calculate_distance(not_done[i])
                    if distance < nearest_distance:
                        nearest_point = not_done[i]
                        nearest_distance = distance

        if nearest_point is not None:
            vehicle.move(nearest_point)
            vehicle.demand -= nearest_point.demand
            nearest_point.demand = Demand(0, 0, 0)
            return nearest_distance, nearest_point
        else:
            nearest_distance, nearest_point = self.go_to_next_magazine(vehicle)
            return nearest_distance, nearest_point

    def compute(self) -> list[Type[Point]]:
        active_vehicles: list[Vehicle] = list(filter(lambda vehicle: not vehicle.is_cat_driver, self.vehicles))
        best_vehicle = active_vehicles[0]

        dem_sum = Demand(0, 0, 0)
        for point in self.clients:
            dem_sum += point.demand

        for i in range(1, len(active_vehicles)):
            if active_vehicles[i].capacity > best_vehicle.capacity:
                best_vehicle = active_vehicles[i]

        try:
            while True:
                self.go_to_next_client(best_vehicle)
        except NoMoreClientsException:
            pass

        return [*self.clients, *self.vehicles, *self.magazines]
