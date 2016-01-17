from __future__ import print_function

import time

import rosgraph.xmlrpc
from rosmaster.master import Master
from illuminant_api import IlluminantHandler


class Illuminant(Master):
    def start(self):
        """
        Start the Goblin Illuminant.
        """
        self.handler = None
        self.master_node = None
        self.uri = None

        handler = IlluminantHandler(self.num_workers)
        master_node = rosgraph.xmlrpc.XmlRpcNode(self.port, handler)
        master_node.start()

        # poll for initialization
        while not master_node.uri:
            time.sleep(0.0001)

            # save fields
        self.handler = handler
        self.master_node = master_node
        self.uri = master_node.uri
