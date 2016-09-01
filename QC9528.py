"""
This program simulates a Quantum Composer 9528 pulser.
"""
from __future__ import division, print_function
import time
import serial
import numpy as np

# ERROR = {
#     '?1': "Incorrect prefix, i.e. no colon or * to start command.",
#     '?2': "Missing command keyword.",
#     '?3': "Invalid command keyword.",
#     '?4': "Missing parameter.",
#     '?5': "Invalid parameter.",
#     '?6': "Query only, command needs a question mark.",
#     '?7': "Invalid query, command does not have a query form.",
#     '?8': "Command unavailable in current system state."
# }
#
# EOL = '\r\n'
#
# # bob = ['INST', 'INSTRUMENT',
# #        'CAT', 'CATALOG',
# #        'FULL',
# #        'COMM', 'COMMANDS',
# #        'NSEL', 'NSELECT',
# #        'SEL', 'SELECT',
# #        'STAT', 'STATE',
# #        'PULS', 'PULSE',
# #        'COUN', 'COUNTER',
# #        'CL', 'CLEAR',
# #        'COUN', 'COUNTS',
# #        'PER', 'PERIOD',
# #        'MOD', 'MODE',
# #        'BCO', 'BCOUNTER',
# #        'PCO', 'PCOUNTER',
# #        'OCO', 'OCOUNTER',
# #        'ICL', 'ICLOCK',
# #        'OCL', 'OCLOCK',
# #        'GAT', 'GATE',
# #        'LOG', 'LOGIC',
# #        'LEV', 'LEVEL',
# #        'TRIG', 'TRIGGER',
# #        'WIDT', 'WIDTH',
# #        'DEL', 'DELAY',
# #        'SYNC',
# #        'MUX',
# #        ]
#
# VALUE = {
#     'inst_cat': 'TO, CHA, CHB, CHC, CHD, CHE, CHF, CHG, CHH',
#     'inst_full': ('T0, 0, CHA, 1, CHB, 2, CHC, 3, CHD, 4, CHE, 5, CHF, 6,'
#                   'CHG, 7, CHH, 8'),
#     'inst_comm': 'Not sure what QC should return here...',
#     'inst_nsel': '0',
#     'inst_sel': 'CHA',
#     'inst_stat': '0',
#     'puls_coun_stat': '0',
# }
#
# inst = {
#     'CAT': {'valid': None, 'value': 'inst_cat'},
#     'CATALOG': {'valid': None, 'value': 'inst_cat'},
#     'FULL': {'valid': None, 'value': 'inst_full'},
#     'COMM': {'valid': None, 'value': 'inst_comm'},
#     'COMMANDS': {'valid': None, 'value': 'inst_comm'},
#     'NSEL': {'valid': str(range(9)), 'value': 'inst_nsel'},
#     'NSELECT': {'valid': str(range(9)), 'value': 'inst_nsel'},
#     'SEL': {'valid': ['T0', 'CHA', 'CHB', 'CHC', 'CHD', 'CHE', 'CHF', 'CHG',
#                       'CHH'], 'value': 'inst_sel'},
#     'SELECT': {'valid': ['T0', 'CHA', 'CHB', 'CHC', 'CHD', 'CHE', 'CHF',
#                          'CHG', 'CHH'], 'value': 'inst_sel'},
#     'STAT': {'valid': ['0', '1'], 'value': 'inst_stat'},
#     'STATE': {'valid': ['0', '1'], 'value': 'inst_stat'},
# }
#
# coun = {
#     'STAT': {'valid': ['0', '1'], 'value': 'puls_coun_stat'},
#     'STATE': {'valid': ['0', '1'], 'value': 'puls_coun_stat'},
#     'CL': '',
#     'CLEAR': '',
# }
#
# puls0 = {
#     'COUN': coun,
#     'COUNTER': coun,
#
# }
#
#
# level1 = {
#     'INST': inst,
#     'INSTRUMENT': inst,
#     'PULS0': puls0,
#     'PULSE0': puls0,
# }
#
# def process(cmd):
#     cmd = cmd.upper()
#
#     if cmd[0] not in ['*', ':']:
#         print(ERROR['?1'])
#         return
#     else:
#         cmd = cmd[1:]
#         b = cmd.split(':')
#
#     # Check to see if string is a query or a setter command
#     if b[-1][-1] is '?':
#         query = True
#         b[-1] = b[-1][:-1]
#     elif ' ' in b[-1]:
#         query = False
#         val = b[-1].split(' ')[-1]
#         b[-1] = b[-1].split(' ')[0]
#     else:
#         print(ERROR['?4'])
#         return
#
#     tmp = level1
#     for i in range(len(b)):
#         if b[i] in tmp:
#             tmp = tmp[b[i]]
#         else:
#             print(ERROR['?3'])
#             return
#
#
#     try:
#         if query:
#             print(VALUE[tmp['value']])
#         else:
#             if tmp['valid'] is None:
#                 print(ERROR['?6'])
#                 return
#             else:
#                 if val == 'ON':
#                     val = '1'
#                 elif val == 'OFF':
#                     val = '0'
#
#                 if val in tmp['valid']:
#                     VALUE[tmp['value']] = val
#                     print(VALUE[tmp['value']])
#                 else:
#                     print(ERROR['?5'])
#                     return
#     except KeyError:
#         print(ERROR['?2'])
#         return
#
# if __name__ == '__main__':
#
#     cmd = ':PULS0:COUN:STAT 1'
#
#     process(cmd)

__version__ = "0.0.1"

EOL = '\r\n'

# # configure the serial connections (the parameters differs on the device you
# # are connecting to)
# ser = serial.Serial(
#     port='COM4',
#     baudrate=9600,
#     parity=serial.PARITY_ODD,
#     stopbits=serial.STOPBITS_TWO,
#     bytesize=serial.SEVENBITS
# )
#
# # Valid commands recognized by the device. In this case, I'm just using the
# # standard '*IDN?' identification command.
# VALID = {"*IDN?": "Ryan's Emulation of a Quantum Composer 9528"}
#
# # Set a 50 ms time between querying the serial port to determine if data have
# # been received.
# poll_time = 0.05
#
# # Run a continuous loop. Program has to be manually aborted.
# while True:
#     time.sleep(poll_time)
#
#     if ser.inWaiting() > 0:
#         # inWaiting provides the current number of bytes in the buffer. Using
#         # this method rather than reading a single byte at a time.
#         input_str = ser.read(ser.inWaiting()).strip(EOL)
#
#         input_str = input_str.upper()
#
#         # Determine if the input_str is in the valid commands.
#         if input_str in VALID.keys():
#             out = VALID[input_str]
#
#         else:
#             out = "ERROR"
#
#         # Use a beta distribution to add some randomness in the time required
#         # for the device to respond. Currently using an average response time
#         # of 50 ms but can be as little as 25 ms or as high as 200 ms.
#         time.sleep(np.random.beta(2, 50) + 0.025)
#
#         ser.write(out + EOL)


import threading
import Queue
import time, random

WORKERS = 100

class Worker(threading.Thread):

    def __init__(self, queue):
        self.__queue = queue
        threading.Thread.__init__(self)

    def run(self):
        while 1:
            item = self.__queue.get()
            if item is None:
                break # reached end of queue

            # pretend we're doing something that takes 10-100 ms
            time.sleep(random.randint(10, 100) / 1000.0)

            print("task {} finished".format(item))

#
# try it

queue = Queue.Queue(0)

for i in range(WORKERS):
    Worker(queue).start() # start a worker

for i in range(100):
    queue.put(i)

for i in range(WORKERS):
    queue.put(None) # add end-of-queue markers


