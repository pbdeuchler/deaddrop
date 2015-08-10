import sendgrid
from django.conf import settings

def send(sender, recipient, content):
	sg = sendgrid.SendGridClient(settings.SENDGRID_API_KEY)

	message = sendgrid.Mail()
	message.add_to(recipient)
	message.set_subject("A secret message from %s" % sender)
	message.set_html(content)
	message.set_from(sender)
	status, msg = sg.send(message)