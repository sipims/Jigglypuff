#!/usr/bin/python
# -*-coding:utf-8 -*-
from web.session import Store
import time

class MongoStore(Store):
  def __init__(self, db, collection_name):
    self.collection = db[collection_name]

  def __contains__(self, key):
    data = self.collection.find_one({'session_id':key})
    return bool(data)

  def __getitem__(self, key):
    now = time.time()
    s = self.collection.find_one({'session_id':key})
    if not s:
      raise KeyError
    else:
      s.update({'atime':now})
    return s

  def __setitem__(self, key, value):
    now = time.time()

    value['atime'] = now

    s = self.collection.find_one({'session_id':key})
    if s:
      value = dict(map(lambda x: (str(x[0]), x[1]), [(k,v) for (k,v) in value.iteritems() if k not in ['_id']]))
      s.update(**value)
      self.collection.save(s)
    else:
      self.collection.insert(value)

  def __delitem__(self, key):
    self.collection.remove({'session_id':key})

  def cleanup(self, timeout):
    last_allowed_time = time.time() - timeout
    self.collection.remove({'atime' : { '$lt' : last_allowed_time}})
