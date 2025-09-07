import os
from dataclasses import dataclass
from pathlib import Path

file_directory = Path(__file__).parent.parent.parent.resolve() / "data"  # This is the path to the data
file_prefix = "C1_2"


@dataclass
class Instance:
    instance: int
    num_vehicles: int
    capacity: int
    id: list[int]
    locations: list[tuple[int, int]]
    demand: list[int]
    ready_time: list[int]
    due_time: list[int]
    service_time: list[int]


def parse_one_instance(instance):
    customers = []

    # Construct the filename based on the directory, prefix, and instance
    filename = os.path.join(file_directory, f"{file_prefix}_{instance}.txt")

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

            # Parse VEHICLE section
            vehicle_section_index = lines.index('VEHICLE\n')
            capacity_line = lines[vehicle_section_index + 2].strip().split()
            num_vehicles = int(capacity_line[0])
            capacity = int(capacity_line[1])

            # Parse CUSTOMER section
            customer_section_index = lines.index('CUSTOMER\n')
            customer_data_lines = lines[customer_section_index + 2:]

            for line in customer_data_lines:
                if line.strip() == '':
                    continue
                fields = line.split()
                if len(fields) == 7:
                    customer_info = {
                        'CUST NO.': int(fields[0]),
                        'XCOORD.': int(fields[1]),
                        'YCOORD.': int(fields[2]),
                        'DEMAND': int(fields[3]),
                        'READY TIME': int(fields[4]),
                        'DUE DATE': int(fields[5]),
                        'SERVICE TIME': int(fields[6])
                    }
                    customers.append(customer_info)

            # Store vehicle data
            vehicles = {
                'num_vehicles': num_vehicles,
                'capacity': capacity
            }

    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None, None

    return vehicles, customers


def get_instance(instance) -> Instance:
    vehicles, customers = parse_one_instance(instance)
    num_vehicles = vehicles['num_vehicles']
    capacity = vehicles['capacity']
    id = [customer['CUST NO.'] for customer in customers]
    locations = [(customer['XCOORD.'], customer['YCOORD.']) for customer in customers]
    demand = [customer['DEMAND'] for customer in customers]
    ready_time = [customer['READY TIME'] for customer in customers]
    due_time = [customer['DUE DATE'] for customer in customers]
    service_time = [customer['SERVICE TIME'] for customer in customers]

    data = Instance(
        instance=instance,
        num_vehicles=num_vehicles,
        capacity=capacity,
        id=id,
        locations=locations,
        demand=demand,
        ready_time=ready_time,
        due_time=due_time,
        service_time=service_time)

    return data
