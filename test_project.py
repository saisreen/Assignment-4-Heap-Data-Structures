"""Unit tests: run python -m unittest -v."""
import unittest
from sorting import heapsort, quicksort, mergesort
from priority_queue import Task, MaxPriorityQueue
from scheduler import simulate


class SortingTests(unittest.TestCase):
    def test_edge_cases(self):
        for sorter in (heapsort, quicksort, mergesort):
            for values in ([], [1], [3, 3, 3], [1, 2, 3], [3, 2, 1], [-4, 0, -4, 9]):
                with self.subTest(sorter=sorter.__name__, values=values):
                    self.assertEqual(sorter(values), sorted(values))
                    self.assertEqual(values, values[:])


class QueueTests(unittest.TestCase):
    def test_priority_and_ties(self):
        q = MaxPriorityQueue()
        for task in (Task('A', 2, 0, 8), Task('B', 5, 0, 10), Task('C', 5, 1, 4)):
            q.insert(task)
        self.assertEqual([q.extract_max().task_id for _ in range(3)], ['C', 'B', 'A'])
        self.assertTrue(q.is_empty())
        with self.assertRaises(IndexError):
            q.extract_max()

    def test_update_and_errors(self):
        q = MaxPriorityQueue()
        q.insert(Task('A', 1, 0, 4))
        q.insert(Task('B', 4, 0, 5))
        q.increase_key('A', 6)
        self.assertEqual(q.extract_max().task_id, 'A')
        q.decrease_key('B', 0)
        self.assertEqual(q.extract_max().priority, 0)
        with self.assertRaises(KeyError):
            q.change_priority('missing', 3)
        q.insert(Task('X', 1, 0, 3))
        with self.assertRaises(ValueError):
            q.insert(Task('X', 2, 0, 3))
        with self.assertRaises(ValueError):
            q.decrease_key('X', 2)

    def test_scheduler(self):
        rows, summary = simulate([Task('A', 1, 0, 3, 2), Task('B', 4, 0, 2, 1)])
        self.assertEqual([r['task_id'] for r in rows], ['B', 'A'])
        self.assertEqual(summary['completed'], 2)
        self.assertEqual(simulate([])[1]['completed'], 0)


if __name__ == '__main__':
    unittest.main()
