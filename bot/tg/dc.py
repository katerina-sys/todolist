from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.utils import list_categories, list_title_categories, create_goal


class TgStates(StatesGroup):
    choice_cat = State()
    title_goal = State()


async def input_cat_for_create_goal(message: types.Message):
    """Выбор категории для создания цели"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    categories = await list_categories(message)
    cat_title = await list_title_categories(message)
    for cat in cat_title:
        keyboard.add(cat)
    await message.answer(f'Выберите категорию для создания цели\n {categories}', reply_markup=keyboard)
    await TgStates.choice_cat.set()


async def input_cat(message: types.Message, state: FSMContext):
    """В случае ошибки повторный ввод категории или сохранение выбранной"""
    cat_title = await list_title_categories(message)
    if message.text.lower() not in cat_title:
        await message.answer('Выберите категорию, использую клавиатуру ниже')
        return
    await state.update_data(cat_title=message.text.lower())
    await TgStates.title_goal.set()
    await message.answer(f'Теперь введи название цели', reply_markup=types.ReplyKeyboardRemove())


async def input_new_goal(message: types.Message, state: FSMContext):
    """Создание новой цели"""
    data = await state.get_data()
    category = data['cat_title']
    await create_goal(message.text, message, category)
    await message.answer(f'Вы создали цель {message.text}')
    await state.finish()


async def command_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Вы отменили действие', reply_markup=types.ReplyKeyboardRemove())


def register_handlers_bot(dp: Dispatcher):
    dp.register_message_handler(command_cancel, commands=['cancel'], state='*')
    dp.register_message_handler(input_cat_for_create_goal, commands=['create'], state=['*'])
    dp.register_message_handler(input_cat, state=TgStates.choice_cat)
    dp.register_message_handler(input_new_goal, state=TgStates.title_goal)

