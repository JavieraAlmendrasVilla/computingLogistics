import random
from math import ceil

import numpy as np

from src.instance.instance import get_instance
from src.utils.feasibilityCheck import is_feasible


def calculate_distance_matrix(locations):
    num_locations = len(locations)
    distance_matrix = np.zeros((num_locations, num_locations))

    for i in range(num_locations):
        for j in range(num_locations):
            distance_matrix[i, j] = np.sqrt(
                (locations[i][0] - locations[j][0]) ** 2 + (locations[i][1] - locations[j][1]) ** 2)

    return distance_matrix


def calculate_route_distance(route, distance_matrix):
    length = 0
    for i in range(1, len(route)):
        length += distance_matrix[route[i - 1]][route[i]]
    return length


def calculate_total_distance(routes, distance_matrix):
    total_distance = 0

    for route in routes:

        total_distance += calculate_route_distance(route, distance_matrix)
    return total_distance


def create_feasible_initial_solution(instance, num_routes):
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
            if is_feasible(route_customers, data.demand, data.capacity,
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


def create_initial_solution_for_vrp(customers):
    depot = 0
    num_customers = len(customers)
    return [[depot, i, depot] for i in range(1, num_customers)]




