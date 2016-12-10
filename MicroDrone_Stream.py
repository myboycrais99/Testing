"""

"""

from __future__ import division, print_function
# from Coordinate_Transform import *
# from reference_ellipsoid import ReferenceEllipsoid
from datetime import datetime
import numpy as np
import serial
import threading

__version__ = "0.0.1"

EOL = '\r\n'


class ReadMicroDrone(threading.Thread):
    def __init__(self, port, baudrate):
        threading.Thread.__init__(self)
        self._ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=None
        )

        self._status = self._crc_status = np.NaN
        self._firmware = self._serial = self._nav_mode = np.NaN
        self._integrity_gps = self._integrity_baro = np.NaN
        self._integrity_magnet = self._guidance_mode = self._batt_volt = np.NaN
        self._machine_err_code = self._flight_num = self._crc_system = np.NaN
        self._cmd_throt = self._cmd_pitch = self._cmd_roll = np.NaN
        self._cmd_yaw = self._e_slider = self._f_slider = np.NaN
        self._g_switch = self._h_button = self._i_switch = np.NaN
        self._alt_throt = self._alt_pitch = self._alt_roll = np.NaN
        self._alt_yaw = self._rc_quality, self._rc_flags, self._crc_rc = np.NaN
        self._motor_front = self._motor_left = self._motor_right = np.NaN
        self._motor_rear = self._crc_motor = np.NaN
        self._time_operating = self._gps_itow = self._gps_week = np.NaN
        self._time_flight = self._crc_time = np.NaN
        self._x = self._y = self._z = self._gps_acc = self._num_sats = np.NaN
        self._crc_gps = np.NaN
        self._speed_N = self._speed_E = self._speed_D = np.NaN
        self._speed_acc = self._crc_speed = np.NaN
        self._roll = self._pitch = self._yaw = self._crc_attitude = np.NaN
        self._height_rel = self._temperature = self._crc_altitude = np.NaN
        self._mag_x = self._mag_y = self._mag_z = self._crc_mag = np.NaN
        self._rel_pos_N = self._rel_pos_E = self._rel_pos_D = np.NaN
        self._crc_rel_pos = np.NaN
        self._way_set = self._way_info = self._way_state = np.NaN
        self._way_id = self._crc_way = np.NaN
        self._pay_id = self._pay_value = self._crc_pay = np.NaN

        self.read()

    def read(self):

        # The emulator sometimes has an issue with input buffer. This line
        # reads the first line of data and ignores it.
        self._ser.readline()

        while True:
            data = self._ser.readline().rstrip().split(',')
            line_code = data[0]

            if line_code == '#0':  # Block 0 - Downlink Status
                # status code: 0 = tx err, 1 = timeout err, 2 = no signal
                self._status, self._crc_status = data[1:]

            elif line_code == '#1':  # Block 1 - System
                [self._firmware, self._serial, self._nav_mode,
                 self._integrity_gps, self._integrity_baro,
                 self._integrity_magnet, self._guidance_mode, self._batt_volt,
                 self._machine_err_code, self._flight_num,
                 self._crc_system] = data[1:]

            elif line_code == '#2':  # Block 2 - Remote Control
                [self._cmd_throt, self._cmd_pitch, self._cmd_roll,
                 self._cmd_yaw, self._e_slider, self._f_slider, self._g_switch,
                 self._h_button, self._i_switch, self._alt_throt,
                 self._alt_pitch, self._alt_roll, self._alt_yaw,
                 self._rc_quality, self._rc_flags, self._crc_rc] = data[1:]

            elif line_code == '#3':  # Block 3 - Motors
                [self._motor_front, self._motor_left, self._motor_right,
                 self._motor_rear, self._crc_motor] = data[1:]

            elif line_code == '#4':  # Block 4 - Time Data
                [self._time_operating, self._gps_itow, self._gps_week,
                 self._time_flight, self._crc_time] = data[1:]

            elif line_code == '#5':  # Block 5 - GPS Position
                [x, y, z, self._gps_acc, self._num_sats,
                 self._crc_gps] = data[1:]
                self._x, self._y, self._z = np.asarray([x, y, z], float) / 100
                print(datetime.now())
                # print(x, y, z)

            elif line_code == '#6':  # Block 6 - GPS Speed
                [self._speed_N, self._speed_E, self._speed_D, self._speed_acc,
                 self._crc_speed] = data[1:]

            elif line_code == '#7':  # Block 7 - Attitude
                [self._roll, self._pitch, self._yaw,
                 self._crc_attitude] = data[1:]

            elif line_code == '#8':  # Block 8 - Altitude
                [self._height_rel, _, self._temperature,
                 self._crc_altitude] = data[1:]

            elif line_code == '#9':  # Block 9 - Magnetometer
                x, y, z, self._crc_mag = data[1:]
                [self._mag_x, self._mag_y,
                 self._mag_z] = np.asarray([x, y, z], float) * 1e6 / 10

            elif line_code == '#10':  # Block 10 - Relative Position
                [self._rel_pos_N, self._rel_pos_E, self._rel_pos_D,
                 self._crc_rel_pos] = data[1:]

            elif line_code == '#11':  # Block 11 - Waypoint
                [self._way_set, self._way_info, self._way_state, self._way_id,
                 self._crc_way] = data[1:]

            elif line_code == '#12':  # Block 12 - Payload
                self._pay_id, self._pay_value, self._crc_pay = data[1:]

            elif line_code == '#13':  # Block 13 - Reserved
                pass

            elif line_code == '#14':  # Block 14 - Reserved
                pass

            elif line_code == '#15':  # Block 15 - Reserved
                pass

            elif line_code == '#16':  # Block 16 - Reserved
                pass


if __name__ == '__main__':
    microdrone = ReadMicroDrone('COM12', 115200)

    microdrone.start()
