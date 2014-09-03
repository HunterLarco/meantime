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
  sender = ndb.StringProperty(indexed=False)
  sent_date = ndb.IntegerProperty(indexed=False)
  
  
  def serve(self, webapp2instance):
    if (not self.isViewable()) or (self.isDisappearing() and self.isRead()):
      # blank 1x1 gif
      uri = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
    else:
      uri = self.uri
      if not self.isRead():
        import time
        self.read_date = int(time.time())
        self.put()
    
    mimetype = uri[uri.index(':')+1 : uri.index(';')]
    data = uri[uri.index(',')+1:]
    
    webapp2instance.response.headers['Content-Type'] = str(mimetype)
    webapp2instance.response.out.write(data.decode('base64'))
  
  
  def getSender(self):
    import model
    return model.SealedUser.getByUID(self.sender)
  
  
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
      viewable_date = self.viewable_timestamp,
      sender        = self.getSender().toPublicDict() if self.getSender() != None else None,
      readdate      = self.read_date,
      sent_date     = self.sent_date
    )


  @classmethod
  def getById(cls, identifier):
    return ndb.Key(urlsafe=identifier).get()

  
  @classmethod
  def fetch(cls, parent, json=False, keys_only=False):
    if json:
      cache = memcache.get('messages_%s' % str(keys_only), namespace='SealedMessage-recipient:(%s)' % str(parent.key))
      # if cache != None:
        # return cache
      messages = cls.query(ancestor = parent.key).fetch(keys_only=keys_only)
      messages = [message.toDict() for message in messages]
      memcache.set('messages_%s' % str(keys_only), messages, time=120, namespace='SealedMessage-recipient:(%s)' % str(parent.key))
    else:
      messages = cls.query(ancestor = parent.key).fetch(keys_only=keys_only)
    return messages


  @classmethod
  def create(cls, uri, sender, recipient, date, disappearing=False):
    import time
    message = cls(parent=recipient.key)
    message.uri = uri
    message.disappearing = disappearing
    message.viewable_timestamp = date
    message.sender = sender.uid
    message.sent_date = int(time.time())
    message.put()
    memcache.delete('messages_%s' % str(False), namespace='SealedMessage-recipient:(%s)' % str(recipient.key))
    memcache.delete('messages_%s' % str(True), namespace='SealedMessage-recipient:(%s)' % str(recipient.key))
    
  