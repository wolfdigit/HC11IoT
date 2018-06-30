from threading import Thread
import SimpleRF
from logging import getLogger
import userLogic
import time
import os, signal

class SerialServer(Thread):
    def __init__(self, nodeIdRange, comport, baudrate=9600):
        self.nodeIdRange = nodeIdRange
        Thread.__init__(self)
        self._log = getLogger('SimpleRF')
        SimpleRF.open(comport, baudrate)

    def run(self):
        while SimpleRF.isOpen():
            time.sleep(0.05)
            try:
                msg = SimpleRF.receive(self.nodeIdRange)
            except Exception as e:
                self._log.debug('exception in mainloop: {0}'.format(e))
                print e
                os.kill(os.getpid(), signal.SIGTERM)
                #continue
            if msg.isValid():
                self._log.info('recv pack: {0}'.format(msg.__str__()))
                print msg
                self.parseIncoming(msg)

    def stop(self):
        self._log.info('STOP received...')
        SimpleRF.close()

    def parseIncoming(self, msg):
        if msg.action=='P':
            SimpleRF.db.present(msg.nodeId, msg.sensorId, msg.payload)
        if msg.action=='U':
            SimpleRF.db.set(msg.nodeId, msg.sensorId, msg.payload)
            self.userLogic(msg)

    def userLogic(self, msg):
        reload(userLogic)
        try:
            actions = userLogic.onChange(msg.nodeId, msg.sensorId, msg.valueFloat, SimpleRF.db.get())
        except:
            self._log.debug('userLogic fail!!!')
            return
        try:
            for line in actions.splitlines():
                tok = line.split('\t')
                self.do(tok[0], tok[1], tok[2])
        except:
            self._log.debug('userLogic action error... action=[{0}]'.format(actions))

    def do(self, nodeId, sensorId, value):
        self._log.info("userLogic action: {0}-{1} := {2}".format(nodeId, sensorId, value))
        SimpleRF.action(nodeId, sensorId, value)