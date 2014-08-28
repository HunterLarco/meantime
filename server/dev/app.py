from google.appengine.ext.webapp import template
import webapp2
import os
from lib import api
from lib.users.handlers import AuthRequestHandler


class MainHandler(AuthRequestHandler):
  def render(self, name):
    import json
    template_values = {
      'user': json.dumps(self.user.toDict() if self.user != None else None)
    }
    # render
    path = os.path.join(os.path.dirname(__file__), 'main.html')
    self.response.out.write(template.render(path, template_values))
  
  class nouser:
    def get(cls, self):
      self.route('nosession')
  
  class hacker:
    def get(cls, self):
      self.response.out.write('We think you\'re a hacker. If not, contact us to continue service with Sealed.')
  
  class sessionlocked:
    def get(cls, self):
      self.render('sessionlocked')
  
  class passlocked:
    def get(cls, self):
      self.render('passlocked')
  
  class nosession:
    def get(cls, self):
      self.render('signup')
  
  class auth:
    def get(cls, self):
      self.render('inbox')


app = webapp2.WSGIApplication([
                ('/api/([^/]+)/([^/]+)/?', api.handler),
                ('/.*', MainHandler)
              ], debug=True)
