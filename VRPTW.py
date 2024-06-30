from instance import get_instance
import numpy as np

def calculate_distance_matrix(locations):
    num_locations = len(locations)
    distance_matrix = np.zeros((num_locations, num_locations))

    for i in range(num_locations):
        for j in range(num_locations):
            distance_matrix[i, j] = np.sqrt(
                (locations[i][0] - locations[j][0]) ** 2 + (locations[i][1] - locations[j][1]) ** 2)

    return distance_matrix


def create_initial_solution(customers):
    depot = 0
    num_customers = len(customers['id'])
    return [[depot, i, depot] for i in range(1, num_customers)]


def is_feasible(route, demand, capacity, ready_time, due_time, service_time, distance_matrix):
    current_time = 0
    total_demand = 0
    for i in range(1, len(route) - 1):
        customer = route[i]
        total_demand += demand[customer]
        travel_time = distance_matrix[route[i - 1]][customer]
        current_time += travel_time
        if current_time < ready_time[customer]:
            current_time = ready_time[customer]
        if current_time > due_time[customer]:
            return False
        current_time += service_time[customer]
    return total_demand <= capacity


def clarkewright_savings(instance):
    # Step 1: Calculate savings
    vehicles, customers = get_instance(instance)
    num_customers = len(customers['id'])
    location = customers['location']
    demand = customers['demand']
    ready_time = customers['ready_time']
    due_time = customers['due_time']
    service_time = customers['service_time']
    depot = 0

    distance_matrix = calculate_distance_matrix(location)
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
    routes = create_initial_solution(customers)
    capacity = vehicles['capacity']  # Assuming all vehicles have the same capacity

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
            if is_feasible(new_route, demand, capacity, ready_time, due_time, service_time, distance_matrix):
                routes.remove(route_i)
                routes.remove(route_j)
                routes.append(new_route)

    # Step 4: Adjust routes to respect time windows
    feasible_routes = []
    for route in routes:
        if is_feasible(route, demand, capacity, ready_time, due_time, service_time, distance_matrix):
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

    return feasible_routes




def main():
    instance = 1
    clarkewright_savings(instance)

if __name__ == '__main__':
    main()