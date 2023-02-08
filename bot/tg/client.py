from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot.utils import verification_user, \
    update_user, list_goals, list_categories, list_tg_user, create_user, get_tg_user


async def command_start(message: types.Message, state: FSMContext):
    await state.finish()
    users = await list_tg_user()
    if users is None:
        await create_user(message)
        user = await get_tg_user(message)
        if user is None:
            await create_user(message)
            code = verification_user()
            await message.answer(f'Добро пожаловать.'
                                 f'Для регистрации введите код на сайте\n{code}')
            await update_user(message, code)
        else:
            await message.answer('Добро пожаловать')
    else:
        user = await get_tg_user(message)
        if user is None:
            await create_user(message)
            code = verification_user()
            await message.answer(f'Добро пожаловать.'
                                 f'Для регистрации введите код на сайте\n{code}')
            await update_user(message, code)
        else:
            await message.answer('Добро пожаловать')


async def command_help(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('start -Запуск бота,\n'
                         'help - Помощь по командам,\n'
                         'goals - Цели,\n'
                         'categories - Категории,\n'
                         'create - Создать цель,\n'
                         'cancel - Отмена')


async def command_goals(message: types.Message, state: FSMContext):
    await state.finish()
    goals = await list_goals(message)
    await message.answer(goals)


async def command_categories(message: types.Message, state: FSMContext):
    await state.finish()
    categories = await list_categories(message)
    await message.answer(categories)


async def unknown_command(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Неизвестная команда. '
                         'Для получения информации по командам введите "/help"')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'], state='*')
    dp.register_message_handler(command_help, commands=['help'], state='*')
    dp.register_message_handler(command_goals, commands=['goals'], state='*')
    dp.register_message_handler(command_categories, commands=['categories'], state='*')
    dp.register_message_handler(unknown_command, state='*')
