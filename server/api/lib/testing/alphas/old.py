"""
' Common Package Imports
"""
from google.appengine.ext import ndb


"""
' Error Constants
"""
EMAIL_IS_USED = 'AU0'
TOKEN_DOESNT_EXIST = 'AU1'
TOKEN_EXPIRED = 'AU2'


"""
' A AlphaUser entity, keeps track of signed up users via email
"""
class AlphaUser(ndb.Model):
  email = ndb.StringProperty(indexed=True)
  token = ndb.StringProperty(indexed=True)
  token_expiration = ndb.IntegerProperty(indexed=False)
  user = ndb.KeyProperty(indexed=False)
  
  
  """
  ' PURPOSE
  '   Generates a token that can be used to grant access on the behalf
  '   of this user from an email link. It renders all prior tokens useless.
  ' PARAMETERS
  '   None
  ' RETURNS
  '   The token
  ' PUTS
  '   1 ~ on token creation
  """
  def formEmailToken(self):
    from hashlib import sha256
    self.token = sha256(self.email+self.key()).hexdigest()
    
    import datetime
    self.token_expiration = datetime.datetime.now() + datetime.timedelta(days=14)
    
    self.put()
      
    return self.token


"""
' PURPOSE
'   Using an email token, get the corresponding AlphaUser entity.
' PARAMETERS
'   <String token>
' RETURNS
'   The AlphaUser entity
' ERRORS
'   TOKEN_DOESNT_EXIST
'   TOKEN_EXPIRED
' PUTS
'   1 ~ if a token is expired, it is removed
"""
def getByToken(token):
  user = AlphaUser.query(AlphaUser.token == token)
  
  if user == None:
    return TOKEN_DOESNT_EXIST
  
  import datetime
  if user.token_expiration < datetime.datetime.now():
    user.token = None
    user.put()
    return TOKEN_EXPIRED
  
  return user


"""
' PURPOSE
'   Returns a list of all AlphaUser entities
' PARAMETERS
'   None
' RETURNS
'   list of all AlphaUser entitites
"""
def all():
  return AlphaUser.query()


"""
' PURPOSE
'   Lists all signup up alpha users' emails so that a group message can be sent out
' PARAMETERS
'   None
' RETURNS
'   list of all alpha emails
"""
def list():
  users = AlphaUser.query()
  emails = []
  for user in users:
    emails.append(user.email)
  return emails


"""
' PURPOSE
'   Given an email, create a new alpha tester
' PARAMETERS
'   <String email>
'   <bool **kwarg sendEmail>
' RETURNS
'   Nothing
' PUTS
'   1 ~ On user creation
' ERRORS
'   EMAIL_IS_USED
' NOTES
'   By default sends a welcome email to the user, this can be
'   changed by the 'sendEmail' kwarg.
"""
def create(email, sendEmail=True):
  user = AlphaUser.query(AlphaUser.email == email).get()
  
  if user != None:
    return EMAIL_IS_USED
  
  user = AlphaUser()
  user.email = email
  user.put()
  
  if sendEmail:
    sendWelcomeEmail(user)


"""
' PURPOSE
'   Sends a welcoming email to a specified user welcoming them
'   to Sealed and tells them we will contact them shortly
' PARAMETERS
'   <AlphaUser user>
' RETURNS
'   Nothing
' NOTES
'   Sends an email
"""
def sendWelcomeEmail(user):
  import os
  from google.appengine.ext.webapp import template
  from google.appengine.api import mail
  
  message = mail.EmailMessage(sender="Sealed Team <admin@trysealed.com>",
                              subject="Thanks for trying Sealed!")
  message.to = user.email
  message.body = template.render(os.path.join(os.path.dirname(__file__), 'emails/welcome/email.txt'),  {})
  message.html = template.render(os.path.join(os.path.dirname(__file__), 'emails/welcome/email.html'), {})
  message.send()