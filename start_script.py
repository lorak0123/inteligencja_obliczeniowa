import os
from dotenv import load_dotenv

from Models.vehicle import Vehicle
from Services.starting_conditions_service import generate_starting_conditions
from engine.multiple_vehicles_engine import MultipleVehiclesEngine
from engine.single_vehicle_engine import SingleVehicleEngine
from visualizer.map_visualizer import draw_point_map

if __name__ == '__main__':
    load_dotenv()
    points = generate_starting_conditions(number_of_points=int(os.environ['NUMBER_OF_POINTS']),
                                          number_of_magazines=int(os.environ['NUMBER_OF_MAGAZINES']))

    # engine = SingleVehicleEngine(points)
    engine = MultipleVehiclesEngine(points)
    computed = engine.compute()

    print(f'Total distance: {sum([vehicle.total_distance for vehicle in list(filter(lambda x: isinstance(x, Vehicle), computed))])}')

    draw_point_map(computed)
