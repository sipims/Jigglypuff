###############################################################
#chris conley
# random wave generator
###############################################################

import wave
import struct
import random

def __make_wav(file_name):
    samples = 2000
    hz = 200
    frame_rate = 66025.0  
    # picks a random number between these values
    term = random.randint(-30000, 30000)
    waver = []
    for x in range(samples):
        #add the random number to the list
        waver.append(term)
        term = random.randint(-30000, 30000)

    #create wav file
    wav_file = wave.open(file_name, "w")
    # o create a wave file you must fill these parameter
    wav_file.setparams((2, 2, 6000, 1000, "NONE", "not compressed"))
    # loop through for each value in the list
    for s in range(1999):
        q = random.randint(1,1999)
        l = waver[q]
        #write the value 10 times to the wave so its somewhat coherent sounding
        for u in range(10):
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



