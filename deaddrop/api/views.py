from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import sys, traceback
from django.http import Http404
import deaddrop.api.models as models
import deaddrop.api.serializers as serializers
from deaddrop.senders import SendgridSender, TwilioSender
from deaddrop.encryption import aesencryptor as encryptor

import uuid
from datetime import datetime, timezone

generage_uid = lambda: str(uuid.uuid1()).replace("-", "")


class SecretCreate(APIView):

    def post(self, request, format=None):
        serializer = serializers.CreateRequestSerializer(data=request.data)
        if serializer.is_valid():
            encrypted_content, key = encryptor.encrypt_secret(serializer.data['secret']['content'])

            if (serializer.data['secret']['expiry_type'] == models.TIME_EXPIRY) and serializer.data['secret'].get('expiry_timestamp', None) is None:
                return Response("An expiry time must be provided", status=status.HTTP_400_BAD_REQUEST)

            if (serializer.data['key_delivery_channel'] == models.SMS_CHANNEL) or (serializer.data['content_delivery_channel'] == models.SMS_CHANNEL):
                if serializer.data['recipient']['phone'] is None:
                    return Response("An phone number must be provided", status=status.HTTP_400_BAD_REQUEST)

            if (serializer.data['key_delivery_channel'] == models.EMAIL_CHANNEL) or (serializer.data['content_delivery_channel'] == models.EMAIL_CHANNEL):
                if serializer.data['recipient']['email'] is None:
                    return Response("An email address must be provided", status=status.HTTP_400_BAD_REQUEST)

            if (serializer.data['key_delivery_channel'] == models.SMS_CHANNEL):
                if serializer.data['recipient']['phone'] is None:
                    return Response("An phone number must be provided", status=status.HTTP_400_BAD_REQUEST)

            secret = models.Secret(content=encrypted_content,
                                    uid=generage_uid(),
                                    expiry_type=serializer.data['secret']['expiry_type'],
                                    expiry_timestamp=serializer.data['secret'].get('expiry_timestamp', None),
                                    management_key=generage_uid())
            # FOR DEBUGGING
            # print(key)
            # print(secret.uid)
            # secret.save()
            # content send logic
            if serializer.data['content_delivery_channel'] == models.EMAIL_CHANNEL:  # sendgrid
                try:
                    SendgridSender.send(serializer.data['sender_reply_address'],
                            serializer.data['recipient']['email'],
                            "https://deaddrop.space/secret/%s" % secret.uid,
                            1)
                except:
                    traceback.print_exc(file=sys.stdout)
                    return Response("Email content send failed", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:  # twilio
                try:
                    TwilioSender.send(serializer.data['sender_reply_address'],
                            serializer.data['recipient']['phone'],
                            "https://deaddrop.space/secret/%s" % secret.uid,
                            1)
                except:
                    traceback.print_exc(file=sys.stdout)
                    return Response("SMS content send failed", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # key send logic
            if serializer.data['key_delivery_channel'] == models.EMAIL_CHANNEL:  # sendgrid
                try:
                    SendgridSender.send(serializer.data['sender_reply_address'],
                            serializer.data['recipient']['email'],
                            key,
                            2)
                except:
                    traceback.print_exc(file=sys.stdout)
                    return Response("Email key send failed", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:  # twilio
                try:
                    TwilioSender.send(serializer.data['sender_reply_address'],
                            serializer.data['recipient']['phone'],
                            key,
                            2)
                except:
                    traceback.print_exc(file=sys.stdout)
                    return Response("SMS key send failed", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            secret.save()
            return Response({"uid": secret.uid, "management_key": secret.management_key},
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SecretDecrypt(APIView):

    def get_object(self, uid):
        try:
            return models.Secret.objects.get(uid=uid)
        except models.Secret.DoesNotExist:
            raise Http404

    def post(self, request, uid=None, format=None):
        requested_secret = self.get_object(uid)
        if requested_secret.expiry_type == models.TIME_EXPIRY:
            if (requested_secret.expiry_timestamp - datetime.now(timezone.utc)).days <= 0:
                requested_secret.delete()
                raise Http404
        serializer = serializers.DecryptRequestSerializer(data=request.data)
        if serializer.is_valid():
            to_decrypt = bytes(requested_secret.content, "utf-8")
            key = serializer.data['key']
            try:
                decrypted_content = encryptor.decrypt_secret(to_decrypt, key)
            except Exception as e:
                print(e)
                result = {"result": None, "error": "Error decrypting content"}
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            result = {"result": decrypted_content, "error": None}

            if int(requested_secret.expiry_type) == models.READ_EXPIRY:
                requested_secret.delete()
            elif (requested_secret.expiry_timestamp - datetime.now(timezone.utc)).days <= 0:
                requested_secret.delete()
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SecretDelete(APIView):

    def post(self, request, contentId=None, format=None):

        try:
            secret = models.Secret.objects.get(uid=contentId)
            management_key = request.data['management_key']
            assert management_key == secret.management_key
            secret.delete()
        except:
            print(request.data.items)
            traceback.print_exc(file=sys.stdout)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
