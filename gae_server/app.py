from lib import users
from lib import api
from lib.caps import uploader

import webapp2








class AuthRequestHandler(webapp2.RequestHandler):
  SESSION_DOESNT_EXIST = users.sessions.SESSION_DOESNT_EXIST
  USER_DOESNT_EXIST = users.USER_DOESNT_EXIST
  USER_LOCKED = users.USER_LOCKED
  HACKER_FOUND = users.sessions.HACKER_FOUND
  SUCCESS = 'auth_router_success'
  
  status = None
  sid = None
  
  
  def __init__(self, *args, **kwargs):
    super(AuthRequestHandler, self).__init__(*args, **kwargs)
    
    from json import loads as ParseJSON
    
    if self.request.method == 'GET':
      uid = None
      sid = None
      ulid = None
    else:
      payload = ParseJSON(self.request.body)
      uid = payload['uid'] if 'uid' in payload else None
      sid = payload['sid'] if 'sid' in payload else None
      ulid = payload['ulid'] if 'ulid' in payload else None
    
    status = users.checkSession(uid, ulid, sid)
    
    if  (status == self.SESSION_DOESNT_EXIST or
         status == self.USER_DOESNT_EXIST    or
         status == self.USER_LOCKED          or
         status == self.HACKER_FOUND)         :
       self.status = status
       return
    
    self.status = self.SUCCESS
    
    if status == None:
      return
    
    self.sid = status
  
  def hasSID(self):
    return self.sid != None
    
    
    
    
    
  





"""
' Get requests always run through Guest permissions
' Throws errors 203 and 204 and those from Permissions
"""
class APIHandler(AuthRequestHandler):
  def route(self, *args):
    if self.status == self.SESSION_DOESNT_EXIST:
      self.RunGuest(*args)
    elif self.status == self.USER_DOESNT_EXIST:
      self.response.out.write(api.response.throw(203, compiled=True))
    elif self.status == self.USER_LOCKED:
      self.RunLockedUser(*args)
    elif self.status == self.HACKER_FOUND:
      self.response.out.write(api.response.throw(002, compiled=True))
      # TODO, stop them
    elif self.status == self.SUCCESS:
      self.RunAuthUser(*args, additionalPayload={
        'setsession': True,
        'session': {
          'sid': self.sid
        }
      } if self.hasSID() else {})
    else:
      self.response.out.write(api.response.throw(000, compiled=True))
  
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
                ('/api/([^/]+)/([^/]+)/?',         APIHandler),
                ('/api/admin/([^/]+)/([^/]+)/?',   AdminAPIHandler),
                ('/data/upload/?',                 uploader.UploadHandler),
                ('/data/(.*)/?',                   uploader.DownloadHandler),
                ('/.*',                            MainHandler)
              ], debug=True)
