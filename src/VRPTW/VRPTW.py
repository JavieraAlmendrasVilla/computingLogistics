from datetime import datetime

from src.instance.instance import get_instance

from src.simulatedAnnealing.calculations import calculate_total_distance, calculate_distance_matrix, \
    create_initial_solution_for_vrp
from src.utils.plots import visualize_routes
from src.utils.solution import createSolution
from src.utils.feasibilityCheck import is_feasible
from src.utils.save import save_solution


def clarkewright_savings(dataset):
    # Step 1: Calculate savings
    startSearchClock = datetime.now().timestamp()
    data = get_instance(dataset)
    num_customers = len(data.id)

    depot = 0

    distance_matrix = calculate_distance_matrix(data.locations)
    savings = {}

    for customer_1 in range(1, num_customers):
        for customer_2 in range(customer_1 + 1, num_customers):
            distance_i = distance_matrix[depot, customer_1]
            distance_j = distance_matrix[depot, customer_2]
            distance_ij = distance_matrix[customer_1, customer_2]
            savings[(customer_1, customer_2)] = distance_i + distance_j - distance_ij

    # Step 2: Sort savings in descending order
    sorted_savings = sorted(savings.items(), key=lambda x: x[1], reverse=True)

    # Step 3: Initialize routes and merge based on savings
    routes = create_initial_solution_for_vrp(data.id)
    visualize_routes(dataset, routes, "initial_solution_for_savings", show=False, save=True)
    initial_distance = calculate_total_distance(routes, distance_matrix)
    capacity = data.capacity  # Assuming all vehicles have the same capacity

    for (customer_1, customer_2), saving in sorted_savings:
        route_i = None
        route_j = None
        for route in routes:
            if customer_1 in route:
                route_i = route
            if customer_2 in route:
                route_j = route
            if route_i and route_j:
                break

        if route_i != route_j and route_i and route_j:
            new_route = route_i[:-1] + route_j[1:]
            if is_feasible(new_route, data.demand, capacity, data.ready_time, data.due_time, data.service_time,
                           distance_matrix):
                routes.remove(route_i)
                routes.remove(route_j)
                routes.append(new_route)

    # Step 4: Adjust routes to respect time windows
    feasible_routes = []
    for route in routes:
        if is_feasible(route, data.demand, capacity, data.ready_time, data.due_time, data.service_time,
                       distance_matrix):
            # Ensure the route starts and ends with the depot
            if route[0] != depot:
                route.insert(0, depot)
            if route[-1] != depot:
                route.append(depot)
            feasible_routes.append(route)
        else:
            print(f"Route {route} is not feasible due to time window constraints.")

    for i, route in enumerate(feasible_routes):
        print(f"Route {i}: {route}")

    best_distance = calculate_total_distance(feasible_routes, distance_matrix)
    endSearchClock = datetime.now().timestamp()
    runtime = endSearchClock - startSearchClock

    print(f"Saving method solution: {feasible_routes}")
    temperatures = []
    solutions = []
    accepted_solutions = []
    acceptance_probabilities = []
    visualize_routes(dataset, feasible_routes, "clarkewright_savings", show=False, save=True)
    solution = createSolution(dataset,"Clarkewright_Savings", "none", routes, initial_distance, best_distance, feasible_routes,runtime,
                   temperatures, solutions, accepted_solutions, acceptance_probabilities)
    save_solution(dataset, solution)
    print(f"Runtime: {runtime}")
    print(f"Initial distance: {initial_distance}")
    print(f"Best distance: {solution.best_distance}")
    print(f"Best routes: {solution.best_routes}")
    return solution


