from google.appengine.ext.webapp import template
import webapp2
import os


from lib import handlers
from lib import api


class MainHandler(handlers.AuthRequestHandler, handlers.CookieHandler):
  
  def override(self):
    return True
    from lib.testing.alphas import constants
    if not constants.alpha_testing_open:
      template_values = {}
      path = os.path.join(os.path.dirname(__file__), 'notopen.html')
      self.response.out.write(template.render(path, template_values))
      return False
    return True
      
  
  class nosession:
    def get(cls, self):
      template_values = {}
      path = os.path.join(os.path.dirname(__file__), 'signin.html')
      self.response.out.write(template.render(path, template_values))
  
  class nouser:
    def get(cls, self):
      self.logout()
      self.route('nosession')
  
  class locked:
    def get(cls, self):
      template_values = {}
      path = os.path.join(os.path.dirname(__file__), 'locked.html')
      self.response.out.write(template.render(path, template_values))
  
  class hacker:
    def get(cls, self):
      self.response.out.write('We think you\'re a hacker. If not, contact us to continue service with Sealed.')
  
  class auth:
    def get(cls, self):
      template_values = {}
      path = os.path.join(os.path.dirname(__file__), 'emulator.html')
      self.response.out.write(template.render(path, template_values))
      





app = webapp2.WSGIApplication([
                ('/api/([^/]+)/([^/]+)/?', handlers.APIHandler),
                ('/.*', MainHandler)
              ], debug=True)
