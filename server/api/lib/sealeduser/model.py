from .. import users

"""
' Common Package Imports
"""
from google.appengine.ext import ndb
import messages



class SealedUser(users.AuthUser.Model):
  
  name = ndb.StringProperty(indexed=True)
  phone = ndb.StringProperty(indexed=True)
  contacts = ndb.PickleProperty(indexed=False)
  
  
  def __init__(self, *args, **kwargs):
    super(SealedUser, self).__init__(*args, **kwargs)
  
  
  def delete(self):
    super(SealedUser, self).delete()
    ndb.delete_multi(self.getMessages(keys_only=True))
  
  
  def getMessage(self, identifier):
    message = messages.SealedMessage.getById(identifier)
    if message.key.parent() != self.key:
      return None
    return message
  
  
  def sendMessage(self, uri, recipients, date, disappearing=False):
    notsignedup = []
    sent_uids = []
    
    for recipient in recipients:
      user = self.__class__.getByEmail(recipient)
      if user == self.USER_DOESNT_EXIST:
        user = self.__class__.getByPhoneNumber(recipient)
        if user == self.USER_DOESNT_EXIST:
          notsignedup.append(recipient)
          continue
      
      sent_uids.append(user.uid)
      messages.SealedMessage.create(uri, self, user, date, disappearing=disappearing)
    
    self.contacts = list(set(self.contacts + sent_uids))
    self.put()
    
    sender = self.name if self.name != None else (self.phone if self.phone != None else self.email)
    
    from ..net import smsclient
    from ..net import emailclient
    
    for recipient in notsignedup:
      if '@' in recipient:
        emailclient.send(recipient, """
I've Invited You to Sealed!

To accept this invitation, click the following link,
or copy and paste the URL into your browser's address
bar:

http://trysealed.com?c=%s
  """ % recipient)
      else:
        smsclient.send(recipient, '%s has sent you a message on Sealed! Sign up at trysealed.com today to view your message!' % sender)
    
    return [contact.toPublicDict() for contact in self.getContacts()]
  
  
  def getContacts(self):
    contacts = []
    for uid in self.contacts:
      user = self.__class__.getByUID(uid)
      if not isinstance(user, self.__class__):
        continue
      contacts.append(user)
    return contacts
  
  
  def changeName(self, name):
    self.name = name
    self.put()
  
  
  def changePhone(self, phone):
    self.phone = phone
    self.put()
  
  
  def getMessages(self, json=False, keys_only=False):
    return messages.SealedMessage.fetch(self, json=json, keys_only=keys_only)
  
  
  def toPublicDict(self):
    return dict(
      email      = self.email,
      fullname   = self.name,
      phone      = self.phone
    )
  
  
  def toDict(self):
    import time
    return dict(
      email      = self.email,
      fullname   = self.name,
      phone      = self.phone,
      contacts   = [contact.toPublicDict() for contact in self.getContacts()],
      messages   = self.getMessages(json=True),
      synctime   = int(time.time()),
      passlocked = self.isLocked(),
      sesslocked = self.session.isLocked()
    )


  @classmethod
  def getByPhoneNumber(cls, number):
    user = cls.query(cls.phone == number).get()
    if user == None:
      return cls.USER_DOESNT_EXIST
    user.loadMeta()
    return user


  @classmethod
  def create(cls, email, password):
    user = super(SealedUser, cls).create(email, password)
    if not isinstance(user, cls):
      return user
    user.contacts = []
    user.put()
    return user