from Cookie import SimpleCookie



class CookieShim():
  # seconds (in this case 30 days)
  DEFAULT_AGE_LIMIT = 60*60*24*30
  DEFAULT_AGE_LIMIT_UNIT = 'seconds'
  
  
  def __init__(self, webapp2Instance):
    self.__client__ = webapp2Instance
  
  
  def get(self, name):
    return self.__client__.request.cookies.get(name)
  
  
  def set(self, name, value):
    import datetime
    cookie = SimpleCookie()
    cookie[name] = value# set the value
    cookie[name]["path"] = "/"# make it accessable to all pages
    cookie[name]["expires"] = (datetime.datetime.now()+datetime.timedelta(seconds=self.DEFAULT_AGE_LIMIT)).strftime('%a, %d %b %Y %H:%M:%S')# set an expiration time
    from os import environ
    if not environ["SERVER_NAME"] == "localhost":# check if not in development
      cookie[name]['domain'] = '.%s' % environ['DEFAULT_VERSION_HOSTNAME']
    self.__client__.response.headers.add_header("Set-Cookie", cookie.output(header=''))# add the cookie string to the response headers
  
  
  def remove(self, name):
    import datetime
    cookie = SimpleCookie()
    cookie[name] = 'delete'
    cookie[name]["expires"] = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%a, %d %b %Y %H:%M:%S')
    # add the cookie string to the response headers
    self.__client__.response.headers.add_header("Set-Cookie", cookie.output(header=''))