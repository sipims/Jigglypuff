###############################################################
#chris conley
# random wave generator
###############################################################
#-----------IMPORTS----------------#
import wave
import struct
import random
from urllib import urlopen
import urllib

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


def __make_wav(file_name):
    samples = 2000
    hz = 200
    frame_rate = 66025.0  
    # picks a random number between these values
    term = random.randint(600, 800)
    waver = []
    #waver = getnum(600,800,samples)
    #print waver

    for x in range(samples):
        #add the random number to the list
        waver.append(term)
        term = random.randint(600, 800)

    #create wav file
    wav_file = wave.open(file_name, "w")
    # o create a wave file you must fill these parameter
    wav_file.setparams((1, 2, 6000, 1000, "NONE", "not compressed"))
    # loop through for each value in the list
    for s in range(1999):
        q = random.randint(1,1999)
        print q
        print len(waver)
        l = waver[q]
        #write the value 10 times to the wave so its somewhat coherent sounding
        for u in range(100):
            wav_file.writeframes(struct.pack('h', int(l)))
            u = u+1
        u=0
    wav_file.close()
    print( "%s written" % file_name )


print ('Enter the name of the wav file you want to create, remember to end it with .wav')
print ('this program will also print the values in the console for copy and pasting into')
print ('text files')
file_name = raw_input("enter file name:") 

__make_wav(file_name)



