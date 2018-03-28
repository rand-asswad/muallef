from subprocess import Popen, PIPE
import numpy as np


def aubioPitch(inputFile, samplerate=44100, bufsize=2048, hopsize=256,
               pitch='default', unit='Hz', stderr=False):
    args = [
        'aubiopitch',
        '--input', inputFile,
        '--samplerate', str(samplerate),
        '--bufsize', str(bufsize),
        '--hopsize', str(hopsize),
        '--pitch', pitch,
        '--pitch-unit', unit,
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
    return np.array(time), np.array(freq)


def hopSamples(array, hopsize):
    return np.array(array[0:len(array):hopsize])


def reduceSamples(time, freq, time_interval):
    i = 1
    while time[i] < time_interval:
        i += 1
    t, f = hopSamples(time, i), hopSamples(freq, i)
    return t, f, len(t)//t[len(t)-1]


def extractDiff(array):
    return [0] + [np.abs(array[i] - array[i-1]) for i in range(1,len(array))]


def findEdges(freq, threshold=10):
    diff = extractDiff(freq)
    edges = [0]
    for i in range(len(freq)-1):
        if diff[i]>threshold and edges[-1]!=(i-1) and diff[i+1]<threshold:
            edges.append(i)
    return edges


def piecewisePitch(time, freq, threshold=10):
    edges = findEdges(freq)
    av = []
    t = []
    for i in range(len(edges)-1):
        av.append(np.average(freq[edges[i]:edges[i+1]]))
        t.append(time[edges[i]])
    return t, av