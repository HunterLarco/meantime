import response
from ..users.handlers import AuthRequestHandler
from Engine import delegate
import Permissions

class APIHandler(AuthRequestHandler):

  class nosession:
    def default(cls, self, dictionary, method):
      self.setHeaders()
      self.RunGuest(dictionary, method)

  class nouser:
    def default(cls, self, dictionary, method):
      self.setHeaders()
      self.response.out.write(response.throw(203, compiled=True))

  class passlocked:
    def default(cls, self, dictionary, method):
      self.setHeaders()
      self.RunPassLockedUser(dictionary, method)
  
  class sessionlocked:
    def default(cls, self, dictionary, method):
      self.setHeaders()
      self.RunSessionLockedUser(dictionary, method)

  class hacker:
    def default(cls, self, dictionary, method):
      self.setHeaders()
      self.response.out.write(response.throw(002, compiled=True))

  class auth:
    def default(cls, self, dictionary, method):
      self.setHeaders()
      self.RunAuthUser(dictionary, method, additionalPayload={
        'setsession': True,
        'session': {
          'sid': self.sid
        }
      } if self.hasSID() else {})

  def RunSessionLockedUser(self, dictionary, method):
    delegate(self, dictionary, method, Permissions.SessionLockedUser, additionalPayload={'userlocked':True})

  def RunPassLockedUser(self, dictionary, method):
    delegate(self, dictionary, method, Permissions.PassLockedUser, additionalPayload={'userlocked':True})

  def RunGuest(self, dictionary, method):
    delegate(self, dictionary, method, Permissions.Guest)

  def RunAuthUser(self, dictionary, method, additionalPayload={}):
    delegate(self, dictionary, method, Permissions.AuthUser, additionalPayload=additionalPayload)

  def setHeaders(self):
    self.response.headers['Access-Control-Allow-Origin'] = '*'
    self.response.headers['Access-Control-Allow-Methods'] = 'PUT, OPTIONS'
    self.response.headers['Access-Control-Allow-Credentials'] = 'true'
    self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'

  def options(self, *args):
    self.response.headers['Content-Type'] = 'application/javascript'
    self.setHeaders()