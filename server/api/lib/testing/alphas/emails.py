"""
' Common Package Imports
"""
from ...shards import List
import emailclient


"""
' Error Constants
"""
EMAIL_IS_USED = 'AEL0'


"""
' PURPOSE
'   Remove an Alpha Tester from testing
' PARAMETERS
'   <String email>
' RETURNS
'   Nothing
"""
def remove(email):
  List.getOrCreate('list', namespace='alphas').run('remove', email)
  
  import users
  users.delete(email)


"""
' PURPOSE
'   Add a alpha tester's email to the list and creates a new account for them
' PARAMETERS
'   <String email>
' ERRORS
'   EMAIL_IS_USED
' RETURNS
'   NOTHING
"""
def add(email):
  if email in all():
    return EMAIL_IS_USED
  List.getOrCreate('list', namespace='alphas').run('add', email)
  
  import users
  users.create(email)
  
  emailclient.send(email, 'welcome')


"""
' PURPOSE
'   Returns a list of all emails thus far
' PARAMETERS
'   None
' RETURNS
'   The list of alpha tester emails
"""
def all():
  return List.getOrCreate('list', namespace='alphas').getValue()