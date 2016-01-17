"""
Illuminant XML-RPC based protocol
"""


class DaemonProtocol(object):
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


class ServerProtocol(object):
    def regCell(self, service, service_uri, daemon_uri):
        pass

    def unregCell(self, service, service_uri, daemon_uri):
        pass

    def getCell(self, service):
        pass
