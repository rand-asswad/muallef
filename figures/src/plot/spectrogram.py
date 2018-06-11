from scipy.io.wavfile import read
from matplotlib import pyplot as plt, colors
import numpy as np


def plot_spectrogram(signal, sample_rate, axis, color_map='plasma', win_size=4096, overlap=None):
    axis.set_title("Spectrogram", pad=20, fontsize=20)
    axis.set_xlabel("Time (s)", fontsize=15)
    axis.set_ylabel("Frequency (Hz)", fontsize=15)
    cmap = plt.get_cmap(color_map)
    if not overlap:
        overlap = int(round(win_size * 0.75))

    plt_out = axis.specgram(signal, Fs=sample_rate, NFFT=win_size, noverlap=overlap,
                            mode='magnitude', scale='dB', cmap=cmap, vmin=-120, vmax=0)
    axis.set_ylim(0, 5000)
    color = plt.colorbar(plt_out[-1])
    color.set_label('Magnitude (dB)', fontsize=15)
    return axis, plt_out


fs, data = read("sounds/piano-a4.wav")
x = data[:, 0]

fig = plt.figure(figsize=(19.2, 10.8))
ax = fig.add_subplot(111)
ax, out = plot_spectrogram(x, fs, ax)

S, f, t, im = out

index = np.argmax(S, axis=0)
pitch = f[index]

fig.savefig('figures/out/spectrogram.png')

ax.plot(t, pitch, "k", label="maximum")
ax.legend(loc="upper right")

fig.savefig('figures/out/spectrogram_pitch.png')
