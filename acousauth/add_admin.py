import hashlib
import pymongo
from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
db = client.mydb2
collection = db.users

def pswd(password):
  return hashlib.sha1(password).hexdigest()

if __name__ == '__main__':
  record = {'username': 'gusss', 'password': pswd('asdkjfds'), 'create_date': datetime.now(), 'authority': 4}
  collection.save(record)
