from docker import Client
from threading import RLock


class DockerDaemon(object):
    def __init__(self, host_ip):
        self.client = Client()
        self.uri = None
        self.container_ports = dict()
        self.lock = RLock()
        self.host_ip = host_ip

    def _ready(self, uri):
        self.uri = uri

    def parse(self, uri):
        container_id, _ = uri[9:].split(':')
        with self.lock:
            port = self.container_ports.get(container_id, None)
            if port is None:
                try:
                    info = self.client.inspect_container(container_id)
                    port = info['NetworkSettings']['Ports']['30000/tcp'][0]['HostPort']
                except:
                    port = None
                else:
                    self.container_ports[container_id] = port
        if port is None:
            return 1, 'Cannot parse [{}]'.format(uri), ''
        else:
            parsed = 'http://{}:{}'.format(self.host_ip, port)
            return 1, 'URI [{}] parsed to [{}]'.format(uri, parsed), parsed
