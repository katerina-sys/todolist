from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.serializers import TgUserSerializer


class BotVerifyView(generics.UpdateAPIView):
    model = TgUser
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']
    serializer_class = TgUserSerializer

    def patch(self, request, *args, **kwargs):
        data = self.serializer_class(request.data).data
        tg_client = TgClient("6138310967:AAHJbueE7x5U6qW6C3vVZNFsLPC1yTbYujo")
        tg_user = TgUser.objects.filter(verification_code=data['verification_code']).first()
        if not tg_user:
            return Response(status.HTTP_400_BAD_REQUEST)
        tg_user.user = request.user
        tg_user.save()
        tg_client.send_message(chat_id=tg_user.tg_chat_id, text="Успешно")
        return Response(data=data, status=status.HTTP_201_CREATED)
