import webapp2

from lib import api


class CronAPI(webapp2.RequestHandler):
  def get(self, method):
    api.delegate(self, 'get', method, api.Permissions.Cron)
  def post(self, dictionary, method):
    api.delegate(self, 'get', method, api.Permissions.Cron)



app = webapp2.WSGIApplication([
      ('/cron/([^/]+)/?',   CronAPI)
  ], debug=True)