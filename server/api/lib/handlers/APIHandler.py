from .. import api
from AuthRequestHandler import AuthRequestHandler

class APIHandler(AuthRequestHandler):
  
  class nosession:
    def default(cls, self, dictionary, method):
      self.setHeaders()
      self.RunGuest(dictionary, method)
  
  class nouser:
    def default(cls, self, dictionary, method):
      self.setHeaders()
      self.response.out.write(api.response.throw(203, compiled=True))
  
  class locked:
    def default(cls, self, dictionary, method):
      self.setHeaders()
      self.RunLockedUser(dictionary, method)
  
  class hacker:
    def default(cls, self, dictionary, method):
      self.setHeaders()
      self.response.out.write(api.response.throw(002, compiled=True))
  
  class auth:
    def default(cls, self, dictionary, method):
      self.setHeaders()
      self.RunAuthUser(dictionary, method, additionalPayload={
        'setsession': True,
        'session': {
          'sid': self.sid
        }
      } if self.hasSID() else {})
      
  def RunLockedUser(self, dictionary, method):
    api.delegate(self, dictionary, method, api.Permissions.LockedUser, additionalPayload={'userlocked':True})
  
  def RunGuest(self, dictionary, method):
    
    api.delegate(self, dictionary, method, api.Permissions.Guest)

  def RunAuthUser(self, dictionary, method, additionalPayload={}):
    api.delegate(self, dictionary, method, api.Permissions.AuthUser, additionalPayload=additionalPayload)
    
  def setHeaders(self):
    self.response.headers['Access-Control-Allow-Origin'] = '*'
    self.response.headers['Access-Control-Allow-Methods'] = 'PUT, OPTIONS'
    self.response.headers['Access-Control-Allow-Credentials'] = 'true'
    self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    
  def options(self, *args):  
    self.response.headers['Content-Type'] = 'application/javascript'
    self.setHeaders()