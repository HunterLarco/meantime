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










class Cron:
  class get:
    def cleansessions(self, *args, **kwargs):
      from lib.users import sessions
      sessions.clean()
    
    def notifications(self, *args, **kwargs):
      from lib.sealeduser.messages import SealedMessage
      SealedMessage.sendNotifications()






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
  
  
  
  class user:
    @require('email', 'password')
    def signup(self, payload):
      from ..sealeduser.model import SealedUser
      user = SealedUser.create(payload['email'], payload['password']);
      if user == SealedUser.EMAIL_IS_USED:
        return response.throw(200)
      return response.reply({
        'setsession': True,
        'session': user.session.toDict(),
        'user': user.toDict()
      })
    
    @require('email', 'password')
    def login(self, payload):
      from ..sealeduser.model import SealedUser
      user = SealedUser.login(
        payload['email'],
        payload['password'],
        timezone = None if not 'timezone' in payload else payload['timezone']
      )
      if user == SealedUser.USER_DOESNT_EXIST:
        return response.throw(203)
      elif user == SealedUser.INCORRECT_LOGIN:
        return response.throw(201)
      elif user == SealedUser.BRUTE_SUSPECTED:
        return response.throw(202)
      else:
        return response.reply({
          'setsession': True,
          'session': user.session.toDict(),
          'user': user.toDict()
        })















# authenticated user map
class AuthUser:
  
  
  class feedback:
    @require('content', 'tags')
    def send(self, payload):
      user = payload['__Webapp2Instance__'].user
      from .. import feedback
      feedback.create(user, payload['content'], payload['tags'])
  
  
  
  class get:
    def message(self, webapp2instance):
      key = webapp2instance.request.get('key')
      user = webapp2instance.user
      message = user.getMessage(key)
      message.serve(webapp2instance)
      return False
  
  
  
  class user:
    
    @require('email')
    def setemail(self, payload):
      user = payload['__Webapp2Instance__'].user
      if user.changeEmail(payload['email']) == user.EMAIL_IS_USED:
        return response.throw(200)
    
    @require('name')
    def setname(self, payload):
      user = payload['__Webapp2Instance__'].user
      user.changeName(payload['name'])
    
    @require('mobile')
    def setmobile(self, payload):
      user = payload['__Webapp2Instance__'].user
      user.changePhone(payload['mobile'])
    
    def delete(self, payload):
      user = payload['__Webapp2Instance__'].user
      user.delete()
    
    @require('password', 'old_password')
    def changepassword(self, payload):
      user = payload['__Webapp2Instance__'].user
      worked = user.changePassword(payload['old_password'], payload['password'])
      if not worked:
        return response.throw(201)
      user.unlock()
    
  class messages:
    
    @require('uri', 'recipients', 'date')
    def send(self, payload):
      disappearing = payload['disappearing'] if 'disappearing' in payload else False
      user = payload['__Webapp2Instance__'].user
      contacts = user.sendMessage(
        payload['uri'],
        payload['recipients'],
        payload['date'],
        disappearing
      )
      return response.reply({
        'contacts': contacts
      })
    
    def get(self, payload):
      user = payload['__Webapp2Instance__'].user
      return response.reply({
        'messages': user.getMessages(json=True)
      })
      
        





class PassLockedUser:
  class user:
    def unlock(self, payload):
      user = payload['__Webapp2Instance__'].user
      user.unlock()
      return response.reply({'passlocked':False})
    
    @require('password', 'old_password')
    def changepassword(self, payload):
      user = payload['__Webapp2Instance__'].user
      worked = user.changePassword(payload['old_password'], payload['password'])
      if not worked:
        return response.throw(201)
      user.unlock()
      return response.reply({'passlocked':False})





class SessionLockedUser:
  class user:
    @require('email', 'password')
    def unlock(self, payload):
      user = payload['__Webapp2Instance__'].user
      status = user.unlockSession(
        payload['email'],
        payload['password']
      )
      if status == user.INCORRECT_LOGIN:
        return response.throw(201)
      else:
        return response.reply({
          'setsession': True,
          'session': user.session.toDict()
        })
      
      
      
      
      