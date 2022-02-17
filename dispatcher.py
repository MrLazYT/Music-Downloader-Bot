from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import *

bot = Bot(token = BOT_TOKEN)

dp = Dispatcher(bot, storage = MemoryStorage())