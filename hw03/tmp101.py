#!/usr/bin/env python3
# Read tmp101 sensor
# Jason Su on 12/16/2022

import smbus
import time
import gpiod
import sys

bus=smbus.SMBus(2)
address=[0x49, 0x4a]
TH=25
TL=22
chip=gpiod.Chip('gpiochip1')
lines=chip.get_lines([16, 28])
lines.request(consumer='alert', type=gpiod.LINE_REQ_EV_BOTH_EDGES)

def pin_callback(evn, address):
    #print("Pin value changed", end="\r")
    if evn.type == gpiod.LineEvent.FALLING_EDGE:
        temp=bus.read_i2c_block_data(address, 0, 2)
        tmp=temp[0]+temp[1]/64
        #print(tmp)
        print(round(tmp*1.8+32, 2))

bus.write_i2c_block_data(address[0], 2, [round(TL)])
bus.write_i2c_block_data(address[0], 3, [round(TH)])
bus.write_byte_data(address[0], 1, 0x80)
bus.write_i2c_block_data(address[1], 2, [round(TL)])
bus.write_i2c_block_data(address[1], 3, [round(TH)])
bus.write_byte_data(address[1], 1, 0x80)
i=0
while True:
    evn_lines = lines.event_wait(sec=1)
    if evn_lines:
        for line in evn_lines:
            vals=lines.get_values()
            if vals[0]==0:
                pin_callback(line.event_read(), address[i])
            if vals[1]==0:
                pin_callback(line.event_read(), address[1])
