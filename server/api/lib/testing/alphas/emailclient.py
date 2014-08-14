def send(email, emailname, template_options={}):
  import os
  from google.appengine.ext.webapp import template
  from google.appengine.api import mail
  
  subjectpath = os.path.join(os.path.dirname(__file__), 'emails/'+emailname+'/subject.txt')
  subject = open(subjectpath, 'rb').read()
  
  message = mail.EmailMessage(sender="Sealed Team <admin@trysealed.com>",
                              subject=subject)
  message.to = email
  message.body = template.render(os.path.join(os.path.dirname(__file__), 'emails/'+emailname+'/body.txt'),  template_options)
  message.html = template.render(os.path.join(os.path.dirname(__file__), 'emails/'+emailname+'/body.html'), template_options)
  message.send()