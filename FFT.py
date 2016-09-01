"""

"""
from __future__ import division, print_function
import matplotlib.pyplot as plt
import numpy as np

f0 = 100e6
sample_rate = 1e9
t = np.arange(0, 10e-6, 1/sample_rate)
y = np.sin(2*np.pi*f0*t)

# fig, ax = plt.subplots()
# ax.plot(t, y)
# plt.show()

n = y.size
yf = np.fft.fft(y)
xf = np.fft.fftfreq(n, d=1/sample_rate)

fig, ax = plt.subplots()
ax.plot(xf[xf > 0], np.abs(yf[xf > 0]))
plt.show()