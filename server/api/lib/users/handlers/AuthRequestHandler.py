from .. import AuthUser
from CookieHandler import CookieHandler


"""
' NOTES
'   The passlocked handler is called when brute force is suspected and the client is logged in
"""
class AuthRequestHandler(CookieHandler):
  
  
  SESSION_DOESNT_EXIST = 'AuthRequestHandler0'
  HACKER_FOUND         = 'AuthRequestHandler1'
  SESSION_LOCKED       = 'AuthRequestHandler2'
  PASSWORD_LOCKED      = 'AuthRequestHandler3'
  USER_DOESNT_EXIST    = 'AuthRequestHandler4'
  SUCCESS              = 'AuthRequestHandler5'

  
  __userclass__ = AuthUser.Model
  status = None
  user = None


  @staticmethod
  def SetUserClass(usercls):
    def runner(cls):
      cls.__userclass__ = usercls
      return cls
    return runner


  def __init__(self, *args, **kwargs):
    super(AuthRequestHandler, self).__init__(*args, **kwargs)
    
    # attempt to get session tokens from the request body
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
    
    # get from cookies if none exist in the request body
    if uid == None or ulid == None or sid == None:
      uid = self.cookies.get('uid') if self.cookies.get('uid') != '' else None
      ulid = self.cookies.get('ulid') if self.cookies.get('ulid') != '' else None
      sid = self.cookies.get('sid') if self.cookies.get('sid') != '' else None
    
    user = self.__userclass__.getBySession(uid, ulid, sid)
    errorstatus = None
    
    if user == self.__userclass__.SESSION_DOESNT_EXIST:
      errorstatus = self.SESSION_DOESNT_EXIST
      
    if user == self.__userclass__.USER_DOESNT_EXIST:
      errorstatus = self.USER_DOESNT_EXIST
    
    if user == self.__userclass__.HACKER_FOUND:
      errorstatus = self.HACKER_FOUND
    
    if errorstatus != None:
      self.status = errorstatus
      return
    
    self.user = user
    
    if self.user.session.changed:
      self.cookies.set('uid', self.user.session.uid)
      self.cookies.set('ulid', self.user.session.ulid)
      self.cookies.set('sid', self.user.session.sid)
    
    if user.isLocked():
      errorstatus = self.PASSWORD_LOCKED
      
    if user.session.isLocked():
      errorstatus = self.SESSION_LOCKED
    
    if errorstatus != None:
      self.status = errorstatus
      return
    
    self.status = self.SUCCESS
    
    
  def get(self, *args, **kwargs):
    self.__route__(*args, **kwargs)
  def post(self, *args, **kwargs):
    self.__route__(*args, **kwargs)
  

  def route(self, handle, *args, **kwargs):
    handle = getattr(self, handle, None)

    if handle == None:
      self.error(409)
      self.response.out.write('<h1>Error 404</h1><h2>Page Not Found</h2>')
      return

    #check manual override
    if hasattr(self, 'override'):
      status = self.override(*args, **kwargs)
      if not status and status != None:
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
    elif self.status == self.PASSWORD_LOCKED:
      handle = 'passlocked'
    elif self.status == self.SESSION_LOCKED:
      handle = 'sessionlocked'
    elif self.status == self.HACKER_FOUND:
      handle = 'hacker'
    elif self.status == self.SUCCESS:
      handle = 'auth'
    self.route(handle, *args, **kwargs)
    
    









