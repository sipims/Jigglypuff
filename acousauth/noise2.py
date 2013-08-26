#truerandom v1.0 beta
#sergio@infosegura.net
#www.infosegura.net

#True random numbers are obtained from http://www.random.org/
#If the module fails to obtain the random list it will return -1

#-----------IMPORTS----------------#
from urllib import urlopen
import urllib
import math
import pyaudio
import sys
import truerandom
import struct
import wave
import random
#-----------CLASSES--------------#
class myURLopener(urllib.FancyURLopener):

    def http_error_401(self, url, fp, errcode, errmsg, headers, data=None):
        print "Warning: cannot open, site requires authentication"
        return None

#-----------FUNCTIONS--------------#
def getnum(min,max,amount):
    global randlist
    try:
        url_opener = myURLopener()
        data = url_opener.open("http://www.random.org/integers/?num="+str(amount)+"&min="+str(min)+"&max="+str(max)+"&col=1&base=10&format=plain&rnd=new")
        randlist=data.readlines()
        data.close()
        randlist[:] = [line.rstrip('\n') for line in randlist]
        
        for n in range(len(randlist)):
            randlist[n]=int(randlist[n])

        return randlist
    
    except:
        randlist=[]
        randlist.append(-1)
        return randlist



PyAudio = pyaudio.PyAudio
RATE = 100000
WAVE = 5800

#waveMatrix = getnum(5600,5601,RATE)
#waveMatrix2 = getnum(600,800,RATE)
term = random.randint(4600, 4800)
waveMatrix = []
#waver = getnum(600,800,samples)
#print waver

for x in range(RATE):
    #add the random number to the list
    waveMatrix.append(term)
    term = random.randint(600, 800)


print waveMatrix
data = ''.join([chr(int(math.sin(x/((RATE/waveMatrix[x])/math.pi))*127+128)) for x in xrange(RATE)])
#create wav file
wav_file = wave.open('ee.wav', "w")

    # o create a wave file you must fill these parameter
wav_file.setparams((1, 2, 6000, 1000, "NONE", "not compressed"))
wav_file.writeframes(data)
wav_file.close()
'''
p = PyAudio()

stream = p.open(format =
                p.get_format_from_width(1),
                channels = 1,
                rate = RATE,
                output = True)
for DISCARD in xrange(5):
    stream.write(data)
stream.stop_stream()
stream.close()
p.terminate()
'''
