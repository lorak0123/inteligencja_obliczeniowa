from typing import Type
import pandas as pd
import numpy as np

from Models.point import Point, Magazine, Client
from Models.vehicle import Vehicle


class StatDataRow:
    def __init__(self, capacity: int,
                 total_dist: float,
                 points: int,
                 mag_returns: int,
                 avg_mag_dist: float,  # z punktu do magazynu i z magazynu do punktu
                 avg_point_dist: float,
                 std_point_dist: float,
                 avg_v_efficiency: float,  # wartosc bezwzgledna z towaru /dystans
                 total_cargo: int,
                 total_tuna: int,
                 total_orange: int,
                 total_uran: int,
                 total_tuna_plus: int,
                 total_tuna_minus: int,
                 total_orange_plus: int,
                 total_orange_minus: int,
                 total_uran_plus: int,
                 total_uran_minus: int):
        self.capacity = capacity
        self.total_dist = total_dist
        self.points = points
        self.mag_returns = mag_returns
        self.avg_mag_dist = avg_mag_dist
        self.avg_point_dist = avg_point_dist
        self.std_point_dist = std_point_dist
        self.avg_v_efficiency = avg_v_efficiency
        self.total_cargo = total_cargo
        self.total_tuna = total_tuna
        self.total_orange = total_orange
        self.total_uran = total_uran
        self.total_tuna_plus = total_tuna_plus
        self.total_tuna_minus = total_tuna_minus
        self.total_orange_plus = total_orange_plus
        self.total_orange_minus = total_orange_minus
        self.total_uran_plus = total_uran_plus
        self.total_uran_minus = total_uran_minus


def CreateStatRows(points: list[Type[Point]]) -> pd.DataFrame:
    vehicles: Vehicle = list(filter(lambda point: isinstance(point, Vehicle), points))

    stat_dataframe_rows = []
    for vehicle in vehicles:
        mag_returns = 0
        points_num = 0
        avg_mag_dist = []
        total_cargo = 0
        total_tuna = 0
        total_orange = 0
        total_uran = 0
        total_tuna_plus = 0
        total_tuna_minus = 0
        total_orange_plus = 0
        total_orange_minus = 0
        total_uran_plus = 0
        total_uran_minus = 0
        for point in vehicle.directions:
            if isinstance(point, Magazine):
                mag_returns += 1
            if isinstance(point, Client):
                points_num += 1
                total_cargo += point.start_demand.uranium + point.start_demand.tuna + point.start_demand.orange
                total_tuna_plus += point.start_demand.tuna if point.start_demand.tuna > 0 else 0
                total_tuna_minus += point.start_demand.tuna if point.start_demand.tuna < 0 else 0
                total_orange_plus += point.start_demand.orange if point.start_demand.orange > 0 else 0
                total_orange_minus += point.start_demand.orange if point.start_demand.orange < 0 else 0
                total_uran_plus += point.start_demand.uranium if point.start_demand.uranium > 0 else 0
                total_uran_minus += point.start_demand.uranium if point.start_demand.uranium < 0 else 0
                total_uran = total_uran_plus + total_uran_minus
                total_orange = total_orange_plus + total_orange_minus
                total_tuna = total_tuna_plus + total_tuna_minus
        point_distances = []
        for i in range(len(vehicle.directions) - 1):
            point_distances.append(vehicle.directions[i].calculate_distance(vehicle.directions[i + 1]))
            if isinstance(vehicle.directions[i], Magazine):
                avg_mag_dist.append(vehicle.directions[i].calculate_distance(vehicle.directions[i + 1]))
                avg_mag_dist.append(vehicle.directions[i].calculate_distance(vehicle.directions[i - 1]))
        total_dist = sum(point_distances)
        efficiency = 0
        if total_dist > 0:
            efficiency = (total_tuna_plus + (-1) * total_tuna_minus + total_orange_plus + (-1) * total_orange_minus
                          + total_uran_plus + (-1) * total_uran_minus) / total_dist
        stat_dataframe_rows.append(StatDataRow(vehicle.capacity,
                                               total_dist,
                                               points_num,
                                               mag_returns,
                                               np.mean(avg_mag_dist) if len(avg_mag_dist) > 0 else 0,
                                               np.mean(point_distances) if len(point_distances) > 0 else 0,
                                               np.std(point_distances) if len(point_distances) > 0 else 0,
                                               efficiency,
                                               total_cargo,
                                               total_tuna,
                                               total_orange,
                                               total_uran,
                                               total_tuna_plus,
                                               total_tuna_minus,
                                               total_orange_plus,
                                               total_orange_minus,
                                               total_uran_plus,
                                               total_uran_minus))
    return stat_dataframe_rows

def CreateStatDataframe(points: list[Type[Point]]):
    stat_dataframe_rows = CreateStatRows(points)
    pd.options.display.width = 0
    df = pd.DataFrame([o.__dict__ for o in stat_dataframe_rows])
    df.loc["Total"] = df.sum()
    df.loc["Avg"] = df.loc["Total"] / (df.shape[0] - 1)
    return df

def BuildTestDataframe(stat_dataframe_rows: list[Type[StatDataRow]]):
    pd.options.display.width = 0
    df = pd.DataFrame([o.__dict__ for o in stat_dataframe_rows])
    df.loc["Total"] = df.sum()
    df.loc["Avg"] = df.loc["Total"] / (df.shape[0] - 1)
    return df.loc['Avg']