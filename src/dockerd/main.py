from SimpleXMLRPCServer import SimpleXMLRPCServer
from docker_daemon import DockerDaemon
import os


def main():
    host_ip = os.environ['HOST_IP']
    instance = DockerDaemon(host_ip)
    server = SimpleXMLRPCServer(('0.0.0.0', 55555))
    server.register_instance(instance)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Interrupted. Bye.')
    except Exception as e:
        raise e


if __name__ == '__main__':
    main()
