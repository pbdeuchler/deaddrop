from twilio.rest import TwilioRestClient 
from django.conf import settings

class TwilioSender:

	def send(self, sender, recipient, content): 
		client = TwilioRestClient(settings.ACCOUNT_SID, settings.AUTH_TOKEN) 
		 
		client.messages.create(
			to= recipient, 
			from_= settings.FROM_NUMBER, 
			body= "Secret key from %s: %s" % (sender,content)  
		)

