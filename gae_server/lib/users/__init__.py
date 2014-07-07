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
  user.put()
  
  return dict(
    UID = user.UID
  )








"""
' Return constants
"""
INCORRECT_LOGIN = 0
SUCCESSFUL_LOGIN = 1
EMAIL_IS_USED = 2
BRUTE_SUSPECTED = 3













"""
' Recieves a webapp2 instance, email, and password
' Attempts to log in and set cookies
' Returns a error constant (INCORRECT_LOGIN, SUCCESSFUL_LOGIN)
"""
def login(Webapp2Instance, email, password):
  if validate(email, password) == INCORRECT_LOGIN:
    user = User.query(User.email == email).get()
    
    if user == None:
      return INCORRECT_LOGIN
    
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
        return BRUTE_SUSPECTED
    
    return INCORRECT_LOGIN
  
  UID = getUID(email, password)
  
  cookieData = sessions.create(UID)
  
  from .. import cookies
  shim = cookies.CookieShim(Webapp2Instance)
  shim.set('UID',  cookieData['UID'])
  shim.set('ULID', cookieData['ULID'])
  shim.set('SID',  cookieData['SID'])
  
  return SUCCESSFUL_LOGIN




















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
"""
def checkSession(Webapp2Instance):
  from .. import cookies
  shim = cookies.CookieShim(Webapp2Instance)
  status = sessions.validate(shim.get('UID'), shim.get('ULID'), shim.get('SID'))
  
  if status == sessions.SESSION_DOESNT_EXIST:
    shim.remove('UID')
    shim.remove('ULID')
    shim.remove('SID')
  elif status == sessions.INCORRECT_SID:
    sessions.watch(shim.get('UID'), shim.get('ULID'))
  
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
  