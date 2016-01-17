from rosmaster.master_api import ROSMasterHandler


class IlluminantHandler(ROSMasterHandler):
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
            print(2333)
