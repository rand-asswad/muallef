import numpy as np
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec

from matplotlib import rcParams
rcParams['text.usetex'] = True
rcParams['font.family'] = 'sans-serif'

fs = 1000
duration = 4.0
N = int(fs * duration)
t = np.arange(N) / float(fs)
f0 = 1.0
f2 = 4 * f0

x1 = np.sin(2 * np.pi * f0 * t)
x2 = np.cos(2*np.pi * f2 * t)
x = x1 + 0.5 * x2

f_max = 6.0
f = np.arange(fs * f_max) / float(fs)
E = np.exp(-2j * np.pi * f.reshape((f.size, 1)) * t)

z1 = np.dot(E, x1)
z2 = np.dot(E, x2)
z = np.dot(E, x)

fig = plt.figure(figsize=(19.2, 10.8))
#fig.suptitle("Linearity of Fourier Transform", fontsize=25)
gs = GridSpec(3, 2, hspace=0.6)

ax10 = fig.add_subplot(gs[0, 0])
ax10.set_title(r'$x_1(t)$', pad=20, fontsize=20)
plt.plot(t, x1)
ax20 = fig.add_subplot(gs[1, 0])
ax20.set_title(r'$x_2(t)$', pad=20, fontsize=20)
plt.plot(t, x2)
ax0 = fig.add_subplot(gs[2, 0])
ax0.set_title(r'$x(t)=x_1(t)+\frac{1}{2}x_2(t)$', pad=20, fontsize=20)
ax0.set_xlabel('Time (s)', fontsize=15)
plt.plot(t, x)

ax11 = fig.add_subplot(gs[0, 1])
ax11.set_title(r'$\hat{x}_1(f)$', pad=20, fontsize=20)
plt.plot(f, z1.real, label="Real part")
plt.plot(f, z1.imag, label="Imaginary part")
ax11.legend(loc='upper right')

ax21 = fig.add_subplot(gs[1, 1])
ax21.set_title(r'$\hat{x}_2(f)$', pad=20, fontsize=20)
plt.plot(f, z2.real, label="Real part")
plt.plot(f, z2.imag, label="Imaginary part")
ax21.legend(loc='upper right')

ax1 = fig.add_subplot(gs[2, 1])
ax1.set_title(r'$\hat{x}(f)$', pad=20, fontsize=20)
ax1.set_xlabel('Frequency (Hz)', fontsize=15)
plt.plot(f, z.real, label="Real part")
plt.plot(f, z.imag, label="Imaginary part")
ax1.legend(loc='upper right')

plt.savefig('../../out/fourier_linearity.png')
