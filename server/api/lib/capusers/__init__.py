"""
' Common Package Imports
"""
from .. import users
from .. import shards
from google.appengine.ext import ndb


"""
' Error Constants
"""
NOT_ENOUGH_PTS = 'CP0'


# -------------------------------------------------------- START OF ENTITY -------------------------------------------------------- #


"""
' PURPOSE
'   Contains all the relevant data for a 'meantime' user.
' NOTES
'   The name 'CapUser' comes from the original name for the
'   app, 'TimeCap'.
"""
class CapUser(ndb.Model):
  
  """
  ' PURPOSE
  '   Returns the shard counter used to count the points for the user.
  ' PARAMETERS
  '   None
  ' RETURNS
  '   A 'DynamicCounter' instance from ../shards/__init__.py
  """
  def getPointsCounter(self):
    return shards.getOrCreate(str(self.key),
           namespace=self.__class__.__name__+'_PointShards')


  """
  ' PURPOSE
  '   Returns the current value of the shard counter for this user's points.
  ' PARAMETERS
  '   None
  ' RETURNS
  '   int
  """
  def getPoints(self):
    return self.getPointsCounter().getValue()


  """
  ' PURPOSE
  '   Adds points to the points shard counter.
  ' PARAMETERS
  '   <int amount>
  ' RETURNS
  '   Nothing
  """
  def addPoints(self, amount):
    counter = self.getPointsCounter()
    counter.add(amount)


  """
  ' PURPOSE
  '   Removes points from the points shard counter.
  '   Also checks if the proper amount of points exists.
  ' PARAMETERS
  '   <int amount>
  ' ERRORS
  '   NOT_ENOUGH_PTS
  ' RETURNS
  '   Nothing
  """
  def spendPoints(self, amount):
    counter = self.getPointsCounter()
    if counter.getValue() < amount:
      return NOT_ENOUGH_PTS
    counter.add(-amount)
  
  
  
  """
  ' PURPOSE
  '   Creates a capsule for this user; using the user as the parent entity
  '   for the capsule.
  ' PARAMETERS
  '   <BlobKey clue>
  '   <BlobKey content>
  '   <String clue_answer>
  ' RETURNS
  '   Nothing
  """
  def createCapsule(self, content):
    from ..caps import Capsule
    cap = Capsule(parent=self.key)
    cap.content = content
    cap.put()


# -------------------------------------------------------- END OF ENTITY -------------------------------------------------------- #


"""
' PURPOSE
'   Logs in a user
' PARAMETERS
'   <String email>
'   <String password>
' RETURNS
'   * see ../users/__init__.py (login)
"""
def login(email, password):
  return users.login(email, password)


"""
' PURPOSE
'   Creates a new user
' PARAMETERS
'   <String email>
'   <String password>
' ERRORS
'   from ../users/__init__.py (EMAIL_IS_USED)
' RETURNS
'   uid, sid, and ulid upon successful creation (auto logs in basically)
' PUTS
'   2 - to create the CapUser
'     - to delete the CapUser if the email is used
"""
def create(email, password):
  user = CapUser()
  user.put()

  status = users.create(email,password,user)
  
  if status == users.EMAIL_IS_USED:
    user.key.delete()
    return status
  
  return status