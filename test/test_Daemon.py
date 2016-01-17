from unittest import TestCase
from xmlrpclib import ServerProxy

from illuminant.protocol import DaemonProtocol
from illuminant.illuminant import Illuminant
from SimpleXMLRPCServer import SimpleXMLRPCServer
from threading import Thread
import time


def port_to_uri(port):
    return 'http://localhost:{}'.format(port)


def run_illuminant(port):
    illuminant = Illuminant(port, 1)

    def _run_illuminant():
        illuminant.start()

    thread = Thread(target=_run_illuminant)
    thread.setDaemon(True)
    thread.start()
    return illuminant


def run_daemon(port, illuminant_uri):
    daemon = DaemonProtocol(port_to_uri(port), illuminant_uri)

    def _run_daemon():
        server = SimpleXMLRPCServer(('localhost', port))
        server.register_instance(daemon)
        server.serve_forever()

    thread = Thread(target=_run_daemon)
    thread.setDaemon(True)
    thread.start()
    return daemon


SERVICE = 'foo'
CALLER_ID = '~'
CALLER_API = 'http://localhost:65535'


class Daemon(TestCase):
    def setUp(self):
        illuminant_port = 33333
        daemon_port = 22322
        self.illuminant_obj = run_illuminant(illuminant_port)
        self.daemon_handler = run_daemon(daemon_port, port_to_uri(illuminant_port))
        self.d = ServerProxy(port_to_uri(daemon_port))
        self.i = ServerProxy(port_to_uri(illuminant_port))
        while self.illuminant_obj.handler is None:
            time.sleep(0.01)
        self.illuminant_handler = self.illuminant_obj.handler

    def test_Daemon(self):
        res = self.d.registerService(CALLER_ID, SERVICE, port_to_uri(0), CALLER_API)
        self.assertEqual(res[0], 1)
        records = self.illuminant_handler.records
        self.assertEqual(len(records[SERVICE]), 1)
        res = self.d.unregisterService(CALLER_ID, SERVICE, port_to_uri(0))
        # self.assertEqual(res[0], 1)
