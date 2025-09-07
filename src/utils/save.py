import json
import os
from pathlib import Path
from src.utils.solution import Solution

path_to_repo = Path(__file__).parent.parent.parent.resolve()  # This is the path to the repository


def save_sa_data_and_solution(dataset, sa, solution: Solution):
    sa_data = sa.__dict__
    solution_data = solution.__dict__

    # Create a DataFrame from the solution data
    result = {
        "data": sa_data,
        "solution": solution_data
    }

    # Save the combined DataFrame to a CSV file
    file_name = (f"results_{dataset}_nodes_{solution.algorithm}_{sa.neighborhood_selection}_{sa.cooling_schedule}"
                 f"_initial_temp_{sa.initial_temperature}_alpha_{sa.alpha}_k_{sa.constant_k}_n_{sa.neighborhood_size}.json")

    final_path = path_to_repo / "results"

    if not os.path.exists(final_path):
        os.makedirs(final_path)

    results_file_path = os.path.join(final_path, f"{file_name}.json").replace("/", os.sep)

    # Check if results.json already exists
    if os.path.exists(results_file_path):
        results_file_path = os.path.join(final_path, f"{file_name}.json").replace("/", os.sep)

    with open(results_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(result, jsonfile, ensure_ascii=False, indent=4)
        print("Results saved successfully.")


def save_sa_data_and_solution_soft(dataset, sa, solution: Solution):
    sa_data = sa.__dict__
    solution_data = solution.__dict__

    # Create a DataFrame from the solution data
    result = {
        "data": sa_data,
        "solution": solution_data
    }

    # Save the combined DataFrame to a CSV file
    file_name = (f"results_{dataset}_nodes_{solution.algorithm}_{sa.neighborhood_selection}_{sa.cooling_schedule}"
                 f"_initial_temp_{sa.initial_temperature}_alpha_{sa.alpha}_k_{sa.constant_k}_n_{sa.neighborhood_size}"
                 f"_p_too_early{sa.penalty_too_early}_p_too_late_{sa.penalty_too_late}_total_p_{sa.total_penalty}.json")

    final_path = path_to_repo / "results_sa_soft"

    if not os.path.exists(final_path):
        os.makedirs(final_path)

    results_file_path = os.path.join(final_path, f"{file_name}.json").replace("/", os.sep)

    # Check if results.json already exists
    if os.path.exists(results_file_path):
        results_file_path = os.path.join(final_path, f"{file_name}.json").replace("/", os.sep)

    with open(results_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(result, jsonfile, ensure_ascii=False, indent=4)
        print("Results saved successfully.")


def save_solution(dataset, solution: Solution):
    solution_data = solution.__dict__

    # Create a DataFrame from the solution data
    result = {
        "solution": solution_data
    }

    # Save the combined DataFrame to a CSV file
    file_name = f"results_{dataset}_{solution.algorithm}.json"

    final_path = path_to_repo / "results"

    if not os.path.exists(final_path):
        os.makedirs(final_path)

    results_file_path = os.path.join(final_path, f"{file_name}.json").replace("/", os.sep)

    # Check if results.json already exists
    if os.path.exists(results_file_path):
        results_file_path = os.path.join(final_path, f"{file_name}.json").replace("/", os.sep)

    with open(results_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(result, jsonfile, ensure_ascii=False, indent=4)
        print("Results saved successfully.")
