from django.db import models

# Create your models here.

from django.db import models


class DatesModelMixin(models.Model):
    class Meta:
        abstract = True  # Помечаем класс как абстрактный – для него не будет таблички в БД

    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата последнего обновления', auto_now=True)


class GoalCategory(DatesModelMixin):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    board = models.ForeignKey(
        'Board', verbose_name="Доска", on_delete=models.PROTECT, related_name="categories"
    )

    title = models.CharField(verbose_name='Название', max_length=255)
    user = models.ForeignKey('core.User', verbose_name='Автор', on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)


class Goal(DatesModelMixin):
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    class Status(models.IntegerChoices):
        to_do = 1, 'К выполнению'
        in_progress = 2, 'В процессе'
        done = 3, 'Выполнено'
        archived = 4, 'Архив'

    class Priority(models.IntegerChoices):
        low = 1, 'Низкий'
        medium = 2, 'Средний'
        high = 3, 'Высокий'
        critical = 4, 'Критический'

    title = models.CharField(verbose_name='Название', max_length=255)
    user = models.ForeignKey('core.User', verbose_name='Автор', related_name='goals', on_delete=models.PROTECT)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    category = models.ForeignKey(GoalCategory, verbose_name='Категория', on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(verbose_name='Статус', choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(verbose_name='Приоритет', choices=Priority.choices,
                                                default=Priority.medium)
    due_date = models.DateTimeField(verbose_name='Дата дедлайна', null=True, blank=True, default=None)

    def __str__(self):
        return self.title


class GoalComment(DatesModelMixin):
    class Meta:
        verbose_name = 'Комментарий к цели'
        verbose_name_plural = 'Комментарии к цели'

    user = models.ForeignKey('core.User', verbose_name='Автор', related_name='goal_comment', on_delete=models.PROTECT)
    goal = models.ForeignKey(Goal, verbose_name='Цель', related_name='goal_comment', on_delete=models.PROTECT)
    text = models.TextField(verbose_name='Текст')


class Board(DatesModelMixin):
    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"

    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class BoardParticipant(DatesModelMixin):
    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    class Role(models.IntegerChoices):
        owner = 1, "Владелец"
        writer = 2, "Редактор"
        reader = 3, "Читатель"

    board = models.ForeignKey(
        Board,
        verbose_name="Доска",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    user = models.ForeignKey(
        "core.User",
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    role = models.PositiveSmallIntegerField(
        verbose_name="Роль", choices=Role.choices, default=Role.owner
    )
