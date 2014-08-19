from lib import api
from lib.caps import uploader

import webapp2
import os
from google.appengine.ext.webapp import template


class MainHandler(webapp2.RequestHandler):
  def get(self):
    gateway = self.request.get('gateway');
    template_values = {
      'gateway': 'http://api.capaching.appspot.com/' if gateway == None or gateway == '' else gateway
    }
    self.response.headers['Content-Type'] = "application/javascript"
    path = os.path.join(os.path.dirname(__file__), 'resources/Request.js')
    self.response.out.write(template.render(path, template_values))
    


app = webapp2.WSGIApplication([
                ('/([^/]+)/([^/]+)/?',         api.handler),
                ('/data/upload/?',             uploader.UploadHandler),
                ('/data/(.*)/?',               uploader.DownloadHandler),
                ('.*',                         MainHandler)
              ], debug=True)
