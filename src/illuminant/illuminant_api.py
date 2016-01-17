import threading

from rosmaster.master_api import ROSMasterHandler
from protocol import ServerProtocol
from collections import defaultdict
from lruheap import LRUHeap
from goblin.xmlrpc.response import ResponseFactory
from rosmaster.master_api import NUM_WORKERS


class ServerAPI(ServerProtocol):
    def __init__(self):
        self.records = defaultdict(LRUHeap)
        self.record_lock = threading.RLock()

    def regCell(self, service, service_uri, daemon_uri):
        with self.record_lock:
            self.records[service].insert(service_uri, daemon_uri)
        return ResponseFactory.service_reg(daemon_uri, service).pack()

    def unregCell(self, service, service_uri, daemon_uri):
        with self.record_lock:
            self.records[service].remove(service_uri, daemon_uri)
        return ResponseFactory.service_unreg(daemon_uri, service).pack()

    def _lookup_cell(self, service):
        uri = None
        with self.record_lock:
            if len(self.records) > 0:
                uri = self.records[service].next()
        return uri


class IlluminantHandler(ROSMasterHandler, ServerAPI):
    def __init__(self, num_workers=NUM_WORKERS):
        super(ROSMasterHandler, self).__init__()
        super(IlluminantHandler, self).__init__()

    def lookupService(self, caller_id, service):
        """
        Forked from ROSMasterHandler
        Lookup all provider of a particular service.
        @param caller_id str: ROS caller id
        @type  caller_id: str
        @param service: fully-qualified name of service to lookup.
        @type: service: str
        @return: (code, message, serviceUrl). service URL is provider's
           ROSRPC URI with address and port.  Fails if there is no provider.
        @rtype: (int, str, str)
        """
        # try to find a clint-registered service
        code, msg, value = super(IlluminantHandler, self).lookupService(caller_id, service)
        if code == 1:  # if got a client-registered service, return it.
            return code, msg, value
        else:  # otherwise, use a cell if possible
            uri = self._lookup_cell(service)
            return ResponseFactory.uri_found(self, uri).pack()
