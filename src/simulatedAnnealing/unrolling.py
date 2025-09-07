import math
import random

from src.VRPTW.VRPTW import is_feasible


def calculate_distance(location1, location2):
    """
    Calculate Euclidean distance between two locations.
    """
    return math.sqrt((location1[0] - location2[0]) ** 2 + (location1[1] - location2[1]) ** 2)


#### Swap vehicles when the route coincides with itself

def find_and_swap_nodes(routes, locations, demand, capacity, ready_time, due_time, service_time, distance_matrix):
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
            if is_feasible(new_route, demand, capacity, ready_time, due_time, service_time, distance_matrix):
                new_routes[route_index] = new_route
                print(f"Feasible route after swap: {new_routes}.")
                return new_routes
            else:
                print("Infeasible route after swap. Reverting.")

    return routes


#### Relocation
def relocation(routes, demand, capacity, ready_time, due_time, service_time, distance_matrix):
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
    if is_feasible(new_route1, demand, capacity, ready_time, due_time, service_time, distance_matrix) and \
            is_feasible(new_route2, demand, capacity, ready_time, due_time, service_time, distance_matrix):
        routes[route1_index] = new_route1
        routes[route2_index] = new_route2
        print(
            f"Relocation applied successfully. Moved customer {customer} from route {route1_index} to route {route2_index}.")
    else:
        print(f"Relocation resulted in infeasible routes. Reverting.")

    return routes
