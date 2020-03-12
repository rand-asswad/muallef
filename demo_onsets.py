from muallef.io import AudioLoader
from muallef.onset import Onset

import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

# matplotlib options
from matplotlib import rcParams
rcParams['savefig.transparent'] = True
rcParams['text.usetex'] = True


# load audio
audio_file = "samples/polyphonic/furElise.wav"
audio = AudioLoader(audio_file)
audio.cut(stop=10)
fs = audio.sampleRate
x = audio.signal
t = audio.time()

onset = Onset(x, fs, method='complex')
onsets = onset()
#peaks = np.interp(onsets, onset.onsetTime, onset.onsetFunction)
#peaks, _ = find_peaks(onset.onsetFunction)

fig, ax = plt.subplots(2, 1, sharex=True)
fig.suptitle("Onset detection using Duxbury's complex ODF", fontsize=16)
ax[0].set_title("Segmented time signal of Beethoven's \"Für Elise\"")
ax[0].plot(t, x)
for on in onsets:
    ax[0].axvline(x=on, color='red')
ax[1].set_title("Duxbury's complex ODF")
ax[1].plot(onset.onsetTime, onset.onsetFunction)
#ax[1].plot(onsets, peaks, marker='x', ls='')
#ax[1].plot(onset.onsetTime[peaks], onset.onsetFunction[peaks], marker='x', ls='')
ax[1].set_xlabel('Time (s)')
plt.show()