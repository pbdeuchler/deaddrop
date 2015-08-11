from twilio.rest import TwilioRestClient 
from django.conf import settings

def send(sender, recipient, content): 
	client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN) 
	 
	client.messages.create(
		to= recipient, 
		from_= settings.TWILIO_FROM_NUMBER, 
		body= "Secret key from %s: %s" % (sender,content)  
	)
