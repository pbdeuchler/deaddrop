from django.db import models

DEFAULT_MAX_LENGTH = 128

EMAIL_CHANNEL = 1
SMS_CHANNEL = 2

CHANNEL_TYPES = (
    (EMAIL_CHANNEL, 'email'),
    (SMS_CHANNEL, 'sms'),
)

TIME_EXPIRY = 1
READ_EXPIRY = 2

EXPIRY_TYPES = (
    (TIME_EXPIRY, 'time'),
    (READ_EXPIRY, 'read'),
)


class Secret(models.Model):
    uid = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    content = models.TextField()
    expiry_type = models.CharField(choices=EXPIRY_TYPES, max_length=1)
    expiry_timestamp = models.DateTimeField(null=True)
    management_key = models.CharField(max_length=DEFAULT_MAX_LENGTH)
