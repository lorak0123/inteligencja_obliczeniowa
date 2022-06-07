import math
import os
from typing import Type

from Models.demand import Demand
from Models.point import Point, Client
from Models.vehicle import Vehicle
from engine.multiple_vehicles_engine import MultipleVehiclesEngine


class MultipleVehiclesEngineV2(MultipleVehiclesEngine):
    def split_into_clusters(self, vehicles: list[Vehicle]) -> dict:
        clusters = super().split_into_clusters(vehicles)
        clusters_keys = list(clusters.keys())
        for i in range(len(clusters_keys) - 1):
            cluster_clients: list[Client] = list(filter(
                lambda point: isinstance(point, Client), clusters[clusters_keys[i]]
            ))
            sum_demand = Demand(0, 0, 0)

            for demand in [client.demand for client in cluster_clients]:
                sum_demand += demand

            next_cluster_clients: list[Client] = list(filter(
                lambda point: isinstance(point, Client), clusters[clusters_keys[i + 1]]
            ))
            while True:
                best_client = next_cluster_clients[0]
                for c in range(1, len(next_cluster_clients)):
                    if sum_demand + next_cluster_clients[c].demand < sum_demand + best_client.demand:
                        best_client = next_cluster_clients[c]

                if sum_demand < sum_demand + best_client.demand:
                    break

                sum_demand += best_client.demand
                clusters[clusters_keys[i]].append(best_client)
                clusters[clusters_keys[i + 1]].remove(best_client)
                next_cluster_clients.remove(best_client)

        return clusters
