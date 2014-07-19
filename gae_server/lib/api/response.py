"""
' Error Responses
"""
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


"""
' PURPOSE
'   Throws an error response, consisting of a error code
'   and error message.
' PARAMETERS
'   <int code>
'   <Tuple dataStruct>
'   <boolean **kwarg compiled>
' RETURNS
'   A dict
' NOTES
'   1. the 'dataStruct' is used to customize information in an error message
'   2. when compiled is true the dict is serialized into JSON format
"""
def throw(code, dataStruct=(), compiled=False):
  response = {
    'stat' : 'fail',
    'code' : code,
    'message' : __ERROR__RESPONSES__[code] % dataStruct
  }
  return compile(response) if compiled else response


"""
' PURPOSE
'   Returns a successful response. May take additional data to add to the response.
' PARAMETERS
'   <Dict **kwarg data>
' RETURNS
'   A dict
"""
def reply(data={}):
  data['stat'] = 'ok'
  return data


"""
' PURPOSE
'   JSON serializes a given dict
' PARAMETERS
'   <Dict JSON>
' RETURNS
'   A string
"""
def compile(JSON):
  import json
  return json.dumps(JSON)