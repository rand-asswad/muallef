from muallef.pitch import MonoPitch
from muallef.io import AudioLoader

from muallef.plot.nmf import plot_matrix, plot_NMF_factors
from muallef.pitch.nmf import NMF

import numpy as np
import matplotlib.pyplot as plt

#from librosa import stft
from scipy.signal import stft as sp_stft
def stft(x, n_fft=2048, hop_length=None):
    noverlap = n_fft // 2 if hop_length is None else n_fft - hop_length
    return sp_stft(x, nperseg=n_fft, noverlap=noverlap)[2]

audio_file = "samples/polyphonic/furElise.wav"
audio = AudioLoader(audio_file)
audio.cut(stop=6)
fs = audio.sampleRate
x = audio.signal
N_fft = 2048
H_fft = 1024

X = stft(x, n_fft=N_fft, hop_length=H_fft)
V = np.log(1 + np.abs(X))
freq_max = 2000

plot_matrix(V, Fs=fs/H_fft, Fs_F=N_fft/fs)
plt.ylim([0, freq_max])

K = V.shape[0]
N = V.shape[1]
R = 30

W_init = np.random.rand(K,R)
H_init = np.random.rand(R,N)

W, H, V_approx, V_approx_err, H_W_error = NMF(V, R, W=W_init, H=H_init, L=200, norm=True)

plot_NMF_factors(W_init, H_init, W_init.dot(H_init), fs, N_fft, H_fft, freq_max)
plot_NMF_factors(W, H, W.dot(H), fs, N_fft, H_fft, freq_max)               

plt.show()