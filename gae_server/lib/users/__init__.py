import sessions





"""
' Recieves an email and password
' Returns the UID of the created user entity or an error constant (EMAIL_IS_USED)
"""
def create(email, password):
  user = User.query(User.email == email).get()
  if user != None:
    return EMAIL_IS_USED
  
  from hashlib import sha256, sha384
  password = sha384(password).hexdigest()
  password = sha256(password).hexdigest()
  
  user = User(parent=ndb.Key('Email', email, 'Password', password))
  user.UID = getUID(email, password)
  user.email = email
  user.brute_force_record = dict()
  user.locked = False
  user.put()
  
  return dict(
    UID = user.UID
  )








"""
' Return constants
"""
INCORRECT_LOGIN = 'U0'
SUCCESSFUL_LOGIN = 'U1'
EMAIL_IS_USED = 'U2'
BRUTE_SUSPECTED = 'U3'
USER_DOESNT_EXIST = 'U4'
SUCCESS = 'U5'
USER_LOCKED = 'U6'











"""
' Recieves a webapp2 instance, email, and password
' Attempts to log in and set cookies
' Returns a error constant (INCORRECT_LOGIN, BRUTE_SUSPECTED)
"""
def login(email, password):
  user = User.query(User.email == email).get()
  
  if validate(email, password) == INCORRECT_LOGIN:
    
    from time import time
    key = int(time())/(60*60*24)
    if not key in user.brute_force_record:
      user.brute_force_record[key] = 0
    user.brute_force_record[key] += 1
    user.put()
    
    a = 12
    p = 100
    f = lambda x: (p-a)/pow(365,float(2)/3)*pow(x,float(2)/3)+a
    count = 0
    
    for date in range(366):
      if key-date in user.brute_force_record:
        count += user.brute_force_record[key-date]
      if count > f(date):
        lock(user)
        return BRUTE_SUSPECTED
    
    return INCORRECT_LOGIN
  
  UID = user.UID
  
  cookieData = sessions.create(UID)
  
  return {
    'uid': cookieData['UID'],
    'ulid': cookieData['ULID'],
    'sid': cookieData['SID']
  }













"""
' Locks a user, takes either the entity of the UID
' Returns an error constant
"""
def lock(user):
  if isinstance(user, basestring):
    user = User.query(User.UID == user).get()
    if user == None:
      return USER_DOESNT_EXIST
  user.locked = True
  user.put()
  return SUCCESS














"""
' Recieves an email and password and attempts to find a user with those credentials
' Returns an error constant (INCORRECT_LOGIN, SUCCESSFUL_LOGIN)
"""
def validate(email, password):
  from hashlib import sha256, sha384
  password = sha384(password).hexdigest()
  password = sha256(password).hexdigest()
  
  ancestor_key = ndb.Key('Email', email, 'Password', password)
  user = User.query(ancestor=ancestor_key).get()
  
  if user == None:
    return INCORRECT_LOGIN
  
  return SUCCESSFUL_LOGIN














"""
' Recieves a webapp instance and determines if the session is valid in addition to watching the session
' Returns a session error constant
'     From users/sessions.py (SESSION_DOESNT_EXIST) or OnSuccess (new SID)
'     From users/__init__.py (USER_DOESNT_EXIST, USER_LOCKED)
' OnSuccess returns nothing or a new SID
"""
def checkSession(UID, ULID, SID):
  status = sessions.validate(UID, ULID, SID)
  
  if status == sessions.SESSION_DOESNT_EXIST:
    return status
  
  if status == sessions.INCORRECT_SID:
    sessions.watch(UID, ULID)
    user = User.query(User.UID == UID).get()
    if user == None:
      return USER_DOESNT_EXIST
    lock(user)
    return USER_LOCKED
  
  user = User.query(User.UID == UID).get()
  if user == None:
    return USER_DOESNT_EXIST
  
  if user.locked:
    return USER_LOCKED
  
  return status













"""
' Recieves an email and password
' Returns a generated UID
"""
def getUID(email, password):
  from hashlib import sha256, sha384
  password = sha384(password).hexdigest()  
  return sha256(email+password).hexdigest()












"""
' The User Entry Model For Easy Access
"""

from google.appengine.ext import ndb

class User(ndb.Model):
  """Models an individual user entry."""
  UID = ndb.StringProperty(indexed=True)
  email = ndb.StringProperty(indexed=True)
  brute_force_record = ndb.PickleProperty(indexed=False)
  locked = ndb.BooleanProperty(indexed=False)
  