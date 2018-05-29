import tty
import sys
import termios
import keyboard
import serial 
import time

class Driver:
    def __init__(self):

        """
        Constructor para poder manejar el carro RC
        """

        self._orig_settings = termios.tcgetattr(sys.stdin)
        self._arduino = serial.Serial('/dev/ttyACM0', 9600)
        time.sleep(2)

    def move_right(self):

        """Procedimiento para moverse hacia la derecha"""
        self._arduino.write('D'.encode())
        
    def move_left(self):
        """Procedimiento para moverse hacia la izquierda"""
        self._arduino.write('A'.encode())
        
    def move_forward(self):
        """Procedimiento para moverse hacia adelante"""
        self._arduino.write('W'.encode())
        
    def move_back(self):
        """Procedimiento para moverse hacia atrás"""
        self._arduino.write('S'.encode())
        
    def stop(self):
        """Procedimiento para detenerse"""
        self._arduino.write('Q'.encode())
        
    def turn_left(self):

        """Procedimiento para girar hacia la izquierda en una curva"""

        i = 0
        self.move_forward()
        time.sleep(0.3)
        self.move_left()
        while i < 4:
            self.move_left()
            time.sleep(0.1)
            i += 1
        self.move_forward()
        time.sleep(0.5)
        self.stop()

        
    def turn_right(self):
        """Procedimiento para girar hacia la derecha en una curva """
        i = 0
        self.move_forward()
        time.sleep(0.3)
        self.move_right()
        while i < 4:
            self.move_right()
            time.sleep(0.1)
            i += 1
        self.move_forward()
        time.sleep(0.5)
        self._stop()
        
    def val_right(self):

        """Procedimiento para moverse hacia la derecha"""

        i = 0
        #self.move_forward()
        #time.sleep(0.1)
        self.move_right()
        while i < 2:
            self.move_right()
            time.sleep(0.2)
            i += 1
        #self.move_forward()
        #time.sleep(0.5)
        self.stop()
        
    def val_left(self):

        """Procedimiento para moverse hacia la izquierda"""
        i = 0
        #self.move_forward()
        #time.sleep(0.1)
        self.move_left()
        while i < 2:
            self.move_left()
            time.sleep(0.2)
            i += 1
        #self.move_forward()
        #time.sleep(0.5)
        self.stop()
        
    def val_stop(self):

        """Procedimiento para hacer la función del stop"""

        self.stop()
        time.sleep(0.6)
        self.val_left()
        time.sleep(0.5)
        self.val_right()
        self.val_right()
        time.sleep(0.5)
        self.val_left()
