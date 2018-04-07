import numpy as np


class Note(object):

    def __init__(self, frequency, ref_freq=440, ref_index=57):
        self.freq = frequency
        flt_index = frequency2index(frequency, ref_freq=ref_freq, ref_index=ref_index)
        self.index = int(round(flt_index))
        self.offset = flt_index - self.index
        self.octave = self.index // 12
        self.local_index = self.index % 12
        self.higher = True if self.offset > 0 else False
        self.silence = True if self.index == -1 else False

    def __str__(self):
        if self.local_index in major_indices:
            output = names[self.local_index] + str(self.octave)
        else:
            if self.higher:
                output = names[self.local_index-1] + str(self.octave) + '#'
            else:
                output = names[self.local_index+1] + str(self.octave) + '♭'
        return output

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    # Prospective class functions : exportAsXML


def frequency2index(frequency, ref_freq=440, ref_index=57, silence_threshold=20):
    if frequency < silence_threshold:
        return -1
    return 12 * np.log2(frequency / ref_freq) + ref_index


def index2frequency(index, ref_freq=440, ref_index=57):
    return 2**((index-ref_index)/12) * ref_freq


major_indices = [0, 2, 4, 5, 7, 9, 11]

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
