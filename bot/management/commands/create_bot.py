from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

from todolist import settings


storage = MemoryStorage()

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)
