"""

"""
from __future__ import division, print_function
import serial
import time

EOL = '\r\n'
ser = serial.Serial(
    port='COM6',
    baudrate=9600,
    timeout=0)

if __name__ == '__main__':

    ser.write("*IDN?"+EOL)
    time.sleep(0.25)

    print(ser.read(ser.inWaiting()).strip(EOL))

    ser.close()
