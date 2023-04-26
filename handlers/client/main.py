from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery
from create_bot import bot
import openai
import os
import time
from data_base import sql_db
from keyboards import keybord_main
from aiogram.dispatcher.filters import Text
from handlers.client.button_func import btn_oppo, btn_premium, btn_endtalk
from handlers.client.ibutton_func import *
from aiogram.types.message import ContentType
from config import OPENAI
from price import *

#API-ключ openai
openai.api_key = OPENAI

#голосовые сообщения
async def voice_handler(message: types.Message):
    if message.voice:
        voice_duration = message.voice.duration
        file_id = message.voice.file_id
        # здесь можно выполнить какие-то действия с голосовым сообщением
        print(f"Получено голосовое сообщение длительностью {voice_duration} с ID файла {file_id}")
        await bot.send_voice(
        chat_id=message.chat.id,
        voice=message.voice.file_id,
    )

#стартовая функция, срабатывает при нажатии на кнопку старт в начале общения с ботом
async def start_command(message : types.Message):
    subscribe = await bot.get_chat_member(chat_id='-1001911096437', user_id=message.from_user.id)
    await message.delete()
    #проверяем подписан ли пользователь на канал с id -1001911096437
    if subscribe.status == 'member' or subscribe.status == 'creator':
        print('Пользователь является подписчиком')
        await bot.send_message(message.from_user.id, '🤖 Приветствую! Я ChatGPT, задайте свой вопрос и я постараюсь ответить на него.', reply_markup=keybord_main)
        time.sleep(2)
        await bot.send_message(message.from_user.id, 'Или можем просто поболтать, если тебе скучно 😇')
        print(message.from_user.username)
        await sql_db.sql_create_user(message)
    elif subscribe.status == 'left':
        print('Пользователь не подписан')
        await bot.send_message(message.from_user.id, '🤖 Приветствую! Я ChatGPT, задайте свой вопрос и я постараюсь ответить на него.')
        time.sleep(2)
        await bot.send_message(message.from_user.id, 'Чтобы продолжить общение со мной, необходимо подписаться на этот канал https://t.me/techinpocket')

#обработка сообщений от пользователя
async def message_user(message : types.Message):
        subscribe = await bot.get_chat_member(chat_id='-1001911096437', user_id=message.from_user.id)
        #проверяем статус подписки на группу
        if subscribe.status == 'member' or subscribe.status == 'creator':
            await sql_db.sql_create_user(message)
            user = await sql_db.sql_check_user(message.from_user.id)
            #проверяем пользователя на наличие в базе данных
            if user == []:
                print('пользователь не зарегистрирован')
            else:
                days = await sql_db.sql_check_limit_days(message.from_user.id)
                requests = await sql_db.sql_check_limit_requests(message.from_user.id)
                #проверяем пользователя на наличие лимитов по подписке
                if days[0]["days"] != 0 or requests[0]["requests"] != 0:
                    #отправка прелоад-сообщения и сохранение id этого сообщения
                    sent_message = await bot.send_message(message.chat.id, 'ChatGPT думает...')
                    sent_message_id = sent_message.message_id
                    context = await sql_db.sql_get_context(message.from_user.id)
                    #получение текста сообщения от пользователя
                    restart_sequence = "Human: "
                    start_sequence = "AI: "
                    if len(context) > 3000:
                        await sql_db.sql_clear_context(message.from_user.id, text='')
                        print('Поле context очищено')
                        context = await sql_db.sql_get_context(message.from_user.id)
                    else:
                        pass
                    message_text = context + '\n' + message.text + '.'
                    #запрос ответа от ChatGPT
                    try:
                        response = openai.Completion.create(
                            model="text-davinci-003",
                            prompt=message_text,
                            temperature=0.5,
                            max_tokens=3000,
                            top_p=1,
                            frequency_penalty=0,
                            presence_penalty=0.6,
                        )
                    except Exception:
                        print('Привышен программный лимит по символам')
                        await bot.delete_message(chat_id=message.chat.id, message_id=sent_message_id)
                        await bot.send_message(message.from_user.id, '⛔ Привышен лимит памяти бота')
                        await sql_db.sql_clear_context(message.from_user.id, text='')
                        time.sleep(2)
                        print('Контекст очищен')
                        await bot.send_message(message.from_user.id, '🗑 Память бота очищена')
                        await bot.send_message(message.from_user.id, '🤖 Начните разговор заново или спросите что-нибудь...')
                    #получение ответа от ChatGPT

                    answer = response.choices[0].text
                    # for el in answer[0:14]:
                    #     if el == ':':
                    #         answer = answer.split(':')[1]
                    answer = answer.replace('\n', '')

                    #отправка ответа пользователю и удаление прелоад-сообщения
                    await bot.send_message(message.from_user.id, answer, reply_markup=keybord_main)
                    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message_id)
                    #проверяем пользователя на наличие лимитов по подписке
                    if requests[0]["requests"] > 0 and days[0]["days"] == 0:
                        #если в подписке нет дней, снимаем 1 запрос
                        await sql_db.sql_minus_requests(message.from_user.id, requests[0]["requests"] - 1)
                    requests = await sql_db.sql_check_limit_requests(message.from_user.id)
                    #### print(context)
                    await sql_db.sql_add_context(message.from_user.id, message_text + '\n' + answer)
                else:
                    await bot.send_message(message.from_user.id, '⚠ У Вас закончилась подписка, необходимо ее продлить')
        else:
            await bot.send_message(message.from_user.id, 'Чтобы продолжить общение со мной, необходимо подписаться на этот канал https://t.me/techinpocket')

#предпродажа премиум-доступа
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

#продажа премиум-доступа
async def successful_payment(message: types.Message):
    req = 0
    prc = 0
    print("Successful payment:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")
    if message.successful_payment.total_amount // 100 == min_req_price:
        req = min_req
        prc = min_req_price
    elif message.successful_payment.total_amount // 100 == middle_req_price:
        req = middle_req
        prc = middle_req_price
    elif message.successful_payment.total_amount // 100 == max_req_price:
        req = max_req
        prc = max_req_price
    elif message.successful_payment.total_amount // 100 == maxlarge_req_price:
        req = maxlarge_req
        prc = maxlarge_req_price
    elif message.successful_payment.total_amount // 100 == min_day_price:
        req = min_day[1]
        prc = min_day_price
    elif message.successful_payment.total_amount // 100 == middle_day_price:
        req = middle_day[1]
        prc = middle_day_price
    elif message.successful_payment.total_amount // 100 == max_day_price:
        req = max_day[1]
        prc = max_day_price
    elif message.successful_payment.total_amount // 100 == maxlarge_day_price:
        req = maxlarge_day[1]
        prc = maxlarge_day_price

    if prc <= maxlarge_req_price:
        requests = await sql_db.sql_check_limit_requests(message.from_user.id)
        await sql_db.sql_plus_requests(message.from_user.id, requests[0]['requests'] + req)
        await bot.send_message(message.from_user.id, f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно")
    else:
        days = await sql_db.sql_check_limit_days(message.from_user.id)
        await sql_db.sql_plus_days(message.from_user.id, days[0]['days'] + req)
        await bot.send_message(message.from_user.id, f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно")

#подтверждние авторства по команде /создатель
async def check_author(message: types.Message):
    await bot.send_message(message.from_user.id, 'Этот бот принадлежит Родионову Ярославу')

#регистрация всех функций
def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(check_author, commands=['создатель'])
    dp.register_message_handler(successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT)
    dp.register_pre_checkout_query_handler(pre_checkout_query, lambda query: True)
    dp.register_message_handler(voice_handler, content_types=types.ContentType.VOICE)
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(btn_oppo, Text(equals="📜 Возможности"))
    dp.register_message_handler(btn_premium, Text(equals="👑 Премиум-доступ"))
    dp.register_message_handler(btn_endtalk, Text(equals="😕 Завершить диалог"))
    dp.register_callback_query_handler(ibtn_starttalk, filter_ibtn_starttalk)
    dp.register_callback_query_handler(ibtn_25, filter_ibtn_25)
    dp.register_callback_query_handler(ibtn_50, filter_ibtn_50)
    dp.register_callback_query_handler(ibtn_100, filter_ibtn_100)
    dp.register_callback_query_handler(ibtn_200, filter_ibtn_200)
    dp.register_callback_query_handler(ibtn_1week, filter_ibtn_1week)
    dp.register_callback_query_handler(ibtn_1month, filter_ibtn_1month)
    dp.register_callback_query_handler(ibtn_6month, filter_ibtn_6month)
    dp.register_callback_query_handler(ibtn_1year, filter_ibtn_1year)
    dp.register_message_handler(message_user)
