#!/usr/bin/python
# -*-coding:utf-8 -*-
import time
import threading
import web
import pymongo
from pymongo import MongoClient
from session import MongoStore
from web import form
from web.contrib.template import render_jinja
import users
import gridfs
import json
import re

# In order to make session work
web.config.debug = False

# Session timeout
web.config.session_parameters['timeout'] = 60 * 60

urls = (
    '/', 'Index',
    '/index', 'Index',
    '/submit', 'Submit',
    '/login', 'Login',
    '/admin', 'Admin',
    '/add', 'Add',
    '/log', 'Log',
    '/edit', 'Edit',
)

# Define the template directory
tmpl = web.template.render("tmpl/")

# Define Jinja2
render = render_jinja(
      'templates',  # Jinja2 template directory
      encoding = 'utf-8',
    )

# Get mongodb
client = MongoClient()
db = client.mydb2

# Get GridFS for avatars
gfsAvatar = gridfs.GridFS(db)

# Create app object here
app = web.application(urls, globals())

# Create session
session = web.session.Session(app, MongoStore(db, 'sessions'))
users.session = session

# Create mongo db's collection
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
    elif user['password'] != post['password']:
      response = {'message': 'nomatch'}
    elif user['authority'] == 1:
      response = {'message': 'nopermission'}
    else:
      users.login(user)
      response = {'message': 'success'}
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
      return json.dumps(response)

  #def POST(self):
    #post = web.input(_method='POST')
    #print post
    #return json.dumps('yes')

    #if post['cmd'] == 'delete':
      #print post['username']


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
    return json.dumps(response)

class Log:
  def GET(self):
    return render.log()

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



if __name__ == "__main__":
    #tCheck=MTimerClass(GetSearchinfo, '',  10);
    #tCheck.setDaemon(True); # 随主线程一起结果
    #tCheck.start();         #线程启动
    app.run()
