import rosgraph.xmlrpc
import time
from daemon_api import DaemonHandler
from rosmaster.master import Master, DEFAULT_MASTER_PORT
from rosmaster.master_api import NUM_WORKERS


class Daemon(Master):
    def __init__(self, illuminant_uri, port=DEFAULT_MASTER_PORT, num_workers=NUM_WORKERS):
        super(Daemon, self).__init__(port, num_workers)
        self.illuminant_uri = illuminant_uri

    def start(self):
        """
        Start the Goblin Illuminant.
        """
        self.handler = None
        self.master_node = None
        self.uri = None

        handler = DaemonHandler(self.illuminant_uri)
        master_node = rosgraph.xmlrpc.XmlRpcNode(self.port, handler)
        master_node.start()

        # poll for initialization
        while not master_node.uri:
            time.sleep(0.0001)

        # save fields
        self.handler = handler
        self.master_node = master_node
        self.uri = master_node.uri
