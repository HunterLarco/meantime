import webapp2

class CookieWorker():
  
  # cookies are split into chunks of this size to ensure they aren't too large
  CHUNK_SIZE = 100
  DEFAULT_EXPIRATION = 60*60*24*30# one month
  
  def __init__(self, Webapp2Instance):
    self.webapp2instance = Webapp2Instance
  
  def get(self, name):
    ### Attempt to string together all the cookie chunks that have been saved ###
    currentChunk = ''
    chunkNumber = 0
    string = ''
    while currentChunk != None and (len(currentChunk) == self.CHUNK_SIZE or currentChunk == ''):
      currentChunk = self.webapp2instance.request.cookies.get(name+'_chunk_'+str(chunkNumber))
      string += currentChunk if currentChunk != None else ''
      chunkNumber += 1# read the next chunk
    ### check if the name does not exist ###
    if string == '':
      return None
    ### return the data
    return string


  def set(self, name, string):
    # import the ceil function from math to use when spliting the encrypted ID every 100 characters
    from math import ceil
    # import SimpleCookie to format the cookie data that we will send to the client to store
    from Cookie import SimpleCookie
    # datetime is used to format the expiration date for the cookies
    import datetime
    # form/encrypt the data
    cookies = [string[i*self.CHUNK_SIZE:(i+1)*self.CHUNK_SIZE] for i in range(int(ceil(float(len(string))/self.CHUNK_SIZE)))]# this splits the cookie as outlined in the previous line
    # iterate through each cookie chunk and add the cookie to the header
    for index in range(len(cookies)):
      cookieValue = cookies[index]
      cookieName = name+'_chunk_'+str(index)
      # create the actuall cookie string to be added to the response headers
      cookie = SimpleCookie()
      cookie[cookieName] = cookieValue# set the value
      cookie[cookieName]["path"] = "/"# make it accessable to all pages
      cookie[cookieName]["expires"] = (datetime.datetime.now()+datetime.timedelta(seconds=self.DEFAULT_EXPIRATION)).strftime('%a, %d %b %Y %H:%M:%S')# set an expiration time
      from os import environ
      if not environ["SERVER_NAME"] == "localhost":# check if not in development
        cookie[cookieName]['domain'] = '.%s' % environ['DEFAULT_VERSION_HOSTNAME']
      self.webapp2instance.response.headers.add_header("Set-Cookie", cookie.output(header=''))# add the cookie string to the response headers


  def remove(self, name):
    # import SimpleCookie to format the cookie data that we will send to the client to modify the expiration dates of currently existing cookies
    from Cookie import SimpleCookie
    # datetime is used to format the expiration date for the cookies
    import datetime
    ### iterate through the cookie chunks used to save the client ID ###
    lastChunk = ''
    currentChunk = ''
    chunkNumber = 0
    expiration = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%a, %d %b %Y %H:%M:%S')
    while currentChunk != None or lastChunk != None:
      lastChunk = currentChunk
      currentChunk = self.webapp2instance.request.cookies.get(name+'_chunk_'+str(chunkNumber))
      if currentChunk != None:
        # delete the cookie by altering the expiration date to now
        cookieName = name+'_chunk_'+str(chunkNumber)
        cookie = SimpleCookie()
        cookie[cookieName] = 'delete'
        cookie[cookieName]["expires"] = expiration
        # add the cookie string to the response headers
        self.webapp2instance.response.headers.add_header("Set-Cookie", cookie.output(header=''))
      chunkNumber += 1# read the next chunk







class CookieHandler(webapp2.RequestHandler):
  
  def __init__(self, *args, **kwargs):
    super(CookieHandler, self).__init__(*args, **kwargs)
    self.cookies = CookieWorker(self)