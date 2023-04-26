from aiogram.types import CallbackQuery
from create_bot import bot
import os
from aiogram import types
from config import TOKENPAY
from price import *

#фильтры отлова колбэков
async def filter_ibtn_starttalk(callback : CallbackQuery):
    return callback.data == 'ibtn_starttalk'
async def filter_ibtn_25(callback : CallbackQuery):
    return callback.data == 'ibtn_25'
async def filter_ibtn_50(callback : CallbackQuery):
    return callback.data == 'ibtn_50'
async def filter_ibtn_100(callback : CallbackQuery):
    return callback.data == 'ibtn_100'
async def filter_ibtn_200(callback : CallbackQuery):
    return callback.data == 'ibtn_200'
async def filter_ibtn_1week(callback : CallbackQuery):
    return callback.data == 'ibtn_1week'
async def filter_ibtn_1month(callback : CallbackQuery):
    return callback.data == 'ibtn_1month'
async def filter_ibtn_6month(callback : CallbackQuery):
    return callback.data == 'ibtn_6month'
async def filter_ibtn_1year(callback : CallbackQuery):
    return callback.data == 'ibtn_1year'


async def ibtn_starttalk(callback : CallbackQuery):
    await bot.answer_callback_query(callback.id)
    await bot.send_message(callback.from_user.id, 'Диалог начат. Ты можешь подстраивать меня под себя и придумывать  различные сценарии/правила, которым я буду следовать. Нажми в меню Завершить диалог, чтобы сбросить мою память.')

async def ibtn_25(callback : CallbackQuery):
    await bot.answer_callback_query(callback.id)
    img = 'https://i.ibb.co/0r11JRj/25.jpg'
    await invoice_requests(callback.from_user.id, min_req, min_req_price, img)

async def ibtn_50(callback : CallbackQuery):
    await bot.answer_callback_query(callback.id)
    img = 'https://i.ibb.co/LQMQjH7/50.jpg'
    await invoice_requests(callback.from_user.id, middle_req, middle_req_price, img)

async def ibtn_100(callback : CallbackQuery):
    await bot.answer_callback_query(callback.id)
    img = 'https://i.ibb.co/JctGbf5/100.jpg'
    await invoice_requests(callback.from_user.id,max_req, max_req_price, img)

async def ibtn_200(callback : CallbackQuery):
    await bot.answer_callback_query(callback.id)
    img = 'https://i.ibb.co/4NLQKPD/200.jpg'
    await invoice_requests(callback.from_user.id, maxlarge_req, maxlarge_req_price, img)

async def ibtn_1week(callback : CallbackQuery):
    await bot.answer_callback_query(callback.id)
    img = 'https://i.ibb.co/Gc9TrW1/1w.jpg'
    await invoice_days(callback.from_user.id, min_day[0], min_day_price, img)

async def ibtn_1month(callback : CallbackQuery):
    await bot.answer_callback_query(callback.id)
    img = 'https://i.ibb.co/V9WrwTB/1m.jpg'
    await invoice_days(callback.from_user.id, middle_day[0], middle_day_price, img)

async def ibtn_6month(callback : CallbackQuery):
    await bot.answer_callback_query(callback.id)
    img = 'https://i.ibb.co/nkHqH6p/6m.jpg'
    await invoice_days(callback.from_user.id, max_day[0], max_day_price, img)

async def ibtn_1year(callback : CallbackQuery):
    await bot.answer_callback_query(callback.id)
    img = 'https://i.ibb.co/Nj6RmCv/1y.jpg'
    await invoice_days(callback.from_user.id, maxlarge_day[0], maxlarge_day_price, img)

        
async def invoice_requests(userid, req, prc, img):
    PRICE = types.LabeledPrice(label=f"{req} запросов к ChatGPT", amount=prc*100) # в копейках
    if TOKENPAY.split(':')[1] == 'LIVE':
        # await bot.send_message(userid, 'Тестовый платеж!!!')
        await bot.send_invoice(userid,
                            title='Премиум-доступ',
                            description=f'Покупка {req} запросов к ChatGPT',
                            provider_token=TOKENPAY,
                            currency='rub',
                            photo_url=img,
                            photo_width=720,
                            photo_height=420,
                            photo_size=720,
                            is_flexible=False,
                            prices=[PRICE],
                            start_parameter="one-month-subscription",
                            payload="test-invoice-payload")

async def invoice_days(userid, day, prc, img):
    PRICE = types.LabeledPrice(label=f"Доступ сроком {day} к ChatGPT", amount=prc*100) # в копейках
    if TOKENPAY.split(':')[1] == 'LIVE':
        # await bot.send_message(userid, 'Тестовый платеж!!!')
        await bot.send_invoice(userid,
                            title='Премиум-доступ',
                            description=f'Покупка премиум-доступа на {day} к ChatGPT',
                            provider_token=TOKENPAY,
                            currency='rub',
                            photo_url=img,
                            photo_width=720,
                            photo_height=420,
                            photo_size=720,
                            is_flexible=False,
                            prices=[PRICE],
                            start_parameter="one-month-subscription",
                            payload="test-invoice-payload")

# ibtn_25
# ibtn_50
# ibtn_100
# ibtn_200
# ibtn_1week 
# ibtn_1month
# ibtn_6month
# ibtn_1year 

# async def ibtn_25(callback : CallbackQuery):
#     PRICE = types.LabeledPrice(label="25 запросов к ChatGPT", amount=60*100) # в копейках
#     await bot.answer_callback_query(callback.id)
#     if TOKENPAY.split(':')[1] == 'TEST':
#         await bot.send_message(callback.from_user.id, 'Тестовый платеж!!!')
#         await bot.send_invoice(callback.from_user.id,
#                             title='Премиум-доступ',
#                             description='Покупка 25 запросов к ChatGPT',
#                             provider_token=TOKENPAY,
#                             currency='rub',
#                             photo_url='https://i.ibb.co/yPhDhB5/25.jpg',
#                             photo_width=720,
#                             photo_height=420,
#                             photo_size=720,
#                             is_flexible=False,
#                             prices=[PRICE],
#                             start_parameter="one-month-subscription",
#                             payload="test-invoice-payload")