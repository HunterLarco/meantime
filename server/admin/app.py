import webapp2

import os
from google.appengine.ext.webapp import template

from lib import api


class AdminAPIHandler(webapp2.RequestHandler):
  def run(self, dictionary, method):
    from google.appengine.api import users

    user = users.get_current_user()

    if user and users.is_current_user_admin():
      api.delegate(self, dictionary, method, api.Permissions.Admin)
      return
        
    self.response.headers['Content-Type'] = "application/javascript"
    self.response.out.write(api.response.throw(002, compiled=True))
  def get(self, dictionary, method):
    self.run(dictionary, method)
  def post(self, dictionary, method):
    self.run(dictionary, method)



app = webapp2.WSGIApplication([
      ('/([^/]+)/([^/]+)/?',   AdminAPIHandler),
      ('/api/([^/]+)/([^/]+)/?',   api.handler)
  ], debug=True)