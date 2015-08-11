from rest_framework import serializers

from .models import Secret, CHANNEL_TYPES, DEFAULT_MAX_LENGTH


class SecretSerializer(serializers.ModelSerializer):
    expiry_timestamp = serializers.DateTimeField(required=False)

    class Meta:
        model = Secret
        exclude = ('uid', 'management_key')


class RecipientSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(max_length=12, required=False)


class CreateRequestSerializer(serializers.Serializer):
    recipient = RecipientSerializer()
    secret = SecretSerializer()
    content_delivery_channel = serializers.ChoiceField(choices=CHANNEL_TYPES)
    key_delivery_channel = serializers.ChoiceField(choices=CHANNEL_TYPES)
    sender_id = serializers.CharField(max_length=DEFAULT_MAX_LENGTH, required=False)
    sender_reply_address = serializers.EmailField(required=False)


class DecryptRequestSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=52)
