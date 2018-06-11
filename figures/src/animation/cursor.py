import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter


class CursorAnimation(FuncAnimation):
    def __init__(self, figure, axis, time):
        self.time = time
        self.cursor = axis.plot([], [])[0]
        self.ylim = list(axis.get_ylim())
        super().__init__(figure, self.__update, frames=time.size, interval=1, repeat=False)

    def __update(self, frame):
        time = [self.time[frame]] * 2
        self.cursor.set_data(time, self.ylim)
        return self.cursor,

    def save(self, filename, writer=None, fps=1, dpi=None, codec=None,
             bitrate=None, extra_args=None, metadata=None, extra_anim=None,
             savefig_kwargs=None):
        super().save(filename, writer=FFMpegWriter(fps=fps), dpi=dpi, codec=codec,
                     bitrate=bitrate, extra_args=extra_args, metadata=metadata,
                     extra_anim=extra_anim, savefig_kwargs=savefig_kwargs)


t = np.arange(100) * (np.pi / 50.0)
x = np.sin(t)

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(t, x)
animation = CursorAnimation(fig, ax, t)
plt.show()
