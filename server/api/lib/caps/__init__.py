"""
' __init__.py Imports
"""
import uploader


"""
' Common Package Imports
"""
from google.appengine.ext import ndb
from .. import shards






class Capsule(ndb.Model):
  content = ndb.BlobKeyProperty(indexed=False)
  
  def getAttemptsCounter(self):
    return shards.getOrCreate(str(self.key),
           namespace=self.__class__.__name__+'_AttemptsShards')
  
  def getAttempts(self):
    return self.getAttemptsCounter().getValue()

  def _strip(self, string):
    import re
    string = re.sub(r'[^\w]', '', string)
    return string.lower()

  def attempt(self, guess):
    self.getAttemptsCounter().add(1)
    return _strip(guess) == _strip(self.clue_answer)
    # TODO stop words