#!/usr/bin/env python3
# Jason Su @ 01/07/2023
from flask import Flask, request, render_template
import curses
import array as arr 
import smbus
import time
import numpy as np 

app = Flask(__name__)
bus = smbus.SMBus(1)  
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

@app.route("/", methods=['GET'])
def index():
    clearMatrix()
    paintPixel(cur, 1)
    templateData = {
            'title' : 'LED Matrix',
        }
    return render_template('index.html',**templateData)
@app.route("/<action>", methods=['GET'])
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
    if cur[0]>=ylen: cur[0]=ylen-1
    if cur[1]>=xlen: cur[1]=xlen-1
    if cur[0]<0: cur[0]=0
    if cur[1]<0: cur[1]=0
    matrix[cur[0]][cur[1]]=1
    paintPixel(cur, 1)    
    templateData = {
            'title' : 'LED Matrix',
        }
    return render_template('index.html',**templateData)



if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8081)