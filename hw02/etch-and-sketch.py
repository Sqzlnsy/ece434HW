#!/usr/bin/env python
import curses
import time
import array as arr 
import gpiod

xlen=15
ylen=15

chip=gpiod.Chip('gpiochip1')
lines=chip.get_lines([15, 12, 14, 29])
lines.request(consumer='blink', type=gpiod.LINE_REQ_DIR_IN)

cur=arr.array('i', [1, 2]) #(y, x)
screen = curses.initscr()
my_window = curses.newwin(ylen+1, 2*xlen+2, 0, 0)

def on_press(k):
    if k == "c": 
        my_window.clear()
        my_window.refresh()
        paintWin(xlen, ylen)
    if k == '\x1b': return False
    if cur[0]>ylen: cur[0]=ylen
    if cur[1]>2*xlen: cur[1]=2*xlen
    if cur[0]<1: cur[0]=1
    if cur[1]<2: cur[1]=2

def paintWin(xlen, ylen):
    for x in range(xlen):
        my_window.addstr(0, 2*x+2, str(x))
    for y in range(ylen):
        my_window.addstr(y+1, 0, str(y)+" ")

paintWin(xlen, ylen)
my_window.refresh()

while (1):
    my_window.addstr(cur[0], cur[1], "X")
    my_window.refresh()
    time.sleep(0.1)
    vals=lines.get_values()
    #print(vals)
    cur[0]=cur[0]+vals[0]-vals[1]
    cur[1]=cur[1]+2*(vals[2]-vals[3])
    if cur[0]>ylen: cur[0]=ylen
    if cur[1]>2*xlen: cur[1]=2*xlen
    if cur[0]<1: cur[0]=1
    if cur[1]<2: cur[1]=2
curses.endwin()