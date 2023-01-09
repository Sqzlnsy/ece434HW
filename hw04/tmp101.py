#!/usr/bin/env python
# Jason Su @ 01/05/2023
import time
import os

tmp1='0049'
tmp2='004a'
i2cPath="/sys/class/i2c-adapter/i2c-1"
if (not os.path.exists(i2cPath+"/1-"+tmp1)):
    print("tmp101 at " + tmp1 + " has not config yet.")

if (not os.path.exists(i2cPath+"/1-"+tmp2)):
    print("tmp101 at " + tmp2 + " has not config yet.")

f1=open(i2cPath+'/1-'+tmp1+"/hwmon/hwmon0/temp1_input", "r")
f2=open(i2cPath+'/1-'+tmp2+"/hwmon/hwmon1/temp1_input", "r")

try:
  while(True):
    time.sleep(1)
    f1.seek(0)
    f2.seek(0)
    print("Temperature: "+f1.read()[:-1]+" | "+f2.read()[:-1], end='\r')
except KeyboardInterrupt:
    f1.close()
    f2.close()

