from google.appengine.ext import ndb

class Session(ndb.Model):
  """Models an individual session entry."""
  SID = ndb.StringProperty()
  watching = ndb.BooleanProperty()











"""
' Return constants
"""
SESSION_DOESNT_EXIST = 0
INCORRECT_SID = 1
WATCHING = 2
SUCCESS = 3











"""
' Recieves a User ID and generates a login token (session token) for that user
' Returns the ULID, UID, and SID that need to be stored as cookies
"""
def create(UID):
  from hashlib import sha256, sha384
  import datetime
  import random
  
  rand = random.SystemRandom()
  
  time = datetime.datetime.now().strftime("%s")
  salt = ''.join(chr(rand.randint(0,255)) for x in range(10))
  ULID = time+salt
  ULID = sha384(ULID).hexdigest()
  ULID = sha256(ULID).hexdigest()
  
  salt = ''.join(chr(rand.randint(0,255)) for x in range(20))
  SID = salt
  SID = sha384(SID).hexdigest()
  SID = sha256(SID).hexdigest()
  
  session = Session(parent=ndb.Key('UID', UID, 'ULID', ULID))
  session.SID = SID
  session.watching = False
  session.put()
  
  return dict(
    SID = SID,
    ULID = ULID,
    UID = UID
  )














"""
' Recieves a UID and ULID then sets the watching boolean to true
' Returns an error constant
"""
def watch(UID, ULID):
  if UID == None or ULID == None:
    return SESSION_DOESNT_EXIST
  
  ancestor_key = ndb.Key('UID', UID, 'ULID', ULID)
  session = Session.query(ancestor=ancestor_key).get()
  
  if session == None:
    return SESSION_DOESNT_EXIST
  
  session.watching = True
  session.put()
  
  return SUCCESS
















"""
' Recieves a UID, ULID, and SID and checks if the user may log in using the session associated with these values
' Returns an error code
"""
def validate(UID, ULID, SID):
  if UID == None or ULID == None or SID == None:
    return SESSION_DOESNT_EXIST
  
  ancestor_key = ndb.Key('UID', UID, 'ULID', ULID)
  session = Session.query(ancestor=ancestor_key).get()
  
  if session == None:
    return SESSION_DOESNT_EXIST
  
  if session.watching:
    return WATCHING
  
  if session.SID != SID:
    return INCORRECT_SID
  
  return SUCCESS