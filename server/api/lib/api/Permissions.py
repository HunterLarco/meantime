# common imports
import response


### within this file, each root class defines what API functions are accessible by POST or GET. that way permission may be changed by simply instruction the API engine to delegate to a different permission map. For example, 'admin' indicates that api url '/constants/add' allows one to add a constant to the database, because a user doesn't have this privilage, their permission map lacks this ability. Note that GET requests must use the get dictionary exclusively








def require(*keys):
  def decorator(funct):
    def reciever(self, payload):
      for key in keys:
        if not key in payload:
          return response.throw(001)
      return funct(self, payload)
    return reciever
  return decorator











class Admin:
  class alphas:
    def list(self, payload):
      from ..testing.alphas import emails
      return response.reply({
        'list': emails.all()
      })
    @require('email')
    def remove(self, payload):
      from ..testing.alphas import emails
      emails.remove(payload['email'])
      return response.reply()
      
  class shards:
    @require('name')
    def profile(self, payload):
      from ..shards import Integer
      return response.reply(Integer.getOrCreate(payload['name']).profile());
    
    @require('name')
    def increment(self, payload):
      from ..shards import Integer
      Integer.getOrCreate(payload['name']).run('add', 1)
    
    @require('name')
    def get(self, payload):
      from ..shards import Integer
      return response.reply({
        'value': Integer.getOrCreate(payload['name']).getValue()
      })













# guest access map
class Guest:
  class alpha:
    @require('email')
    def signup(self, payload):
      from ..testing.alphas import emails
      status = emails.add(payload['email'])
      if status == emails.EMAIL_IS_USED:
        return response.throw(200)
    
    @require('email', 'password')
    def login(self, payload):
      from .. import users
      from ..testing.alphas.users import AlphaUser
      user = AlphaUser.login(
        payload['email'],
        payload['password']
      )
      if user == AlphaUser.USER_DOESNT_EXIST:
        return response.throw(203)
      elif user == AlphaUser.INCORRECT_LOGIN:
        return response.throw(201)
      elif user == AlphaUser.BRUTE_SUSPECTED:
        return response.throw(202)
      else:
        return response.reply({
          'setsession': True,
          'session': user.session.toDict()
        })















# authenticated user map
class AuthUser:
  class upload:
    def geturl(self, payload):
      from .. import caps
      return response.reply({
        'url': caps.uploader.getUrl()
      })
        





class PassLockedUser:
  class alpha:
    def unlock(self, payload):
      user = payload['__Webapp2Instance__'].user
      if user == None:
        return response.throw(203)
      user.unlock()
    
    @require('password', 'old_password')
    def changepassword(self, payload):
      user = payload['__Webapp2Instance__'].user
      if user == None:
        return response.throw(203)
      worked = user.changePassword(payload['old_password'], payload['password'])
      if not worked:
        return response.throw(201)
      user.unlock()





class SessionLockedUser:
  class alpha:
    @require('email', 'password')
    def login(self, payload):
      from ..testing.alphas.users import AlphaUser
      
      user = payload['__Webapp2Instance__'].user
      if user == None:
        return response.throw(203)
      
      status = user.unlockSession(
        payload['email'],
        payload['password']
      )
      
      if status == AlphaUser.INCORRECT_LOGIN:
        return response.throw(201)
      else:
        return response.reply({
          'setsession': True,
          'session': user.session.toDict(),
          'userlocked': False
        })
      
      
      
      
      