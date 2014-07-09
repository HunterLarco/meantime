from google.appengine.ext import ndb

class Session(ndb.Model):
  """Models an individual session entry."""
  expiration = ndb.DateTimeProperty(indexed=False)
  SID = ndb.StringProperty(indexed=False)
  watching = ndb.BooleanProperty(indexed=False)
  watchingTokens = ndb.PickleProperty(indexed=False)











"""
' Return constants
"""
SESSION_DOESNT_EXIST = 'S0'
INCORRECT_SID = 'S1'
WATCHING = 'S2'
HACKER_FOUND = 'S3'











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
  
  session = Session(parent=ndb.Key('UID', UID, 'ULID', ULID))
  
  createSID(session)
  
  session.watchingTokens = []
  session.watching = False
  session.put()
  
  return dict(
    SID = session.SID,
    ULID = ULID,
    UID = UID
  )














"""
' Given a session, create a new SID for it and expiration
' Returns nothing
"""
def createSID(session):
  from hashlib import sha256, sha384
  import random
  
  rand = random.SystemRandom()
  
  salt = ''.join(chr(rand.randint(0,255)) for x in range(20))
  SID = salt
  SID = sha384(SID).hexdigest()
  SID = sha256(SID).hexdigest()
  
  import datetime
  expiration = datetime.datetime.now() + datetime.timedelta(hours=1)

  session.expiration = expiration
  session.SID = SID











"""
' Recieves a UID and ULID then sets the watching boolean to true
' Returns an error constant (SESSION_DOESNT_EXIST)
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














"""
' Given a UID, ULID, and SID. Clears the SID form the suspicious users list: 'watchingTokens' array.
' Returns an error constant (SESSION_DOESNT_EXIST)
"""
def clearWatchingSID(UID, ULID, SID):
  if UID == None or ULID == None:
    return SESSION_DOESNT_EXIST
  
  ancestor_key = ndb.Key('UID', UID, 'ULID', ULID)
  session = Session.query(ancestor=ancestor_key).get()
  
  if session == None:
    return SESSION_DOESNT_EXIST
  
  if SID in session.watchingTokens:
    session.watchingTokens.remove(SID)
    session.put()


















"""
' Recieves a UID, ULID, and SID and checks if the user may log in using the session associated with these values
' Returns an error code (SESSION_DOESNT_EXIST, WATCHING, INCORRECT_SID, or new SID)
"""
def validate(UID, ULID, SID):
  if UID == None or ULID == None or SID == None:
    return SESSION_DOESNT_EXIST
  
  ancestor_key = ndb.Key('UID', UID, 'ULID', ULID)
  session = Session.query(ancestor=ancestor_key).get()
  
  if session == None:
    return SESSION_DOESNT_EXIST
  
  if session.watching:
    if SID in session.watchingTokens and len(session.watchingTokens) == 1:
      return HACKER_FOUND
    return WATCHING
  
  if session.SID != SID:
    session.watchingTokens.append(SID)
    session.watchingTokens.append(session.SID)
    return INCORRECT_SID
  
  import datetime
  now = datetime.datetime.now()
  if now > session.expiration:
    createSID(session)
    session.put()
    return session.SID