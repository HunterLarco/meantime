# ADAPTED FROM <https://developers.google.com/appengine/articles/sharding_counters>

"""
' Common Package Imports  
"""
from google.appengine.ext import ndb
from google.appengine.api import memcache


"""
' PURPOSE
'   Given a name and namespace, return a DynamicShard if one exists, or
'   create a new one if it doesn't and return that
' PARAMETERS
'   <String name>
'   <String **kwarg namespace>
' RETURNS
'   A ndb.Model instance
' PUTS
'   1 - when a new DynamicShard is created
"""
def getOrCreate(name, namespace=None):
  return DynamicCounter.get_or_insert(name, namespace=namespace)


# -------------------------------------------------------- START OF ENTITY -------------------------------------------------------- #


"""
' PURPOSE
'   The ndb.Model that runs all the shards and tracks data.
'   It's used for everything.
' NOTES
'   Use the 'getOrCreate' method to access DynamicCounters
"""
class DynamicCounter(ndb.Model):
  num_shards = ndb.IntegerProperty(default=20)
  
  SHARD_KEY_TEMPLATE = 'shard-{}-{:d}'
  
  
  """
  ' PURPOSE
  '   Return the value associated with this counter
  ' PARAMETERS
  '   None
  ' RETURNS
  '   int
  ' NOTES
  '   Uses the memcache to remember data (deleted on change)
  """
  def getValue(self):
    name = self.getName()
    total = memcache.get(name)
    if total is None:
        total = 0
        all_keys = self.getAllShardKeys()
        for counter in ndb.get_multi(all_keys):
            if counter is not None:
                total += counter.count
        memcache.add(name, total, 60)
    return total
  
  
  """
  ' PURPOSE
  '   Adds the parameter 'amount' to the counter
  ' PARAMETERS
  '   <int amount>
  ' RETURNS
  '   Nothing
  """
  def add(self, amount):
    DATA = dict(tries=0)
    self._increment(DATA, amount)
    
    ndb.transaction(lambda: memcache.incr(self.getName(), delta=amount))
    
    if DATA['tries'] > 1:
      self._increase_shards(2)
  
  
  """
  ' PURPOSE
  '   A 'private' method that is used to add data to a random shard
  '   and retry if it fails
  ' PARAMETERS
  '   <Dict retrydata> ~ counts how many times the function is run
  '   <int amount>
  ' RETURNS
  '   Nothing
  ' PUTS
  '   1 - after changing a shard's data
  ' NOTES
  '   '@ndb.transactional' forces the function to roll back on datastore
  '   error so that we are garaunteed it will work lest it fails multiple
  '   times.
  """
  @ndb.transactional
  def _increment(self, retrydata, amount):
    import random
    
    name = self.getName()
    num_shards = self.num_shards
    
    index = random.randint(0, num_shards - 1)
    shard_key_string = self.SHARD_KEY_TEMPLATE.format(name, index)
    counter = DynamicShard.get_by_id(shard_key_string)
    if counter is None:
        counter = DynamicShard(id=shard_key_string)
    counter.count += amount
    counter.put()
    
    retrydata['tries'] += 1
  
  
  """
  ' PURPOSE
  '   Returns the serialized name associated with this counter
  ' PARAMETERS
  '   None
  ' RETURNS
  '   Nothing
  """
  def getName(self):
    return self.key.id()
  
  
  """
  ' PURPOSE
  '   A 'private' method that increases the amount of shards by the
  '   provided amount.
  ' PARAMETERS
  '   <int amount>
  ' RETURNS
  '   Nothing
  ' PUTS
  '   1 - on changing the amount of shards
  """
  @ndb.transactional
  def _increase_shards(self, amount):
    name = self.getName()
    if amount > 0:
      self.num_shards += amount
      self.put()
  
  
  """
  ' PURPOSE
  '   Returns all the possible shard keys associated with this counter
  ' PARAMETERS
  '   None
  ' RETURNS
  '   Nothing
  """
  def getAllShardKeys(self):
    name = self.getName()
    shard_key_strings = [self.SHARD_KEY_TEMPLATE.format(name, index)
                         for index in range(self.num_shards)]
    return [ndb.Key(DynamicShard, shard_key_string)
            for shard_key_string in shard_key_strings]


  """
  ' PURPOSE
  '   Provides some basic statistics about this counter
  ' PARAMETERS
  '   None
  ' RETURNS
  '   Nothing
  """
  def profile(self):
    all_keys = self.getAllShardKeys()
  
    keycount = 0

    for counter in ndb.get_multi(all_keys):
        if counter is not None:
            keycount += 1
  
    return dict(
      shards_available = len(all_keys),
      shards_used = keycount
    )


# -------------------------------------------------------- END OF ENTITY -------------------------------------------------------- #


"""
' PURPOSE
'   The ndb.Model entity for Shards. It only contains
'   a count that may be changed at any time.
"""
class DynamicShard(ndb.Model):
  count = ndb.IntegerProperty(default=0)