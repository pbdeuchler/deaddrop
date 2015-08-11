import sendgrid
from django.conf import settings

def send(sender, recipient, content, type):
	sg = sendgrid.SendGridClient(settings.SENDGRID_API_KEY)

	message = sendgrid.Mail()
	message.add_to(recipient)
	if( type == 1):
		message.set_subject("A secret message from %s" % sender)
	elif type == 2:
		message.set_subject("A secret key from %s" % sender)
	else:
		message.set_subject("A secret from %s" % sender)
	message.set_html(content)
	message.set_from(sender)
	status, msg = sg.send(message)