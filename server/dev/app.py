from google.appengine.ext.webapp import template
import webapp2
import os
from lib import api
from lib.users.handlers import AuthRequestHandler


class MainHandler(AuthRequestHandler):
  def render(self, name, header_visible=False):
    # check first visit cookie
    if self.request.cookies.get('firstvisit') != 'done' and self.user == None:
      name = 'firstvisit'
      header_visible = False
    # generate template values
    gone = 'opaque gone'
    template_values = {
      'visibility': {
        'inbox': gone,
        'signup': gone,
        'passlocked': gone,
        'sessionlocked': gone,
        'header': gone,
        'firstvisit': gone
      }
    }
    # set visibility for css
    if name in template_values['visibility']:
      template_values['visibility'][name] = ''
    if header_visible:
      template_values['visibility']['header'] = ''
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
      self.render('inbox', header_visible=True)


app = webapp2.WSGIApplication([
                ('/api/([^/]+)/([^/]+)/?', api.handler),
                ('/.*', MainHandler)
              ], debug=True)
