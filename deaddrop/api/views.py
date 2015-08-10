from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

import models
import serializers

import datetime, uuid


class SecretCreate(APIView):

    def post(self, request, format=None):
        serializer = serializers.CreateRequestSerializer(data=request.data)
        if serializer.is_valid():

            encryped_content, key = encrypt(serializer.data['content'])
            secret = models.Secret(content=encryped_content,
                                    key=key, uid=str(uuid.uuid1()),
                                    expiry_type=serializer.data['expiry_type'],
                                    expiry_timestamp=serializer.data['expiry_timestamp'])
            secret.save()

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
                decrypted_content = requested_secret.decrypt(serializer.data)
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
