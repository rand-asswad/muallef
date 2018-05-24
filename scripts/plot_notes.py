#!/bin/python3

import sys
print(sys.path)
import argparse
from matplotlib import pyplot as plt
from . import notes
from .utils.io import read_audio, plot_step_function

parser = argparse.ArgumentParser(description="Extracts notes from audio file.")

parser.add_argument('input', help='Input file name or path')
parser.add_argument('-b', '--buffer', type=int, help='buffer size', default=2048)
parser.add_argument('-p', '--pitch', help='pitch detection method', default='yinfft')
parser.add_argument('-o', '--onset', help='onset detection method', default='complex')
parser.add_argument('-t', '--time', help='time unit (seconds, samples)', default='seconds')
parser.add_argument('--plot', action='store_true', default=True)
parser.add_argument('--stdout', action='store_true', default=False)

args = parser.parse_args()

fs, x = read_audio(args.input)
time, midi = notes.detect(x, fs, bufferSize=args.buffer, unit=args.time,
                          pitchMethod=args.pitch, onsetMethod=args.onset)

if args.plot:
    plot_step_function(time, midi)
    plt.show()

if args.stdout:
    print("time\tmidi note")
    for i in range(time.size):
        print(time[i],"\t", midi[i])
