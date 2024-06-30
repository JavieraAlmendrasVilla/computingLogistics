import time
import numpy as np
from VRPTW import create_initial_solution, is_feasible, clarkewright_savings, calculate_distance_matrix
from instance import get_instance

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


def simulatedAnnealing(instance):
    vehicles, customers = get_instance(instance)

    if vehicles is None or customers is None:
        print("Instance data could not be loaded.")
        return

    capacity = vehicles['capacity']
    demand = customers['demand']
    ready_time = customers['ready_time']
    due_time = customers['due_time']
    service_time = customers['service_time']
    initial_routes = create_initial_solution(customers)
    distance_matrix = calculate_distance_matrix(customers['location'])

    current_routes = initial_routes.copy()
    best_routes = initial_routes.copy()
    current_distance = calculate_total_distance(current_routes, distance_matrix)
    best_distance = current_distance

    # Simulated Annealing parameters
    alpha = 0.1 * current_distance
    beta = 0.9
    time_limit = 1
    iterations = 100

    np.random.seed(0)

    start_time = time.time()
    #while time.time() - start_time < time_limit:
    while alpha > 0.0001:
        improve = False
        current_routes = clarkewright_savings(instance)
        for i in range(iterations):
            # Select a random route
            current_distance = calculate_total_distance(current_routes, distance_matrix)
            route_index = np.random.randint(0, len(current_routes))  # Index of the route
            route = current_routes[route_index] # list selected

            # Select two random customers
            if len(route) > 2:
                customer_1 = np.random.randint(1, len(route) - 1)  # Index of the first customer
                customer_2 = np.random.randint(1, len(route) - 1)  # Index of the second customer
                while customer_2 == customer_1:  # Ensure customer_1 and customer_2 are not the same
                    customer_2 = np.random.randint(1, len(route) - 1)

                # Swap customers within one route
                new_route = swap_customers_within_route(route, customer_1, customer_2, demand, capacity, ready_time,
                                                        due_time, service_time, distance_matrix)
                route_distance = calculate_route_distance(route, distance_matrix)
                new_route_distance = calculate_route_distance(new_route, distance_matrix)
                if new_route_distance < route_distance:
                    current_routes[route_index] = new_route
                    current_distance -= route_distance - new_route_distance
                    improve = True

            # Swap customers between two routes
            new_routes = swap_customers_between_routes(current_routes, demand, capacity, ready_time, due_time,
                                                       service_time, distance_matrix)
            new_routes_distance = calculate_total_distance(new_routes, distance_matrix)
            if new_routes_distance < current_distance:
                best_routes = new_routes
                best_distance = new_routes_distance
                improve = True

        if improve:
            alpha *= beta
        else:
            alpha = 0.1 * current_distance

    print("Best distance:", best_distance)
    print("Best routes:", best_routes)

    return best_distance, best_routes


def swap_customers_within_route(route, customer_1,customer_2, demand, capacity, ready_time, due_time, service_time, distance_matrix):
    new_route = route.copy()
        # swap customers
    new_route[customer_1], new_route[customer_2] = new_route[customer_2], new_route[customer_1]
    if is_feasible(new_route, demand, capacity, ready_time, due_time, service_time, distance_matrix):
            return new_route
    else:
        print("Swaping within route is infeasible.")
    return route

def swap_customers_between_routes(current_routes, demand, capacity, ready_time, due_time, service_time, distance_matrix):
    route_1 = np.random.randint(0, len(current_routes))  # index of the first route
    route_2 = np.random.randint(0, len(current_routes))  # index of the second route
    customer_1 = np.random.randint(1, len(current_routes[route_1]) - 1)  # index of the first customer
    customer_2 = np.random.randint(1, len(current_routes[route_2]) - 1)  # index of the second customer
    if route_1 != route_2 and current_routes[route_1][customer_1] != current_routes[route_2][customer_2]:
        new_route_1 = current_routes[route_1].copy()
        new_route_2 = current_routes[route_2].copy()
        new_route_1[customer_1], new_route_2[customer_2] = new_route_2[customer_2], new_route_1[customer_1]
        if is_feasible(new_route_1, demand, capacity, ready_time, due_time, service_time, distance_matrix) and is_feasible(
                new_route_2, demand, capacity, ready_time, due_time, service_time, distance_matrix):
            current_routes[route_1] = new_route_1
            current_routes[route_2] = new_route_2
        else:
            print("Swaping between routes is infeasible.")
    else:
        print("No customers to swap between routes.")
    return current_routes

if __name__ == '__main__':
    print(get_instance(1))
    simulatedAnnealing(1)
