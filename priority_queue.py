"""Indexed max-heap for urgent laboratory equipment calibration tasks."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    task_id: str
    priority: int
    arrival_time: int
    deadline: int
    duration: int = 1

    def __post_init__(self):
        if not self.task_id:
            raise ValueError('task_id must not be empty')
        if self.priority < 0 or self.arrival_time < 0 or self.deadline < 0 or self.duration <= 0:
            raise ValueError('priority, arrival and deadline must be nonnegative; duration must be positive')


class MaxPriorityQueue:
    """Higher priority first; earlier deadline and arrival break ties."""

    def __init__(self):
        self.heap = []
        self.positions = {}

    @staticmethod
    def _rank(task):
        return (task.priority, -task.deadline, -task.arrival_time)

    def _higher(self, left, right):
        a, b = self.heap[left], self.heap[right]
        return self._rank(a) > self._rank(b) or (self._rank(a) == self._rank(b) and a.task_id < b.task_id)

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.positions[self.heap[i].task_id] = i
        self.positions[self.heap[j].task_id] = j

    def _up(self, i):
        while i > 0:
            p = (i - 1) // 2
            if not self._higher(i, p):
                break
            self._swap(i, p)
            i = p

    def _down(self, i):
        n = len(self.heap)
        while 2 * i + 1 < n:
            child = 2 * i + 1
            if child + 1 < n and self._higher(child + 1, child):
                child += 1
            if not self._higher(child, i):
                break
            self._swap(i, child)
            i = child

    def insert(self, task):
        if task.task_id in self.positions:
            raise ValueError('duplicate task ID')
        self.positions[task.task_id] = len(self.heap)
        self.heap.append(task)
        self._up(len(self.heap) - 1)

    def extract_max(self):
        if self.is_empty():
            raise IndexError('cannot extract from an empty queue')
        top = self.heap[0]
        last = self.heap.pop()
        del self.positions[top.task_id]
        if self.heap:
            self.heap[0] = last
            self.positions[last.task_id] = 0
            self._down(0)
        return top

    def change_priority(self, task_id, new_priority):
        if new_priority < 0:
            raise ValueError('priority must be nonnegative')
        if task_id not in self.positions:
            raise KeyError(task_id)
        i = self.positions[task_id]
        old = self.heap[i]
        self.heap[i] = Task(old.task_id, new_priority, old.arrival_time, old.deadline, old.duration)
        self._up(i)
        self._down(self.positions[task_id])

    def increase_key(self, task_id, new_priority):
        if task_id not in self.positions:
            raise KeyError(task_id)
        if new_priority < self.heap[self.positions[task_id]].priority:
            raise ValueError('new priority must be >= current priority')
        self.change_priority(task_id, new_priority)

    def decrease_key(self, task_id, new_priority):
        if task_id not in self.positions:
            raise KeyError(task_id)
        if new_priority > self.heap[self.positions[task_id]].priority:
            raise ValueError('new priority must be <= current priority')
        self.change_priority(task_id, new_priority)

    def is_empty(self):
        return not self.heap

    def __len__(self):
        return len(self.heap)
