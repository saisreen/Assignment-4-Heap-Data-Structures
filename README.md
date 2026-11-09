# Smart Laboratory Calibration Scheduler — Assignment 4

An original Python project showing array-based max-heaps, Heapsort, and priority scheduling of laboratory equipment calibration jobs.

## Requirements
Python 3.9 or newer; standard library only. No installation required.

## Run
From the project folder:
```bash
python scheduler.py
python benchmark.py
python -m unittest -v
```
The benchmark writes `benchmark_results.csv` to the current folder. Each result is the median of five timed runs in milliseconds; your computer may produce different timings.

## Files
- `sorting.py`: Heapsort, randomized three-way Quicksort, bottom-up Merge Sort.
- `priority_queue.py`: Task model and indexed max-priority queue.
- `scheduler.py`: single-technician, non-preemptive scheduler simulation.
- `benchmark.py`: repeatable benchmark across four input distributions.
- `benchmark_results.csv`: measured results from one local run.
- `test_project.py`: automated correctness and edge-case tests.
- `Assignment4_Report.docx`: written analysis and experiment findings.

## Scheduling rules
The largest numeric priority goes first. Equal priorities use the earliest deadline, then earliest arrival, then lexicographically smallest task ID. Jobs are added only when they arrive; an active job is never interrupted. The scheduler is a simulation, not a guarantee that deadlines are met.

## Main findings
Heapsort uses O(n log n) time even on ordered input, while the in-place heap operations need O(1) auxiliary storage (this implementation copies the input, so total extra storage is O(n)). Priority changes and extraction take O(log n) time with an ID-to-index dictionary. Timings depend on hardware, Python version, and input shape.
