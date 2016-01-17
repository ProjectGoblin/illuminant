"""
Services lookup-table using LRU algorithm
"""
import heapq
from functools import total_ordering


@total_ordering
class ServiceRecord(object):
    __slots__ = ('counter', 'service_uri', 'daemon_uri')

    def __init__(self, service_uri, daemon_uri):
        self.counter = 0
        self.service_uri = service_uri
        self.daemon_uri = daemon_uri

    def __lt__(self, other):
        if isinstance(other, ServiceRecord):
            return self.counter < other.counter
        raise TypeError('Cannot compare ServiceRecord wit {}'.format(type(other)))

    def __eq__(self, other):
        if isinstance(other, ServiceRecord):
            return self.caller_id == other.caller_id and self.service_api == other.service_api
        raise TypeError('Cannot compare ServiceRecord wit {}'.format(type(other)))

    def count(self, value=None):
        if value is None:
            self.counter += 1
        else:
            self.counter = value

    def match(self, caller_id, service_api):
        return self.caller_id == caller_id and self.service_api == service_api

    def value(self):
        return self.caller_id, self.service_api


class LRUHeap:
    def __init__(self, record_type=ServiceRecord):
        self.record_type = record_type if record_type is not None else ServiceRecord
        self.heap = []
        self.size = 0

    def insert(self, caller_id, service_api):
        if not self.has(caller_id, service_api):
            heapq.heappush(self.heap, self.record_type(caller_id, service_api))
            self.size += 1

    def has(self, caller_id, service_api):
        for record in self.heap:
            if record.match(caller_id, service_api):
                return True
        else:
            return False

    def remove(self, caller_id, service_api):
        # mark
        delete_counter = 0
        for record in self.heap:
            if record.match(caller_id, service_api):
                record.count(-1)
                delete_counter += 1
        # pop
        if delete_counter > 0:
            heapq.heapify(self.heap)
            self.heap = self.heap[delete_counter:]
            heapq.heapify(self.heap)

    def __iter__(self):
        return self

    def next(self):
        if self.size > 0:
            value = self.heap[0].value()
            self.heap[0].count()
            heapq.heapify(self.heap)
            return value
        else:
            raise StopIteration

    def __len__(self):
        return len(self.heap)

    def __nonzero__(self):
        return len(self.heap) == 0
