from src.part import Part
from src.notes import sci_pitch
from src.scale import Scale, find_scale
from src.utils import play_wav, plot_step_function

from matplotlib import pyplot as plt
import numpy as np

inputFile = 'sounds/czardas1.wav'

p = Part(inputFile)

s = p.scale()
print(s)

wav_time = np.arange(p.file_data.size) / float(p.sample_rate)

# time = []
# pitch = []
# for note in p.notes:
#    time.append(note.time)
#    pitch.append(note.freq)
# time = np.array(time)
# pitch = np.array(pitch)

plt.plot(wav_time, p.file_data)
# plt.plot(time, pitch, "ro")
plt.xlabel("Time (s)")
plt.ylabel("Freq (Hz)")
# plt.show()

print(max(p.file_data))
