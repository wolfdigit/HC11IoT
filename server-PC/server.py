#!/usr/bin/env python
# -*- coding: utf8 -*-

import SimpleRF
import time
import signal, sys
from SerialServer import SerialServer
import WebUI

nodeIdRange = range(1,8)
comport = "COM3"
baudrate = 9600


import locale
import sys; reload(sys)
sys.setdefaultencoding(locale.getpreferredencoding())         # TODO: ugly magic!!!

'''
    Logging
'''
import logging
import logging.handlers
log = logging.getLogger('SimpleRF')
log.propagate = False
if not log.handlers:
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler = logging.handlers.RotatingFileHandler('SimpleRF.log', maxBytes=4000000, backupCount=5)
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)

serialGW = None
def exithandler(signal, frame):
    global serialGW
    print 'Ctrl-C.... Exiting'
    serialGW.stop()
    serialGW.join()
    sys.exit(0)

if __name__ == "__main__":
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, exithandler)
    serialGW = SerialServer(nodeIdRange, comport, baudrate)
    serialGW.daemon = True
    serialGW.start()
    #SimpleRF.db.set(7,1,99)
    #WebUI.app.run(host='0.0.0.0', port=5000, debug=True)
    WebUI.app.run(host='0.0.0.0', port=5000)

