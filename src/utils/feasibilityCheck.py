
def is_feasible(route, demand, capacity, ready_time, due_time, service_time, distance_matrix):
    current_time = 0
    total_demand = 0
    print(f"Checking feasibility of route {route}.")
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
    result = total_demand <= capacity
    if result:
        print(f"Route {route} is feasible.")
    else:
        print(f"Route {route} is not feasible due to capacity constraints.")
    return result
