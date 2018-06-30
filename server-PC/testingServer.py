#!/usr/bin/env python

import SimpleRF
import time

SimpleRF.open("COM22")
i = 0
while True:
    i += 1
    msg = SimpleRF.receive(range(1,8))
    if msg.isValid():
        print msg
    SimpleRF.action(7, 2, i%2)
    time.sleep(1.0)