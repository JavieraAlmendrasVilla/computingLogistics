import random

from src.utils.feasibilityCheck import is_feasible


def one_opt_operator(routes, demand, capacity, ready_time, due_time, service_time, distance_matrix):
    print("Applying 1-Opt operator.")
    num_routes = len(routes)

    # Select two different random routes
    route_indices = random.sample(range(num_routes), 2)
    route1_index, route2_index = route_indices[0], route_indices[1]
    route1, route2 = routes[route1_index], routes[route2_index]

    # Ensure both routes have more than two nodes (excluding depots)
    if len(route1) <= 2 or len(route2) <= 2:
        print("Routes are too short to apply 1-Opt.")
        return routes

    # Randomly select a customer (excluding depot) to move from route1 to route2
    customer_index = random.randint(1, len(route1) - 2)
    customer = route1[customer_index]

    # Create new routes for feasibility check
    new_route1 = route1[:customer_index] + route1[customer_index + 1:]
    new_route2 = route2[:]
    new_route2.insert(random.randint(1, len(new_route2) - 1), customer)

    # Check if the new routes are feasible
    if is_feasible(new_route1, demand, capacity, ready_time, due_time, service_time, distance_matrix) and \
       is_feasible(new_route2, demand, capacity, ready_time, due_time, service_time, distance_matrix):
        routes[route1_index] = new_route1
        routes[route2_index] = new_route2
        print(f"1-Opt operator applied successfully. Moved customer {customer} from route {route1_index} to route {route2_index}.")
    else:
        print(f"1-Opt operator resulted in infeasible routes. Reverting.")

    return routes


def two_opt_operator(routes, demand, capacity, ready_time, due_time, service_time, distance_matrix):
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
    if is_feasible(new_route1, demand, capacity, ready_time, due_time, service_time, distance_matrix) and \
            is_feasible(new_route2, demand, capacity, ready_time, due_time, service_time, distance_matrix):
        routes[route1_index] = new_route1
        routes[route2_index] = new_route2
        print(f"2-Opt operator applied successfully.")
    else:
        print(f"2-Opt operator resulted in infeasible routes. Reverting.")

    return routes



