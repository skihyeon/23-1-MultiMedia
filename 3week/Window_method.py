import scipy.signal as signal
import fplot
n = 15
h = signal.firwin(n, cutoff=0.25, window="hamming")
fplot.mfreqz(h)
fplot.show()
fplot.impz(h)
fplot.show()


h_hp = signal.firwin(255, cutoff=0.5, window="hamming", pass_zero='highpass')
fplot.mfreqz(h_hp)
fplot.show()

h_bp = signal.firwin(255, [0.2,0.5], window="hamming", pass_zero='bandpass')
fplot.mfreqz(h_bp)
fplot.show()

h_bs = signal.firwin(255, [0.2, 0.5], window="hamming", pass_zero='bandstop')
fplot.mfreqz(h_bs)
fplot.show()