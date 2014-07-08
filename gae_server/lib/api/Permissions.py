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
      from .. import users
      status = users.create(
        payload['email'],
        payload['password']
      )
      if status == users.EMAIL_IS_USED:
        return response.throw(200)
  
    @require('email', 'password')
    def login(self, payload):
      from .. import users
      status = users.login(
        payload['email'],
        payload['password']
      )
      if status == users.INCORRECT_LOGIN:
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
      
      
    def status(self, webapp2):
      from .. import users
      status = users.checkSession(webapp2)
      if status == users.sessions.WATCHING:
        return response.reply({'status' : 'sessions.watching'})
      elif status == users.sessions.SUCCESS:
        return response.reply({'status' : 'sessions.success'})
      elif status == users.sessions.SESSION_DOESNT_EXIST:
        return response.reply({'status' : 'sessions.session_doesnt_exist'})
      elif status == users.USER_DOESNT_EXIST:
        return response.reply({'status' : 'users.user_doesnt_exist'})
      elif status == users.USER_LOCKED:
        return response.reply({'status' : 'users.locked'})
      elif status == users.sessions.INCORRECT_SID:
        return response.reply({'status' : 'sessions.incorrect_sid'})
      else:
        return response.reply({'status' : 'unknown status'})



















# authenticated user map
class AuthUser:
  pass