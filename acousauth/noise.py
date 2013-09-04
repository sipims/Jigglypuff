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
from numpy import linspace,sin,pi,int16
from scipy.io.wavfile import write
from align import WaveData

#RATE = 350000
RATE = 1200
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



# tone synthesis
def note(freq, len, amp=1, rate=44100):
 amp = 20000
 t = linspace(0,len,len*rate)
 data = sin(2*pi*freq*t)*amp
 return data.astype(int16) # two byte integers

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

    waveMatrix = []

    # sin wave parameters 
    samples = 10000
    hz = 600.0
    frame_rate = 22025.0
    amp = 44100.0

    # make sin wave for sync
    sinwave = make_sinewave(samples, hz, frame_rate, amp)

    # make empty
    empty = make_empty(20000)

    #tone600 = note(1620,0.001,amp=10000)
    #tone800 = note(1820,0.001,amp=10000)

    #data = ''.join([chr(int(math.sin(x/((RATE/waveMatrix[x])/math.pi))*127+128)) for x in xrange(RATE)])
    #create wav file
    wav_file = wave.open(filename, "w")
    # o create a wave file you must fill these parameter
    wav_file.setparams((1, 2, 44100, 44100*4, "NONE", "not compressed"))
    # add sin wave
    for s in empty:
        wav_file.writeframes(struct.pack('h',int(s)))
    # add sin wave
    for s in sinwave:
        wav_file.writeframes(struct.pack('h', int(s)))
    
    # add noise data
    print sinwave
    print waveMatrix

    # make rand noise
    term = 90000
    for x in range(RATE):
        freq = random.randint(600, 800)
        #add the random number to the list
        if(term > 15000):
             wav_file.writeframes(note(freq,0.01,amp=term))
        else:
             wav_file.writeframes(note(freq,0.01,amp=term))
        #term = random.randint(10000, 20000)
    '''
    for x in range(RATE):
        #add random
        waveMatrix.append(term)
        term = random.randint(5800,7350)
    data = ''.join([chr(int(math.sin(x/((RATE/waveMatrix[x])/math.pi))*127+128)) for x in xrange(RATE)])
    wav_file.writeframes(data)
    '''
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


def make_calibration(lowfreq, highfreq, filename):
    waveMatrix = []
    #create wav file
    wav_file = wave.open(filename, "w")
    # o create a wave file you must fill these parameter
    wav_file.setparams((1, 2, 44100, 44100*4, "NONE", "not compressed"))
    # make rand noise
    #for freq in range(lowfreq, highfreq): 
        #add the random number to the list
    
    for freq in range(lowfreq, highfreq):
        for k in range(5):
            #freq = 600
            term = 20000
            wav_file.writeframes(note(freq,0.01,amp=term))
    wav_file.close()


def create_noise(origin, received):
    ori = WaveData(origin)
    base = WaveData(received)
    #print len(base.array)
    #print len(ori.array)
    print base.array[:1000]
    ava_cut = []
    for i in range(len(base.array)):
        if find_zero(base.array[i-1], base.array[i]) == True:
            ava_cut.append(i)

def find_zero(poA, poB):
    if poA < 0 and poB > 0:
        return True
    elif poA > 0 and poB < 0:
        return True

def make_empty(samples):
    waver = []
    for x in range(samples):
        waver.append(0)
    return waver

def make_sinewave(samples, hz, frame_rate, amp):
    waver = []
    # loop through and create a sin wave useing the variables
    for x in range(samples):
        calculator = math.sin(2*math.pi*hz*(x/frame_rate))*amp/2
        waver.append(calculator)
    return waver

#__make_soundfile('sine.wav')
#make_calibration(600, 800, 'cali.wav')
psudorand_noise(RATE, WAVE, './static/noise.wav')
#create_noise('./static/noise.wav','noise.wav')
# A tone, 2 seconds, 44100 samples per second
#tone = note(600,2,amp=10000)

#write('440hzAtone.wav',44100,tone) # writing the sound to a file
