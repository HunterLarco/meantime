import webapp2

class CookieWorker():
  
  
  DEFAULT_EXPIRATION = 60*60*24*30# one month
  
  
  def __init__(self, Webapp2Instance):
    self.webapp2instance = Webapp2Instance
  
  
  def get(self, name):
    string = self.webapp2instance.request.cookies.get(name)
    if string == '':
      return None
    return string


  def set(self, name, string, seconds=None):
    if seconds == None:
      seconds = self.DEFAULT_EXPIRATION
    from Cookie import SimpleCookie
    import datetime
    cookie = SimpleCookie()
    cookie[name] = string
    cookie[name]["path"] = "/"
    cookie[name]["expires"] = (datetime.datetime.now()+datetime.timedelta(seconds=seconds)).strftime('%a, %d %b %Y %H:%M:%S')
    self.webapp2instance.response.headers.add_header("Set-Cookie", cookie.output(header=''))


  def remove(self, name):
    self.set(name, 'remove', seconds=-1)







class CookieHandler(webapp2.RequestHandler):
  
  def __init__(self, *args, **kwargs):
    super(CookieHandler, self).__init__(*args, **kwargs)
    self.cookies = CookieWorker(self)