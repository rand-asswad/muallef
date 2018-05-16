from src.part import Part
from src.notes import sci_pitch
from src.scale import Scale, find_scale
from src.utils import play_wav, plot_step_function

from matplotlib import pyplot as plt
import numpy as np

inputFile = 'sounds/reiding-cut.wav'

p = Part(inputFile)

#s = p.scale()
#print(s)

#play_wav(inputFile)

p.plot_pitch(MIDI=True)
wav_time = np.arange(p.file_data.size) / float(p.sample_rate)
envelope = p.find_envelope()

from scipy.signal import argrelmin
local_mins = argrelmin(envelope)
t = [wav_time[i] for i in local_mins]
a = [p.notes[i].midi for i in local_mins]
plt.plot(t, a, "bo")


# time = []
# pitch = []
# for note in p.notes:
#    time.append(note.time)
#    pitch.append(note.freq)
# time = np.array(time)
# pitch = np.array(pitch)

# plt.plot(wav_time, p.file_data, label='signal')
# plt.plot(wav_time, envelope, label='envelope')

#plt.plot(time, pitch, "ro")
plt.xlabel("Time (s)")
# plt.ylabel("Freq (Hz)")
plt.show()
