"""Non-preemptive, single-technician laboratory calibration scheduler."""
from priority_queue import Task, MaxPriorityQueue


def simulate(tasks):
    """Tasks become eligible at arrival; priority is fixed unless manually updated."""
    ordered = sorted(tasks, key=lambda t: (t.arrival_time, t.task_id))
    if len({t.task_id for t in ordered}) != len(ordered):
        raise ValueError('duplicate task IDs in scheduler input')
    queue = MaxPriorityQueue()
    clock = 0
    index = 0
    results = []
    while index < len(ordered) or not queue.is_empty():
        if queue.is_empty() and index < len(ordered) and clock < ordered[index].arrival_time:
            clock = ordered[index].arrival_time
        while index < len(ordered) and ordered[index].arrival_time <= clock:
            queue.insert(ordered[index])
            index += 1
        if queue.is_empty():
            continue
        task = queue.extract_max()
        start = clock
        clock += task.duration
        results.append({'task_id': task.task_id, 'priority': task.priority,
                        'start': start, 'finish': clock, 'wait': start - task.arrival_time,
                        'deadline': task.deadline, 'late': clock > task.deadline})
    count = len(results)
    return results, {'completed': count,
                     'average_wait': round(sum(r['wait'] for r in results) / count, 2) if count else 0,
                     'late_tasks': sum(r['late'] for r in results)}


if __name__ == '__main__':
    tasks = [Task('MICROSCOPE-A', 3, 0, 9, 3), Task('CENTRIFUGE-B', 5, 0, 4, 2),
             Task('INCUBATOR-C', 5, 1, 6, 2), Task('SPECTROMETER-D', 2, 2, 8, 3),
             Task('FREEZER-E', 4, 4, 10, 2)]
    rows, summary = simulate(tasks)
    for row in rows:
        print(row)
    print('Summary:', summary)
