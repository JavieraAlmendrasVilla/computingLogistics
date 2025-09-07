import os
import json
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pandasgui import show

path_to_results = Path(__file__).parent / "results"
path_to_best_results = path_to_results.parent / "best_results"
path_to_worst_results = path_to_results.parent / "worst_results"


def flatten_json(json_data, prefix=''):
    flattened = {}
    for key, value in json_data.items():
        new_key = prefix + '_' + key if prefix else key
        if isinstance(value, dict):
            flattened.update(flatten_json(value, new_key))
        elif isinstance(value, list):
            if value and isinstance(value[0], dict):  # Check if the list is not empty and contains dictionaries
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        flattened.update(flatten_json(item, f"{new_key}_{i}"))
                    else:
                        flattened[f"{new_key}_{i}"] = item
            else:  # Handle lists of primitives or empty lists
                flattened[new_key] = value
        else:
            flattened[new_key] = value
    return flattened


def flatten_all_json_files_in_dir():
    directory = path_to_results
    results = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                flattened_data = flatten_json(data)
                results.append(flattened_data)
    df = pd.DataFrame(results)
    df.to_csv(path_to_results / "flattened_results.csv", index=False)
    return df


def best_and_worst_results(df, dataset: int, algorithm: str):
    data = df[(df['solution_dataset'] == dataset) & (df['solution_algorithm'] == algorithm)]
    best = data.loc[data['solution_best_distance'].idxmin()]
    worst = data.loc[data['solution_best_distance'].idxmax()]
    path_to_best_results = path_to_results.parent / "best_results"
    path_to_worst_results = path_to_results.parent / "worst_results"

    if not os.path.exists(path_to_best_results):
        os.makedirs(path_to_best_results)
    with open(path_to_best_results / f"best_results_{dataset}_{algorithm}.json", 'w', encoding='utf-8') as jsonfile:
        json.dump(best.to_dict(), jsonfile, ensure_ascii=False, indent=4)

    if not os.path.exists(path_to_worst_results):
        os.makedirs(path_to_worst_results)
    with open(path_to_worst_results / f"worst_results_{dataset}_{algorithm}.json", 'w', encoding='utf-8') as jsonfile:
        json.dump(worst.to_dict(), jsonfile, ensure_ascii=False, indent=4)

    return print(best), print(worst)


def plot_barplot(df):
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 12

    sns.barplot(data=df, x='data_neighborhood_selection', y='solution_best_distance', hue='solution_dataset',
                palette='colorblind')
    plt.title("Best distance by neighborhood selection")
    plt.xlabel("Neighborhood selection")
    plt.ylabel("Best distance")
    plt.legend(loc='upper right')
    path_to_plots = path_to_results.parent / "plots"
    plt.savefig(path_to_plots / "best_distance_by_neighborhood_selection.png")
    plt.show()


if __name__ == "__main__":
    df = flatten_all_json_files_in_dir()
    show(df)
