import numpy as np
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
from matplotlib.animation import FuncAnimation, FFMpegWriter

from matplotlib import rcParams
rcParams['text.usetex'] = True
rcParams['font.family'] = 'sans-serif'


class FourierPlot(object):
    def __init__(self, signal, sample_rate, t0=0.0, fps=None):
        # data
        self.x = signal
        self.fs = sample_rate
        self.duration = signal.size / float(fs)
        self.t = np.arange(signal.size) / float(fs) + t0
        f = self.t.reshape((t.size, 1))
        E = np.exp(-2j * np.pi * f * self.t)
        self.f = f.squeeze()
        self.z = np.multiply(E, signal)
        self.fourier = np.average(self.z, axis=1)

        # plots
        fig = plt.figure(figsize=(19.2, 10.8))
        grid = GridSpec(2, 2, height_ratios=[1, 2], width_ratios=[1, 2], wspace=0.1, hspace=0.5)
        x_range = (0.0, self.duration)
        #fig.suptitle("Visual demonstration of the Fourier Transform", fontsize=30)

        # signal plot
        ax_sig = fig.add_subplot(grid[0, :], xlim=x_range)
        ax_sig.set_title(r'$x(t)$', pad=20, fontsize=20)
        ## signal
        self.sig_plot = ax_sig.plot(self.t, self.x, label='Signal')[0]
        ## period lines
        nb_lines = int(round(self.duration * self.f[-1]))
        self.sig_lines = tuple([ax_sig.plot([], [], linestyle='--', color='k')[0] for i in range(nb_lines)])
        self.sig_lines[0].set_label('Period')
        ## plot accessories
        ax_sig.legend(loc='upper right')
        ax_sig.set_xlabel('Time (s)', fontsize=15)
        ax_sig.set_ylabel('Intensity', fontsize=15)

        # polar plot
        ax_polar = fig.add_subplot(grid[1, 0])
        ax_polar.set_title(r'$x(t)\cdot e^{-2\pi ft}$', pad=20, fontsize=20)
        ax_polar.axis('equal')
        ax_polar.axis([-1.5, 1.5, -1.5, 1.5])
        self.polar = ax_polar.plot([], [], label='Signal')[0]
        self.center = {
            'point': ax_polar.plot([], [], 'ro', label='Barycenter')[0],
            'abs': ax_polar.plot([],[], color='r', linestyle='-')[0],
        }
        self.freq = ax_polar.text(-1.3, 1.1, '', fontsize=20)
        ax_polar.legend(loc='upper right')
        ax_polar.set_xlabel('Real axis', fontsize=15)
        ax_polar.set_ylabel('Imaginary axis', fontsize=15)

        # fourier
        subgrid = GridSpecFromSubplotSpec(2, 1, subplot_spec=grid[1, 1], hspace=0.0)
        ax_cartesian = fig.add_subplot(subgrid[0, 0], xlim=x_range, ylim=(-1.1, 1.1))
        self.ft_real = ax_cartesian.plot([], [], label="Real part")[0]
        self.ft_imag = ax_cartesian.plot([], [], label="Imaginary part")[0]
        ax_cartesian.legend(loc='upper right')
        ax_cartesian.set_xticks([])
        barycenter = r'$\frac{1}{t_2-t_1}\int\limits_{t_1}^{t_2} x(t)\cdot e^{-2\pi ft}\cdot \mathrm{d}t$'
        ax_cartesian.set_title(barycenter, fontsize=20)

        ax_magnitude = fig.add_subplot(subgrid[1, 0], xlim=x_range, ylim=(-1.1, 1.1))
        self.ft_abs = ax_magnitude.plot([], [], label="Magnitude")[0]
        ax_magnitude.legend(loc='upper right')
        ax_magnitude.set_xlabel('Frequency (Hz)', fontsize=15)

        # animation
        self.animation = FuncAnimation(fig, self.__update,
                                       frames=signal.size, interval=1, repeat=False)

    def __update(self, frame):
        self.__update_signal(frame)
        self.__update_polar(frame)
        self.__update_fourier(frame)
        plots = self.sig_lines + (self.sig_plot,)
        plots += tuple(self.center.values()) + (self.polar,)
        plots += (self.ft_real, self.ft_imag, self.ft_abs,)
        return plots

    def __update_signal(self, frame):
        period = 1.0 / self.f[frame] if frame else 0
        t_seg = 0
        for line in self.sig_lines:
            t_seg += period
            line.set_data([t_seg, t_seg], [-1.1, 1.1])

    def __update_polar(self, frame):
        zf = self.z[frame, :]
        self.polar.set_data(zf.real, zf.imag)
        cf = self.fourier[frame]
        self.center['point'].set_data(cf.real, cf.imag)
        self.center['abs'].set_data([0, cf.real], [0, cf.imag])
        self.freq.set_text(r'$f=' + str(self.f[frame]) + r'$')

    def __update_fourier(self, frame):
        ft = self.fourier
        self.ft_real.set_data(self.f[:frame], ft[:frame].real)
        self.ft_imag.set_data(self.f[:frame], ft[:frame].imag)
        self.ft_abs.set_data(self.f[:frame], np.abs(ft[:frame]))


fs = 1000
duration = 5.0
N = int(fs * duration)
t = np.arange(N) / float(fs)
f0 = 3
x = np.cos(2 * np.pi * f0 * t)
plot = FourierPlot(x, fs)
#plot.animation.save('fourier.mp4', writer=FFMpegWriter(fps=200))
plt.show()
