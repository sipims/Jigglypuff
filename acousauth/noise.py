#truerandom v1.0 beta
#sergio@infosegura.net
#www.infosegura.net

#True random numbers are obtained from http://www.random.org/
#If the module fails to obtain the random list it will return -1

#-----------IMPORTS----------------#
from urllib import urlopen
import urllib
import math
#import pyaudio
import sys
import truerandom
import struct
import wave
import random


RATE = 10000
WAVE = 5800


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

# rate should less than 10000 or the API will fail
def truerand_noise(RATE, WAVE, filename):
    # sin wave parameters 
    samples = 5000
    hz = 600.0
    frame_rate = 22025.0
    amp = 44100.0

    # make sin wave for sync
    sinwave = make_sinewave(samples, hz, frame_rate, amp)
    waveMatrix = getnum(600,800,RATE)
    data = ''.join([chr(int(math.sin(x/((RATE/waveMatrix[x])/math.pi))*127+128)) for x in xrange(RATE)])
    #create wav file
    wav_file = wave.open(filename, "w")
    wav_file.setparams((1, 2, 6000, 1000, "NONE", "not compressed"))
    # add sin wave
    for s in sinwave:
        wav_file.writeframes(struct.pack('h', int(s)))
    wav_file.writeframes(data)
    wav_file.close()



def psudorand_noise(RATE, WAVE, filename):

    term = random.randint(600, 800)
    waveMatrix = []

    # sin wave parameters 
    samples = 5000
    hz = 600.0
    frame_rate = 22025.0
    amp = 44100.0

    # make sin wave for sync
    sinwave = make_sinewave(samples, hz, frame_rate, amp)

    # make rand noise
    for x in range(RATE):
        #add the random number to the list
        waveMatrix.append(term)
        term = random.randint(600, 800)
    data = ''.join([chr(int(math.sin(x/((RATE/waveMatrix[x])/math.pi))*127+128)) for x in xrange(RATE)])
    #create wav file
    wav_file = wave.open(filename, "w")
    # o create a wave file you must fill these parameter
    wav_file.setparams((1, 2, 6000, 1000, "NONE", "not compressed"))
    # add sin wave
    for s in sinwave:
        wav_file.writeframes(struct.pack('h', int(s)))
    
    # add noise data
    print sinwave
    print waveMatrix
    wav_file.writeframes(data)
    wav_file.close()


def __make_soundfile(file_name):
    samples = 5000
    hz = 440.0
    frame_rate = 22025.0 
    amp = 44100.0     
    waver = []
    # loop through and create a sin wave useing the variables
    for x in range(samples):
        calculator = math.sin(2*math.pi*hz*(x/frame_rate))*amp/2
        waver.append(calculator)
    #create wav file
    wav_file = wave.open(file_name, "w")
    #to create a wave file you must fill these parameters, its the stuff you see in the first 5 lines of the txt file
    wav_file.setparams((1, 2, frame_rate, samples, "NONE", "not compressed"))
    # write the sample to the file
    for s in waver:
        wav_file.writeframes(struct.pack('h', int(s)))
    wav_file.close()
    print( "%s written" % file_name )


def make_sinewave(samples, hz, frame_rate, amp):
    waver = []
    # loop through and create a sin wave useing the variables
    for x in range(samples):
        calculator = math.sin(2*math.pi*hz*(x/frame_rate))*amp/2
        waver.append(calculator)
    return waver

#__make_soundfile('sine.wav')
psudorand_noise(RATE, WAVE, 'noise.wav')
