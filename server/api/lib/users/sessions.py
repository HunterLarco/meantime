"""
' Error Constants
"""
SESSION_DOESNT_EXIST = 'S0'
WATCHING = 'S2'
HACKER_FOUND = 'S3'


"""
' PURPOSE
'   The Session Model (entity)
' KEYS
'   SID - the unique action id associated with each session, they expire every hour
'   expiration - marks the time that the current SID expires
'   watching - is true when this session entity is being watched because a hacker is suspected
'   watchingTokens - a list of all SID tokens that are suspected of being belonged to a hacker
"""
from google.appengine.ext import ndb
class Session(ndb.Model):
  expiration = ndb.DateTimeProperty(indexed=False)
  SID = ndb.StringProperty(indexed=False)
  watching = ndb.BooleanProperty(indexed=False)
  watchingTokens = ndb.PickleProperty(indexed=False)
  user_key = ndb.KeyProperty(indexed=False)


"""
' PURPOSE
'   Return the session entity with a corresponding UID and ULID
' PARAMETERS
'   <String UID>
'   <String ULID>
' RETURNS
'   A session entity or None
' NOTES
'   This uses ancestor keys thus it has strong consistency
"""
def getSessionByTokens(UID, ULID):
  ancestor_key = ndb.Key('UID', UID, 'ULID', ULID)
  return Session.query(ancestor=ancestor_key).get()


"""
' PURPOSE
'   Generates a ULID
' PARAMETERS
'   None
' RETURNS
'   Returns a dict containing the generated ULID
"""
def formULID():
  import random
  rand = random.SystemRandom()
  
  import datetime
  time = datetime.datetime.now().strftime("%s")
  
  salt = ''.join(chr(rand.randint(0,255)) for x in range(10))
  
  from hashlib import sha256, sha384
  ULID = time+salt
  ULID = sha384(ULID).hexdigest()
  ULID = sha256(ULID).hexdigest()
  
  return dict(
    ULID = ULID
  )


"""
' PURPOSE
'   Generates a SID and signs an expration for that SID
' PARAMETERS
'   None
' RETURNS
'   A dict containing the generated SID and corresponding expiration date
"""
def formSID():
  import random
  rand = random.SystemRandom()
  
  salt = ''.join(chr(rand.randint(0,255)) for x in range(20))
  
  from hashlib import sha256, sha384
  SID = salt
  SID = sha384(SID).hexdigest()
  SID = sha256(SID).hexdigest()
  
  import datetime
  expiration = datetime.datetime.now() + datetime.timedelta(hours=1)

  return dict(
    expiration = expiration,
    SID = SID
  )


"""
' PURPOSE
'   Creates a new session for a user based on their UID
' PARAMETERS
'   <String UID>
' RETURNS
'   <SessionObject session>
' PUTS
'   1 - after creating the session
"""
def create(UID, userkey):
  ULID = formULID()['ULID']
  
  session = Session(parent=ndb.Key('UID', UID, 'ULID', ULID))
  
  SID_Data = formSID()
  SID = SID_Data['SID']
  expiration = SID_Data['expiration']
  
  session.SID = SID
  session.expiration = expiration
  session.watchingTokens = []
  session.watching = False
  session.user_key = userkey
  session.put()
  
  return SessionObject(UID, ULID, SID)


"""
' PURPOSE
'   Clears a given SID from the suspicious users list: aka 'watchingTokens' array.
' PARAMETERS
'   <String UID>
'   <String ULID>
'   <String SID>
' ERRORS
'   SESSION_DOESNT_EXIST
' PUTS
'   1 - after removing a SID from the watchingTokens list
' RETURNS
'   Nothing
"""
def clearWatchingSID(UID, ULID, SID):
  if UID == None or ULID == None:
    return SESSION_DOESNT_EXIST
  
  session = getSessionByTokens(UID, ULID)
  
  if session == None:
    return SESSION_DOESNT_EXIST
  
  if SID in session.watchingTokens:
    session.watchingTokens.remove(SID)
    session.put()


"""
' PURPOSE
'   Checks if the user may log in using the session associated with their auth tokens (UID, ULID, SID)
' PARAMETERS
'   <String UID>
'   <String ULID>
'   <String SID>
' ERRORS
'   SESSION_DOESNT_EXIST
'   HACKER_FOUND
'   WATCHING
' RETURNS
'   A dict containing the session and the entity corresponding
'   to the saved entity key property.
' PUTS
'   1 - upon assigning a new SID if it expires
"""
def validate(UID, ULID, SID):
  if UID == None or ULID == None or SID == None:
    return SESSION_DOESNT_EXIST
  
  session = getSessionByTokens(UID, ULID)
  
  if session == None:
    return SESSION_DOESNT_EXIST
  
  if session.watching:
    if SID in session.watchingTokens and len(session.watchingTokens) == 1:
      return HACKER_FOUND
    return WATCHING
  
  if session.SID != SID:
    session.watching = True
    session.watchingTokens.append(SID)
    session.watchingTokens.append(session.SID)
    session.put()
    return WATCHING
  
  sessionobj = SessionObject(UID, ULID, session.SID)
  
  import datetime
  now = datetime.datetime.now()
  if now > session.expiration:
    
    SID_Data = formSID()
    session.SID = SID_Data['SID']
    session.expiration = SID_Data['expiration']
    session.put()
    
    sessionobj.sid = session.SID
    
  entity = session.user_key.get()
  if entity == None:
    return None
  
  return dict(
    entity = entity,
    session = sessionobj
  )


"""
' PURPOSE
'   Contains session data and indicates if any changes were made to it.
'   This class is how user entities interact with sessions.
' PARAMETERS
'   __init__
'     <String uid>
'     <String ulid>
'     <String sid>
"""
class SessionObject(object):
  
  changed = False
  
  
  """
  ' PURPOSE
  '   A toString method for the SessionObject
  ' PARAMETERS
  '   None
  ' RETURNS
  '   A string representing this object
  """
  def __str__(self):
    return "%s(\n\tUID=%s,\n\tULID=%s,\n\tSID=%s\n)" % (self.__class__.__name__, self.uid, self.ulid, self.sid)
  
  
  """
  ' PURPOSE
  '   Returns the object as a dictionary
  ' PARAMETERS
  '   None
  ' RETURNS
  '   <dict uid='', ulid='', sid=''>
  """
  def toDict(self):
    return dict(
      uid = self.uid,
      ulid = self.ulid,
      sid = self.sid
    )
  
  
  """
  ' PURPOSE
  '   Getter and setter for the uid
  ' NOTES
  '   On change, the changed variable is set to true
  """
  @property
  def uid(self):
    return self.__uid__
  @uid.setter
  def uid(self, uid):
    self.__uid__ = uid
    self.changed = True
  
  
  """
  ' PURPOSE
  '   Getter and setter for the ulid
  ' NOTES
  '   On change, the changed variable is set to true
  """
  @property
  def ulid(self):
    return self.__ulid__
  @ulid.setter
  def ulid(self, ulid):
    self.__ulid__ = ulid
    self.changed = True
  
  
  """
  ' PURPOSE
  '   Getter and setter for the sid
  ' NOTES
  '   On change, the changed variable is set to true
  """
  @property
  def sid(self):
    return self.__sid__
  @sid.setter
  def sid(self, sid):
    self.__sid__ = sid
    self.changed = True
  
  
  """
  ' PURPOSE
  '   Initializes the object with the current uid, ulid, and sid
  '   while leaving the changed variable as false
  ' PARAMETERS
  '   <String uid>
  '   <String ulid>
  '   <String sid>
  ' RETURNS
  '   <SessionObject session>
  """
  def __init__(self, uid, ulid, sid):
    self.__uid__ = uid
    self.__ulid__ = ulid
    self.__sid__ = sid
  
  