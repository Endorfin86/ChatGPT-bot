from aiogram import executor
from create_bot import dp
from data_base import sql_db
import asyncio

#функция стартующая при запуске бота
async def on_startup(_):
    await sql_db.sql_start()
    asyncio.create_task(sql_db.sql_minus_day())

#импорт функций из пакета client
from handlers.client import main
main.register_handlers_client(dp)

#запуск бота
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

