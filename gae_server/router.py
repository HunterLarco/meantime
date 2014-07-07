#from lib.moment import GuestRouter
#from lib.moment import AuthRouter
from lib import users


#app = users.app(GuestRouter, AuthRouter, debug=True)


import webapp2
import os
from google.appengine.ext.webapp import template




class SignupTest(webapp2.RequestHandler):
  def get(self):
    self.response.out.write("""
      Signup<br/>
      <form action='/signup' method='post'>
        <input name='email'/><br/>
        <input name='password'/><br/>
        <input type='submit'/>
      </form>
    """)
  def post(self):
    response = users.create(
      self.request.get('email'),
      self.request.get('password')
    )
    if response == users.EMAIL_IS_USED:
      self.response.out.write("email is used")
    else:
      self.response.out.write("success")





class LoginTest(webapp2.RequestHandler):
  def get(self):
    self.response.out.write("""
      Login<br/>
      <form action='/login' method='post'>
        <input name='email'/><br/>
        <input type='password' name='password'/><br/>
        <input type='submit'/>
      </form>
    """)
  def post(self):
    response = users.login(
      self,
      self.request.get('email'),
      self.request.get('password')
    )
    if response == users.INCORRECT_LOGIN:
      self.response.out.write("login failed")
    elif response == users.BRUTE_SUSPECTED:
      self.response.out.write("BRUTE_SUSPECTED")
    else:
      self.response.out.write("login success")




class StatusTest(webapp2.RequestHandler):
  def get(self):
    status = users.checkSession(self)
    if status == users.sessions.WATCHING:
      self.response.out.write('watching')
    elif status == users.sessions.SUCCESS:
      self.response.out.write('success')
    elif status == users.sessions.SESSION_DOESNT_EXIST:
      self.response.out.write('session doesn\'t exist')
    else:
      self.response.out.write('failure')




app = webapp2.WSGIApplication([
                ('/signup/?', SignupTest),
                ('/login/?', LoginTest),
                ('/', StatusTest)
              ], debug=True)
