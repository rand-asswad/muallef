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
sys.path.append(path.join(current_dir, '../../..'))
from muallef.utils import source
from muallef.onset import onset_function
from muallef.onset.peak_picker import peak_pick
from figures.src.util import output_name

violin = source("sounds/violin/violin-a4.wav")
piano = source("sounds/piano/piano-a4.wav")

down = 2.0
fig = plt.figure(figsize=(19.2/down, 10.8/down))
#fig.suptitle("Linearity of Fourier Transform", fontsize=25)
gs = GridSpec(2, 2, hspace=0.5)

v0 = fig.add_subplot(gs[0, 0])
v0.plot(violin.get_time(), violin.signal)
v0.set_title("Violin signal playing note A4")

p0 = fig.add_subplot(gs[0, 1])
p0.plot(piano.get_time(), piano.signal)
p0.set_title("Piano signal playing note A4")

time_v, odf_v = onset_function(violin.signal, violin.sampleRate, windowSize=2048)
time_p, odf_p = onset_function(piano.signal, piano.sampleRate, windowSize=2048)

onsets_v = peak_pick(odf_v, 1)
onsets_p = peak_pick(odf_p, 0.1)

v1 = fig.add_subplot(gs[1, 0])
v1.plot(time_v, odf_v)
v1.plot(time_v[onsets_v], odf_v[onsets_v], marker="x", ls="")
v1.set_title("Onset Detection Function for violin signal")

p1 = fig.add_subplot(gs[1, 1])
p1.plot(time_p, odf_p)
p1.plot(time_p[onsets_p], odf_p[onsets_p], marker="x", ls="")
p1.set_title("Onset Detection Function for piano signal")

fig.savefig("figures/out/onset.png")
