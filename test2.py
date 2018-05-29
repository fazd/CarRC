import tty
import sys
import termios
import keyboard
import serial 
import time

orig_settings = termios.tcgetattr(sys.stdin)
arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)

tty.setraw(sys.stdin)
x = 0
while x != chr(27): # ESC
    x=sys.stdin.read(1)[0]
    #print(sys.stdin.read(1))
    sys.stdout.flush()
    #print("You pressed", x)
    if x == 'w':
        #print('You Pressed w!')
        #time.sleep(1) 
        arduino.write('W'.encode())
        #time.sleep(0.1)
    elif x == 'a':
        #print('You Pressed a!')
        #time.sleep(1) 
        arduino.write('A'.encode())
        #time.sleep(0.05)
    elif x == 's': 
        #print('You Pressed s!')
        #time.sleep(1) 
        arduino.write('S'.encode())
        #time.sleep(0.05)
    elif x == 'd': 
        #print('You Pressed d!')
        #time.sleep(1) 
        arduino.write('D'.encode())
        #time.sleep(0.05)
    else: 
        #print('You Pressed q!')
        #time.sleep(1) 
        arduino.write('Q'.encode())
    #arduino.write('Q'.encode()) 

termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)