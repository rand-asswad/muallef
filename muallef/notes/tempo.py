import numpy as np


def detect_tempo(time, notes):
    duration = np.diff(time)
    gcf = pseudo_gcf(duration[np.argwhere(notes > 0)])
    tempo = np.rint(duration / gcf)
    index = np.argwhere(tempo > 0)
    return tempo[index], notes[index]


def pseudo_gcf(array):
    offset = np.full(array.shape, np.inf)
    for i in range(len(array)):
        if array[i] > 0:
            multiples = array / array[i]
            offset[i] = np.sum(np.abs(multiples - np.rint(multiples, dtype=float)))
    index = np.argmin(offset)
    return array[index]
