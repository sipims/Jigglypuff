#!/usr/bin/python
# -*-coding:utf-8 -*-
import web
from datetime import datetime
import users

collection = None

def login(username):
  log = {'username': username, 'operation': 'Login', 'operate_date': datetime.now()}
  collection.save(log)

def add_user(add_user):
  user = users.get_user_by_sid()
  log = {'username': user['username'], 'operation': 'Add user - ' + add_user, 'operate_date': datetime.now()}
  collection.save(log)

def delete_user(delete_user):
  user = users.get_user_by_sid()
  log = {'username': user['username'], 'operation': 'Delete user - ' + delete_user, 'operate_date': datetime.now()}
  collection.save(log)

def change_password(username):
  user = users.get_user_by_sid()
  log = {'username': user['username'], 'operation': 'Change password - ' + username, 'operate_date': datetime.now()}
  collection.save(log)

def open_door(username):
  user = users.get_user_by_sid()
  log = {'username': user['username'], 'operation': 'Open the door - ' + username, 'operate_date': datetime.now()}
  collection.save(log)

def close_door(username):
  user = users.get_user_by_sid()
  log = {'username': user['username'], 'operation': 'Close the door - ' + username, 'operate_date': datetime.now()}
  collection.save(log)

def get_all_logs():
  return collection.find()
