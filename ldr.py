"""
ldr.py

Display analog data from Arduino using Python (matplotlib)

Author: Mahesh Venkitachalam
Website: electronut.in
"""

import argparse
import serial
# import numpy as np
# from time import sleep
from collections import deque

import matplotlib.pyplot as plt
import matplotlib.animation as animation


# plot class
class AnalogPlot:
    # constr
    def __init__(self, str_port, max_len):
        # open serial port
        self.ser = serial.Serial(str_port, 9600)

        self.ax = deque([0.0] * max_len)
        self.ay = deque([0.0] * max_len)
        self.maxLen = max_len

    # add to buffer
    def add_to_buf(self, buf, val):
        if len(buf) < self.maxLen:
            buf.append(val)
        else:
            buf.pop()
            buf.appendleft(val)

    # add data
    def add(self, data):
        assert len(data) == 2
        self.add_to_buf(self.ax, data[0])
        self.add_to_buf(self.ay, data[1])

    # update plot
    def update(self, frame_num, a0, a1):
        try:
            line = self.ser.readline().split(',')
            # data = [float(val) for val in line.split()]
            if line[0] == '#5':
                data = line[1:3]
                # print data
                if len(data) == 2:
                    self.add(data)
                    a0.set_data(range(self.maxLen), self.ax)
                    a1.set_data(range(self.maxLen), self.ay)
        except KeyboardInterrupt:
            print('exiting')

        return a0,

        # clean up

    def close(self):
        # close serial
        self.ser.flush()
        self.ser.close()

        # main() function


def main():
    # create parser
    parser = argparse.ArgumentParser(description="LDR serial")

    # add expected arguments
    parser.add_argument('--port', dest='port', required=True)

    # parse args
    args = parser.parse_args()

    # str_port = '/dev/tty.usbserial-A7006Yqh'
    str_port = args.port

    print('reading from serial port %s...' % str_port)

    # plot parameters
    analog_plot = AnalogPlot(str_port, 100)

    print('plotting data...')

    # set up animation
    fig = plt.figure()
    ax = plt.axes(xlim=(0, 100), ylim=(0, 1023))
    ax.grid(b=True)
    a0, = ax.plot([], [])
    a1, = ax.plot([], [])
    anim = animation.FuncAnimation(fig, analog_plot.update,
                                   fargs=(a0, a1),
                                   interval=5)

    # show plot
    plt.show()

    # clean up
    analog_plot.close()

    print('exiting.')


# call main
if __name__ == '__main__':
    main()
