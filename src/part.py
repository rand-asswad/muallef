from subprocess import Popen, PIPE
from scipy.io import wavfile
import numpy as np


class Part(object):
    def __init__(self, input_file):
        self.input_file = input_file
        self.sample_rate, self.file_data = wavfile.read(input_file)
        self.pitch = None
        self.pitch_log = None
        self.time = None
        self.diff = None

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
        self.time = np.array(time)
        self.pitch = np.array(freq)
        self.__frequency_log()

    def __frequency_log(self, threshold=10):
        self.pitch_log = []
        for f in self.pitch:
            if f > threshold:
                self.pitch_log.append(12 * np.log2(f))
            else:
                self.pitch_log.append(-1)
        self.pitch_log = np.array(self.pitch_log)

    def pitch_diff(self):
        freq = self.pitch_log
        diff = [0] * (len(freq) - 1)
        b = freq[-1]
        for i in range(len(freq) - 2, -1, -1):
            a = freq[i]
            diff[i] = b - a
            b = a
        self.diff = np.array(diff)

    def reduce_samples(self, threshold=0.8):
        t, x, h = [], [], []
        x.append(self.pitch_log[0])
        t.append(self.time[0])
        for i in range(1, len(self.diff)):
            if np.abs(self.diff[i-1]) > threshold:
                x.append(self.pitch_log[i])
                t.append(self.time[i])
                h.append(self.diff[i])
        return np.array(t), np.array(x), np.array(h)

    def __get_edges(self, threshold=0.8):
        indices = []
        for i in range(1, len(self.diff)):
            if np.abs(self.diff[i-1]) > threshold:
                indices.append(i)
        return indices

    def pitch_per_piece(self, threshold=None):
        edges = self.__get_edges(threshold) if threshold else self.__get_edges()
        av = []
        t = []
        for i in range(len(edges)-1):
            av.append(np.average(self.pitch_log[edges[i]:edges[i+1]]))
            t.append(self.time[edges[i]])
        return t, av
