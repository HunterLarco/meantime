# common imports
import response


### Purpose
# this function takes a dictionary name and method name to run an API MAP, really an example will make it clear. It essentially allows remote access to selective functions within the system through the API engine. Callback functions may be used in get requests with the URL parameter 'callback'.
### NOTE
# GET API requests must use the get dictionary
### Example Usage
# class API_HANDLERS_MAP:
#   class subjects:
#     def add(self, payload):
#       return KFE2.System.subjects.add(payload['SubjectName'])
# class AdminAPIAccess(webapp2.RequestHandler):
#   def post(self, dictionary, method):
#     KFE2.API.Engine.delegate(self, dictionary, method, API_HANDLERS_MAP)
# app = ('/admin/api/([^/]+)/([^/]+).*', AdminAPIAccess)
def delegate(Webapp2Instance, DictionaryName, MethodName, API_HANDLERS_MAP):
  # set the response as a JSON <or javascript>
  Webapp2Instance.response.headers['Content-Type'] = "application/javascript"
  ### Load the dictionary and the method in that dictionary from the Permissions Map ###
  # if either does not exist throw an error
  dictionary = getattr(API_HANDLERS_MAP, DictionaryName, None)
  if dictionary != None:
    method = getattr(dictionary, MethodName, None)
    if callable(method):
      import types
      func = types.MethodType(method, dictionary(), dictionary)# bind 'method' to it's parent class, 'dictionary'. This is so it isn't an unbound function: this would throw errors
      # used so that if the request isn't a post, then the 'get' dictionary is required and so that the request body isn't parsed
      if Webapp2Instance.request.method == 'POST':
        if DictionaryName == 'get':# 'get' dictionary is exclusively used for GET requests
          Webapp2Instance.response.out.write(response.throw(103, compiled=True))
          return
        from json import loads as ParseJSON
        payload = ParseJSON(Webapp2Instance.request.body)
        payload['__Webapp2Instance__'] = Webapp2Instance
        result = func(payload)
        Webapp2Instance.response.out.write(response.compile(response.reply() if result == None else result))
        return
      if DictionaryName == 'get':
        # if there is a callback function specified, use it
        result = func(Webapp2Instance)
        result = response.reply() if result == None else result
        if Webapp2Instance.request.get('callback') != None and Webapp2Instance.request.get('callback') != '':
          data = '%s(%s);' % (Webapp2Instance.request.get('callback'), response.compile(result))
        else:
          data = response.compile(result)
        Webapp2Instance.response.out.write(data)
        return
      Webapp2Instance.response.out.write(response.throw(102, compiled=True))
      return
    else:
      Webapp2Instance.response.out.write(response.throw(100, (DictionaryName, MethodName), compiled=True))
      return
  else:
    Webapp2Instance.response.out.write(response.throw(101, DictionaryName, compiled=True))
    return