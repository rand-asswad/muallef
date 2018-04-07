from src.part import Part

from matplotlib import pyplot as plt
import numpy as np

inputFile = 'sounds/czardas1.wav'

p = Part(inputFile)

p.find_pitch()
p.pitch_diff()
#t, x, h = p.reduce_samples(threshold=0.5)
t, x = p.pitch_per_piece(threshold=0.5)

plt.plot(p.time, p.pitch_log, 'bo')
plt.plot(t, x, 'ro')
#plt.plot(p.time[:-1], p.diff, 'ro')
plt.xlabel('Time (s)')
plt.ylabel('Pitch Logarithm (log(Hz))')
plt.show()