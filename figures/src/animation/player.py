import numpy as np
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
from matplotlib.animation import FuncAnimation, FFMpegWriter

from matplotlib import rcParams
rcParams['text.usetex'] = True
rcParams['font.family'] = 'sans-serif'

import sys
from os import path
current_dir = path.dirname(path.realpath(__file__))
sys.path.append(path.join(current_dir, '..'))
sys.path.append(path.join(current_dir, '../..'))
from muallef.utils import source
from figures.src import util


class CursorPlot(object):
    def __init__(self, data, sample_rate, audio_file):
        # data
        self.audio_file = audio_file
        x = data
        self.fs = sample_rate
        self.t = np.arange(data.size) / float(self.fs)

        # plots
        fig = plt.figure(figsize=(19.2, 10.8))

        # signal plot
        ax_sig = fig.add_subplot(111, ylim=(-1, 1))
        ## signal
        signal_plot = ax_sig.plot(self.t, x, label='Signal')[0]
        ## period lines
        self.cursor = ax_sig.plot([], [], linestyle='-', color='k')[0]
        ## plot accessories
        ax_sig.set_xlabel('Time (s)', fontsize=15)
        ax_sig.set_ylabel('Intensity', fontsize=15)

        # animation
        self.animation = FuncAnimation(fig, self.__update,
                                       frames=data.size, interval=1, repeat=False)

    def __update(self, frame):
        time = [self.t[frame]] * 2
        self.cursor.set_data(time, [-1, 1])
        return self.cursor

    def save_silent(self, output_path):
        self.animation.save(output_path, writer=FFMpegWriter(fps=self.fs))

    def save(self, audio_file=None, video_file=None):
        if not audio_file:
            audio_file = self.audio_file
        if not video_file:
            video_file = util.output_name(audio_file, format='mp4')
        self.save_silent(video_file)
        process_out = util.combine_audio_video(video_file)


input_file = "sounds/violin/violin-a4.wav"
sound = source(input_file)
x = sound.signal
fs = sound.sampleRate
x, fs = x[::128], fs // 128
plot = CursorPlot(x, fs, input_file)
