import os
import optparse
import sys
import time
import logging
import socket
import rosmaster.master
from rosmaster.main import NUM_WORKERS
from illuminant import Illuminant
from daemon import Daemon


def configure_logging():
    """
    Setup filesystem logging for the master
    """
    filename = 'illuminant.log'
    import rosgraph.names
    import rosgraph.roslogging
    mappings = rosgraph.names.load_mappings(sys.argv)
    if '__log' in mappings:
        logfilename_remap = mappings['__log']
        filename = os.path.abspath(logfilename_remap)
    _log_filename = rosgraph.roslogging.configure_logging('rosmaster', logging.DEBUG, filename=filename)


def illuminant_main(argv=sys.argv, stdout=sys.stdout, env=os.environ):
    parser = optparse.OptionParser(usage="usage: zenmaster [options]")
    parser.add_option("--core",
                      dest="core", action="store_true", default=False,
                      help="run as core")
    parser.add_option("-p", "--port",
                      dest="port", default=0,
                      help="override port", metavar="PORT")
    parser.add_option("-w", "--numworkers",
                      dest="num_workers", default=NUM_WORKERS, type=int,
                      help="override number of worker threads", metavar="NUM_WORKERS")
    parser.add_option("-t", "--timeout",
                      dest="timeout",
                      help="override the socket connection timeout (in seconds).", metavar="TIMEOUT")
    options, args = parser.parse_args(argv[1:])

    # only arg that zenmaster supports is __log remapping of logfilename
    for arg in args:
        if not arg.startswith('__log:='):
            parser.error("unrecognized arg: %s" % arg)
    configure_logging()

    port = rosmaster.master.DEFAULT_MASTER_PORT
    if options.port:
        port = int(options.port)

    if not options.core:
        print("""


ACHTUNG WARNING ACHTUNG WARNING ACHTUNG
WARNING ACHTUNG WARNING ACHTUNG WARNING


Standalone illuminant has been deprecated just like 'rosmaster'
Please use 'glcore' instead


ACHTUNG WARNING ACHTUNG WARNING ACHTUNG
WARNING ACHTUNG WARNING ACHTUNG WARNING


""")

    logger = logging.getLogger("illuminant.main")
    logger.info("initialization complete, waiting for shutdown")

    if options.timeout is not None and float(options.timeout) >= 0.0:
        logger.info("Setting socket timeout to %s" % options.timeout)
        socket.setdefaulttimeout(float(options.timeout))

    illuminant = None
    try:
        logger.info("Starting ROS Master Node")
        illuminant = Illuminant(port, options.num_workers)
        illuminant.start()

        while illuminant.ok():
            time.sleep(.1)
    except KeyboardInterrupt:
        logger.info("keyboard interrupt, stopping master...")
        if illuminant is not None:
            illuminant.stop()
    except Exception as e:
        logger.error("error occurred, {}".format(e))


def daemon_main():
    configure_logging()
    daemon = None
    logger = logging.getLogger("daemon.main")
    try:
        daemon = Daemon('http://illuminant:11311')
        daemon.start()
        while daemon.ok():
            time.sleep(.1)
    except KeyboardInterrupt:
        if daemon is not None:
            daemon.stop()
    except Exception as e:
        logger.error("error occurred, {}".format(e))
