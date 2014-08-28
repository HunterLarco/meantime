"""
' Common Package Imports
"""
from google.appengine.ext import ndb
from google.appengine.api import memcache



class SealedMessage(ndb.Model):
  
  uri = ndb.TextProperty(indexed=False)
  disappearing = ndb.BooleanProperty(indexed=False)
  viewable_timestamp = ndb.IntegerProperty(indexed=False)
  read_date = ndb.IntegerProperty(indexed=False)
  
  # give or take a day for time zones
  def isViewable(self):
    import time
    return int(time.time()) > self.viewable_timestamp-60*60*24
  
  
  def isDisappearing(self):
    return self.disappearing
  
  
  def isRead(self):
    return self.read_date != None


  def toDict(self):
    return dict(
      key           = self.key.urlsafe(),
      disappearing  = self.disappearing,
      viewable_date = self.viewable_timestamp
    )


  @classmethod
  def getById(cls, identifier):
    return ndb.Key(urlsafe=identifier).get()

  
  @classmethod
  def fetch(cls, parent, json=False, keys_only=False):
    if json:
      cache = memcache.get('messages_%s' % str(keys_only), namespace='SealedMessage-recipient:(%s)' % str(parent.key))
      if cache != None:
        return cache
      messages = cls.query(ancestor = parent.key).fetch(keys_only=keys_only)
      messages = [message.toDict() for message in messages]
      memcache.set('messages_%s' % str(keys_only), messages, time=120, namespace='SealedMessage-recipient:(%s)' % str(parent.key))
    else:
      messages = cls.query(ancestor = parent.key).fetch(keys_only=keys_only)
    return messages


  @classmethod
  def create(cls, uri, parent, date, disappearing=False):
    message = cls(parent=parent.key)
    message.uri = uri
    message.disappearing = disappearing
    message.viewable_timestamp = date
    message.put()
    memcache.delete('messages_%s' % str(False), namespace='SealedMessage-recipient:(%s)' % str(parent.key))
    memcache.delete('messages_%s' % str(True), namespace='SealedMessage-recipient:(%s)' % str(parent.key))
    
  