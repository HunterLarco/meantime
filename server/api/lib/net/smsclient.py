from twilio.rest import TwilioRestClient

account = "AC4729eb5c74c3f374006fa8d7b14b2095"
token = "d08614cab5d8c46a2a8cda4f63e17520"

# assumes USA if no country code given

def send(recipient, body):
  if recipient[0] != '+':
    recipient = '+1' + recipient
  client = TwilioRestClient(account, token)
  message = client.messages.create(to=recipient, from_="+12698200001",
                                   body=body)