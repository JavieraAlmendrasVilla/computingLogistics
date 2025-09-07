from dataclasses import dataclass, field
from typing import List


@dataclass
class Solution:
    dataset: int
    algorithm: str
    neighborhood_selection: str
    initial_distance: float
    best_distance: float
    initial_routes: List[List[int]]
    best_routes: List[List[int]]
    runtime: float
    temperatures: List[float] = field(default_factory=list)
    solutions: List[float] = field(default_factory=list)
    accepted_solutions: List[float] = field(default_factory=list)
    acceptance_probabilities: List[float] = field(default_factory=list)


def createSolution(dataset: int, algorithm: str, neighborhood_selection: str, initial_routes: List[List[int]],
                   initial_distance: float, best_distance: float, best_routes: List[List[int]], runtime: float,
                   temperatures: List[float], solutions: List[float], accepted_solutions: List[float],
                   acceptance_probabilities: List[float]) -> Solution:
    return Solution(dataset=dataset, algorithm=algorithm, neighborhood_selection=neighborhood_selection,
                    initial_distance=initial_distance, best_distance=best_distance,
                    initial_routes=initial_routes,
                    best_routes=best_routes,
                    runtime=runtime,
                    temperatures=temperatures, solutions=solutions, accepted_solutions=accepted_solutions,
                    acceptance_probabilities=acceptance_probabilities)
