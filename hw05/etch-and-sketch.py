#!/usr/bin/env python3
# Jason Su @ 01/16/2023
import curses
import array as arr 
import smbus
import time
import numpy as np 
import os

imu='0053'
i2cPath="/sys/class/i2c-adapter/i2c-2"

bus = smbus.SMBus(2)  
LEDM = 0x70        

xlen=8
ylen=8


cur=arr.array('i', [0, 0]) #(y, x)

def paintPixel(cur, k):
    temp=matrixConvert(matrix,cur[1])
    bus.write_byte_data(LEDM, cur[1]*2, temp)
    if k:
        temp&=~(1<<cur[0])
    bus.write_byte_data(LEDM, cur[1]*2+1, temp)

def clearMatrix():
    global matrix
    matrix=np.zeros((ylen, xlen), dtype=np.uint8)
    bus.write_byte_data(LEDM, 0x80, 0) 
    bus.write_byte_data(LEDM, 0x21, 0)   # Start oscillator (p10)
    bus.write_i2c_block_data(LEDM, 0, [0]*(2*xlen))
    bus.write_byte_data(LEDM, 0x81, 0)   # Disp on, blink off (p11)
    bus.write_byte_data(LEDM, 0xe7, 0)   # Full brightness (page 15)

def matrixConvert(mat, col):
    if (col>=0):
        sum=0
        for i in range(ylen):
            sum+=(mat[i][col]<<i)
    else: 
        sum=[0]*8
        for i in range(xlen):
            for j in range(ylen):
                sum[i]+=(mat[j][i]<<j)
    return sum    

clearMatrix()
matrix[cur[0]][cur[1]]=1
paintPixel(cur, 1)
if (not os.path.exists(i2cPath+"/2-"+imu+"/iio:device1")):
    print("adxl345 " + imu + " has not config yet.")
fx=open(i2cPath+'/2-'+imu+"/iio:device1/in_accel_x_raw", "r")
fy=open(i2cPath+'/2-'+imu+"/iio:device1/in_accel_y_raw", "r")
fz=open(i2cPath+'/2-'+imu+"/iio:device1/in_accel_z_raw", "r")

def move(action):
    if action == 'up':
        print("Move Up")
        cur[0]-=1
    elif action == 'down':
        print("Move Down")
        cur[0]+=1
    elif action == 'left':
        print("Move Left")
        paintPixel(cur, 0)
        cur[1]+=1
    elif action == 'right':
        print("Move Right")
        paintPixel(cur, 0)
        cur[1]-=1
    elif action == 'clear':
        clearMatrix()
    if cur[0]>=ylen: cur[0]=ylen-1
    if cur[1]>=xlen: cur[1]=xlen-1
    if cur[0]<0: cur[0]=0
    if cur[1]<0: cur[1]=0
    matrix[cur[0]][cur[1]]=1
    paintPixel(cur, 1)    

try:
  while(True):
    time.sleep(1)
    fx.seek(0)
    fy.seek(0)
    fz.seek(0)
    x_accel=fx.read()[:-1]
    y_accel=fy.read()[:-1]
    z_accel=fz.read()[:-1]
    #print("X-axis: "+x_accel+" | Y-axis: "+y_accel+" | Z-axis: "+z_accel+"   ", end='\r')
    if int(x_accel)>=100:
        move('left')
    elif int(x_accel)<=-100:
        move('right')
    if int(y_accel)>=100:
        move('down')
    elif int(y_accel)<=-100:
        move('up')
    if int(z_accel)<=-10:
        move('clear')
except KeyboardInterrupt:
    fx.close()
    fy.close()
    fz.close()
