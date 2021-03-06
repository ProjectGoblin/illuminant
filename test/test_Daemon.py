from unittest import TestCase
from xmlrpclib import ServerProxy

from illuminant.daemon import Daemon
from illuminant.illuminant import Illuminant
from threading import Thread
import time
import random


def port_to_uri(port):
    return 'http://localhost:{}'.format(port)


def uri_to_port(uri):
    return int(uri[17:])


def run_illuminant(port):
    illuminant = Illuminant(port, 1)

    def _run_illuminant():
        illuminant.start()

    thread = Thread(target=_run_illuminant)
    thread.setDaemon(True)
    thread.start()
    return illuminant


def run_daemon(port, illuminant_uri):
    daemon = Daemon(illuminant_uri, port=port)

    def _run_daemon():
        daemon.start()

    thread = Thread(target=_run_daemon)
    thread.setDaemon(True)
    thread.start()
    return daemon


SERVICE = 'foo'
CALLER_ID = '~'
CALLER_API = 'http://localhost:65535'


class TestDaemon(TestCase):
    def setUp(self):
        illuminant_port = random.randrange(10000, 30000)
        daemon_port = random.randrange(10000, 30000)
        self.illuminant_obj = run_illuminant(illuminant_port)
        self.daemon_obj = run_daemon(daemon_port, port_to_uri(illuminant_port))
        self.d = ServerProxy(port_to_uri(daemon_port))
        self.i = ServerProxy(port_to_uri(illuminant_port))
        while self.illuminant_obj.handler is None:
            time.sleep(0.01)
        self.illuminant_handler = self.illuminant_obj.handler
        while self.daemon_obj.handler is None:
            time.sleep(0.01)
        self.daemon_handler = self.illuminant_obj.handler

    def test_Daemon(self):
        res = self.d.registerService(CALLER_ID, SERVICE, port_to_uri(0), CALLER_API)
        self.assertEqual(res[0], 1)
        records = self.illuminant_handler.records
        self.assertEqual(len(records[SERVICE]), 1)
        res = self.d.unregisterService(CALLER_ID, SERVICE, port_to_uri(0))
        self.assertEqual(res[0], 1)

    def test_LRU(self, times=10):
        for i in range(times):
            self.d.registerService(CALLER_ID, SERVICE, port_to_uri(i), CALLER_API)
        ports = []
        for i in range(times):
            res = self.d.lookupService(CALLER_ID, SERVICE)
            ports.append(uri_to_port(res[2]))
        ports.sort()
        self.assertEqual(ports, list(range(times)))
