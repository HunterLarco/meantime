from .. import users
from .. import shards





"""
' The Cap-User Entry Model For Easy Access
"""

from google.appengine.ext import ndb

class CapUser(ndb.Model):
  """Models an individual user entry."""
  
  def getPointsCounter(self):
    return shards.getOrCreate(str(self.key),
           namespace=self.__class__.__name__+'_PointShards')

  def getPoints(self):
    return self.getPointsCounter().getValue()

  def addPoints(self, amount):
    counter = self.getPointsCounter()
    counter.add(amount)

  def spendPoints(self, amount):
    counter = self.getPointsCounter()
    if counter.getValue() < amount:
      return NOT_ENOUGH_PTS
    counter.add(-amount)



  







"""
' Error constants
"""
NOT_ENOUGH_PTS = 'CP0'














"""
' Recieves an email and password
' Logs in the user
' See delegated method for returns
"""
def login(email, password):
  return users.login(email, password)















"""
' Recieves an email and a password
' Creates a user
' Returns error constant
'     from ../users/__init__.py (EMAIL_IS_USED)
"""
def create(email, password):
  user = CapUser()
  user.put()

  status = users.create(email,password,user)
  
  if status == users.EMAIL_IS_USED:
    return status