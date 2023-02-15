from django.urls import path

from bot.views import BotVerifyView

urlpatterns = [
    path('verify', TgUserVerificationView.as_view(), name='verify'),
]
