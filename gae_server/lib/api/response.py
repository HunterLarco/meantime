# all error responses
__ERROR__RESPONSES__ = {
  000 : "An unexpected error occurred",
  001 : "Parameter Missing",
  002 : "Access Denied",
  003 : "Error Code 404",
  
  100 : "API Handler Map Dictionary '%s' Does Not contain Method '%s'",
  101 : "API Handler Map Does Not Contain Dictionary '%s'",
  102 : "GET API Requests Must Use The 'get' Dictionary In The Permissions Map",
  103 : "A POST API Request May Not Use The 'get' Dictionary",
  
  # users
  200 : "Email Alread In Use",
  201 : "Incorrect Login Credentials",
  202 : "Brute Force Suspected",
  203 : "User Doesn't Exist",
  204 : "User Account Locked",
  
  #sessions:
  300 : "Session Doesn't Exist"
}

# throw error response
def throw(code, dataStruct=(), compiled=False):# dataStruct is used to add data to the messages and compile determines if the response should be auto-compiled
  # format the response
  response = {
    'stat' : 'fail',
    'code' : code,
    'message' : __ERROR__RESPONSES__[code] % dataStruct
  }
  # return the response <compile if specicfied>
  if compiled:
    return compile(response)
  else:
    return response


# returns a successful response
def reply(data={}):
  data['stat'] = 'ok'
  return data


# compiles response for output
def compile(JSON):
  import json
  return json.dumps(JSON)