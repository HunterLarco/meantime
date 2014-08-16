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
    error = super(Model, self).changeEmail(email)
    if error != None:
      return error
    
    session = sessions.create(self.uid, self.__parent__.key)
    self.session.uid = session.uid
    self.session.ulid = session.ulid
    self.session.sid = session.sid
  
  
  @classmethod
  def getBySession(cls, uid, ulid, sid):
    session_data = sessions.validate(uid, ulid, sid)
    
    if session_data == None:
      return cls.SESSION_DOESNT_EXIST
    elif session_data == sessions.SESSION_DOESNT_EXIST:
      return cls.SESSION_DOESNT_EXIST
    elif session_data == sessions.HACKER_FOUND:
      return cls.HACKER_FOUND
    elif session_data == sessions.WATCHING:
      return cls.SESSION_LOCKED
    
    meta = session_data['entity']
    session = session_data['session']
    
    if meta == None:
      return cls.USER_DOESNT_EXIST
    
    user = meta.getUser()
    
    if user == None:
      return cls.USER_DOESNT_EXIST
    
    user.session = session
    if user.isLocked():
      return cls.BRUTE_SUSPECTED
    
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







