import numpy as np


class Note(object):

    def __init__(self, frequency, ref_freq=440, ref_index=57):
        self.freq = frequency
        self.__fltIndex = map_log(frequency, ref_freq=ref_freq, ref_index=ref_index)
        self.index = int(round(self.__fltIndex))
        self.octave = self.index // 12
        self.local_index = self.index % 12
        self.higher = True if self.index == int(self.__fltIndex) else False

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


def map_log(frequency, ref_freq=440, ref_index=57):
    return 12 * np.log2(frequency / ref_freq) + ref_index


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
