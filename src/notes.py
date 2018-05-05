import numpy as np


class Note(object):
    counter = [0] * 12

    def __init__(self, time, frequency, A_freq=440):
        self.time = time
        self.freq = frequency
        log_freq = frequency2index(frequency, A=A_freq)
        self.midi = int(round(log_freq))
        if self.midi != -1:
            self.octave = self.midi // 12 - 1
            self.index = self.midi % 12
            self.counter[self.index] += 1
        else:
            self.octave = None
            self.index = None

    def __str__(self):
        return sci_pitch[self.index] + str(self.octave)

    def __eq__(self, other):
        return self.midi == other.midi

    def __ne__(self, other):
        return not self.__eq__(other)

    # Prospective class functions : exportAsXML


def frequency2index(frequency, A=440, silence_threshold=10):
    if frequency < silence_threshold:
        return -1
    return 57 + 12 * (np.log2(frequency) - np.log2(A))


def index2frequency(index, A=440):
    return 2**((index-57)/12) * A


major_indices = [0, 2, 4, 5, 7, 9, 11]

sci_pitch = {
    -1: 'S',
    0: 'C',
    1: 'C#/D♭',
    2: 'D',
    3: 'D#/E♭',
    4: 'E',
    5: 'F',
    6: 'F#/G♭',
    7: 'G',
    8: 'G#/A♭',
    9: 'A',
    10: 'A#/B♭',
    11: 'B',
}

letters = {
    0: 'C',
    2: 'D',
    4: 'E',
    5: 'F',
    7: 'G',
    9: 'A',
    11: 'B',
}

names = {
    0: 'Do',
    2: 'Re',
    4: 'Mi',
    5: 'Fa',
    7: 'Sol',
    9: 'La',
    11: 'Si',
}
