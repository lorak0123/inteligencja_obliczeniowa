import inspect
import os
import random

from dotenv import load_dotenv

from Services.starting_conditions_service import generate_starting_conditions
from Services.stats_service import CreateStatDataframe
from visualizer.map_visualizer import draw_point_map
import engine
from Services.test_service import RunTests


if __name__ == '__main__':
    load_dotenv()
    Engine = getattr(engine, os.environ.get('ENGINE', 'SingleVehicleEngine'))
    if os.environ.get('RANDOM_DATA', 'True') == 'False':
        random.seed(2)

    points = generate_starting_conditions(number_of_points=int(os.environ['NUMBER_OF_POINTS']),
                                          number_of_magazines=int(os.environ['NUMBER_OF_MAGAZINES']))
    multiVehicle = True

    engine = Engine(points)
    computed = engine.compute()
    statDataframe = CreateStatDataframe(computed, multiVehicle, False)
    print(statDataframe)
    draw_point_map(computed)

    RunTests(Engine, multiVehicle=multiVehicle, test_num=100)


