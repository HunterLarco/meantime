import response
from ..users.handlers import AuthRequestHandler
from Engine import delegate
import Permissions

class APIHandler(AuthRequestHandler):
  
  def override(self, *args, **kwargs):
    self.setHeaders()

  class nosession:
    def default(cls, self, dictionary, method):
      self.RunGuest(dictionary, method)

  class nouser:
    def default(cls, self, dictionary, method):
      self.response.out.write(response.throw(203, compiled=True))

  class passlocked:
    def default(cls, self, dictionary, method):
      self.RunPassLockedUser(dictionary, method)
  
  class sessionlocked:
    def default(cls, self, dictionary, method):
      self.RunSessionLockedUser(dictionary, method)

  class hacker:
    def default(cls, self, dictionary, method):
      self.response.out.write(response.throw(002, compiled=True))

  class auth:
    def default(cls, self, dictionary, method):
      self.RunAuthUser(dictionary, method)

  def RunSessionLockedUser(self, dictionary, method):
    additionalPayload = {
      'setsession': True,
      'session': self.user.session.toDict()
    } if self.user.session.changed else {}
    additionalPayload['sesslocked'] = True
    delegate(self, dictionary, method, Permissions.SessionLockedUser, additionalPayload=additionalPayload)

  def RunPassLockedUser(self, dictionary, method):
    additionalPayload = {
      'setsession': True,
      'session': self.user.session.toDict()
    } if self.user.session.changed else {}
    additionalPayload['passlocked'] = True
    delegate(self, dictionary, method, Permissions.PassLockedUser, additionalPayload=additionalPayload)

  def RunGuest(self, dictionary, method):
    delegate(self, dictionary, method, Permissions.Guest)

  def RunAuthUser(self, dictionary, method):
    delegate(self, dictionary, method, Permissions.AuthUser, additionalPayload={
      'setsession': True,
      'session': self.user.session.toDict()
    } if self.user.session.changed else {})

  def setHeaders(self):
    self.response.headers['Access-Control-Allow-Origin'] = '*'
    self.response.headers['Access-Control-Allow-Methods'] = 'PUT, OPTIONS'
    self.response.headers['Access-Control-Allow-Credentials'] = 'true'
    self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'

  def options(self, *args):
    self.response.headers['Content-Type'] = 'application/javascript'
    self.setHeaders()