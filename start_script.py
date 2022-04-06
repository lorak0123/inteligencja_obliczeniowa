import os
import random

from dotenv import load_dotenv

from Models.vehicle import Vehicle
from Services.starting_conditions_service import generate_starting_conditions
from Services.stats_service import CreateStatDataframe
from engine.multiple_vehicles_engine import MultipleVehiclesEngine
from engine.single_vehicle_engine import SingleVehicleEngine
from visualizer.map_visualizer import draw_point_map
from Services.test_service import RunTests


if __name__ == '__main__':
    load_dotenv()
    if os.environ.get('RANDOM_DATA', 'True') == 'False':
        random.seed(1)

    points = generate_starting_conditions(number_of_points=int(os.environ['NUMBER_OF_POINTS']),
                                          number_of_magazines=int(os.environ['NUMBER_OF_MAGAZINES']))

    # engine = SingleVehicleEngine(points)
    # engine = MultipleVehiclesEngine(points)
    # computed = engine.compute()
    # statDataframe = CreateStatDataframe(computed)
    # print(statDataframe)

    # draw_point_map(computed)
    RunTests(multiVehicle=True, test_num=1000)
