from mdp import fastica
from scikits.audiolab import wavread, wavwrite
from numpy import abs, max, array
import commands


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
	print len(sig1)
	print len(sig2)
	sig1, sig2 = chop_sig(sig1, sig2)
	print len(sig1)
	print len(sig2)

	wavwrite(array([sig1, sig2]).T, 'mixed.wav', fs1, enc1)
	 
	# Load in the stereo file
	recording, fs, enc = wavread('mixed.wav')
	 
	# Perform FastICA algorithm on the two channels
	sources = fastica(recording)
	 
	# The output levels of this algorithm are arbitrary, so normalize them to 1.0.

	m = []
	for k in sources:
		m.append(k[0])
	# Write back to a file
	wavwrite(array(m), 'sources.wav', fs, enc)

def stereo2mono(wave_file):
  """
  Convert the stereo file to mono using Sox and default options
  """
  #Check if sox is installed
  status, output = commands.getstatusoutput('sox')
  if output[-9:] == 'not found':
    print " "
    print "Sox is not installed!"
    print "Please install with: sudo apt-get install sox libsox*"
    print " "
    print "Exiting program."
    print " "
    sys.exit()
  #Get the stereo filename
  print " "
  print "Stereo file, will convert to mono."
  print " "
  mono_name = "mono11.wav"
  status, output = commands.getstatusoutput('sox ' + wave_file + ' -c 1 ' + mono_name)
  print " "
  if status != 0:
      print "Problem with file ", wave_file[:-4]
      print "   Could not be converted to mono:,"
      print output
      print " "
      print "Exiting program."
      sys.exit()
  else:
      print "Stereo to mono conversion completed.\n"
#   status, output = commands.getstatusoutput('rm -f ' + wave_file)
#   print output
#   status, output = commands.getstatusoutput('mv ' + mono_name + " " + wave_file)
#   if status != 0:
#   print output
#     sys.exit()
  return mono_name


fastICA('mono_1.wav','noise_1.wav')
stereo2mono('sources.wav')
