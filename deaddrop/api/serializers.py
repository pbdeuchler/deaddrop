from rest_framework import serializers

from django.conf import settings

from web.models import UserProfile

User = settings.AUTH_USER_MODEL
