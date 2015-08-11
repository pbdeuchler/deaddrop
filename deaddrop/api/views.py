from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

import deaddrop.api.models as models
import deaddrop.api.serializers as serializers
from deaddrop.senders import SendgridSender, TwilioSender
from deaddrop.encryption import encryptor

import datetime, uuid

generage_uid = lambda: str(uuid.uuid1()).replace("-", "")


class SecretCreate(APIView):

    def post(self, request, format=None):
        serializer = serializers.CreateRequestSerializer(data=request.data)
        if serializer.is_valid():
            e = encryptor.AESEncryptor()
            encryped_content, key = e.encrypt_secret(serializer.data['secret']['content'])
            if (serializer.data['secret']['expiry_type'] == models.TIME_EXPIRY) and serializer.data.get('expiry_timestamp', None) is None:
                return Response("An expiry time must be provided", status=status.HTTP_400_BAD_REQUEST)
            secret = models.Secret(content=encryped_content,
                                    uid=generage_uid(),
                                    expiry_type=serializer.data['secret']['expiry_type'],
                                    expiry_timestamp=serializer.data['secret'].get('expiry_timestamp', None),
                                    management_key=generage_uid())
            print(secret)
            secret.save()

            # content send logic
            if serializer.data['content_delivery_channel'] == models.EMAIL_CHANNEL:  # sendgrid
                ss = SendgridSender.SendgridSender()
                try:
                    ss.send(serializer.data['sender_reply_address'],
                            serializer.recipient.data['email'],
                            secret.content)
                except:
                    return Response(None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:  # twilio
                ts = TwilioSender.TwilioSender()
                try:
                    ts.send(serializer.data['sender_reply_address'],
                            serializer.recipient.data['email'],
                            secret.content)
                except:
                    return Response(None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # key send logic
            if serializer.data['key_delivery_channel'] == models.EMAIL_CHANNEL:  # sendgrid
                ss = SendgridSender.SendgridSender()
                try:
                    ss.send(serializer.data['sender_reply_address'],
                            serializer.recipient.data['email'],
                            key)
                except:
                    return Response(None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:  # twilio
                ts = TwilioSender.TwilioSender()
                try:
                    ts.send(serializer.data['sender_reply_address'],
                            serializer.recipient.data['phone'],
                            key)
                except:
                    return Response(None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
        serializer = serializers.DecryptRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                e = encryptor.AESEncryptor()
                decrypted_content = e.decrypt_secret(serializer.data, serializer.data['key'])
                result = {"result": decrypted_content, "error": None}
                if requested_secret.expiry_type == models.READ_EXPIRY:
                    requested_secret.delete()
                elif (requested_secret.expiry_timestamp - datetime.datetime.now()).seconds <= 0:
                    requested_secret.delete()
                return Response(result, status=status.HTTP_200_OK)
            except:
                result = {"result": None, "error": "Error decrypting content"}
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
