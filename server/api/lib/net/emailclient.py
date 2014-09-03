from google.appengine.api import mail

def send(recipient, body):
  message = mail.EmailMessage()
  message.sender = 'admin@trysealed.com'
  message.to = recipient
  message.body = body
  message.send()