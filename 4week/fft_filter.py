import numpy as np
from scipy import signal
from scipy.io import wavfile
import sys

WL = 256
WR = 128

def stft(x, w, step):
    wlen = len(w)
    nsampl = len(x)
    if x.ndim == 1:  # mono
        Xtf = np.array([np.fft.rfft(w*x[i:i+wlen]) for i in range(0,nsampl-wlen+1,step)]) + 1e-12*(1+1j)
    elif x.ndim == 2:  # stereo
        Xtf = np.array([np.fft.rfft(w*x[i:i+wlen,:], axis=0) for i in range(0,nsampl-wlen+1,step)]) + 1e-12*(1+1j)
    return Xtf


def istft(Xtf, w, step, nsampl):
    nframe, nfreq = Xtf.shape
    wlen = len(w)

    y = np.zeros(nsampl)
    ws = np.zeros(nsampl)

    for i in range(0, nframe):
        y[i*step:i*step+wlen] += w*np.fft.irfft(Xtf[i, :])
        ws[i*step:i*step+wlen] += w*w

    ws[ws==0] = 1
    y = y/ws

    return y

def filter_ft(mag, fcut, ftype):
    Nf, ft_bin = mag.shape
    fmag = np.zeros([Nf, ft_bin])
    fcut_pos = int(ft_bin*fcut)

    if ftype=='lowpass':
        fmag[:,0:fcut_pos] = mag[:,0:fcut_pos]
    if ftype=='highpass':
        fmag[:,fcut_pos:ft_bin] = mag[:,fcut_pos:ft_bin]
    if ftype=='bandpass':
        fmag[:,int(ft_bin*0.2):int(ft_bin*0.3)] = mag[:,int(ft_bin*0.2):int(ft_bin*0.3)]
    if ftype=='bandstop':
        fmag[:,0:int(ft_bin*0.2)] = mag[:,0:int(ft_bin*0.2)]
        fmag[:,int(ft_bin*0.2):ft_bin] = mag[:,int(ft_bin*0.4):ft_bin]
    return fmag

fs, data = wavfile.read(sys.argv[1])
fcut = float(sys.argv[3])
w = signal.hann(WL)
Xf = stft(data[:,0], w, WR)
Mag = np.abs(Xf)
Phs = np.angle(Xf)
fMag = filter_ft(Mag, fcut, sys.argv[4])
Xfr = fMag*np.exp(1j*Phs)
y = istft(Xfr, w, WR, len(data))
wavfile.write(sys.argv[2], fs, y.astype(np.int16))
