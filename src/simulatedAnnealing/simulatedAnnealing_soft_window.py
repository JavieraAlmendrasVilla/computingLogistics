import random
from dataclasses import dataclass
from datetime import datetime
from math import ceil

import numpy as np

from src.instance.instance import get_instance
from src.simulatedAnnealing.calculations import calculate_distance_matrix, \
    calculate_total_distance, create_feasible_initial_solution
from src.simulatedAnnealing.coolingSchedules import reduce_temperature
from src.simulatedAnnealing.unrolling import calculate_distance

from src.utils.plots import visualize_routes, visualize_routes_sa_soft
from src.utils.save import save_sa_data_and_solution_soft
from src.utils.solution import createSolution
from src.utils.feasibilityCheck import is_feasible


@dataclass
class SimulatedAnnealingSoft:
    starting_method: str
    initial_temperature: float
    alpha: float
    final_temperature: float
    cooling_schedule: str
    constant_k: float
    neighborhood_size: int
    neighborhood_selection: str
    penalty_too_early: float
    penalty_too_late: float
    total_penalty: float

    def __post_init__(self):
        if self.neighborhood_selection not in ["unroll", "1_opt", "2_opt"]:
            raise ValueError("Neighborhood selection must be either 'unrolling' or 'swapping'")


def getSimulatedAnnelingSoft():
    sa = SimulatedAnnealingSoft(
        starting_method="feasible",
        initial_temperature=1,
        alpha=0.9,
        final_temperature=0.01,
        cooling_schedule="geometric",
        constant_k=0.7,
        neighborhood_size=10,
        neighborhood_selection="unroll",
        penalty_too_early=1,
        penalty_too_late=1,
        total_penalty=0
    )

    return sa


def simulatedAnnealing_soft(dataset: int, sa: SimulatedAnnealingSoft):
    startSearchClock = datetime.now().timestamp()
    data = get_instance(dataset)
    num_routes = data.num_vehicles
    distance_matrix = calculate_distance_matrix(data.locations)
    initial_routes = create_feasible_initial_solution(dataset, num_routes)
    visualize_routes(dataset, initial_routes, "initial_solution_soft_for_sa", show=False, save=True)

    initial_distance = calculate_total_distance(initial_routes, distance_matrix)
    print(f"Initial distance: {round(initial_distance)}")
    current_routes = initial_routes.copy()
    best_routes = initial_routes.copy()

    current_penalty = sum_penalty(sa, current_routes, data.ready_time, data.due_time, data.service_time, distance_matrix)
    best_penalty = current_penalty

    ## distance
    current_distance = initial_distance
    best_distance = current_distance

    # Simulated Annealing parameters
    initial_temperature = sa.initial_temperature
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

        new_routes = current_routes.copy()

        if sa.neighborhood_selection == "unroll":
            new_routes = find_and_swap_nodes_soft(new_routes, data.locations, data.demand, data.capacity,
                                                  data.ready_time, data.due_time, data.service_time, distance_matrix)

            new_routes = relocation_soft(new_routes, data.demand, data.capacity, data.ready_time, data.due_time,
                                         data.service_time,
                                         distance_matrix)
        if sa.neighborhood_selection == "1_opt":
            new_routes = one_opt_operator_soft(new_routes, data.demand, data.capacity, data.ready_time,
                                               data.due_time,
                                               data.service_time, distance_matrix)

        if sa.neighborhood_selection == "2_opt":
            new_routes = two_opt_operator_soft(new_routes, data.demand, data.capacity, data.ready_time,
                                               data.due_time,
                                               data.service_time, distance_matrix)

        # Evaluate the new solution with penalties for soft time window violations
        new_penalty = sum_penalty(sa, new_routes, data.ready_time, data.due_time, data.service_time,
                                  distance_matrix)
        new_distance = calculate_total_distance(new_routes, distance_matrix)

        solutions.append(new_distance)
        print(f"New distance: {round(new_distance)}")
        delta = new_distance - current_distance

        if delta < 0 and new_penalty < sa.total_penalty:
            print(f"Delta distance: {delta}")
            current_routes = new_routes
            current_distance = new_distance
            current_penalty = new_penalty
            solutions.append(current_distance)
            if new_distance < best_distance and new_penalty < sa.total_penalty:
                best_routes = new_routes
                best_distance = new_distance
                best_penalty = new_penalty
                print(f"New best distance: {round(best_distance)}")
            elif np.random.rand() < np.exp(-delta / k * current_temperature):
                acceptance_probabilities.append(np.exp(-delta / k * current_temperature))
                current_routes = new_routes
                current_distance = new_distance
                current_penalty = new_penalty
                accepted_solutions.append(current_distance)
                print(
                    f"Solution {round(current_distance)} accepted with probability {np.exp(-delta / k * current_temperature)}")
                print(f"New best distance: {round(current_distance)}")
        if current_distance < best_distance and current_penalty < sa.total_penalty:
            best_routes = current_routes
            best_distance = current_distance
            best_penalty = current_penalty
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
    print("Best penalty:", best_penalty)

    endSearchClock = datetime.now().timestamp()
    runtime = endSearchClock - startSearchClock
    print(f"Runtime: {runtime}")
    solution = createSolution(dataset, "Simulated Annealing Soft", sa.neighborhood_selection, initial_routes,
                              initial_distance,
                              best_distance, best_routes, runtime, temperatures, solutions, accepted_solutions,
                              acceptance_probabilities)
    save_sa_data_and_solution_soft(dataset, sa, solution)
    visualize_routes_sa_soft(dataset, solution.best_routes, sa, show=False, save=True)
    return solution


def create_feasible_soft_initial_solution(instance, num_routes):
    random.seed(0)
    data = get_instance(instance)
    num_customers = len(data.id) - 1

    # Convert customers data into a list of dictionaries for easier manipulation
    customers_list = [
        {'id': data.id[i], 'location': data.locations[i], 'demand': data.demand[i],
         'ready_time': data.ready_time[i], 'due_time': data.due_time[i],
         'service_time': data.service_time[i]} for i in range(1, num_customers + 1)
    ]

    # Sort customers by their ready time
    sorted_customers_by_ready_time = sorted(customers_list, key=lambda x: x['ready_time'])

    # Extract sorted IDs for route creation
    sorted_ids = [customer['id'] for customer in sorted_customers_by_ready_time]

    # Distance matrix (assuming it's available)
    distance_matrix = calculate_distance_matrix(data.locations)
    n_customers_per_route = ceil(num_customers / num_routes)

    while True:
        # Shuffle sorted IDs to randomize selection
        random.shuffle(sorted_ids)

        # Create routes
        routes = []
        for i in range(0, num_customers, n_customers_per_route):
            route_customers = [0]  # Start with depot
            for j in range(n_customers_per_route):
                if i + j < num_customers:
                    route_customers.append(sorted_ids[i + j])
            route_customers.append(0)  # End with depot

            # Check feasibility of the route
            if is_feasible_soft(route_customers, data.demand, data.capacity,
                                data.ready_time, data.due_time, data.service_time, distance_matrix):
                routes.append(route_customers)
            else:
                break  # Break if current route is not feasible

        # Check if all customers are included exactly once
        if len(routes) == ceil(num_customers / n_customers_per_route):
            break  # Break if feasible solution is found

    # Output the initial solution
    print(f"Initial solution: {routes}")
    return routes


def sum_penalty(sa, routes, ready_time, due_time, service_time, distance_matrix):
    total_penalty = 0
    total_distance = 0

    for route in routes:
        current_time = 0
        route_distance = 0

        for i in range(1, len(route)):
            customer = route[i]

            # Calculate travel time from previous customer to current customer
            travel_time = distance_matrix[route[i - 1]][customer]
            current_time += travel_time
            route_distance += travel_time

            # Check if current time is within the hard time window [LBi, UBi]
            if current_time < ready_time[customer]:
                # Penalty for arriving too early (soft window: [LBi, ai))
                penalty = (ready_time[customer] - current_time) * sa.penalty_too_early
                total_penalty += penalty

            if ready_time[customer] <= current_time <= due_time[customer]:
                penalty = 0
                total_penalty += penalty

            # Check if current time is within the hard time window [ai, bi]
            if current_time > due_time[customer]:
                # Penalty for arriving too late (soft window: (bi, UBi])
                penalty = (current_time - due_time[customer]) * sa.penalty_too_late
                total_penalty += penalty

            # Add service time
            current_time += service_time[customer]

        total_distance += route_distance

    print(f"Total distance: {round(total_distance)}")
    print(f"Total penalty: {round(total_penalty)}")

    return total_penalty


def is_feasible_soft(route, demand, capacity, ready_time, due_time, service_time, distance_matrix):
    current_time = 0
    total_demand = 0
    print(f"Checking feasibility of route {route}.")
    for i in range(1, len(route) - 1):
        customer = route[i]
        total_demand += demand[customer]
        travel_time = distance_matrix[route[i - 1]][customer]
        current_time += travel_time
        if ready_time[customer] <= current_time < (
                due_time[customer] - service_time[customer]):
            if total_demand <= capacity:
                return True
        if current_time < ready_time[customer]:
            current_time = ready_time[customer]
        if current_time > due_time[customer]:
            return False
        current_time += service_time[customer]
    result = total_demand <= capacity
    if result:
        print(f"Route {route} is feasible.")
    else:
        print(f"Route {route} is not feasible due to capacity constraints.")
    return result


### Neighborhood operators

def one_opt_operator_soft(routes, demand, capacity, ready_time, due_time, service_time, distance_matrix):
    print("Applying 1-Opt operator.")
    num_routes = len(routes)

    # Select two different random routes
    route_indices = random.sample(range(num_routes), 2)
    route1_index, route2_index = route_indices[0], route_indices[1]
    route1, route2 = routes[route1_index], routes[route2_index]

    # Randomly select a customer (excluding depot) to move between routes
    if len(route1) <= 2 or len(route2) <= 2:
        print("Routes are too short to apply 1-Opt.")
        return routes

    customer_index = random.randint(1, len(route1) - 2)
    customer = route1[customer_index]

    # Check if moving customer from route1 to route2 is feasible
    new_route1 = route1[:customer_index] + route1[customer_index + 1:]
    new_route2 = route2[:]

    if is_feasible_soft(new_route2 + [customer], demand, capacity, ready_time, due_time, service_time,
                        distance_matrix):
        new_route2.append(customer)
        routes[route1_index] = new_route1
        routes[route2_index] = new_route2
        print(f"1-Opt operator applied successfully.")
    else:
        print(f"1-Opt operator resulted in infeasible routes. Reverting.")

    return routes


def two_opt_operator_soft(routes, demand, capacity, ready_time, due_time, service_time, distance_matrix):
    print("Applying 2-Opt operator.")
    num_routes = len(routes)

    # Select two different random routes
    route_indices = random.sample(range(num_routes), 2)
    route1_index, route2_index = route_indices[0], route_indices[1]
    route1, route2 = routes[route1_index], routes[route2_index]

    # Randomly select two different customers (excluding depot) to swap between routes
    if len(route1) <= 2 or len(route2) <= 2:
        print("Routes are too short to apply 2-Opt.")
        return routes

    customer_indices = random.sample(range(1, len(route1) - 1), 2)
    customer1_index, customer2_index = customer_indices[0], customer_indices[1]

    customer1 = route1[customer1_index]
    customer2 = route2[customer2_index]

    # Swap customers between routes
    new_route1 = route1[:customer1_index] + [customer2] + route1[customer1_index + 1:]
    new_route2 = route2[:customer2_index] + [customer1] + route2[customer2_index + 1:]

    # Check feasibility of new routes
    if is_feasible_soft(new_route1, demand, capacity, ready_time, due_time, service_time, distance_matrix) and \
            is_feasible_soft(new_route2, demand, capacity, ready_time, due_time, service_time, distance_matrix):
        routes[route1_index] = new_route1
        routes[route2_index] = new_route2
        print(f"2-Opt operator applied successfully.")
    else:
        print(f"2-Opt operator resulted in infeasible routes. Reverting.")

    return routes


#### unroll

def find_and_swap_nodes_soft(routes, locations, demand, capacity, ready_time, due_time, service_time,
                             distance_matrix):
    """
    Find nodes i and i+1 such that distance(i, i+2) < distance(i, i+1), and swap i+1 and i+2.
    Ignore the depot nodes at the beginning and end of the route.
    Check feasibility of the new route after the swap.
    """
    new_routes = routes.copy()
    num_routes = len(routes)

    # Select a random route
    route_indices = random.sample(range(num_routes), 1)
    print(f"route indeces: {route_indices}")

    route_index = route_indices[0]
    print(f"route index: {route_index}")
    route = routes[route_index]
    print(f"Route: {route}")

    print(f"Location: {locations}")
    num_nodes = len(route)
    for node_index in range(1, num_nodes - 2):
        # Skip depot nodes

        if node_index == 0 or node_index + 2 == num_nodes - 1:
            continue

        # Calculate distances
        dist_i_i1 = calculate_distance(locations[route[node_index]], locations[node_index + 1])
        print(f"Distance between {route[node_index]} and {route[node_index + 1]}: {dist_i_i1}")
        dist_i_i2 = calculate_distance(locations[route[node_index]], locations[route[node_index + 2]])
        print(f"Distance between {route[node_index]} and {route[node_index + 2]}: {dist_i_i2}")

        # Check condition for swap
        if dist_i_i2 < dist_i_i1:
            # Swap nodes i+1 and i+2
            new_route = route[:]
            new_route[node_index + 1], new_route[node_index + 2] = new_route[node_index + 2], new_route[node_index + 1]
            print(f"Swapping nodes {route[node_index + 1]} and {route[node_index + 2]} in route {route_index}.")

            # Check feasibility of the new route
            if is_feasible_soft(new_route, demand, capacity, ready_time, due_time, service_time, distance_matrix):
                new_routes[route_index] = new_route
                print(f"Feasible route after swap: {new_routes}.")
                return new_routes
            else:
                print("Infeasible route after swap. Reverting.")

    return routes


def relocation_soft(routes, demand, capacity, ready_time, due_time, service_time, distance_matrix):
    print("Relocation process started.")

    num_routes = len(routes)

    # Select two different random routes
    route_indices = random.sample(range(num_routes), 2)
    route1_index, route2_index = route_indices[0], route_indices[1]
    route1, route2 = routes[route1_index], routes[route2_index]

    # Ensure both routes have more than two nodes (excluding depots)
    if len(route1) <= 2 or len(route2) <= 2:
        print("Routes are too short to apply Relocation.")
        return routes

    # Randomly select a customer (excluding depot) to move from route1 to route2
    customer_index = random.randint(1, len(route1) - 2)
    customer = route1[customer_index]

    # Create new routes for feasibility check
    new_route1 = route1[:customer_index] + route1[customer_index + 1:]
    new_route2 = route2[:]
    new_route2.insert(random.randint(1, len(new_route2) - 1), customer)

    # Check if the new routes are feasible
    if is_feasible_soft(new_route1, demand, capacity, ready_time, due_time, service_time, distance_matrix) and \
            is_feasible_soft(new_route2, demand, capacity, ready_time, due_time, service_time, distance_matrix):
        routes[route1_index] = new_route1
        routes[route2_index] = new_route2
        print(
            f"Relocation applied successfully. Moved customer {customer} from route {route1_index} to route {route2_index}.")
    else:
        print(f"Relocation resulted in infeasible routes. Reverting.")

    return routes


if __name__ == '__main__':
    sa = getSimulatedAnnelingSoft()
    simulatedAnnealing_soft(9, sa)
