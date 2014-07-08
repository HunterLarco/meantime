from lib import users
from lib import api

import webapp2


class APIHandler(webapp2.RequestHandler):
  def post(self, dictionary, method):
    api.delegate(self, dictionary, method, api.Permissions.Guest)
  def get(self, dictionary, method):
    api.delegate(self, dictionary, method, api.Permissions.Guest)


class TestHandler(webapp2.RequestHandler):
  def get(self):
    status = users.checkSession(self)
    if status == users.sessions.WATCHING:
      self.response.out.write('watching')
    elif status == users.sessions.SUCCESS:
      self.response.out.write('success')
    elif status == users.sessions.SESSION_DOESNT_EXIST:
      self.response.out.write('session doesn\'t exist')
    elif status == users.USER_DOESNT_EXIST:
      self.response.out.write('user doesn\'t exist')
    elif status == users.USER_LOCKED:
      self.response.out.write('user locked')
    else:
      self.response.out.write('failure')



class MainHandler(webapp2.RequestHandler):
  def run(self):
    self.response.headers['Content-Type'] = "application/javascript"
    self.response.out.write(api.response.throw(003, compiled=True))
  def get(self):
    self.run()
  def post(self):
    self.run()



app = webapp2.WSGIApplication([
                ('/api/([^/]+)/([^/]+)/?', APIHandler),
                ('/.*', MainHandler)
              ], debug=True)
