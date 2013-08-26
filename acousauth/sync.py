import wave
from struct import *
#read wav file
wav_file = wave.open('noise.wav', "rb")
data = wav_file.readframes(wav_file.getnframes())

s = []
i = 0
for item in data:
	if i == 1:
		s =   s + str(item)
		print unpack('h', s)
		i = 0
	else:
		s = str(item)
		i = 1
