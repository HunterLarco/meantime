from AbstractUser import AbstractUser
import sessions


class Model(AbstractUser):
  
  EMAIL_IS_USED     = 'AUTHU0'
  INCORRECT_LOGIN   = 'AUTHU1'
  USER_DOESNT_EXIST = 'AUTHU2'
  BRUTE_SUSPECTED   = 'AUTHU3'
  
  SESSION_DOESNT_EXIST = 'AUTHU100'
  HACKER_FOUND         = 'AUTHU101'
  SESSION_LOCKED       = 'AUTHU102'
  
  session = None
  
  
  def changeEmail(self, email):
    oldkey = self.__parent__.key
    
    error = super(Model, self).changeEmail(email)
    if error != None:
      return error
    
    newkey = self.__parent__.key
    sessions.alterKey(oldkey, newkey)
  
  
  def unlockSession(self, email, password):
    if not self.__parent__.matchPassword(password):
      return self.INCORRECT_LOGIN
    if not self.__parent__.email == email:
      return self.INCORRECT_LOGIN
    self.session.exonerate()
    self.session = sessions.create(self.uid, self.__parent__.key)
    
    

  
  """
  ' ALWAYS CHECK IS LOCKED and SESSION IS LOCKED
  """
  @classmethod
  def getBySession(cls, uid, ulid, sid):
    session_data = sessions.validate(uid, ulid, sid)
    
    if session_data == None:
      return cls.SESSION_DOESNT_EXIST
    elif session_data == sessions.SESSION_DOESNT_EXIST:
      return cls.SESSION_DOESNT_EXIST
    elif session_data == sessions.HACKER_FOUND:
      return cls.HACKER_FOUND
    
    meta = session_data['entity']
    session = session_data['session']
    
    if meta == None:
      return cls.USER_DOESNT_EXIST
    
    user = meta.getUser()
    
    if user == None:
      return cls.USER_DOESNT_EXIST
    
    user.session = session
    
    return user
  
  
  @classmethod
  def login(cls, email, password):
    user = super(Model, cls).login(email, password)
    if not isinstance(user, cls):
      return user
    
    user.session = sessions.create(user.uid, user.__parent__.key)
    return user
  
  
  @classmethod
  def create(cls, email, password):
    user = super(Model, cls).create(email, password)
    if not isinstance(user, cls):
      return user
    
    user.session = sessions.create(user.uid, user.__parent__.key)
    return user







