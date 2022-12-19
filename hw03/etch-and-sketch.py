#!/usr/bin/env python
#Jason Su 12/18/2022
import curses
import array as arr 
import smbus
import time
import numpy as np 
import gpiod
from datetime import timedelta

COUNTERPATH1='/dev/bone/counter/1/count0'
COUNTERPATH2='/dev/bone/counter/2/count0'
maxCount='100000'
gap=5

bus = smbus.SMBus(2)  
LEDM = 0x70        

xlen=8
ylen=8


cur=arr.array('i', [0, 0]) #(y, x)
screen = curses.initscr()
my_window = curses.newwin(ylen+1, 2*xlen+2, 0, 0)

def paintWin(xlen, ylen):
    for x in range(xlen):
        my_window.addstr(0, 2*x+2, str(x))
    for y in range(ylen):
        my_window.addstr(y+1, 0, str(y)+" ")

def paintX(cur):
    my_window.addstr(cur[0]+1, cur[1]*2+2, "X")

def paintPixel(cur):
    temp=matrixConvert(matrix,cur[1])
    bus.write_byte_data(LEDM, cur[1]*2, temp)
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
    
f1=open(COUNTERPATH1+'/ceiling', 'w')
f1.write(maxCount)
f1.close()
f2=open(COUNTERPATH2+'/ceiling', 'w')
f2.write(maxCount)
f2.close()
f1=open(COUNTERPATH1+'/enable', 'w')
f1.write('1')
f1.close()
f2=open(COUNTERPATH2+'/enable', 'w')
f2.write('1')
f2.close()
f1=open(COUNTERPATH1+'/count', 'r')
f2=open(COUNTERPATH2+'/count', 'r')

chip=gpiod.Chip('gpiochip1')
line=chip.get_lines([16])
line.request(consumer='alert', type=gpiod.LINE_REQ_EV_BOTH_EDGES)

paintWin(xlen, ylen)
my_window.refresh()
curses.noecho()
clearMatrix()

olddata1=int(f1.read()[:-1])
olddata2=int(f2.read()[:-1])

while (1):
    paintX(cur)
    matrix[cur[0]][cur[1]]=1
    paintPixel(cur)
    my_window.refresh()
    evn = line.event_wait(0)
    if evn:
        if evn[0].event_read().type == gpiod.LineEvent.FALLING_EDGE: # use pin interrput to clear the screen (could be alert pin of a temp101)
            my_window.clear()
            my_window.refresh()
            paintWin(xlen, ylen)
            clearMatrix()
    f1.seek(0)
    data=int(f1.read()[:-1])
    if data>olddata1+gap: # encode 1 control moving up and down
        olddata1=data
        cur[0]+=1
    elif data < olddata1-gap:
        olddata1=data
        cur[0]-=1
    f2.seek(0)
    data=int(f2.read()[:-1])
    if data>olddata2+gap: # encode 2 control moving left and right
        olddata2=data
        cur[1]+=1
    elif data < olddata2-gap:
        olddata2=data
        cur[1]-=1
    if cur[0]>=ylen: cur[0]=ylen-1
    if cur[1]>=xlen: cur[1]=xlen-1
    if cur[0]<0: cur[0]=0
    if cur[1]<0: cur[1]=0