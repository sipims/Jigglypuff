#!/usr/bin/python
# -*-coding:utf-8 -*-
import time
import threading
import web
import pymongo
from pymongo import MongoClient
from session import MongoStore
from web import form
import users

web.config.debug = False
web.config.session_parameters['timeout'] = 60

urls = (
    '/', 'Index',
    '/index', 'Index',
    '/submit', 'Submit',
    '/login', 'Login',
    '/admin', 'Admin',
    '/register', 'Register',
    '/favicon.ico', 'Favicon'
)

# Define the template directory
tmpl = web.template.render("tmpl/")

# Get mongodb
client = MongoClient()
db = client.mydb2

# Create app object here
app = web.application(urls, globals())

# Create session
session = web.session.Session(app, MongoStore(db, 'sessions'))
users.session = session
users.collection = db.users

class Index:
    def GET(self):
        return tmpl.index()

    def POST(self):
        #data = web.data()
        return "OK"

class Submit:
    def POST(self):
        data = web.data()
        f = open("./temp",'w')
        f.write(data)
        f.close()
        #print data
        return "OK"

class Login:
  def __init__(self):
    self.login = form.Form(
          form.Textbox('username'),
          form.Password('password'),
          form.Button('Login'),
        )

  def GET(self):
    form = self.login()
    return tmpl.login(form)

  def POST(self):
    post = web.input(_method='POST')
    #try:
    user = users.authenticate(post['username'], post['password'])
    if user is None:
      return "Not found"
    else:
      users.login(user)
      return web.seeother('/admin')

class Admin:
  def GET(self):
    user = users.get_user_by_sid()
    if user is None:
      return web.seeother('/login')
    else:
      return user['username']

class Register:
  def __init__(self):
    self.register = form.Form(
          form.Textbox('username'),
          form.Password('password'),
          form.Password('pwdagain'),
          form.Button('Sign Up'),
        )

  def GET(self):
    form = self.register()
    return tmpl.register(form)

  def POST(self):
    post = web.input(_method='POST')

    username = post['username']
    pwd      = post['password']
    pwdagain = post['pwdagain']

    # Validate
    if username or pwd or passwd is None:
      return "field blank"
    elif pwd != pwdagain:
      return "password not the same"
    elif users.get_user_by_name(username) is not None:
      return "user exists"
    else:
      user = users.register(username=username, password=pwd)
      return "Insert success"

class Favicon:
  def GET(self):
    with open('static/favicon.ico', 'rb') as f:
      return f.read()

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



if __name__ == "__main__":
    #tCheck=MTimerClass(GetSearchinfo, '',  10);
    #tCheck.setDaemon(True); # 随主线程一起结果
    #tCheck.start();         #线程启动
    app.run()
