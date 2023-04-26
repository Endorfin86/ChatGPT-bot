from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

#главная клавиатура
btn_endtalk = KeyboardButton('😕 Завершить диалог')
btn_oppo = KeyboardButton('📜 Возможности')
btn_premium = KeyboardButton('👑 Премиум-доступ')
keybord_main = ReplyKeyboardMarkup(resize_keyboard=True).row(btn_oppo, btn_premium).add(btn_endtalk)

#inline-клавиатура под вызываемым сообщением с кнопки главного меню "Возможности"
ibtn_starttalk = InlineKeyboardButton('Начать диалог', callback_data='ibtn_starttalk')
ikeyboard_oppo = InlineKeyboardMarkup().add(ibtn_starttalk)

#inline-клавиатура под вызываемым сообщением с кнопки главного меню "Премиум-доступ"
ibtn_25 = InlineKeyboardButton('25 шт - 60₽', callback_data='ibtn_25')
ibtn_50 = InlineKeyboardButton('50 шт - 89₽', callback_data='ibtn_50')
ibtn_100 = InlineKeyboardButton('100 шт - 129₽', callback_data='ibtn_50')
ibtn_200 = InlineKeyboardButton('200 шт - 199₽', callback_data='ibtn_200')
ibtn_1week = InlineKeyboardButton('1 неделя - 299₽', callback_data='ibtn_1week')
ibtn_1month = InlineKeyboardButton('1 месяц - 499₽', callback_data='ibtn_1month')
ibtn_6month = InlineKeyboardButton('6 месяцев - 999₽', callback_data='ibtn_6month')
ibtn_1year = InlineKeyboardButton('1 год - 1499₽', callback_data='ibtn_1year')

ikeyboard_premium = InlineKeyboardMarkup().row(ibtn_25, ibtn_50).row(ibtn_100, ibtn_200).row(ibtn_1week, ibtn_1month).row(ibtn_6month, ibtn_1year)