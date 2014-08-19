from .. import users

"""
' Common Package Imports
"""
from google.appengine.ext import ndb



class SealedUser(users.AuthUser.Model):
  def __init__(self, *args, **kwargs):
    super(SealedUser, self).__init__(*args, **kwargs)

  @classmethod
  def create(cls, email, password):
    user = super(SealedUser, cls).create(email, password)
    if not isinstance(user, cls):
      return user
    
    user.put()
    return user