"""
Illuminant XML-RPC based protocol
"""

from xmlrpclib import ServerProxy


def interrupted_response(value):
    return 1, 'Interrupted by daemon', value


class OverwrittenAPI(object):
    def __init__(self, illuminant_uri):
        self.illuminant_uri = illuminant_uri
        self.illuminant_proxy = ServerProxy(illuminant_uri)

    def _dispatch(self, method, params):
        """
        Dispatch all methods not included in DaemonProtocol will be dispatch to Illuminant
        """
        if method in self.__dict__:
            return self.__dict__[method](*params)
        else:
            return getattr(self.illuminant_proxy, method)(*params)


class DaemonProtocol(OverwrittenAPI):
    def __init__(self, daemon_uri, illuminant_uri):
        super(DaemonProtocol, self).__init__(illuminant_uri)
        self.daemon_uri = daemon_uri

    # METHODS FOR ILLUMINANT TO CONTROL SELL
    def launch(self, package_name):
        pass

    def execute(self, command):
        pass

    def terminate(self):
        pass

    def is_alive(self):
        pass

    def is_busy(self):
        pass

    # METHODS FOR ILLUMINANT TO MAINTAIN SERVICES
    def registerService(self, caller_id, service, service_api, caller_api):
        """
        This will register service to illuminant, not Master
        """
        self.illuminant_proxy.regCell(service, service_api, self.daemon_uri)

    def unregisterService(self, caller_id, service, service_api):
        """
        This will unregister service from illuminant, not Master
        """
        self.illuminant_proxy.unregCell(service, service_api, self.daemon_uri)

    # THESE METHODS INTERRUPT ORIGINAL CALLS AND DO NOTHING
    def registerPublisher(self, caller_id, topic, topic_type, caller_api):
        return interrupted_response([])

    def registerSubscriber(self, caller_id, topic, topic_type, caller_api):
        return interrupted_response([])

    def unregisterPublisher(self, caller_id, topic, caller_api):
        return interrupted_response(0)

    def unregisterSubscriber(self, caller_id, topic, caller_api):
        return interrupted_response(0)


class ServerProtocol(object):
    def regCell(self, service, service_uri, daemon_uri):
        pass

    def unregCell(self, service, service_uri, daemon_uri):
        pass
