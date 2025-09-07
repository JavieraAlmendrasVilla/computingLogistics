from pathlib import Path
import sys

from src.VRPTW.VRPTW import clarkewright_savings
from src.simulatedAnnealing.simulatedAnnealing_soft_window import SimulatedAnnealingSoft, getSimulatedAnnelingSoft, \
    simulatedAnnealing_soft

path = Path(__file__).parent.resolve()
sys.argv.append(str(path))
from src.simulatedAnnealing.simulatedAnnealing import simulatedAnnealing, getSimulatedAnneling, SimulatedAnnealing
from sklearn.model_selection import ParameterGrid


def tune_parameters(dataset: int):
    params = {
        'starting_method': ["feasible"],
        'initial_temperature': [0.1, 0.5, 1],
        'alpha': [0.6, 0.7, 0.8, 0.9],
        'final_temperature': [0.01],
        'cooling_schedule': ["geometric"],
        'constant_k': [0.7, 0.8, 1],
        'neighborhood_size': [5, 10],
        'neighborhood_selection': ["unroll", "1_opt", "2_opt"]
    }

    # Run simulated annealing for all parameter combinations and store results
    results = []

    for param in ParameterGrid(params):
        result = simulatedAnnealing(dataset, SimulatedAnnealing(**param))
        results.append({
            "start_method": param["starting_method"],
            "neighborhood_definition": param["neighborhood_selection"],
            "initial_temperature": param["initial_temperature"],
            "final_temperature": param["final_temperature"],
            "cooling_schedule": param["cooling_schedule"],
            "alpha": param["alpha"],
            "iterations": param["neighborhood_size"],
            "result": result
        })


def tune_soft_parameters(dataset: int):
    params = {
        'starting_method': ["feasible"],
        'initial_temperature': [1],
        'alpha': [0.9],
        'final_temperature': [0.01],
        'cooling_schedule': ["geometric"],
        'constant_k': [0.7],
        'neighborhood_size': [10],
        'neighborhood_selection': ["unroll", "1_opt", "2_opt"],
        'penalty_too_early': [1.0],
        'penalty_too_late': [1.0, 1.5, 2.0],
        'total_penalty': [400, 500]
    }

    # Run simulated annealing for all parameter combinations and store results
    results = []

    for param in ParameterGrid(params):
        result = simulatedAnnealing_soft(dataset, SimulatedAnnealingSoft(**param))
        results.append({
            "start_method": param["starting_method"],
            "neighborhood_definition": param["neighborhood_selection"],
            "initial_temperature": param["initial_temperature"],
            "final_temperature": param["final_temperature"],
            "cooling_schedule": param["cooling_schedule"],
            "alpha": param["alpha"],
            "iterations": param["neighborhood_size"],
            "result": result
        })


def run(dataset: int):
    sa = getSimulatedAnneling()
    simulatedAnnealing(dataset, sa)


if __name__ == "__main__":
    number_of_nodes = 9
    run(number_of_nodes)
