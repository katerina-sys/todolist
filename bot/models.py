from django.db import models

# Create your models here.
from django.utils.crypto import get_random_string


class TgUser(models.Model):
    tg_user_id = models.BigIntegerField(verbose_name='tg user id', unique=True)
    tg_chat_id = models.BigIntegerField(verbose_name='tg chat id')
    username = models.CharField(max_length=155, verbose_name='tg username', null=True, blank=True, default=None)
    user = models.ForeignKey('core.User', verbose_name='Пользователь', on_delete=models.PROTECT,
                             null=True, blank=True, default=None)
    verification_code = models.CharField(max_length=12, verbose_name='Код подтверждения')

    class Meta:
        verbose_name = 'tg пользователь'
        verbose_name_plural = 'tg пользователи'

    def generate_validation_code(self) -> str:
        code = get_random_string(10)
        self.verification_code = code
        self.save()
        return code
