import os
from typing import Type

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
        max_demand = max([vehicle.capacity/6, int(os.environ['MAX_DEMAND'])])
        vehicle.demand = Demand(uranium=max_demand,
                                tuna=max_demand,
                                orange=max_demand)

    def go_to_next_client(self, vehicle: Vehicle):
        not_done = list(filter(lambda client: client.not_done, self.clients))

        if len(not_done) == 0:
            raise NoMoreClientsException('No more clients')

        actual = Point(vehicle.x_coordinate, vehicle.y_coordinate)
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
        else:
            self.go_to_next_magazine(vehicle)

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
