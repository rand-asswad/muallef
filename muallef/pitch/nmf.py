"""
Module: muallef.pitch.nmf
Source: LibFMP.C8.S3_NMF
Author: Frank Zalkow, Meinard Mueller
License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License

This file is taken of the FMP Notebooks (https://www.audiolabs-erlangen.de/FMP).
"""

import numpy as np
from matplotlib import pyplot as plt


from numba import jit

@jit(nopython=True)
def NMF(V, R, thresh=0.001, L=1000, W=None, H=None, norm=False, report=False):
    """NMF algorithm with Euclidean distance

    Notebook: C8/C8S3_NMFbasic.ipynb

    Args:
        V: Nonnegative matrix of size K x N
        R: Rank parameter
        thresh: Threshold used as stop criterion
        L: Maximal number of iteration
        W: Nonnegative matrix of size K x R used for initialization
        H: Nonnegative matrix of size R x N used for initialization
        norm (bool): Applies max-normalization of columns of final W
        report (bool): Reports errors during runtime

    Returns:
        W: Nonnegative matrix of size K x R
        H: Nonnegative matrix of size R x N
        V_approx: Nonnegative matrix W*H of size K x N
        V_approx_err: Error between V and V_approx
        H_W_error: History of errors of subsequent H and W matrices
    """
    K = V.shape[0]
    N = V.shape[1]
    if W is None:
        W = np.random.rand(K,R)
    if H is None:
        H = np.random.rand(R,N)
    V = V.astype(np.float64)
    W = W.astype(np.float64)
    H = H.astype(np.float64)
    H_W_error = np.zeros((2,L))
    ell = 1
    below_thresh = False
    eps_machine = np.finfo(np.float32).eps
    while not below_thresh and ell <= L:
        H_ell = H
        W_ell = W
        H = H * ( W.transpose().dot(V) / (W.transpose().dot(W).dot(H)+ eps_machine) )
        W = W * ( V.dot(H.transpose()) / (W.dot(H).dot(H.transpose())+ eps_machine) )
        #H = np.multiply( H, np.divide( np.matmul(np.transpose(W), V), np.matmul(np.matmul(np.transpose(W), W), H))) #H+1 = H *p ((W^T * V) /p (W^T * W * H))
        #W = np.multiply( W, np.divide( np.matmul(V, np.transpose(H)), np.matmul(np.matmul(W, H), np.transpose(H)))) # W+1 = W *p ((V * H^T) /p (W * H * H^T))
        H_error = np.linalg.norm(H-H_ell, ord=2)
        W_error = np.linalg.norm(W - W_ell, ord=2)
        H_W_error[:, ell-1] = [H_error, W_error]
        if report:
            print('Iteration: ',ell,', H_error: ',H_error,', W_error: ',W_error)
        if H_error < thresh and W_error < thresh:
            below_thresh = True
            H_W_error = H_W_error[:,0:ell]
        ell += 1
    if norm:
        for r in range(R):
            v_max = np.max(W[:,r])
            if v_max > 0:
                W[:,r] = W[:,r] / v_max
                H[r,:] = H[r,:] * v_max
    V_approx = W.dot(H)
    V_approx_err = np.linalg.norm(V-V_approx, ord=2)
    return W, H, V_approx, V_approx_err, H_W_error