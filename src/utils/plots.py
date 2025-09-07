from pathlib import Path

from matplotlib import pyplot as plt

from src.instance.instance import get_instance

path_to_repo = Path(__file__).parent.parent.parent.resolve()  # This is the path to the repository


def visualize_routes_sa(dataset, current_routes, sa, show=False, save=False):
    """
    Visualize the vehicle routes using matplotlib.
    """
    instance = get_instance(dataset)
    plt.figure(figsize=(10, 10))

    # Plot each customer
    for customer_id, (x, y) in zip(instance.id, instance.locations):
        plt.scatter(x, y, c='blue')
        plt.text(x, y, str(customer_id), fontsize=12, ha='right')

    # Plot each route
    for route_index, route in enumerate(current_routes):
        route_coordinates = [instance.locations[node] for node in route]
        route_coordinates.append(route_coordinates[0])  # To complete the loop to the depot
        xs, ys = zip(*route_coordinates)
        plt.plot(xs, ys, marker='o', label=f'Route {route_index + 1}')

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Vehicle Routes')
    plt.legend()
    plt.grid(True)
    if save:
        path_to_plots = path_to_repo / 'plots'
        file_name = (f"plot_{dataset}_nodes_{sa.neighborhood_selection}_{sa.cooling_schedule}"
                     f"_initial_temp_{sa.initial_temperature}_alpha_{sa.alpha}_k_{sa.constant_k}_n_{sa.neighborhood_size}.png")
        if not path_to_plots.exists():
            path_to_plots.mkdir()
        plt.savefig(path_to_plots / file_name)
        print(f"Plot saved as {file_name}")
    if show:
        plt.show()


def visualize_routes_sa_soft(dataset, current_routes, sa, show=False, save=False):
    """
    Visualize the vehicle routes using matplotlib.
    """
    instance = get_instance(dataset)
    plt.figure(figsize=(10, 10))

    # Plot each customer
    for customer_id, (x, y) in zip(instance.id, instance.locations):
        plt.scatter(x, y, c='blue')
        plt.text(x, y, str(customer_id), fontsize=12, ha='right')

    # Plot each route
    for route_index, route in enumerate(current_routes):
        route_coordinates = [instance.locations[node] for node in route]
        route_coordinates.append(route_coordinates[0])  # To complete the loop to the depot
        xs, ys = zip(*route_coordinates)
        plt.plot(xs, ys, marker='o', label=f'Route {route_index + 1}')

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Vehicle Routes')
    plt.legend()
    plt.grid(True)
    if save:
        path_to_plots = path_to_repo / 'plots_soft'
        file_name = (f"plot_{dataset}_nodes_{sa.neighborhood_selection}_{sa.cooling_schedule}"
                     f"_initial_temp_{sa.initial_temperature}_alpha_{sa.alpha}_k_{sa.constant_k}_n_{sa.neighborhood_size}"
                     f"_p_too_early{sa.penalty_too_early}_p_too_late_{sa.penalty_too_late}_total_p_{sa.total_penalty}.png")
        if not path_to_plots.exists():
            path_to_plots.mkdir()
        plt.savefig(path_to_plots / file_name)
        print(f"Plot saved as {file_name}")
    if show:
        plt.show()


def visualize_routes(dataset, current_routes, name, show=False, save=False):
    """
    Visualize the vehicle routes using matplotlib.
    """
    instance = get_instance(dataset)
    plt.figure(figsize=(10, 10))

    # Plot each customer
    for customer_id, (x, y) in zip(instance.id, instance.locations):
        plt.scatter(x, y, c='blue')
        plt.text(x, y, str(customer_id), fontsize=12, ha='right')

    # Plot each route
    for route_index, route in enumerate(current_routes):
        route_coordinates = [instance.locations[node] for node in route]
        route_coordinates.append(route_coordinates[0])  # To complete the loop to the depot
        xs, ys = zip(*route_coordinates)
        plt.plot(xs, ys, marker='o', label=f'Route {route_index + 1}')

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Vehicle Routes')
    plt.legend()
    plt.grid(True)
    if save:
        path_to_plots = path_to_repo / 'plots'
        file_name = f"{dataset}_nodes_{name}.png"
        if not path_to_plots.exists():
            path_to_plots.mkdir()
        plt.savefig(path_to_plots / file_name)
        print(f"Plot saved as {file_name}")
    if show:
        plt.show()
