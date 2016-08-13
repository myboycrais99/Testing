# -*- coding: utf-8 -*-
"""Create a binary data file from data retrieved from an oscilloscope.

"""

from __future__ import division, print_function

import struct
import array

__version__ = "0.0.1"

if __name__ == '__main__':
    pass

    a = array.array('c', ' ' * 1024)

    # The first value in every log file is the version number. As features are
    # added/removed, the offset location of data in the file may change. The
    # exact layout will not change for a given version number. ANY modification
    # to byte layout necessitates incrementing the version number.
    layout = {
        'version': {'type': '8s', 'offset': 0, 'value': __version__},
        't0': {'type': 'd', 'offset': 8, 'value': 0.0},
        'num_pts': {'type': 'L', 'offset': 16, 'value': 25000},
        'dt': {'type': 'd', 'offset': 20, 'value': 1/50e9},
    }

    for param in iter(layout):
        struct.pack_into('{}'.format(layout[param]['type']), a,
                         int(layout[param]['offset']), layout[param]['value'])

    for param in iter(layout):
        b = struct.unpack_from('{}'.format(layout[param]['type']), a,
                               int(layout[param]['offset']))

        print("{}: {}".format(param, b[0]))
