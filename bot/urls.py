from django.urls import path

from bot.views import TgUserVerificationView

urlpatterns = [
    path('verify', TgUserVerificationView.as_view(), name='verify'),
]
