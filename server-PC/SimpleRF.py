import serial
import random
import time

ser = None

class Message:
  nodeId = -1
  packetId = 'A'
  sensorId = 0
  action = 'A'
  payload = ""
  def __str__(self):
    return self.__dict__.__str__()
  def __repr__(self):
    return self.__str__()
  def isValid(self):
    return self.nodeId>=0
  @property
  def valueInt(self):
    try:
      return int(self.payload)
    except:
      return None
  @property
  def valueFloat(self):
    try:
      return float(self.payload)
    except:
      return None
  @property
  def valueString(self):
    return str(self.payload)

def __init__():
  random.seed()
__init__()

def open(comport, baudrate=9600):
  global ser
  if not ser or not ser.isOpen():
    ser = serial.Serial(comport, baudrate)
    if not ser.isOpen():
      ser.open()

def close():
  global ser
  if ser.isOpen():
    ser.close()
  #ser = None
  
def isOpen():
  return ser.isOpen()

def parseMsg(line):
  #none = {'nodeId':-1, 'packetId':'A', 'sensorId':0, 'action':'A', 'payload':""}
  none = Message()
  retv = Message()
  if line[0]=='#':
    try:
      i = j = 1
      while j<len(line) and line[j]!=',':
        j += 1
      #retv['nodeId'] = int(line[i:j])
      retv.nodeId = int(line[i:j])
      #retv['packetId'] = line[j+1]
      retv.packetId = line[j+1]
      i = j+3
      j = i
      while j<len(line) and line[j]!=',':
        j += 1
      #retv['sensorId'] = int(line[i:j])
      retv.sensorId = int(line[i:j])
      #retv['action'] = line[j+1]
      retv.action = line[j+1]
      #retv['payload'] = line[j+3:]
      retv.payload = line[j+3:-1]
    except:
      retv = none
  return retv


def receive(nodeIds=[]):
  retv = Message()
  if not ser.isOpen():
    return retv
  while ser.in_waiting>0:
    line = ser.readline()
    msg = parseMsg(line)
    if nodeIds==[] or msg.nodeId in nodeIds:
      retv = msg
  return retv

def formatMsg(nodeId, packetId, sensorId, action, payload):
  return "#"+str(nodeId)+","+packetId+","+str(sensorId)+","+action+","+payload+"\n"

def action(nodeId, sensorId, value):
  packetId = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
  msg = formatMsg(nodeId, packetId, sensorId, 'D', str(value))
  ser.write(msg)
  
class record():
  nodeId = -1
  sensorId = -1
  desc = ""
  value = -1
  lastSeen = -1

  def __init__(self, nodeId, sensorId, desc="", value=-1, lastSeen=time.time()):
    self.nodeId = nodeId
    self.sensorId = sensorId
    self.desc = desc
    self.value = value
    self.lastSeen = lastSeen
  def __str__(self):
    return self.__dict__.__str__()
  def __repr__(self):
    return self.__str__()
  @property
  def valueInt(self):
    try:
      return int(self.value)
    except:
      return None
  @property
  def valueFloat(self):
    try:
      return float(self.value)
    except:
      return None
  @property
  def valueString(self):
    return str(self.value)


class Db():
  # nodeId, sensorId, desc, last value, last seen
  _db = {}
  def get(self, nodeId=-1, sensorId=-1):
    if nodeId<0:
      return self._db
    if sensorId>=0:
      key = (nodeId,sensorId)
      if key in self._db:
        return { key: self._db[key] }
      else:
        return {}
    retv = {}
    for k in self._db:
      if k[0]==nodeId:
        retv[k] = self._db[k]
    return retv

  def set(self, nodeId, sensorId, value):
    if (nodeId,sensorId) in self._db:
      newRcd = self._db[(nodeId,sensorId)]
      newRcd.value = value
      newRcd.lastSeen = time.time()
    else:
      newRcd = record(nodeId, sensorId, "no desc", value)
    self._db[(nodeId,sensorId)] = newRcd

  def present(self, nodeId, sensorId, desc):
    if (nodeId,sensorId) in self._db:
      newRcd = self._db[(nodeId,sensorId)]
      newRcd.desc = desc
      #newRcd.lastSeen = time.time()
    else:
      newRcd = record(nodeId, sensorId, desc)
    self._db[(nodeId,sensorId)] = newRcd
db = Db()