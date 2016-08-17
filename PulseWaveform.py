"""

"""

from __future__ import division, print_function
import matplotlib.pyplot as plt
import numpy as np

pw_start = 100
pw_stop = 1000
pw_inc = 10

sample_rate = 0.00002e9
dt = 1 / sample_rate
f0 = 0.01e6
pw = 500e-9
num_cycles = 30

steps = np.arange(pw_start, pw_stop + pw_inc, pw_inc)
n = np.zeros(len(steps) * num_cycles, dtype=float)
for i in range(len(steps)):
    n[i * num_cycles:i * num_cycles + num_cycles] = steps[i]

bob = np.zeros(len(n), dtype=float)
bob[1:] = np.cumsum(1 / n[1:])

t_wave = np.arange(0, pw, dt)
# y_wave = np.sin(2*np.pi*f0*t_wave)
y_wave = np.ones_like(t_wave)

t = np.arange(0, bob[-1]+pw, dt)

idx = np.round(bob*sample_rate).astype(np.int64)
t_len = int(len(t_wave))
y = np.zeros(len(t), dtype=float)

for i in idx:
    y[i:i+t_len] = y_wave

# fig, ax = plt.subplots()
# ax.plot(t, y)
# plt.show()

n = y.size
yf = np.fft.fft(y)
xf = np.fft.fftfreq(n, d=1/sample_rate)

fig, ax = plt.subplots()
ax.plot(xf[xf > 0], np.abs(yf[xf > 0]))
ax.set_xlim(0, 2*pw_stop)
plt.show()
