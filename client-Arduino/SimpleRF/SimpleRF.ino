#define NODEID 7

#include "SimpleRF.h"

void setup() {
  pinMode(13, OUTPUT);
}

void presentation() {
  present(1, "millisecond");
  present(2, "LED13");
}

void loop() {
  forEvery(60000) {
    presentation();
  }
  
  forEvery(3000) {
    update(1, millis());
  }

  Message msg = receive();
  if (msg.sensorId==2) {
    digitalWrite(13, msg.valueInt());
  }
}
