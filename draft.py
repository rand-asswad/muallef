from src.notes import Note, frequency2index, index2frequency
from src.pitch import aubioPitch, reduceSamples, piecewisePitch, extractDiff

from scipy.io import wavfile
from matplotlib import pyplot as plt
import numpy as np

inputFile = 'sounds/czardas1.wav'
fs, data = wavfile.read(inputFile)

# Detect pitch
t, f = aubioPitch(inputFile, samplerate=fs)

diff = extractDiff(f)

# Round pitch
linear = np.array([frequency2index(x) for x in f])
index = np.array([int(round(n)) for n in linear])


# Filter
def filterNotes(time, keys, time_tol=0.1):
    hop = 0
    while time[hop] < time_tol:
        hop += 1
    indices = np.array(keys)
    for i in range(hop, len(time)-hop):
        for j in range(i-hop+1, i+hop):
            if keys[j] != keys[i-hop]:
                indices[i] = -1
                break
    return indices


final = filterNotes(t, index, time_tol=0.1)

plt.plot(t, linear, 'bo')
plt.plot(t, final, 'go')
plt.plot(t, diff, 'ro')
plt.show()

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