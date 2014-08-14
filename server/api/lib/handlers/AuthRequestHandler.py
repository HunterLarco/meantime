from .. import users
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
      try:
        payload = ParseJSON(self.request.body)
        uid = payload['uid'] if 'uid' in payload else None
        sid = payload['sid'] if 'sid' in payload else None
        ulid = payload['ulid'] if 'ulid' in payload else None
      except:
        uid = None
        ulid = None
        sid = None
    
    if uid == None or ulid == None or sid == None:
      uid = self.request.cookies.get('uid') if self.request.cookies.get('uid') != '' else None
      ulid = self.request.cookies.get('ulid') if self.request.cookies.get('ulid') != '' else None
      sid = self.request.cookies.get('sid') if self.request.cookies.get('sid') != '' else None
    
    
    
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
  
  
  def get(self, *args, **kwargs):
    self.__route__(*args, **kwargs)
  def post(self, *args, **kwargs):
    self.__route__(*args, **kwargs)
  
  
  def logout(self):
    self.cookies.remove('UID')
    self.cookies.remove('ULID')
    self.cookies.remove('SID')
  
  
  def route(self, handle, *args, **kwargs):
    handle = getattr(self, handle, None)
    
    if handle == None:
      self.error(409)
      self.response.out.write('<h1>Error 404</h1><h2>Page Not Found</h2>')
      return
      
    #check manual override
    if hasattr(self, 'override'):
      status = self.override(*args, **kwargs)
      if not status:
        return
    
    method = getattr(handle, self.request.method.lower(), None)
    
    if callable(method):
      # bind the method to its parent class
      import types
      function = types.MethodType(method, handle(), handle)
      function(self, *args, **kwargs)
      return
    
    # call the default method
    default = getattr(handle, 'default', None)
    
    if not callable(default):
      self.error(405)
      self.response.out.write('<h1>Error 405</h1><h2>Method Not Allowed</h2>')
      return
    import types
    function = types.MethodType(default, handle(), handle)
    function(self, *args, **kwargs)
    
    
  def __route__(self, *args, **kwargs):
    if self.status == self.SESSION_DOESNT_EXIST:
      handle = 'nosession'
    elif self.status == self.USER_DOESNT_EXIST:
      handle = 'nouser'
    elif self.status == self.USER_LOCKED:
      handle = 'locked'
    elif self.status == self.HACKER_FOUND:
      handle = 'hacker'
    elif self.status == self.SUCCESS:
      handle = 'auth'
    self.route(handle, *args, **kwargs)
