from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import numpy as np

from src.simulatedAnnealing.coolingSchedules import reduce_temperature
from src.simulatedAnnealing.n_opt import two_opt_operator, one_opt_operator
from src.utils.plots import visualize_routes, visualize_routes_sa
from src.utils.save import save_sa_data_and_solution
from src.utils.solution import createSolution
from src.simulatedAnnealing.calculations import create_feasible_initial_solution, calculate_total_distance, \
    calculate_distance_matrix
from src.instance.instance import get_instance
from src.simulatedAnnealing.unrolling import relocation, find_and_swap_nodes

path_to_repo = Path(__file__).parent.parent.parent.resolve()  # This is the path to the repository


@dataclass
class SimulatedAnnealing:
    starting_method: str
    initial_temperature: float
    alpha: float
    final_temperature: float
    cooling_schedule: str
    constant_k: float
    neighborhood_size: int
    neighborhood_selection: str

    def __post_init__(self):
        if self.neighborhood_selection not in ["unroll", "1_opt", "2_opt"]:
            raise ValueError("Neighborhood selection must be either 'unrolling' or 'swapping'")
        if self.cooling_schedule not in ["geometric", "cauchy", "logarithmic", "geometricMomentum"]:
            raise ValueError(
                "Cooling schedule must be either 'geometric', 'cauchy', 'logarithmic' or 'geometricMomentum'")


def getSimulatedAnneling():
    sa = SimulatedAnnealing(
        starting_method="feasible",
        initial_temperature=0.5,
        alpha=0.9,
        final_temperature=0.001,
        cooling_schedule="geometric",
        constant_k=0.7,
        neighborhood_size=5,
        neighborhood_selection="1_opt"
    )

    return sa


def simulatedAnnealing(dataset: int, sa: SimulatedAnnealing):
    startSearchClock = datetime.now().timestamp()
    data = get_instance(dataset)
    num_routes = data.num_vehicles
    distance_matrix = calculate_distance_matrix(data.locations)
    initial_routes = create_feasible_initial_solution(dataset, num_routes)
    visualize_routes(dataset, initial_routes, "initial_solution_for_sa", show=False, save=True)

    current_routes = initial_routes.copy()
    best_routes = initial_routes.copy()
    initial_distance = calculate_total_distance(current_routes, distance_matrix)
    print(f"Initial distance: {round(initial_distance)}")
    current_distance = initial_distance
    best_distance = current_distance

    # Simulated Annealing parameters
    initial_temperature = initial_distance * sa.initial_temperature
    current_temperature = initial_temperature
    k = sa.constant_k
    final_temperature = sa.final_temperature
    iterations = sa.neighborhood_size
    temperatures = []
    solutions = []
    accepted_solutions = []
    acceptance_probabilities = []

    np.random.seed(0)
    counter = 0
    print(
        f"Solution entered Simulated Annealing with {round(current_distance)} as initial solution and {round(current_temperature)} as initial temperature.")
    while current_temperature > final_temperature:
        print(f"Current temperature: {current_temperature}")
        new_routes = current_routes.copy()

        if sa.neighborhood_selection == "unroll":
            new_routes = relocation(new_routes, data.demand, data.capacity, data.ready_time, data.due_time, data.service_time, distance_matrix)
            new_routes = find_and_swap_nodes(new_routes, data.locations, data.demand, data.capacity, data.ready_time,
                                             data.due_time, data.service_time, distance_matrix)

        if sa.neighborhood_selection == "1_opt":
            new_routes = one_opt_operator(new_routes, data.demand, data.capacity, data.ready_time, data.due_time,
                                          data.service_time, distance_matrix)

        if sa.neighborhood_selection == "2_opt":
            new_routes = two_opt_operator(new_routes, data.demand, data.capacity, data.ready_time, data.due_time,
                                          data.service_time, distance_matrix)
        print(f"New routes: {new_routes}")
        new_distance = calculate_total_distance(new_routes, distance_matrix)
        solutions.append(new_distance)
        print(f"New distance: {round(new_distance)}")
        delta_distance = new_distance - current_distance
        if delta_distance < 0:
            print(f"Delta distance: {delta_distance}")
            current_routes = new_routes
            current_distance = new_distance
            solutions.append(current_distance)
            if new_distance < best_distance:
                best_routes = new_routes
                best_distance = new_distance
                print(f"New best distance: {round(best_distance)}")
        elif np.random.rand() < np.exp(-delta_distance / k * current_temperature):
            print(f"Delta distance: {delta_distance}")
            print(f"Exponent: {-delta_distance / k * current_temperature}")
            acceptance_probabilities.append(np.exp(-delta_distance / k * current_temperature))
            current_routes = new_routes
            current_distance = new_distance
            accepted_solutions.append(current_distance)
            print(
                f"Solution {round(current_distance)} accepted with probability {np.exp(-delta_distance / k * current_temperature)}")
            print(f"New best distance: {round(current_distance)}")
        if current_distance < best_distance:
            best_routes = current_routes
            best_distance = current_distance
            print(f"New best distance: {round(best_distance)}")
        counter += 1
        if counter % iterations == 0:
            current_temperature = reduce_temperature(current_temperature, sa)  ## review this
            temperatures.append(current_temperature)
            print(f"New Temperature: {current_temperature}")

    print(f"Temperature: {current_temperature}")
    print("Initial distance:", initial_distance)
    print("Best distance:", best_distance)
    print("Best routes:", best_routes)

    endSearchClock = datetime.now().timestamp()
    runtime = endSearchClock - startSearchClock
    print(f"Runtime: {runtime}")
    solution = createSolution(dataset, "Simulated Annealing", sa.neighborhood_selection, initial_routes, initial_distance,
                              best_distance, best_routes, runtime, temperatures, solutions, accepted_solutions,
                              acceptance_probabilities)
    visualize_routes_sa(dataset, solution.best_routes, sa, show=False, save=True)
    save_sa_data_and_solution(dataset, sa, solution)

    return solution

if __name__ == "__main__":
    sa = getSimulatedAnneling()
    simulatedAnnealing(20, sa)