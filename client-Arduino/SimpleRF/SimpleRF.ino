#define NODEID 7

#include "SimpleRF.h"

void setup() {
  present(1, "output");
  present(2, "LED13");
  pinMode(13, OUTPUT);
}

void loop() {
  forEvery(3000) {
    update(1, "XD");
  }

  Message msg = receive();
  if (msg.sensorId==2) {
    digitalWrite(13, msg.valueInt());
  }
}
