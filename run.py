import json
from pathlib import Path
import sys
path = Path(__file__).parent.resolve()
sys.argv.append(str(path))
from simulatedAnnealing import simulatedAnnealing


def run():
    path_results = path / "results"
    if not path_results.exists():
        path_results.mkdir()
    for i in range(1, 11):
        best_distance, best_routes = simulatedAnnealing(i)

        output_data = {
            'instance': i,
            'best_distance': best_distance,
            'best_routes': best_routes
        }
        output_file = path_results / f"results_{i}.json"
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=4)


if __name__ == "__main__":
    run()
