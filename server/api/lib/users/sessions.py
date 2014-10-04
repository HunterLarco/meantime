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
  lastedit = ndb.DateTimeProperty(indexed=True, auto_now=True)
  expiration = ndb.DateTimeProperty(indexed=False)
  SID = ndb.StringProperty(indexed=False)
  watching = ndb.BooleanProperty(indexed=False)
  watchingTokens = ndb.PickleProperty(indexed=False)
  user_key = ndb.KeyProperty(indexed=True)


"""
' PURPOSE
'   Removes tokens which haven't been changed in over two months
' PARAMETERS
'   Nothing
' RETURNS
'   None
"""
def clean():
  import datetime
  query = Session.query(Session.lastedit < datetime.datetime.now()-datetime.timedelta(days=30*2))
  ndb.delete_multi(query.fetch(keys_only=True))


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
  
  return SessionObject(UID, ULID, SID, session)


"""
' PURPOSE
'   If a user's key changes, alter all sessions with the old key
' PARAMETERS
'   <String old_key>
'   <String new_key>
' RETURNS
'   Nothing
"""
def alterKey(old_key, new_key):
  for session in Session.query(Session.user_key == old_key):
    session.user_key = new_key
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
' RETURNS
'   A dict containing the session and the entity corresponding
'   to the saved entity key property. If the session is being watched,
'   that is reflected in the returned dict's session object
' PUTS
'   1 - upon assigning a new SID if it expires
"""
def validate(UID, ULID, SID):
  if UID == None or ULID == None or SID == None:
    return SESSION_DOESNT_EXIST
  
  session = getSessionByTokens(UID, ULID)
  
  if session == None:
    return SESSION_DOESNT_EXIST
  
  sessionobj = SessionObject(UID, ULID, session.SID, session)
  entity = session.user_key.get()
  
  if session.watching:
    if SID in session.watchingTokens and len(session.watchingTokens) == 1:
      return HACKER_FOUND
    return dict(
      entity = entity,
      session = sessionobj
    )
  
  if session.SID != SID:
    session.watching = True
    session.watchingTokens.append(SID)
    session.watchingTokens.append(session.SID)
    session.put()
    return dict(
      entity = entity,
      session = sessionobj
    )
  
  sessionobj = SessionObject(UID, ULID, session.SID, session)
  
  import datetime
  now = datetime.datetime.now()
  if now > session.expiration:
    
    SID_Data = formSID()
    session.SID = SID_Data['SID']
    session.expiration = SID_Data['expiration']
    session.put()
    
    sessionobj.sid = session.SID
  
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
  '   Returns whether or not the sessino has been locked
  ' PARAMETERS
  '   None
  ' RETURNS
  '   Boolean
  """
  def isLocked(self):
    return self.__parent__.watching
  
  
  """
  ' PURPOSE
  '   Clears the current sid from a session. Indicates they
  '   aren't a hacker.
  ' PARAMETERS
  '   None
  ' RETURNS
  '   Nothing
  """
  def exonerate(self):
    session = self.__parent__
    if self.sid in session.watchingTokens:
      session.watchingTokens.remove(self.sid)
      session.put()
    
  
  
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
    if self.__uid__ == uid:
      return
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
    if self.__ulid__ == ulid:
      return
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
    if self.__sid__ == sid:
      return
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
  '   <Session sessoinentity>
  ' RETURNS
  '   <SessionObject session>
  """
  def __init__(self, uid, ulid, sid, sessionentity):
    self.__parent__ = sessionentity
    self.__uid__ = uid
    self.__ulid__ = ulid
    self.__sid__ = sid
  
  