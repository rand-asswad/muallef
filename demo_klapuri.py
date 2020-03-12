from muallef.io import AudioLoader
from muallef.pitch import MultiPitch
from muallef.util.units import Hz_to_MIDI

import numpy as np
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
frameSize = 2048


klapuri = MultiPitch(x, fs, method='klapuri', frameSize=frameSize)
pitch = Hz_to_MIDI(klapuri())
time = np.arange(pitch.shape[1]) * (frameSize / fs)

fig, ax = plt.subplots()
fig.suptitle("Multi-pitch estimation using Klapuri's iterative method", fontsize=16)
ax.set_title("Piano roll of Beethoven's \"Für Elise\"")
for m in range(pitch.shape[0]):
    ax.scatter(time, pitch[m])
ax.set_xlabel('Time (s)')
ax.set_ylabel('Pitch (MIDI)')
ax.set_ylim(20, 109)

plt.show()