from protocol import DaemonProtocol
import subprocess
import threading


class DaemonHandler(DaemonProtocol):
    def _ok(self):
        return True

    def _shutdown(self):
        return True

    def __init__(self, illuminant_uri):
        super(DaemonHandler, self).__init__(illuminant_uri)
        self.command = None
        self.running = False
        self.process = None
        self.r_lock = threading.RLock()

    def terminate(self):
        with self.r_lock:
            self.process.kill()
        return 1, 'terminate', True

    def launch(self, args):
        with self.r_lock:
            self.command = args
            self.process = subprocess.Popen(args, shell=True)
            pid = self.process.pid
        return 1, 'launch', pid

    def is_busy(self):
        return 1, 'is_busy', False

    def is_alive(self):
        with self.r_lock:
            flag = self.process.poll() is None
        return 1, 'is_alive', flag

    def execute(self, command):
        return self.launch(command)
