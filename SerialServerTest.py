"""
This code is a simple example of a server running on a serial port. This code
listens on the designated port, determines if a valid entry is provided, and
then provides the proper response. Otherwise, an error is returned.

Requires the use of a COM port emulator. Currently using com2com available at
"https://sourceforge.net/projects/com0com/".
"""

from __future__ import division, print_function
import time
import serial
import numpy as np


__version__ = "0.0.1"


EOL = '\r\n'

# configure the serial connections (the parameters differs on the device you
# are connecting to)
ser = serial.Serial(
    port='COM5',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

# Valid commands recognized by the device. In this case, I'm just using the
# standard '*IDN?' identification command.
VALID = {"*IDN?": "Ryan's Emulation of a Tektronix DPO7000 Oscilloscope"}

# Set a 50 ms time between querying the serial port to determine if data have
# been received.
poll_time = 0.05

# Run a continuous loop. Program has to be manually aborted.
while True:
    time.sleep(poll_time)

    if ser.inWaiting() > 0:
        # inWaiting provides the current number of bytes in the buffer. Using
        # this method rather than reading a single byte at a time.
        input_str = ser.read(ser.inWaiting()).strip(EOL)

        # Determine if the input_str is in the valid commands.
        if input_str in VALID.keys():
            out = VALID[input_str]

        else:
            out = "ERROR"

        # Use a beta distribution to add some randomness in the time required
        # for the device to respond. Currently using an average response time
        # of 50 ms but can be as little as 25 ms or as high as 200 ms.
        time.sleep(np.random.beta(2, 50) + 0.025)


        ser.write(out + EOL)
