"""
Module: muallef.plot.nmf
Source: LibFMP.B.plot
Author: Frank Zalkow, Meinard Mueller
License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License

This file is taken of the FMP Notebooks (https://www.audiolabs-erlangen.de/FMP).
"""

import numpy as np
from numpy.linalg import norm
from scipy.fft import rfft, rfftfreq
from matplotlib import pyplot as plt


def plot_matrix(X, Fs=1, Fs_F=1, T_coef=None, F_coef=None, xlabel='Time (seconds)', ylabel='Frequency (Hz)', title='',
                dpi=72, colorbar=True, colorbar_aspect=20.0, ax=None, figsize=(6, 3), **kwargs):
    """Plot a matrix, e.g. a spectrogram or a tempogram

    Notebook: B/B_PythonVisualization.ipynb

    Args:
        X: The matrix
        Fs: Sample rate for axis 1
        Fs_F: Sample rate for axis 0
        T_coef: Time coeffients. If None, will be computed, based on Fs.
        F_coef: Frequency coeffients. If None, will be computed, based on Fs_F.
        xlabel: Label for x axis
        ylabel: Label for y axis
        title: Title for plot
        dpi: Dots per inch
        colorbar: Create a colorbar.
        colorbar_aspect: Aspect used for colorbar, in case only a single axes is used.
        ax: Either (1.) a list of two axes (first used for matrix, second for colorbar), or (2.) a list with a single
            axes (used for matrix), or (3.) None (an axes will be created).
        figsize: Width, height in inches
        **kwargs: Keyword arguments for matplotlib.pyplot.imshow

    Returns:
        fig: The created matplotlib figure or None if ax was given.
        ax: The used axes.
        im: The image plot
    """
    fig = None
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)
        ax = [ax]
    if T_coef is None:
        T_coef = np.arange(X.shape[1]) / Fs
    if F_coef is None:
        F_coef = np.arange(X.shape[0]) / Fs_F

    if 'extent' not in kwargs:
        x_ext1 = (T_coef[1] - T_coef[0]) / 2
        x_ext2 = (T_coef[-1] - T_coef[-2]) / 2
        y_ext1 = (F_coef[1] - F_coef[0]) / 2
        y_ext2 = (F_coef[-1] - F_coef[-2]) / 2
        kwargs['extent'] = [T_coef[0] - x_ext1, T_coef[-1] + x_ext2, F_coef[0] - y_ext1, F_coef[-1] + y_ext2]
    if 'cmap' not in kwargs:
        kwargs['cmap'] = 'gray_r'
    if 'aspect' not in kwargs:
        kwargs['aspect'] = 'auto'
    if 'origin' not in kwargs:
        kwargs['origin'] = 'lower'

    im = ax[0].imshow(X, **kwargs)

    if len(ax) == 2 and colorbar:
        plt.colorbar(im, cax=ax[1])
    elif len(ax) == 2 and not colorbar:
        ax[1].set_axis_off()
    elif len(ax) == 1 and colorbar:
        plt.sca(ax[0])
        plt.colorbar(im, aspect=colorbar_aspect)

    ax[0].set_xlabel(xlabel)
    ax[0].set_ylabel(ylabel)
    ax[0].set_title(title)

    if fig is not None:
        plt.tight_layout()

    return fig, ax, im


def plot_NMF_factors(W, H, V, Fs, N_fft, H_fft, freq_max, label_pitch=None, title_W='W', title_H='H', title_V='V',figsize=(17,5)):
    """Plots the factore of an NMF-based spectral decomposition
    
    Notebook: C8/C8S3_NMFSpecFac.ipynb
    
    Args: 
        W: Template matrix
        H: Activation matrix
        V: Reconstructed input matrix
        Fs: Sampling frequency
        N_fft: FFT length
        H_fft: Hopsize
        freq_max: Maximum frequency to be plotted
        label_pitch: Labels for the different pitches
        title_W, title_H, title_V: Titles for the plots
        figsize: Size of the figure
    """    
    R = W.shape[1]
    N = H.shape[1]
    cmap = 'gray_r'
    dur_sec = (N-1) * H_fft / Fs
    #if label_pitch is None:
    #    label_pitch = np.arange(R)
    if R > 40:
        label_pitch = np.arange(0, R, 5)
    elif R > 20:
        label_pitch = np.arange(0, R, 2)
    else:
        label_pitch = np.arange(R)
        
    plt.figure(figsize=figsize)
    plt.subplot(131)
    plt.imshow(W, cmap=cmap, origin='lower', aspect='auto', extent=[0, R, 0, Fs/2])
    plt.ylim([0, freq_max]);
    plt.colorbar()
    #plt.xticks(np.arange(R) + 0.5, label_pitch)
    plt.xticks(label_pitch)
    plt.xlabel('Pitch')
    plt.ylabel('Frequency (Hz)')
    plt.title(title_W, fontsize=14)
    
    plt.subplot(132)
    plt.imshow(H, cmap=cmap, origin='lower', aspect='auto', extent=[0, dur_sec, 0, R])
    plt.colorbar()    
    #plt.yticks(np.arange(R) + 0.5, label_pitch)
    plt.yticks(label_pitch)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Pitch')
    plt.title(title_H, fontsize=14)
    
    plt.subplot(133)
    plt.imshow(V, cmap=cmap, origin='lower', aspect='auto', extent=[0, dur_sec, 0, Fs/2])
    plt.ylim([0, freq_max]);
    plt.colorbar()    
    plt.xlabel('Time (seconds)')    
    plt.ylabel('Frequency (Hz)')
    plt.title(title_V, fontsize=14)
    
    plt.tight_layout()
    plt.show()