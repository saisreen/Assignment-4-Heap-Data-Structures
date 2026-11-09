"""Repeatable sorting benchmark. Writes results to benchmark_results.csv."""
import csv
import random
import statistics
import time
from sorting import heapsort, quicksort, mergesort


def run_benchmark(sizes=(100, 1000, 5000), repetitions=5):
    rng = random.Random(42)
    rows = []
    algorithms = [('Heapsort', heapsort), ('Quicksort', quicksort), ('Merge Sort', mergesort)]
    for size in sizes:
        original = [rng.randint(0, size * 2) for _ in range(size)]
        inputs = {'sorted': sorted(original), 'reverse': sorted(original, reverse=True),
                  'random': original, 'duplicates': [rng.randint(0, 9) for _ in range(size)]}
        for distribution, data in inputs.items():
            expected = sorted(data)
            for name, algorithm in algorithms:
                timings = []
                for _ in range(repetitions):
                    start = time.perf_counter()
                    result = algorithm(data)
                    elapsed = time.perf_counter() - start
                    assert result == expected, f'{name} produced incorrect output'
                    timings.append(elapsed * 1000)
                rows.append({'size': size, 'distribution': distribution, 'algorithm': name,
                             'median_ms': round(statistics.median(timings), 4)})
    with open('benchmark_results.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['size', 'distribution', 'algorithm', 'median_ms'])
        writer.writeheader()
        writer.writerows(rows)
    return rows


if __name__ == '__main__':
    for row in run_benchmark():
        print(row)
