from utils.notes import Note
from utils.pitch import aubioPitch, reduceSamples, piecewisePitch

from scipy.io import wavfile
from matplotlib import pyplot as plt
import numpy as np

inputFile = 'sounds/violin1.wav'
fs, data = wavfile.read(inputFile)

# Detect pitch
t, f = aubioPitch(inputFile, samplerate=fs)

# Reduce points
time, freq, down_fs = reduceSamples(t, f, 0.05)

# Extract edge points
time, freq = piecewisePitch(time, freq)

for i in range(len(time)):
    n = Note(freq[i])
    print("At t=",time[i],"\tNote = ",n)

plt.plot(t, f, 'bo') # Pitch graph
plt.plot(time, freq, 'ro') # extracted pieces
plt.xlabel('Time (s)')
plt.ylabel('Pitch (Hz)')
plt.show()