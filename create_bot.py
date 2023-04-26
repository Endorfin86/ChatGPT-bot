from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from config import TOKEN

#создание бота
bot = Bot(token=TOKEN)
#запуск бота
dp = Dispatcher(bot)