from twilio.rest import TwilioRestClient 
from django.conf import settings

def send(sender, recipient, content, type): 
	client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN) 
	body = "" 
	if type == 1:
		body = "Secret message from %s: %s" % (sender, content)
	elif type == 2:
		body = "Secret key from %s: %s" % (sender, content)
	else:
		body = "A secret from %s: %s" % (sender, content)
	client.messages.create(
		to= recipient, 
		from_= settings.TWILIO_FROM_NUMBER, 
		body= body
	)
