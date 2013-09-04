#!/usr/bin/python
# -*-coding:utf-8 -*-
import os;
import sys;

#abspath = os.path.dirname(__file__)
#sys.path.append(abspath)
#os.chdir(abspath)

import time;
import threading;
import web
import pymongo
from pymongo import MongoClient
from session import MongoStore
from web import form
from web.contrib.template import render_jinja
import users
import logs
import gridfs
import struct
import commands
import json
import re
import sys,wave
import subprocess
from align import align_file
from levenshtein import match
#import numpy as np
#from scikits.audiolab import Sndfile, Format
#import struct

# In order to make session work
web.config.debug = False

# Session timeout
web.config.session_parameters['timeout'] = 60 * 60

render = render_jinja(
      'templates',
      encoding = 'utf-8',
    )

urls = (
    '/', 'index',
    '/index', 'index',
    '/submit', 'Submit',
    '/login', 'Login',
    '/admin', 'Admin',
    '/add', 'Add',
    '/log', 'Log',
    '/edit', 'Edit',
    '/test', 'Test',
    '/sse', 'Sse',
    '/adjusting', 'Adjusting',
    '/noise', 'Noise',
)

# Create app object here
app = web.application(urls, globals())
application = app.wsgifunc()

# Get mongodb
client = MongoClient()
db = client.mydb2

# Get GridFS for avatars
#gfsAvatar = gridfs.GridFS(db)


# Create session
session = web.session.Session(app, MongoStore(db, 'sessions'))
users.session = session

# Create mongo db's collection
users.collection = db.users
logs.collection = db.logs

i = 0
class index:
    def GET(self):
        #tmpl = web.template.render("tmpl/")
        #return tmpl.index()
        return render.index()

    def POST(self):
        #data = web.data()
        return "OK"

class Adjusting:
    def GET(self):
        tmpl = web.template.render("tmpl/")
        return tmpl.adjust()

    def POST(self):
        #data = web.data()
        return "OK"

class Noise:
    def POST(self):
        global i
        data = web.data()
        filename = "temp["+str(i)+"].wav"
        if len(data) > 800000:
          # process the audio data, delete several unused info
          data = data[229:-44]
          # create wave file (stereo)
          wavfile = wave.open(filename,'wb')
          wavfile.setparams((2, 2, 44100, 44100*4, 'NONE', 'not compressed'))
          wavfile.writeframes(data)
          wavfile.close()
          # change it to mono version
          stereo2mono(filename,"noise.wav")
          i = i + 1
        else:  # if data length is too small, pass
          pass
        return "ERROR"


class Submit:
    def POST(self):
	print "here submit"
        global i
        data = web.data()
        filename = "temp["+str(i)+"].wav"
        #sig = np.array([0, 1, 0, -1, 0], dtype=np.float32)
        #f = Sndfile(filename, 'w', Format('wav','pcm32'), 1, 44100)
        #f.write_frames(data)
        #f.close()
        if len(data) > 800000:
          # process the audio data, delete several unused info
          data = data[229:-44]
          # create wave file (stereo)
          wavfile = wave.open(filename,'wb')
          wavfile.setparams((2, 2, 44100, 44100*4, 'NONE', 'not compressed'))
          wavfile.writeframes(data)
          wavfile.close()
          # change it to mono version
          stereo2mono(filename, "mono.wav")
          res_test = run_minimodem('mono.wav',100, 800, 600)
          align_file("mono.wav", "noise.wav", 20000, 5000)
          # denoise
          run_sox()
          # run minimodem to decode FSK
          # run minimodem to decode FSK
          res = run_minimodem('out.wav',100, 800, 600)
          #print match('ddb1cb5590e7530043830f044779250667cb148a',res)
          pwd_list = users.get_all_password()
          #print match('chensi',res)
          
          if res != 1:
            for item in pwd_list:
              if match(res, item) == True:
                print "Match record"
                return "DONE"
            return "ERROR"


          i = i + 1
          #print data
        else:  # if data length is too small, pass
          pass
        return "ERROR"

class Login:
  '''
    Login page: for admin to login
  '''

  def GET(self):
    return render.login()

  def POST(self):
    post = web.input(_method='POST')

    user = users.get_user_by_name(post['username'])
    if user is None:
      response = {'message': 'nonexist'}
    elif user['password'] != users.pswd(post['password']):
      response = {'message': 'nomatch'}
    elif user['authority'] == 1:
      response = {'message': 'nopermission'}
    else:
      users.login(user)
      response = {'message': 'success'}

      logs.login(post['username'])
    return json.dumps(response)

class Admin:
  '''
    Admin page: show all the registered users.
  '''

  def GET(self):
    query = web.ctx.query

    if query == "":
      user = users.get_user_by_sid()
      if user is None:
        return web.seeother('/login')
      else:
        return render.admin(users=users.get_all_users())
    else:
      pattern = re.compile(r'method=(.+?)&username=(.+)')
      result = pattern.findall(query)
      method = result[0][0]
      username = result[0][1]

      if method == 'delete':
        users.del_user_by_name(username)
        response = {'message': 'delete'}

        logs.delete_user(username)
      return json.dumps(response)

class Add:
  '''
    Add page: for admin to add new user
  '''

  def GET(self):
    user = users.get_user_by_sid()
    if user is None:
      return web.seeother('/login')
    else:
      return render.add()

  def POST(self):
    post = web.input(_method='POST')

    # Validate
    user = users.get_user_by_name(post['username'])
    if user is not None:
      response = {'message': 'false'}
    else:
      auth = 1 if post['authority'] == 'guest' else 0
      user = users.add(username=post['username'], password=post['password'], authority=auth)
      response = {'message': 'true'}

      logs.add_user(post['username'])
    return json.dumps(response)

class Log:
  def GET(self):
    return render.log(logs=logs.get_all_logs())

class Edit:
  def GET(self):
    query = web.ctx.query

    if query == '':
      return web.seeother('/admin')
    else:
      return render.edit()

  def POST(self):
    post = web.input(_method='POST')
    query = web.ctx.query
    pattern = re.compile(r'username=(.+)')
    result = pattern.findall(query)
    username = result[0]

    if username == '':
      response = {'message': 'false'}
    else:
      users.change_password(username, post['password'])
      response = {'message': 'true'}

      print 'Change pwd'
      logs.change_password(username)
    return json.dumps(response)




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
    {} -c 1".format(str(bitrate),str(mark),str(space),str(filename))

    try:
        process1 = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process1.wait()
        for line in iter(process1.stdout.readline, b''):
            print "RESULT:",line
            return line
    except Exception,E:
        print "Error in executing minimodem"
        return 1

def run_sox():
    command = "sh denoise.sh 100"
    try:
        process1 = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process1.wait()
        for line in iter(process1.stdout.readline, b''):
            print "RESULT:",line
    except Exception,E:
        print "Error in executing minimodem"
        return 1



def stereo2mono(wave_file, mono_name):
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
  #mono_name = "mono.wav"
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

class Test:
  def GET(self):
    return render.test()

# Default status is close
door_status = 0

class Sse:
  def GET(self):
    web.header('content-type', 'text/event-stream')
    web.header('Cache-Control', 'no-cache')
    while True:
      if door_status == 1:
        yield 'data: %s\n\n' % (json.dumps({'door': 'open'}))
        door_status == 0
      time.sleep(1)

if __name__ == "__main__":
    #app = web.application(urls, globals())
   # run_sox()
    #app = web.application(urls, globals())
    #tCheck=MTimerClass(GetSearchinfo, '',  10);
    #tCheck.setDaemon(True); # 随主线程一起结果
    #tCheck.start();         #线程启动
    app.run()
    #run_minimodem('test.wav',100, 1600, 800)
