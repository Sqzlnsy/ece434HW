#!/usr/bin/env python
# Jason Su @ 12/10/2022
import time
import os

# Pin60
pin="60"
GPIOPATH='/sys/class/gpio/'

if (not os.path.exists(GPIOPATH+"gpio"+pin)):
    f=open(GPIOPATH+"export", "w")
    f.write(pin)
    f.close()

f=open(GPIOPATH+"gpio"+pin+"/direction", "w")
f.write("out")
f.close()

f=open(GPIOPATH+"gpio"+pin+"/value", "w")
while True:
    f.seek(0)
    f.write("1")
#    time.sleep(0.5)

    f.seek(0)
    f.write("0")
#    time.sleep(0.5)

f.close()
