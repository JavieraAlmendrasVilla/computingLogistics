import os
import glob

file_directory = r"data/"
file_prefix = "R2_10"

def parse_vrp_tw_files():
    vehicles = []
    customers = []

    # Find all files matching the pattern
    file_pattern = os.path.join(file_directory, f"{file_prefix}_*.txt")
    file_list = glob.glob(file_pattern)

    for filename in file_list:
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()

                # Parse VEHICLE section
                vehicle_section_index = lines.index('VEHICLE\n')
                capacity_line = lines[vehicle_section_index + 2].strip().split()
                num_vehicles = int(capacity_line[0])
                capacity = int(capacity_line[1])
                #vehicles = [capacity] * num_vehicles

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

                # Store vehicle capacity
                vehicles.append(num_vehicles)
                vehicles.append(capacity)


        except FileNotFoundError:
            print(f"File {filename} not found.")
            continue

def parse_one_instance(instance):
    customers = []
    vehicles = {}

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


def get_instance(instance):
    vehicles, customers = parse_one_instance(instance)

    if vehicles is None or customers is None:
        return None, None

    customers_dict = {
        'id': [customer['CUST NO.'] for customer in customers],
        'location': [(customer['XCOORD.'], customer['YCOORD.']) for customer in customers],
        'demand': [customer['DEMAND'] for customer in customers],
        'ready_time': [customer['READY TIME'] for customer in customers],
        'due_time': [customer['DUE DATE'] for customer in customers],
        'service_time': [customer['SERVICE TIME'] for customer in customers]
    }

    return vehicles, customers_dict
def main():

    vehicles, customers = get_instance(1)
    # Example output usage:
    print(vehicles, customers)

if __name__ == "__main__":
    main()