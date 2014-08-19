"""
' A quick-lookup hashtable where each bit in a byte array is a single key. Therefore very efficient with
' both memory and speed when trying to see if something is in the hash table or not.
"""







# 6 character hash
def hash(string):
  # begin ToHex function
  def ToHex(num):
    hexValue = '%x' % num
    modV = len(hexValue) % 3
    if modV != 0:
      for i in range(3-modV):
        hexValue = "0" + hexValue
    return hexValue
  # end ToHex function
  
  # pack into a multiple of 32
  packing = 32 - len(string) % 32
  for i in range(packing):
    string += chr(0)
  
  # primes
  primes = [5381, 2129]
  
  # iterate through "chunks"/multiples of 32 characters
  for j in range(len(string)/32):
    piece = string[j*32:(j+1)*32]
    for i in range(len(piece)/16):
      pi = i % len(primes)
      subString = piece[i*16:(i+1)*16]
      for k in range(len(subString)):
        char = ord(subString[k])
        # 0xfff --- thus this sub-hash is always a maximum of 3-digits
        primes[pi] = (primes[pi] * (32) + primes[pi] + char) & 0xfff
  return ''.join([ToHex(x) for x in primes])






class BinaryHashTable():
  data = bytearray(16**6/8)
  
  def __init__(self):
    for i in range(len(self.data)):
      self.data[i] = chr(0)
  
  def add(self, key):
    hashed = hash(key)
    number = int(hashed, 16)
    key_bin = number / 8
    relative_number = number - key_bin*8
    bin_value = self.data[key_bin]
    new = bin_value ^ 2**relative_number
    self.data[key_bin] = new
  
  def has(self, key):
    hashed = hash(key)
    number = int(hashed, 16)
    key_bin = number / 8
    relative_number = number - key_bin*8
    bin_value = self.data[key_bin]
    return bin_value & 2**relative_number != 0



