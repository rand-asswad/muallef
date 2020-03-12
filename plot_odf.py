from muallef.io import AudioLoader
from muallef.onset import Onset

import numpy as np
import matplotlib.pyplot as plt

# matplotlib options
from matplotlib import rcParams
rcParams['savefig.transparent'] = True
rcParams['text.usetex'] = True

method = {
    'HFC': 'hfc',
    'Complex': 'complex',
    'Phase Deviation': 'complex_phase',
}


# load audio
audio_file = "samples/polyphonic/furElise.wav"
audio = AudioLoader(audio_file)
audio.cut(stop=10)
fs = audio.sampleRate
x = audio.signal
t = audio.time()

fig, ax = plt.subplots(len(method)+1, 1, sharex=True)
i = 0
ax[i].plot(t, x)
ax[i].yaxis.set_ticklabels([])
ax[i].set_ylabel("Signal")
for key in method.keys():
    i += 1
    onset = Onset(x, fs, method=method[key])
    onsets = onset()
    ax[i].plot(onset.onsetTime, onset.onsetFunction)
    ax[i].yaxis.set_ticklabels([])
    ax[i].set_ylabel(key)

ax[-1].set_xlabel('Time (s)')
plt.show()