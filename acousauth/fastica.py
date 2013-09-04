from mdp import fastica
from scikits.audiolab import wavread, wavwrite
from numpy import abs, max, array
 

def chop_sig(sig1, sig2):
	min_len = get_length(sig1, sig2)
	return sig1[0:min_len], sig2[0:min_len]

def get_length(sig1, sig2):
	len1 = len(sig1)
	len2 = len(sig2)
	if len1 > len2:
		return len2
	else:
		return len1


#sig1, fs1, enc1 = wavread('mix.wav')
#sig2, fs2, enc2 = wavread('jamming.wav')
#mixed1 = sig1 + 0.5 * sig2
#mixed2 = sig2 + 0.6 * sig1
 
def fastICA(mix_file, jamming_file):
	sig1, fs1, enc1 = wavread(mix_file)
	sig2, fs2, enc2 = wavread(jamming_file)
	sig1, sig2 = chop_sig(sig1, sig2)
	print len(sig1)
	print len(sig2)

	wavwrite(array([sig1, sig2]).T, 'mixed.wav', fs1, enc1)
	 
	# Load in the stereo file
	recording, fs, enc = wavread('mixed.wav')
	 
	# Perform FastICA algorithm on the two channels
	sources = fastica(recording)
	 
	# The output levels of this algorithm are arbitrary, so normalize them to 1.0.
	sources /= max(abs(sources), axis = 0)
	 
	# Write back to a file
	wavwrite(sources, 'sources.wav', fs, enc)


fastICA('mono.wav','ee.wav')
