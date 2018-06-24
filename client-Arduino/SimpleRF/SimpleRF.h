#ifndef _SIMPLERF_H_
#define _SIMPLERF_H_

#ifndef NODEID
#define NODEID 1
#endif

void initVariant() {
  randomSeed(analogRead(0));
  Serial1.begin(9600);
}

String formatMsg(int nodeId, String packetId, int sensorId, String action, String payload) {
  String msg = String("#") +String(nodeId)+String(",") +packetId+String(",") +String(sensorId)+String(",") +action+String(",") +payload+String("\n");
  return msg;
}

void present(int nodeId, int sensorId, String desc) {
  char packetId[] = "A";
  packetId[0] += random(1,26);
  String msg = formatMsg(nodeId, packetId, sensorId, "P", desc);
  Serial1.write(msg.c_str(), msg.length());
}
void present(int sensorId, String desc) {
  present(NODEID, sensorId, desc);
}

void update(int nodeId, int sensorId, String value) {
  char packetId[] = "A";
  packetId[0] += random(1,26);
  String msg = formatMsg(nodeId, packetId, sensorId, "U", value);
  Serial1.write(msg.c_str(), msg.length());
}
void update(int sensorId, String value) {
  update(NODEID, sensorId, value);
}
void update(int nodeId, int sensorId, int value) {
  update(nodeId, sensorId, String(value));
}
void update(int sensorId, int value) {
  update(NODEID, sensorId, value);
}
void update(int nodeId, int sensorId, float value) {
  update(nodeId, sensorId, String(value));
}
void update(int sensorId, float value) {
  update(NODEID, sensorId, value);
}

class Message {
  public:
  int nodeId=-1;
  char packetId='A';
  int sensorId=0;
  char action='A';
  String payload="";

  bool isValid() {
    return nodeId>=0;
  }

  int valueInt() {
    return payload.toInt();
  }

  float valueFloat() {
    return payload.toFloat();
  }

  String valueString() {
    return payload;
  }
};

// #33,P,12,ACT,payload\n
// # node, packetid, sensor id, action, payload \n
// action: present, update, act, req = {P, U, A, R}
Message parseMsg(char line[], int len) {
  static const Message none = Message();
  Message retv = Message();
  int i,j;
  for (i=1,j=i; j<len&&line[j]!=','; j++);
  if (j==len) return none;
  line[j] = '\0';
  retv.nodeId = String(line+i).toInt();
  i = j+1;
  retv.packetId = line[i];
  for (i=i+2,j=i; j<len&&line[j]!=','; j++);
  if (j==len) return none;
  line[j] = '\0';
  retv.sensorId = String(line+i).toInt();
  i = j+1;
  retv.action = line[i];
  retv.payload = String(line+i+2);
  return retv;
}

Message receive(int nodeId=NODEID) {
  static char line[1024];
  static int len=0;

  Message retv = Message();

  unsigned long startT = millis();
  while (millis()-startT<100) {
    while (Serial1.available()>0) {
      int c = Serial1.read();
      if (c=='#') {
        len = 0;
        line[len++] = c;
      }
      else if (c=='\n') {
        line[len] = '\0';
        Message newMsg = parseMsg(line, len);
        if (nodeId<0 || newMsg.nodeId==nodeId) {
          retv = newMsg;
        }
      }
      else {
        line[len++] = c;
      }
    }
  }

  return retv;
}

#define COMBINE(X,Y) X##Y
#define _tVar(line) COMBINE(_timer,line)
#define forEvery(_t) static unsigned long _tVar(__LINE__) = 0; if ( millis()-_tVar(__LINE__)>=_t&&((_tVar(__LINE__)=millis())||1) )

#endif  // _SIMPLERF_H_
