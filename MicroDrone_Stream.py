"""

"""

from __future__ import division, print_function
# from Coordinate_Transform import *
# from reference_ellipsoid import ReferenceEllipsoid
import serial


__version__ = "0.0.1"


EOL = '\r\n'

# try:
#     ser.close()
# except NameError:
#     pass

ser = serial.Serial(
    port='COM12',
    baudrate=115200,
    timeout=None
    )

# ellipse = ReferenceEllipsoid('wgs84')

if __name__ == '__main__':

    while True:
        data = ser.readline().rstrip().split(',')

        if data[0] == '#5':
            X, Y, Z, gps_acc, num_sats, crc_gps = data[1:]

            print(X, Y, Z)
