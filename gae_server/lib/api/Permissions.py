# common imports
import response


### within this file, each root class defines what API functions are accessible by POST or GET. that way permission may be changed by simply instruction the API engine to delegate to a different permission map. For example, 'admin' indicates that api url '/api/constants/add' allows one to add a constant to the database, because a user doesn't have this privilage, their permission map lacks this ability. Note that GET requests must use the get dictionary exclusively








def require(*keys):
  def decorator(funct):
    def reciever(self, payload):
      for key in keys:
        if not key in payload:
          return response.throw(001)
      return funct(self, payload)
    return reciever
  return decorator







# guest access map
class Guest:
  class user:
    @require('email', 'password')
    def signup(self, payload):
      from .. import capusers
      from .. import users
      status = capusers.create(
        payload['email'],
        payload['password'],
      )
      if status == users.EMAIL_IS_USED:
        return response.throw(200)
  
  
    @require('email', 'password')
    def login(self, payload):
      from .. import users
      from .. import capusers
      status = capusers.login(
        payload['email'],
        payload['password']
      )
      if status == users.USER_DOESNT_EXIST:
        return response.throw(203)
      elif status == users.INCORRECT_LOGIN:
        return response.throw(201)
      elif status == users.BRUTE_SUSPECTED:
        return response.throw(202)
      else:
        return response.reply({
          'setsession': True,
          'session': status
        })




  
  class get:
    def version(self, webapp2):
      return response.reply({
        'version' : '0.0.0 Beta'
      })















# authenticated user map
class AuthUser:
  class points:
    pass









class LockedUser:
  class user:
    @require('email', 'password')
    def login(self, payload):
      from .. import users
      from .. import capusers
      status = capusers.login(
        payload['email'],
        payload['password']
      )
      if status == users.USER_DOESNT_EXIST:
        return response.throw(203)
      elif status == users.INCORRECT_LOGIN:
        return response.throw(201)
      elif status == users.BRUTE_SUSPECTED:
        return response.throw(202)
      else:
        users.sessions.clearWatchingSID(
          payload['uid'],
          payload['ulid'],
          payload['sid']
        )
        return response.reply({
          'setsession': True,
          'session': status,
          'userlocked': False
        })
      
      
      
      
      