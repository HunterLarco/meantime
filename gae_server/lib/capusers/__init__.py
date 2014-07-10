from .. import users





"""
' The Cap-User Entry Model For Easy Access
"""

from google.appengine.ext import ndb

class CapUser(ndb.Model):
  """Models an individual user entry."""
  points = ndb.IntegerProperty(indexed=False)








"""
' Error constants
"""
NOT_ENOUGH_PTS = 'CP0'









"""
' Recieves a user and amount of points to spend
' Uses those points, BUT DOES NOT SAVE THE ENTITY
' Returns error constant (NOT_ENOUGH_PTS)
"""
def spendPoints(user, amount):
  if user.points < amount:
    return NOT_ENOUGH_PTS
  
  user.points -= amount












"""
' Recieves a user and amount of points to spend
' Gives those points to the account, BUT DOES NOT SAVE THE ENTITY
' Returns nothing
"""
def transactPoints(user, amount):
  user.points += amount











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
  user.points = 0
  user.put()

  status = users.create(email,password,user)
  
  if status == users.EMAIL_IS_USED:
    return status