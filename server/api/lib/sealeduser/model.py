from .. import users

"""
' Common Package Imports
"""
from google.appengine.ext import ndb
import messages



class SealedUser(users.AuthUser.Model):
  
  name = ndb.StringProperty(indexed=True)
  phone = ndb.StringProperty(indexed=True)
  contacts = ndb.KeyProperty(indexed=False, repeated=True)
  pendingcontacts = ndb.StringProperty(indexed=True, repeated=True)
  timezone = ndb.IntegerProperty(indexed=True)
  
  
  def __init__(self, *args, **kwargs):
    super(SealedUser, self).__init__(*args, **kwargs)
  
  
  def delete(self):
    super(SealedUser, self).delete()
    ndb.delete_multi(self.getMessages(keys_only=True))
  
  
  def getMessage(self, identifier):
    message = messages.SealedMessage.getById(identifier)
    if message.key.parent() != self.key and message.sender != self.key:
      return None
    return message
  
  
  
  
  
  
  
  
  @classmethod
  def updateAllPendingContacts(cls, user, value):
    pending = cls.query(cls.pendingcontacts == value).fetch()
    for entity in pending:
      entity.pendingcontacts.remove(value)
      if not user.key in entity.contacts:
        entity.contacts.append(user.key)
        entity.put()
    messages.PendingMessage.checkNewContact(value, user)
  
  
  @classmethod
  def getAllRecipients(cls, recipients):
    output = []
    for recipient in recipients:
      recipient = str(recipient)
      user = cls.getByEmail(recipient)
      if user == cls.USER_DOESNT_EXIST:
        user = cls.getByPhoneNumber(recipient)
        if user == cls.USER_DOESNT_EXIST:
          output.append(recipient)
          continue
      output.append(user)
    return output
  
  
  def sendMessage(self, uri, recipients, date, disappearing=False):
    recipients = self.__class__.getAllRecipients(recipients)
    
    for user in recipients:
      if isinstance(user, str):
        if not user in self.pendingcontacts:
          self.pendingcontacts.append(user)
      elif not user.key in self.contacts:
        self.contacts.append(user.key)
    
    self.put()
    
    messages.send(uri, self, recipients, date, disappearing=disappearing)
    
    return self.getContactList()
  
  
  
  
  
  
  
  
  
  
  
  def getContacts(self):
    contacts = []
    for key in self.contacts:
      user = key.get()
      if user == None:
        continue
      user.loadMeta()
      contacts.append(user)
    return contacts
  
  
  def getContactList(self):
    return [contact.toPublicDict() for contact in self.getContacts()] + self.pendingcontacts
  
  
  def changeName(self, name):
    self.name = name
    self.put()
  
  
  def changePhone(self, phone):
    self.__class__.updateAllPendingContacts(self, phone)
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
      contacts   = self.getContactList(),
      messages   = self.getMessages(json=True),
      synctime   = int(time.time()),
      passlocked = self.isLocked(),
      sesslocked = self.session.isLocked()
    )


  def getTimezone(self):
    return 0 if self.timezone == None else self.timezone


  def setTimezone(self, offset):
    if self.timezone == offset:
      return
    self.timezone = offset
    self.put()


  @classmethod
  def getByPhoneNumber(cls, number):
    user = cls.query(cls.phone == number).get()
    if user == None:
      return cls.USER_DOESNT_EXIST
    user.loadMeta()
    return user


  @classmethod
  def login(cls, email, password, timezone=None):
    user = super(SealedUser, cls).login(email, password)
    if not isinstance(user, cls):
      return user
    if timezone == None:
      return user
    user.setTimezone(timezone)
    return user


  @classmethod
  def create(cls, email, password):
    user = super(SealedUser, cls).create(email, password)
    if not isinstance(user, cls):
      return user
    user.contacts = []
    user.pendingcontacts = []
    user.put()
    
    # users with this contact pending
    cls.updateAllPendingContacts(user, email)
    
    return user