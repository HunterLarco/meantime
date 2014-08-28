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
    
    for recipient in recipients:
      user = self.__class__.getByEmail(recipient)
      if user == self.USER_DOESNT_EXIST:
        user = self.__class__.getByPhoneNumber(recipient)
        if user == self.USER_DOESNT_EXIST:
          notsignedup.append(recipient)
          continue
      
      messages.SealedMessage.create(uri, user, date, disappearing=disappearing)
  
  
  def changeName(self, name):
    self.name = name
    self.put()
  
  
  def changePhone(self, phone):
    self.phone = phone
    self.put()
  
  
  def getMessages(self, json=False, keys_only=False):
    return messages.SealedMessage.fetch(self, json=json, keys_only=keys_only)
  
  
  def toDict(self):
    import time
    return dict(
      email      = self.email,
      fullname   = self.name,
      phone      = self.phone,
      contacts   = self.contacts,
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
    return user


  @classmethod
  def create(cls, email, password):
    user = super(SealedUser, cls).create(email, password)
    if not isinstance(user, cls):
      return user
    user.put()
    return user