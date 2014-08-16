"""
' Common Package Imports
"""
from google.appengine.ext import ndb
import sessions
















def smarthash(string):
  from hashlib import sha256, md5
  string = md5(string+'*t7)_(@&63)').hexdigest()
  string = sha256(string).hexdigest()
  return string



class UserMetaData(ndb.Model):
  password =           ndb.StringProperty  (indexed=True)
  email =              ndb.StringProperty  (indexed=True)
  brute_force_record = ndb.PickleProperty  (indexed=False)
  password_locked =    ndb.BooleanProperty (indexed=False)
  entity_key =         ndb.KeyProperty     (indexed=False)
  
  
  """
  ' Error Constants
  """
  EMAIL_IS_USED =     'UMD0'
  USER_DOESNT_EXIST = 'UMD1'
  BRUTE_SUSPECTED =   'UMD2'
  INCORRECT_LOGIN =   'UMD3'
  
  
  def setPassword(self, password):
    self.password = smarthash(password)
    self.put()
  
  
  def changeEmail(self, email, abstractuser, namespace=None):
    user = self.__class__.getByEmail(email, namespace=namespace);
    if user != None:
      return self.EMAIL_IS_USED
    uid = smarthash(email)
    meta = self.__class__(parent=ndb.Key('uid', uid, namespace=namespace))
    meta.populate(**self.to_dict())
    meta.email = email
    meta.put()
    abstractuser.__parent__ = meta
    self.key.delete()
  
  
  def getUser(self):
    user = self.entity_key.get()
    user.__parent__ = self
    return user
  
  
  def matchPassword(self, password):
    return smarthash(password) == self.password
  
  
  @classmethod
  def getByUID(cls, uid, namespace=None):
    ancestor_key = ndb.Key('uid', uid, namespace=namespace)
    return cls.query(ancestor=ancestor_key).get()
  
  
  @classmethod
  def getByEmail(cls, email, namespace=None):
    return cls.getByUID(smarthash(email), namespace=namespace)
  
  
  @classmethod
  def create(cls, email, password, namespace=None):
    user = cls.getByEmail(email, namespace=namespace);
  
    if user != None:
      return cls.EMAIL_IS_USED
  
    password = smarthash(password)
    uid = smarthash(email)
  
    user = cls(parent=ndb.Key('uid', uid, namespace=namespace))
    user.password = password
    user.email = email
    user.brute_force_record = dict()
    user.password_locked = False
    user.entity_key = None
    user.put()
    
    return user


  def lock(self):
    self.password_locked = True
  
  
  def unlock(self):
    meta.password_locked = False
    meta.brute_force_record = dict()


  @classmethod
  def login(cls, email, password, namespace=None):
    meta = cls.getByEmail(email, namespace=namespace)
    if meta == None:
      return cls.USER_DOESNT_EXIST
    
    if meta.password_locked:
      return cls.BRUTE_SUSPECTED
    
    if not meta.matchPassword(password):
      
      from time import time
      key = int(time())/(60*60*24)
      if not key in meta.brute_force_record:
        meta.brute_force_record[key] = 0
      meta.brute_force_record[key] += 1
  
      a = 12
      p = 100
      f = lambda x: (p-a)/pow(365,float(2)/3)*pow(x,float(2)/3)+a
      count = 0
  
      for date in range(366):
        if key-date in meta.brute_force_record:
          count += meta.brute_force_record[key-date]
        if count > f(date):
          meta.lock()
          meta.put()
          return cls.BRUTE_SUSPECTED
  
      meta.put()
      return cls.INCORRECT_LOGIN
    
    return meta.getUser()



















class AbstractUser(ndb.Model):
  
  """
  ' Error Constants
  """
  EMAIL_IS_USED     = 'ABCU0'
  INCORRECT_LOGIN   = 'ABCU1'
  USER_DOESNT_EXIST = 'ABCU2'
  BRUTE_SUSPECTED   = 'ABCU3'
  
  
  @property
  def __parent__(self):
    return self.__parententity__ if hasattr(self, '__parententity__') else None
  @__parent__.setter
  def __parent__(self, entity):
    self.__parententity__ = entity
    self.email = entity.email
    self.uid = entity.key.pairs()[0][1]
  
  
  def changePassword(self, password):
    self.__parent__.setPassword(password)
  
  
  def isLocked(self):
    return self.__parent__.password_locked
  
  
  def changeEmail(self, email):
    error = self.__parent__.changeEmail(email, self, namespace=self.__class__.__name__)
    if error == self.__parent__.EMAIL_IS_USED:
      return self.EMAIL_IS_USED
  
  
  def delete(self):
    self.__parent__.key.delete()
    self.key.delete()
  
  
  def put(self, *args, **kwargs):
    oldkey = self.key
    super(AbstractUser, self).put(*args, **kwargs)
    if oldkey == None:
      self.__parent__.entity_key = self.key
      self.__parent__.put()
  
  
  @classmethod
  def create(cls, email, password):
    meta = UserMetaData.create(email, password, namespace=cls.__name__)
    if meta == UserMetaData.EMAIL_IS_USED:
      return cls.EMAIL_IS_USED
    user = cls()
    user.__parent__ = meta
    return user
  
  
  @classmethod
  def login(cls, email, password):
    status = UserMetaData.login(email, password, namespace=cls.__name__)
    if status == UserMetaData.USER_DOESNT_EXIST:
      return cls.USER_DOESNT_EXIST
    if status == UserMetaData.BRUTE_SUSPECTED:
      return cls.BRUTE_SUSPECTED
    if status == UserMetaData.INCORRECT_LOGIN:
      return cls.INCORRECT_LOGIN
    return status
  
  
  @classmethod
  def getByUID(cls, uid):
    meta = UserMetaData.getByUID(uid, namespace=cls.__name__)
    if meta == None:
      return cls.USER_DOESNT_EXIST
    return meta.getUser()
  
  
  @classmethod
  def getByEmail(cls, email):
    meta = UserMetaData.getByEmail(email, namespace=cls.__name__)
    if meta == None:
      return cls.USER_DOESNT_EXIST
    return meta.getUser()



