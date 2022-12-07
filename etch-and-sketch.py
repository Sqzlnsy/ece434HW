import curses
from pynput import keyboard
import array as arr 

xlen=10
ylen=10


cur=arr.array('i', [1, 2]) #(y, x)
screen = curses.initscr()
my_window = curses.newwin(ylen+1, 2*xlen+1, 0, 0)

def on_press(key):
    if key == keyboard.Key.esc:
        return False 
    try:
        k = key.char
    except:
        k = key.name 
    if k in ['up', 'down', 'left', 'right', 'esc', 'c']:  
        if k == "up": cur[0]=cur[0]-1
        if k == "down": cur[0]=cur[0]+1
        if k == "left": cur[1]=cur[1]-2
        if k == "right": cur[1]=cur[1]+2
        if k == "c": 
            my_window.clear()
            my_window.refresh()
            paintWin(xlen, ylen)
        if k=="esc": return False  
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

listener = keyboard.Listener(on_press=on_press)
listener.start()  

while (1):
    my_window.addstr(cur[0], cur[1], "X")
    my_window.refresh()