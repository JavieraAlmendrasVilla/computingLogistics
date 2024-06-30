from pathlib import Path
import sys
path = Path(__file__).parent.resolve()
sys.argv.append(str(path))
from simulatedAnnealing import simulatedAnnealing


def main():
    simulatedAnnealing(1)