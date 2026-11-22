"""
Define a PriorityQueue class wrapper around the heapq module
"""
import heapq as pq


class PriorityQueue:
    """
    Implements a priority queue by wrapping the functions of the heapq module.
    """

    def __init__(self):
        self.heap = []

    def push(self, key, cost):
        """
        Push a pair of (key,cost) into the queue.
        """
        pq.heappush(self.heap, (cost, key))

    def is_empty(self):
        """
        Returns True if the queue is empty
        """
        return len(self.heap) == 0

    def is_member(self, key):
        """
        Returns True if the key appears in the queue
        """
        return key in [k for (_, k) in self.heap]

    def pop(self):
        """
        Return a pair (key,cost) corresponding to the element with lowest cost in the queue.
        Raises IndexError if the queue is empty.
        """

        def pair_switch(a):
            """
            Switches the two elements of a pair
            """
            return (a[1], a[0])

        return pair_switch(pq.heappop(self.heap))
