from utils.notes import Note
from utils.pitch import aubioPitch, reduceSamples, piecewisePitch

from scipy.io import wavfile
from matplotlib import pyplot as plt
import numpy as np

inputFile = 'sounds/czardas1.wav'
fs, data = wavfile.read(inputFile)

# Detect pitch
t, f = aubioPitch(inputFile, samplerate=fs)

# Reduce points
time, freq, down_fs = reduceSamples(t, f, 0.05)

notes = []
times = []
for i in range(len(time)):
    try:
        n = Note(freq[i], ref_freq=442)
        if not notes or notes[-1] != n:
            notes.append(n)
            times.append(time[i])
    except OverflowError or ZeroDivisionError:
        pass

def removeShortNotes(times, notes, time_tol=0.15):
    t = []
    n = []
    for i in range(len(times)-1):
        if times[i+1]-times[i] >= time_tol:
            t.append(times[i])
            n.append(notes[i])
    t.append(times[-1])
    n.append(notes[-1])
    return t, n

times, notes = removeShortNotes(times, notes, time_tol=0.2)
for i in range(len(times)):
    print('AT t= ', times[i], '\t Note = ', notes[i])


#plt.plot(t, f, 'bo') # Pitch graph
#plt.plot(time, freq, 'ro') # extracted pieces
#plt.xlabel('Time (s)')
#plt.ylabel('Pitch (Hz)')
#plt.show()