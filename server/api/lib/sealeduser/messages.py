"""
' Common Package Imports
"""
from google.appengine.ext import ndb





#
#     sender = self.name if self.name != None else (self.phone if self.phone != None else self.email)
#
#     from ..net import smsclient
#     from ..net import emailclient
#
#     for recipient in notsignedup:
#       if '@' in recipient:
#         emailclient.send(recipient, """
# I've Invited You to Sealed!
#
# To accept this invitation, click the following link,
# or copy and paste the URL into your browser's address
# bar:
#
# http://trysealed.com?c=%s
#   """ % recipient)
#       else:
#         smsclient.send(recipient, '%s has sent you a message on Sealed! Sign up at trysealed.com today to view your message!' % sender)
#






def __inviteuser__(user, sender):
  if '@' in user:
    from ..net import emailclient
    sender = sender.name if sender.name != None else sender.email
    emailclient.send(user, """
    %s Invited You to Sealed!
    
    To accept this invitation, click the following link,
    or copy and paste the URL into your browser's address
    bar:
    
    http://trysealed.com?c=%s
    """ % (sender, user), 'Welcome To Sealed!')
  
  else:
    from ..net import smsclient
    sender = sender.name if sender.name != None else (sender.phone if sender.phone != None else sender.email)
    smsclient.send(user, '%s has sent you a message on Sealed! Sign up at trysealed.com today to view your message!' % sender)
    


def send(uri, sender, recipients, date, disappearing=False):
  for user in recipients:
    if isinstance(user, str):
      __inviteuser__(user, sender)
      PendingMessage.create(user, uri, sender, date, disappearing=disappearing)
    else:
      SealedMessage.create(uri, sender, user, date, disappearing=disappearing)
  






class PendingMessage(ndb.Model):
  
  uri = ndb.TextProperty(indexed=False)
  sender = ndb.KeyProperty(indexed=True)
  disappearing = ndb.BooleanProperty(indexed=False)
  viewable = ndb.IntegerProperty(indexed=False)
  sent_date = ndb.IntegerProperty(indexed=False)
  
  
  def send(self, recipient):
    message = SealedMessage.create(self.uri, self.sender.get(), recipient, self.viewable, disappearing=self.disappearing, sent_date=self.sent_date)
    self.key.delete()
    return message
  
  
  def getSender(self):
    sender = self.sender.get()
    sender.loadMeta()
    return sender
  
  
  def toDict(self):
    return dict(
      key           = self.key.urlsafe(),
      disappearing  = self.disappearing,
      viewable_date = self.viewable,
      sender        = self.getSender().toPublicDict() if self.getSender() != None else None,
      readdate      = None,
      sent_date     = self.sent_date,
      recipient     = self.key.parent().pairs()[0][1]
    )
  
  
  @classmethod
  def checkNewContact(cls, original_raw_recipient, recipient):
    entities = cls.query(ancestor = ndb.Key('pendingcontact', original_raw_recipient))
    if entities.count() == 0:
      return
    for entity in entities:
      entity.send(recipient)
  
  
  @classmethod
  def create(cls, recipient, uri, sender, viewable, disappearing=False):
    import time
    entity = cls(parent=ndb.Key('pendingcontact', recipient))
    entity.uri = uri
    entity.sender = sender.key
    entity.viewable = viewable
    entity.disappearing = disappearing
    entity.sent_date = int(time.time())
    entity.put()
    









class SealedMessage(ndb.Model):
  
  uri = ndb.TextProperty(indexed=False)
  disappearing = ndb.BooleanProperty(indexed=False)
  viewable_timestamp = ndb.IntegerProperty(indexed=False)
  read_date = ndb.IntegerProperty(indexed=False)
  sender = ndb.KeyProperty(indexed=True)
  sent_date = ndb.IntegerProperty(indexed=False)
  
  
  def serve(self, webapp2instance):
    if (not self.isViewable()) or (self.isDisappearing() and self.isRead() and webapp2instance.user.key != self.sender):
      # blank 1x1 gif
      uri = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
    else:
      uri = self.uri
      if not self.isRead() and (webapp2instance.user.key != self.sender or self.sender == self.key.parent()):
        import time
        self.read_date = int(time.time())
        self.put()
    
    mimetype = uri[uri.index(':')+1 : uri.index(';')]
    data = uri[uri.index(',')+1:]
    
    webapp2instance.response.headers['Content-Type'] = str(mimetype)
    webapp2instance.response.out.write(data.decode('base64'))
  
  
  def getSender(self):
    sender = self.sender.get()
    sender.loadMeta()
    return sender
  
  
  def getRecipient(self):
    sender = self.key.parent().get()
    sender.loadMeta()
    return sender
  
  
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
      sent_date     = self.sent_date,
      recipient     = self.getRecipient().toPublicDict() if self.getRecipient() != None else None
    )


  @classmethod
  def getById(cls, identifier):
    return ndb.Key(urlsafe=identifier).get()

  
  @classmethod
  def fetch(cls, recipient, json=False, keys_only=False):
    messages =  cls.query(ancestor    = recipient.key).fetch(keys_only=keys_only)
    messages += cls.query(cls.sender == recipient.key).fetch(keys_only=keys_only)
    messages += PendingMessage.query(PendingMessage.sender == recipient.key).fetch(keys_only=keys_only)
    if keys_only:
      return [str(key) for key in messages] if json else messages
    return [message.toDict() for message in messages] if json else messages


  @classmethod
  def getBySender(cls, sender):
    return cls.query(cls.sender == sender.key).fetch()


  @classmethod
  def create(cls, uri, sender, recipient, date, disappearing=False, sent_date=None):
    import time
    message = cls(parent=recipient.key)
    message.uri = uri
    message.disappearing = disappearing
    message.viewable_timestamp = date
    message.sender = sender.key
    message.sent_date = int(time.time()) if sent_date == None else sent_date
    message.put()
    
  