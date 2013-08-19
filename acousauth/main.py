#!/usr/bin/python
# -*-coding:utf-8 -*-
import time;
import threading;
import web
import sys,wave
import subprocess
#import numpy as np
#from scikits.audiolab import Sndfile, Format
#import struct
urls = (
    '/', 'index',
    '/submit', 'submit'
)

i = 0
class index:
    def GET(self):
        tmpl = web.template.render("tmpl/")
        return tmpl.index()

    def POST(self):
        #data = web.data()
        return "OK"


class submit:


    def POST(self):
        global i
        data = web.data()
        filename = "temp["+str(i)+"].wav"
        #sig = np.array([0, 1, 0, -1, 0], dtype=np.float32)
        #f = Sndfile(filename, 'w', Format('wav','pcm32'), 1, 44100)
        #f.write_frames(data)
        #f.close()
        data = data[229:-44]
        
        #wavfile = float32_wav_file(data, 44100)
        #f = open(filename,'wb')
        #f.write(wavfile)
        #f.close()
        #filename = "test.wav"
        #ifile = wave.open("temp.wav")
        wavfile = wave.open(filename,'wb')
        #wavfile.setparams(ifile.getparams())
        wavfile.setparams((1, 2, 44100, 44100*4, 'NONE', 'not compressed'))
        #sampwidth = ifile.getsampwidth()
        #print sampwidth
        #fmts = (None, "=B", "=h", None, "=l")
        #fmt = fmts[sampwidth]
        #dcs = (None, 128, 0, None, 0)
        #dc = dcs[sampwidth]
        #for i in range (ifile.getnframes()):
         #   iframe = 
        wavfile.writeframes(data)
        wavfile.close()
        #f = open(filename,'wb')
        #f.write(data)
        #f.close()
        i = i + 1
        #print data
        return "OK"


class MTimerClass(threading.Thread):  # cookie监控时钟
    def __init__(self,fn,args=(),sleep=1):        
        threading.Thread.__init__(self)
        self.fn = fn  
        self.args = args  
        self.sleep = sleep 
        self.setDaemon(True)
        
        self.isPlay = True  #当前是否运行 
        self.fnPlay = False #当前已经完成运行
        self.thread_stop=False; 
        
    def SetSleep(self,sleep): # 重新设置 时间间隔
        self.sleep=sleep;
        
    def __do(self):
        self.fnPlay = True;
        apply(self.fn,self.args);
        self.fnPlay = False 

    def run(self): 
        while self.isPlay : 
            if self.thread_stop==True:
                break;
            #if SubCommon.ifexeStop==True:  #可以外部调用 来关掉线程。
            #    print 'thread break'
            #    break;  
            #print self.sleep;
            time.sleep(self.sleep) 
            self.__do();
            
    def stop(self):  
        #stop the loop  
        self.thread_stop = True;
        self.isPlay = False; 
        while True:
            if not self.fnPlay : break             
            time.sleep(0.01)

def GetSearchinfo():
    # to do
    pass;


def run_minimodem(filename, bitrate, mark, space):
    command = "minimodem -r {} -M {} -S {} -f\
    {}".format(str(bitrate),str(mark),str(space),str(filename))
    
    try:
        process1 = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process1.wait()
        for line in iter(process1.stdout.readline, b''):
            print "RESULT:",line
        
    except Exception,E:
        print "Error in executing minimodem"
        return 1
    

def float32_wav_file(sample_array, sample_rate):
  byte_count = (len(sample_array)) * 4  # 32-bit floats
  wav_file = ""
  # write the header
  wav_file += struct.pack('<ccccIccccccccIHHIIHH',
    'R', 'I', 'F', 'F',
    byte_count + 0x2c - 8,  # header size
    'W', 'A', 'V', 'E', 'f', 'm', 't', ' ',
    0x10,  # size of 'fmt ' header
    3,  # format 3 = floating-point PCM
    1,  # channels
    sample_rate,  # samples / second
    sample_rate * 4,  # bytes / second
    4,  # block alignment
    32)  # bits / sample
  wav_file += struct.pack('<ccccI',
    'd', 'a', 't', 'a', byte_count)
  for sample in sample_array:
    wav_file += struct.pack("<f", float(sample))
  return wav_file

if __name__ == "__main__":
    #app = web.application(urls, globals())
    #tCheck=MTimerClass(GetSearchinfo, '',  10);
    #tCheck.setDaemon(True); # 随主线程一起结果
    #tCheck.start();         #线程启动
    #app.run()
    run_minimodem('test.wav',100, 1600, 800) 
