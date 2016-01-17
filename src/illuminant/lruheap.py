"""
Services lookup-table using LRU algorithm
"""
import heapq
from functools import total_ordering


@total_ordering
class ServiceRecord(object):
    __slots__ = ('weight', 'service_uri', 'daemon_uri')

    def __init__(self, service_uri, daemon_uri):
        self.weight = 0
        self.service_uri = service_uri
        self.daemon_uri = daemon_uri

    def __lt__(self, other):
        if isinstance(other, ServiceRecord):
            return self.weight < other.weight
        raise TypeError('Cannot compare ServiceRecord wit {}'.format(type(other)))

    def __eq__(self, other):
        if isinstance(other, ServiceRecord):
            return self.daemon_uri == other.daemon_uri and self.service_uri == other.service_uri
        raise TypeError('Cannot compare ServiceRecord wit {}'.format(type(other)))

    def update_weigh(self, value=None):
        if value is None:
            self.weight += 1
        else:
            self.weight = value

    def match(self, service_uri, daemon_uri):
        return self.daemon_uri == daemon_uri and self.service_uri == service_uri

    def value(self):
        return self.daemon_uri, self.service_uri


class LRUHeap:
    def __init__(self, record_type=ServiceRecord):
        self.record_type = record_type if record_type is not None else ServiceRecord
        self.heap = []
        self.size = 0

    def insert(self, service_uri, daemon_uri):
        if not self.has(service_uri, daemon_uri):
            heapq.heappush(self.heap, self.record_type(service_uri, daemon_uri))
            self.size += 1

    def has(self, service_uri, daemon_uri):
        for record in self.heap:
            if record.match(service_uri, daemon_uri):
                return True
        else:
            return False

    def remove(self, service_uri, daemon_uri):
        # mark
        delete_weight = 0
        for record in self.heap:
            if record.match(service_uri, daemon_uri):
                record.weight(-1)
                delete_weight += 1
        # pop
        if delete_weight > 0:
            heapq.heapify(self.heap)
            self.heap = self.heap[delete_weight:]
            heapq.heapify(self.heap)

    def __iter__(self):
        return self

    def next(self):
        if self.size > 0:
            value = self.heap[0].value()
            self.heap[0].update_weigh()
            heapq.heapify(self.heap)
            return value
        else:
            raise StopIteration

    def __len__(self):
        return len(self.heap)

    def __nonzero__(self):
        return len(self.heap) == 0
