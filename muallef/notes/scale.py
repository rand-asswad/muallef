import numpy as np
from numpy.linalg import norm


C_major = np.array([1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=bool)
sharp = [6, 1, 8, 3, 10, 5, 0]
flat = [10, 3, 8, 1, 6, 11, 4]


def detect_scale(notes, duration=None):
    scales = [np.roll(C_major, i) for i in range(12)]
    part = count_notes(notes, duration)
    diff = np.array([norm(part - s) for s in scales], dtype=float)
    return np.argmin(diff)


def count_notes(notes, duration=None):
    notes = np.rint(notes).astype(dtype=int)
    index = np.argwhere(notes > 0)
    octave = np.remainder(notes[index], 12)
    duration = duration[index] if duration else np.ones(index.shape)

    result = np.zeros(12)
    for n in range(12):
        args = np.where(octave == n)
        result[n] = np.dot(octave[args], duration[args])
    result /= result.max()
    return result


def scale_signature(base_note):
    scale = np.roll(C_major, base_note)
    sharps = 0
    while scale[sharp[sharps]] and sharps < 7:
        sharps += 1
    flats = 0
    while scale[flat[flats]] and flats < 7:
        flats += 1
    if sharps or flats:
        if not flats:
            tone = +1
            number = sharps
        elif not sharps:
            tone = -1
            number = flats
        else:
            if sharps < flats:
                tone = +1
                number = sharps
            elif sharps == flats:
                tone = 0
                number = 6
            else:
                tone = -1
                number = flats
    else:
        tone = 0
        number = 0
    return number, tone
