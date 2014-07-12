"""
' Common Package Imports
"""
import sessions


"""
' Error Constants
"""
INCORRECT_LOGIN = 'U0'
SUCCESSFUL_LOGIN = 'U1'
EMAIL_IS_USED = 'U2'
BRUTE_SUSPECTED = 'U3'
USER_DOESNT_EXIST = 'U4'
SUCCESS = 'U5'
USER_LOCKED = 'U6'


"""
' PURPOSE
'   The User Model (entity)
' KEYS
'   UID - a unique user identification token that also is used to
'         confirm a correct password.
'   email - the email address of the user
'   brute_force_record - a record of failed login attempts by date
'   locked - a boolean determining if the user can be used or not
'   entity - the entity linked to this user for additional data
"""
from google.appengine.ext import ndb
class User(ndb.Model):
  UID = ndb.StringProperty(indexed=True)
  email = ndb.StringProperty(indexed=True)
  brute_force_record = ndb.PickleProperty(indexed=False)
  locked = ndb.BooleanProperty(indexed=False)
  entity = ndb.KeyProperty(indexed=False)


"""
' PURPOSE
'   Return the user entity with a corresponding email
' PARAMETERS
'   <String email>
' RETURNS
'   A user entity or None
' NOTES
'   This uses ancestor keys thus it has strong consistency
"""
def getUserByEmail(email):
  ancestor_key = ndb.Key(User, 'Entity', 'Email', email)
  return User.query(ancestor=ancestor_key).get()


"""
' PURPOSE
'   Given a password, hash it into an unrecognizable string
' PARAMETERS
'   <String password>
' RETURNS
'   A hex digest as a string
"""
def hashPassword(password):
  from hashlib import sha256, sha384
  password = sha384(password).hexdigest()
  password = sha256(password).hexdigest()
  return password


"""
' PURPOSE
'   Given an email and password, form the unique UID for that user
' PARAMETERS
'   <String email>
'   <String **hashed password>
' RETURNS
'   The formed UID
"""
def formUID(email, password):
  from hashlib import sha256, md5
  email = md5(email).hexdigest()
  return sha256(email+password).hexdigest()


"""
' PURPOSE
'   Return the user entity with a corresponding UID
' PARAMETERS
'   <String UID>
' RETURNS
'   A user entity or None
' NOTES
'   This does not use ancestor keys thus it has weak consistency.
'   Use 'getUserByEmail' for strong consistency
"""
def getUserByUID(UID):
  return User.query(User.UID == UID).get()


"""
' PURPOSE
'   Checks if a user has a correct password or not
' PARAMETERS
'   <User **ndb.model user>
'   <String password>
' RETURNS
'   A boolean answering the purpose (true if the password is correct)
"""
def hasCorrectPassword(user, password):
  password = hashPassword(password)
  uid = formUID(user.email, password)
  return user.UID == uid


"""
' PURPOSE
'   Given a user, lock that user and send the user an email
'   about the problem.
' PARAMETERS
'   <User **ndb.Model user>
' RETURNS
'   Nothing
' NOTES
'   Does not put the user entity
"""
def lock(user):
  user.locked = True
  sendLockedEmail(user)


"""
' PURPOSE
'   Given a user, unlock that user.
' PARAMETERS
'   <User **ndb.Model user>
' RETURNS
'   Nothing
' NOTES
'   Does not put the user entity
"""
def unlock(user):
  user.locked = False



"""
' PURPOSE
'   Sends an email notification to a user informing
'   that their account has been locked
' PARAMETERS
'   <User **ndb.Model user>
' RETURNS
'   Nothing
"""
def sendLockedEmail(user):
  from google.appengine.api import mail

  message = mail.EmailMessage(sender="meantime <info.meantime@gmail.com>",
                              subject="There is suspicious activity on your account")
  message.to = user.email
  message.body = 'Please log back in'

  message.send()


"""
' PURPOSE
'   Creates a new user entity and links it to another datastore entity
'   so that people who use this package can easily link more data
'   to a user entity form this package.
' PARAMETERS
'   <String email>
'   <String password>
'   <ndb.Model **kwarg entity>
' ERRORS
'   EMAIL_IS_USED
' RETURNS
'   A dict containing the new user UID upon success
' PUTS
'   1 - to save the created entity
"""
def create(email, password, entity=None):
  user = getUserByEmail(email);
  
  if user != None:
    return EMAIL_IS_USED
  
  password = hashPassword(password)
  
  user = User(parent=ndb.Key(User, 'Entity', 'Email', email))
  user.UID = formUID(email, password)
  user.email = email
  user.brute_force_record = dict()
  user.locked = False
  user.entity = entity.key
  user.put()
  
  return dict(
    UID = user.UID
  )


"""
' PURPOSE
'   Logs in a user by email and password while also monitoring for
'   brute force attacks on the account
' PARAMETERS
'   <String email>
'   <String password>
' ERRORS
'   USER_DOESNT_EXIST
'   BRUTE_SUSPECTED
'   INCORRECT_LOGIN
' RETURNS
'   A dict containing session tokens upon success (uid, ulid, sid)
' PUTS
'   1 - to lock the user
'     - (or) to unlock the user
'     - (or) to update the brute force record
"""
def login(email, password):
  user = getUserByEmail(email)
  
  if user == None:
    return USER_DOESNT_EXIST
  
  if not hasCorrectPassword(user, password):
    
    from time import time
    key = int(time())/(60*60*24)
    if not key in user.brute_force_record:
      user.brute_force_record[key] = 0
    user.brute_force_record[key] += 1
    
    a = 12
    p = 100
    f = lambda x: (p-a)/pow(365,float(2)/3)*pow(x,float(2)/3)+a
    count = 0
    
    for date in range(366):
      if key-date in user.brute_force_record:
        count += user.brute_force_record[key-date]
      if count > f(date):
        lock(user)
        user.put()
        return BRUTE_SUSPECTED
    
    user.put()
    return INCORRECT_LOGIN
    
  cookieData = sessions.create(user.UID)
  
  unlock(user)
  user.put()
  
  return dict(
    uid = cookieData['UID'],
    ulid = cookieData['ULID'],
    sid = cookieData['SID']
  )


"""
' PURPOSE
'   Determines if the session provided by a client is invalid
' PARAMETERS
'   <String UID>
'   <String ULID>
'   <String SID>
' ERRORS
'   From users/sessions.py (SESSION_DOESNT_EXIST, HACKER_FOUND) or OnSuccess (new SID)
'   From users/__init__.py (USER_DOESNT_EXIST, USER_LOCKED)
' RETURNS
'   A new SID upon success
' PUTS
'   1 - on user lock due to invalid SID
"""
def checkSession(UID, ULID, SID):
  status = sessions.validate(UID, ULID, SID)
  
  if status == sessions.SESSION_DOESNT_EXIST:
    return status
  
  if status == sessions.HACKER_FOUND:
    return status
  
  if status == sessions.WATCHING:
    return USER_LOCKED
  
  user = getUserByUID(UID)
  if user == None:
    return USER_DOESNT_EXIST
  
  if status == sessions.INCORRECT_SID:
    sessions.watch(UID, ULID)
    lock(user)
    user.put()
    return USER_LOCKED
  
  if user.locked:
    return USER_LOCKED
  
  return status