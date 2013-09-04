from scipy.signal import butter, lfilter
from scikits.audiolab import wavread, wavwrite
 
sig2, fs2, enc2 = wavread('ran.wav')



def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
 
    b, a = butter(order, [low, high], btype='band')
    y = lfilter(b, a, data)
    return y



cut_noise = butter_bandpass_filter(sig2, 600, 800, fs2)

for val in cut_noise:
	val = val * 100000000
	print val

wavwrite(cut_noise, 'sources1.wav', fs2, enc2)