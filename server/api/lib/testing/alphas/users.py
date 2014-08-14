"""
' Common Package Imports
"""
from google.appengine.ext import ndb
from ... import users



class AlphaUser(users.AbstractUser):
  
  opened = ndb.BooleanProperty(indexed=True)
  
  def __init__(self, *args, **kwargs):
    super(AlphaUser, self).__init__(*args, **kwargs)




"""
' PURPOSE
'   Creates a new alpha user a placeholder as the password.
'   The password will be set when access is granted for the
'   First time. The password will be bypassed and a new one
'   Set by the user.
' PARAMETERS
'   <String email>
' ERRORS
'   from .../users/__init__.py (EMAIL_IS_USED)
' RETURNS
'   Nothing
' PUTS
'   1 - to create the new AlphaUser entity
"""
def create(email):
  user = AlphaUser()
  user.opened = False
  user.put()
  
  status = users.create(email, 'password', user)
  
  if status == users.EMAIL_IS_USED:
    return status
  
  import constants
  if constants.alpha_testing_open:
    openAccount(user)



def delete(email):
  user = users.getUserByEmail(email)
  if user == None:
    return
  
  user.delete()



def openAccount(user):
  from hashlib import sha256
  import random
  password = sha256(str(random.random())).hexdigest()
  
  user.setPassword(password)
  
  user.opened = True
  user.put()
  
  import emailclient
  emails.send(user.email(), 'openaccount', {
    'password': password
  })
  
  return password



