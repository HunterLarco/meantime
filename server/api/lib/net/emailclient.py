from google.appengine.api import mail

def send(recipient, body, subject=None):
  message = mail.EmailMessage()
  message.sender = 'Sealed Team <admin@trysealed.com>'
  message.to = recipient
  message.body = body
  if subject != None:
    message.subject = subject
  message.send()