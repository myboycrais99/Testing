"""

"""

from __future__ import division, print_function
from datetime import datetime
import time
import serial

__version__ = '0.0.1'

EOL = '\r\n'
UAS_DATARATE = 0.10  # Ardupilot has a 10 Hz data stream rate

ser = serial.Serial(
    port='COM10',
    baudrate=115200,
    writeTimeout=0
)


with open('MicroDrone_data_stream.txt', 'r') as f:
    data = f.readlines()

    mavlink = ''
    for i, out in enumerate(data):
        mavlink += out

while True:
    start = datetime.now()

    ser.flushOutput()
    ser.write(mavlink)

    t = (datetime.now()-start).total_seconds()
    if t > UAS_DATARATE:
        pass
    else:
        time.sleep(UAS_DATARATE - t)
