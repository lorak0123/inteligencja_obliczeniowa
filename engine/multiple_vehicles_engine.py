import math
import os
from typing import Type

from Models.point import Point
from Models.vehicle import Vehicle
from engine.engine_interface import EngineInterface
from engine.single_vehicle_engine import SingleVehicleEngine


class MultipleVehiclesEngine(EngineInterface):
    def split_into_clusters(self, vehicles: list[Vehicle]) -> dict:
        number_of_clusters = len(vehicles)
        map_size_x = int(os.environ['MAP_SIZE_X'])
        map_size_y = int(os.environ['MAP_SIZE_Y'])
        clusters = {}
        for i in range(number_of_clusters):
            degree = 360 / number_of_clusters * i
            x = map_size_x * math.sin(math.radians(degree)) / 10 + map_size_x / 2
            y = map_size_y * math.cos(math.radians(degree)) / 10 + map_size_y / 2
            clusters[Point(x, y)] = []

        for point in self.clients:
            tmp_center = None
            tmp_distance = None
            for cluster_center in clusters.keys():
                if tmp_center is None or point.calculate_distance(cluster_center) < tmp_distance:
                    tmp_center = cluster_center
                    tmp_distance = point.calculate_distance(cluster_center)

            clusters[tmp_center].append(point)

        for cluster_center in clusters.keys():
            best_vehicle = None
            best_vehicle_distance = None
            for vehicle in vehicles:
                if best_vehicle is None or cluster_center.calculate_distance(vehicle) < best_vehicle_distance:
                    best_vehicle = vehicle
                    best_vehicle_distance = cluster_center.calculate_distance(vehicle)

            clusters[cluster_center].append(best_vehicle)
            vehicles.remove(best_vehicle)

        return clusters

    def compute(self) -> list[Type[Point]]:
        active_vehicles: list[Vehicle] = list(filter(lambda vehicle: not vehicle.is_cat_driver, self.vehicles))
        clusters = self.split_into_clusters(active_vehicles)

        res = []
        for cluster in clusters.values():
            engine = SingleVehicleEngine([*cluster, *self.magazines])
            res += engine.compute()

        return [*res]
