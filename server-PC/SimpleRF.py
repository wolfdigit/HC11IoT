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
    return self.payload

def __init__():
  random.seed()
__init__()

def open(comport, baudrate=9600):
  global ser
  ser = serial.Serial(comport, baudrate)

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
  #none = {'nodeId':-1, 'packetId':'A', 'sensorId':0, 'action':'A', 'payload':""}
  none = Message()
  retv = Message()
  startT = time.time()
  while time.time()-startT<0.1:
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
  
'''
def update(nodeId, sensorId, value):
  packetId = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
  msg = formatMsg(nodeId, packetId, sensorId, 'U', str(value))
  ser.write(msg)

def present(nodeId, sensorId, desc):
  packetId = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
  msg = formatMsg(nodeId, packetId, sensorId, 'P', desc)
  ser.write(msg)
'''