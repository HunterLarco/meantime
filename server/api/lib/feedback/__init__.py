from google.appengine.ext import ndb


class Feedback(ndb.Model):
  
  content = ndb.TextProperty()
  tags = ndb.StringProperty(repeated=True, indexed=True)
  user = ndb.KeyProperty(indexed=True)


def create(user, content, tags=[]):
  f = Feedback()
  f.user = user.key
  f.content = content
  f.tags = tags
  f.put()
  return f