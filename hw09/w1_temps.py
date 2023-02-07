#!/usr/bin/env python
# Jason Su @ 01/05/2023
import time
import os

w1_path="/sys/class/hwmon"
if (not os.path.exists(w1_path)):
    print("MAX31820 has not config yet.")

f1=open(w1_path+"/hwmon0/temp1_input", "r")
f2=open(w1_path+"/hwmon1/temp1_input", "r")
f3=open(w1_path+"/hwmon2/temp1_input", "r")

try:
  while(True):
    time.sleep(1)
    f1.seek(0)
    f2.seek(0)
    f3.seek(0)
    print("Temperature: "+f1.read()[:-1]+" | "+f2.read()[:-1]+" | "+f3.read()[:-1], end='\r')
except KeyboardInterrupt:
    f1.close()
    f2.close()
    f3.close()

