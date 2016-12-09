"""

"""

from __future__ import division, print_function
import time
import serial


__version__ = '0.0.1'

# try:
#     ser.close()
# except NameError:
#     pass


EOL = '\r\n'
UAS_DATARATE = 0.10  # Ardupilot has a 10 Hz data stream rate

ser = serial.Serial(
    port='COM10',
    baudrate=115200
)


with open('MicroDrone_data_stream.txt', 'r') as f:
    data = f.readlines()

while True:
    for i, out in enumerate(data):

        if out[:2] == '#1':
            ser.flushOutput()
            time.sleep(UAS_DATARATE)

        ser.write(out)
