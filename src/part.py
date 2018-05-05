from subprocess import Popen, PIPE
from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt

from .utils import array_difference
from .notes import Note
from .scale import Scale, find_scale


class Part(object):
    def __init__(self, input_file):
        self.input_file = input_file
        self.sample_rate, self.file_data = wavfile.read(input_file)
        self.notes, self.scale_arr = self.find_pitch()

    def find_pitch(self, bufsize=2048, hopsize=256, pitch='default'):
        args = [
            'aubiopitch',
            '--input', self.input_file,
            '--samplerate', str(self.sample_rate),
            '--bufsize', str(bufsize),
            '--hopsize', str(hopsize),
            '--pitch', pitch,
            '--pitch-unit', 'Hz',
        ]

        process = Popen(args, stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()
        output, error = output.decode().split('\n'), error.decode()
        time = []
        freq = []
        for line in output:
            try:
                x, y = line.split(' ')
                time.append(float(x))
                freq.append(float(y))
            except:
                error += line + '\n'
        Note.counter = [0] * 12
        notes = []
        for i in range(len(time)):
            notes.append(Note(time[i], freq[i]))
        scale = np.array(Note.counter)
        scale = scale / max(scale)
        return notes, scale

    def plot_pitch(self):
        time = []
        midi = []
        for note in self.notes:
            time.append(note.time)
            midi.append(note.midi)
        time = np.array(time)
        midi = np.array(midi)
        plt.plot(time, midi, 'bo')
        plt.xlabel('Time (s)')
        plt.ylabel('Midi note')
        plt.show()

    def scale(self):
        return find_scale(self.scale_arr)
