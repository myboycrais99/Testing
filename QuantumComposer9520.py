"""


"""
from __future__ import division, print_function
import serial
import time

EOL = '\r\n'
QC = serial.Serial(
    port='COM3',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

if __name__ == '__main__':

    cmd = '*idn?'
    QC.write(cmd+EOL)
    time.sleep(0.25)

    print(QC.read(QC.inWaiting()).strip(EOL))

    QC.close()