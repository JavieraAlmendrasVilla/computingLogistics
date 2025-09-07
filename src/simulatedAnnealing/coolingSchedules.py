def CS_geometric(current_temperature, alpha):
    current_temperature *= alpha
    return current_temperature


def reduce_temperature(current_temperature, sa):
    if sa.cooling_schedule == "geometric":
        current_temperature = CS_geometric(current_temperature, sa.alpha)

    return current_temperature
