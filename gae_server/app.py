from lib import users
from lib import api

import webapp2


"""
' Get requests always run through Guest permissions
' Throws errors 203 and 204 and those from Permissions
"""
class APIHandler(webapp2.RequestHandler):
  def route(self, *args):
    from json import loads as ParseJSON
    payload = ParseJSON(self.request.body)
    uid = payload['uid'] if 'uid' in payload else None
    sid = payload['sid'] if 'sid' in payload else None
    ulid = payload['ulid'] if 'ulid' in payload else None
    status = users.checkSession(uid, ulid, sid)
    if status == users.sessions.SESSION_DOESNT_EXIST:
      self.RunGuest(*args)
    elif status == users.USER_DOESNT_EXIST:
      self.response.out.write(api.response.throw(203, compiled=True))
    elif status == users.USER_LOCKED:
      self.RunLockedUser(*args)
    elif status == users.sessions.HACKER_FOUND:
      self.response.out.write(api.response.throw(002, compiled=True))
      # TODO, stop them
    else:
      if status == None:
        self.RunAuthUser(*args)
      else:
        self.RunAuthUser(*args, additionalPayload={
          'setsession': True,
          'session': {
            'sid': status
          }
        })
  
  def RunLockedUser(self, dictionary, method):
    api.delegate(self, dictionary, method, api.Permissions.LockedUser, additionalPayload={'userlocked':True})
  
  def RunGuest(self, dictionary, method):
    api.delegate(self, dictionary, method, api.Permissions.Guest)

  def RunAuthUser(self, dictionary, method, additionalPayload={}):
    api.delegate(self, dictionary, method, api.Permissions.AuthUser, additionalPayload=additionalPayload)
      
  def post(self, *args):
    self.route(*args)
  def get(self, dictionary, method):
    self.RunGuest(dictionary, method)





"""
' Throws error 003
"""
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
