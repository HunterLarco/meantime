"""
' Common Package Imports
"""
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import urllib



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








class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    
    import logging
    logging.error('THE DAMN THING UPLOADED, HUNTER!')
    
    logging.error(self.get_uploads())
    
    content_file = self.get_uploads()[0]
  
    from .. import users
    user = users.get(self.request.get('uid'))
    
    user.createCapsule(content_file.key())
    
    from ..api import response
    self.response.headers['Content-Type'] = "application/javascript"
    self.response.out.write(response.compile(response.reply()))








def getUrl():
  return blobstore.create_upload_url('/data/upload')