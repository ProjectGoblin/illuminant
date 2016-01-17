"""
Illuminant XML-RPC based protocol
"""


def interrupted_response(value):
    return 1, 'Interrupted by daemon', value


class DaemonProtocol(object):
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
        pass

    def unregisterService(self, caller_id, service, service_api):
        """
        This will unregister service from illuminant, not Master
        """
        pass

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

    def getCell(self, service):
        pass
