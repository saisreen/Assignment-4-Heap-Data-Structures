"""Sorting algorithms for a reproducible heap performance study."""
import random


def heapsort(values):
    """Return an ascending sorted copy, using an in-place max-heap on that copy."""
    a = list(values)
    n = len(a)

    def sift_down(root, end):
        while 2 * root + 1 < end:
            child = 2 * root + 1
            if child + 1 < end and a[child] < a[child + 1]:
                child += 1
            if a[root] >= a[child]:
                return
            a[root], a[child] = a[child], a[root]
            root = child

    for root in range(n // 2 - 1, -1, -1):
        sift_down(root, n)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down(0, end)
    return a


def quicksort(values):
    """Random-pivot three-way Quicksort, with bounded-depth recursive calls."""
    a = list(values)
    rng = random.Random(2026)

    def sort(lo, hi):
        while lo < hi:
            pivot = a[rng.randint(lo, hi)]
            lt, i, gt = lo, lo, hi
            while i <= gt:
                if a[i] < pivot:
                    a[lt], a[i] = a[i], a[lt]
                    lt += 1
                    i += 1
                elif a[i] > pivot:
                    a[gt], a[i] = a[i], a[gt]
                    gt -= 1
                else:
                    i += 1
            if lt - lo < hi - gt:
                sort(lo, lt - 1)
                lo = gt + 1
            else:
                sort(gt + 1, hi)
                hi = lt - 1

    sort(0, len(a) - 1)
    return a


def mergesort(values):
    """Bottom-up Merge Sort with O(n) temporary storage."""
    a = list(values)
    n = len(a)
    temp = [None] * n
    width = 1
    while width < n:
        for start in range(0, n, 2 * width):
            mid, end = min(start + width, n), min(start + 2 * width, n)
            i, j, k = start, mid, start
            while i < mid and j < end:
                if a[i] <= a[j]:
                    temp[k] = a[i]
                    i += 1
                else:
                    temp[k] = a[j]
                    j += 1
                k += 1
            while i < mid:
                temp[k] = a[i]
                i += 1
                k += 1
            while j < end:
                temp[k] = a[j]
                j += 1
                k += 1
        a, temp = temp, a
        width *= 2
    return a
