import os
import random
import pandas as pd

from Services.starting_conditions_service import generate_starting_conditions
from Services.stats_service import CreateStatDataframe, CreateStatRows, BuildTestDataframe
from engine.multiple_vehicles_engine import MultipleVehiclesEngine
from engine.single_vehicle_engine import SingleVehicleEngine

import sys


def progress_bar(count, total, status='', bar_len=60):
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    fmt = '[%s] %s%s ...%s' % (bar, percents, '%', status)
    print('\b' * len(fmt), end='')
    sys.stdout.write(fmt)
    sys.stdout.flush()


def RunTests(engine_class, multiVehicle: bool, test_num: int):
    if os.environ.get('RANDOM_DATA', 'True') == 'False':
        random.seed(1)
    stat_data_rows = []
    for i in range(test_num):
        points = generate_starting_conditions(number_of_points=int(os.environ['NUMBER_OF_POINTS']),
                                              number_of_magazines=int(os.environ['NUMBER_OF_MAGAZINES']))

        engine = engine_class(points)
        computed = engine.compute()
        stat_data_rows.extend(CreateStatRows(computed, multiVehicle, True))
        progress_bar(i, test_num)
    test_data = BuildTestDataframe(stat_data_rows)
    print('\n')
    print(test_data)
