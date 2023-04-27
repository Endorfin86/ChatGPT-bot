from aiogram import types
from create_bot import bot
from data_base import sql_db
from keyboards.client_kb.main_kb import ikeyboard_oppo, ikeyboard_premium

#при нажатии на кнопку возможности
async def btn_oppo(message : types.Message):
    await message.delete()
    await bot.send_message(message.from_user.id, 
'''🔥 Давай расскажу чем я могу тебе помочь?\n\n\
1️⃣ Создать резюме. С моей помощью ты можешь устроиться на работу мечты, ведь я могу написать хорошее резюме\n\
2️⃣ Написать текст на любую тему. Это поможет тебе в работе и учебе\n\
3️⃣ Перевести текст с иностранного языка\n\
4️⃣ Ответить на интересующие тебя вопросы. Чаще всего у меня получается это лучше, чем у известных поисковиков\n\
5️⃣ Написать код, перевести его с одного языка на другой и найти ошибки\n\
6️⃣ Планировать и осуществлять расчеты. Например, ты можешь за считанные секунды получить готовый план питания для похудения\n\n\
💡Это лишь малая часть моего функционала. Задавай мне любые задачи, а я постараюсь тебе помочь.\n\n\
🔥 Чтобы начать общение, нажми ниже на "💡 Начать диалог"  и напиши мне сообщение  👇🏻''',
reply_markup=ikeyboard_oppo)

#при нажатии на кнопку премиум доступ
async def btn_premium(message : types.Message):
    await message.delete()
    days = await sql_db.sql_check_limit_days(message.from_user.id)
    days = days[0]['days']
    requests = await sql_db.sql_check_limit_requests(message.from_user.id)
    requests = requests[0]['requests']
    await bot.send_message(message.from_user.id, 
f'''Доступно: {requests} запросов\n\n\
Доступно: {days} дней\n\n\
🔥 Функции, доступные для Premium-аккаунтов:\n\n\
🔘Безлимитное кол-во запросов\n\
🔘Бот понимает контекст\n\
🔘Приоритет запросов''',
reply_markup=ikeyboard_premium)

#при нажатии на кнопку диалог завершен
async def btn_endtalk(message : types.Message):
    await message.delete()
    await bot.send_message(message.from_user.id, '🔄 Диалог завершен. Память бота очищена.')
    await sql_db.sql_clear_context(message.from_user.id, text='')