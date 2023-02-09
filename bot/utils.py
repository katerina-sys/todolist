import string
from random import choice

from asgiref.sync import sync_to_async
import bot
from bot.models import TgUser
from goals.models import Goal, GoalCategory


def verification_user():
    """Верификационный код для идентификации пользователя"""
    v_code = "".join(choice(string.ascii_letters + string.digits) for _ in range(12))
    return v_code


@sync_to_async
def list_tg_user():
    """Список пользователей в БД TgUser"""
    tg_users = TgUser.objects.all()
    if tg_users.count() > 0:
        tg_user_msg = [f'#{item.user}' for item in tg_users]
        return tg_user_msg
    else:
        return None


@sync_to_async
def create_user(message):
    """Создание ТГ пользователя"""
    tg_user = TgUser.objects.get_or_create(
        tg_user_id=message.from_user['id'],
        tg_chat_id=message.chat.id,
        username=message.from_user['first_name']
    )
    return tg_user


@sync_to_async
def update_user(message, code):
    """Обновление поля verification_code ТГ пользователя"""
    TgUser.objects.filter(tg_chat_id=message.chat.id).update(verification_code=code)


@sync_to_async
def get_tg_user(message):
    """Проверка на наличие в БД пользователя"""
    try:
        tg_user = TgUser.objects.filter(tg_chat_id=message.chat.id).first()
        return tg_user.user
    except AttributeError:
        return None


@sync_to_async
def list_goals(message):
    """Список целей пользователя"""
    tg_user = TgUser.objects.filter(tg_chat_id=message.chat.id).first()
    goals = Goal.objects.filter(user=tg_user.user).exclude(status=Goal.Status.archived)
    if goals.count() > 0:
        goals_msg = [f'#{item.id} {item.title}' for item in goals]
        return '\n'.join(goals_msg)
    else:
        return 'Целей нет'


@sync_to_async
def list_categories(message):
    """Список категорий"""
    tg_user = TgUser.objects.filter(tg_chat_id=message.chat.id).first()
    categories = GoalCategory.objects.filter(user=tg_user.user, is_deleted=False)
    if categories.count() > 0:
        categories_msg = [f'#{item.id} {item.title}' for item in categories]
        return '\n'.join(categories_msg)
    else:
        return 'Ошибка запроса'


@sync_to_async
def list_title_categories(message):
    """Список наименований категорий (исп. для создания цели)"""
    tg_user = TgUser.objects.filter(tg_chat_id=message.chat.id).first()
    categories = GoalCategory.objects.filter(user=tg_user.user, is_deleted=False)
    if categories.count() > 0:
        categories_msg = [f'{item.title}' for item in categories]
        return categories_msg
    else:
        return 'Ошибка запроса'


@sync_to_async
def create_goal(text, message, category):
    """Создание цели"""
    tg_user = TgUser.objects.filter(tg_chat_id=message.chat.id).first()
    cat = GoalCategory.objects.filter(title__contains=category, user=tg_user.user, is_deleted=False).first()
    print(cat)
    goal = Goal.objects.create(
        title=text,
        user=tg_user.user,
        category_id=cat.id
    )
    
