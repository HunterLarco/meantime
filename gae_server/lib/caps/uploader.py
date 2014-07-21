"""
' Globals
"""
DEV_APP_SERVER_BLOBSTORE_ENTITY_PORT = 8092


"""
' Common Package Imports
"""
import os
import urllib
from poster import multipart_encode, MultipartParam
from google.appengine.api import urlfetch
from google.appengine.ext import blobstore
import webapp2
from google.appengine.ext.webapp import blobstore_handlers


"""
' PURPOSE
'   Writes the given data string to a blob
' PARAMETERS
'   <String data>
' RETURNS
'   None on failure and the new blob key on success
' NOTES
'   Works by creating an blob upload URL and then steals its
'   headers and forces the given data into the request. It then
'   spoofs the post request.
"""
def upload(data):
  global DEV_APP_SERVER_BLOBSTORE_ENTITY_PORT        
  params = []
  params.append(MultipartParam(
      "file",
      filename='file',
      value=data))
  payloadgen, headers = multipart_encode(params)
  payload = str().join(payloadgen)
  url = None
  if development():
    url = urlfetch.fetch(
       url=("http://localhost:%d/data/setup_upload" %
             DEV_APP_SERVER_BLOBSTORE_ENTITY_PORT)).content
  else:
    url = urlfetch.fetch(
           "http://%s.latest.%s.appspot.com/data/setup_upload" %
           (os.environ["CURRENT_VERSION_ID"].split(".")[0],
            os.environ["APPLICATION_ID"].replace("s~", ""))).content
  try:
    result = urlfetch.fetch(
        url=url,
        payload=payload,
        method=urlfetch.POST,
        headers=headers,
        deadline=10,
        follow_redirects=False)
    if "location" in result.headers:
      location = result.headers["location"]
      key = location[location.rfind("/") + 1:]
      return key
    else:
      return None
  except:
    return None


"""
' PURPOSE
'   Determines if in dev or production right now
' PARAMETERS
'   None
' RETURNS
'   True if in development 
"""
def development():
  return os.environ['SERVER_SOFTWARE'].find('Development') == 0 


"""
' PURPOSE
'   This is the webapp2 handler that creates a blob upload url which is stolen
'   by the 'upload' function along with its headers to spoof a request.
"""
class SetupHandler(webapp2.RequestHandler):
  def get(self):
    self.response.out.write(blobstore.create_upload_url('/data/upload'))

"""
' PURPOSE
'   This is the webapp2 handler that actually recieves the data string from
'   the function 'upload' and saves it to blob.
"""
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    upload_files = self.get_uploads('file')
    blob_info = upload_files[0]
    self.redirect('%s' % blob_info.key())

"""
' PURPOSE
'   This webapp2 handler serves a blob given its key.
"""
class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, key):
    key = str(urllib.unquote(key))
    blob_info = blobstore.BlobInfo.get(key)
    self.send_blob(blob_info)
  def post(self, key):
    self.error(404)