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
  blob_key = ndb.BlobProperty(indexed=False)
  clue = ndb.BlobProperty(indexed=False)
  clue_answer = ndb.StringProperty(indexed=False)
  
  def getAttemptsCounter(self):
    return shards.getOrCreate(str(self.key),
           namespace=self.__class__.__name__+'_AttemptsShards')
  
  def getAttempts(self):
    return self.getAttemptsCounter().getValue()

  def attempt(self, guess):
    self.getAttemptsCounter().add(1)
    return guess == self.clue_answer
    # TODO stop words