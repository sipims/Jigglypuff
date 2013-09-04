#!/usr/bin/python
# -*-coding:utf-8 -*-
import web
import hashlib
from datetime import datetime

'''
  This module is used as a model module for users.
  It contains all the CRUD operations.
'''

#SALTY_GOODNESS = u'5gR3dvtres$@;1£56u&&$"FDergjngrekjkj4223234erwgnkvgdvdfkm'

#Must be set by the thing importing this module
collection = None
session = None

def get_user_by_sid():
  try:
    user = collection.find_one({'_id':session._user_id})
    return user
  except AttributeError:
    print "exception"
    return None

def get_user_by_name(name):
  try:
    user = collection.find_one({'username' : name})
    return user
  except AttributeError:
    return None

def get_all_users():
  return collection.find()

def authenticate(username, password):
  user = collection.find_one({'username':username, 'password':pswd(password)})
  return user if user else None

def login(user):
  session._user_id = user['_id']
  return user

def logout():
  session.kill()

def add(**kwargs):
  kwargs['create_date'] = datetime.now()
  user = collection.save(kwargs)
  return user

def del_user_by_name(name):
  collection.remove({'username':name})

def change_password(name, password):
  collection.update({'username': name}, {'$set': {'password': pswd(password)}})

def pswd(password):
  #seasoned = password + SALTY_GOODNESS
  #seasoned = seasoned.encode('utf-8')
  return hashlib.sha1(password).hexdigest()
  #return password

def login_required(function, login_page='/login/'):
  def inner(*args, **kwargs):
    if get_user():
      return function(*args, **kwargs)
    else:
      return web.seeother(login_page+'?next=%s' % web.ctx.get('path','/'))
    return inner
