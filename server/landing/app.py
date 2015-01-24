from google.appengine.ext.webapp import template
import webapp2
import os


class MainHandler(webapp2.RequestHandler):
  def get(self):
    template_values = {}
    path = os.path.join(os.path.dirname(__file__), 'main.html')
    self.response.out.write(template.render(path, template_values))


class AddEmail(webapp2.RequestHandler):
  def get(self):
    self.redirect('/')
  def post(self):
    email = self.request.get('email')
    SendEmail(email);


def SendEmail(email):
  from google.appengine.api import mail
  message = mail.EmailMessage(sender="Sealed Team <admin@trysealed.com>",
                              subject='New Beta Tester')
  message.to = 'hjlarco@gmail.com'
  message.body = "Hey Alex! <%s> just signed up to become a beta tester" % email
  message.html = message.body
  message.send()


app = webapp2.WSGIApplication([
                ('/addemail/?', AddEmail),
                ('/.*', MainHandler)
              ], debug=True)
