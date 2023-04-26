from create_bot import bot
import asyncpg
import time
import datetime
import asyncio

#подключаемся к базе данных и создаем таблицу пользователи, если такой нет
async def sql_start():
    global pool
    pool = await asyncpg.create_pool(
        user='postgres',
        password='postgres',
        database='botgpt',
        host='postgres',
        port=5432
    )
    await pool.execute("CREATE TABLE IF NOT EXISTS users (userid NUMERIC(20) PRIMARY KEY, username VARCHAR(50) DEFAULT '', subscription BOOLEAN NOT NULL DEFAULT FALSE, days INTEGER NOT NULL DEFAULT 0, requests INTEGER NOT NULL DEFAULT 5, context TEXT DEFAULT '', UNIQUE (userid))")
    print('Бот запущен')

async def sql_minus_day():
    while True:
        await pool.execute("UPDATE users SET days = days - 1 WHERE days > 0")
        await asyncio.sleep(86400)

#создаем пользователя
async def sql_create_user(message):
    username = message.from_user.username
    userid = message.from_user.id
    if username == None:
        await pool.execute("INSERT INTO users VALUES ($1, $2, $3, $4, $5, $6) ON CONFLICT (userid) DO NOTHING", userid, 'no_username', False, 0, 5, '')
    else:    
        await pool.execute("INSERT INTO users VALUES ($1, $2, $3, $4, $5, $6) ON CONFLICT (userid) DO NOTHING", userid, username, False, 0, 5, '')

#проверяем пользователя на наличие в базе данных
async def sql_check_user(userid):
    user = await pool.fetch("SELECT * FROM users WHERE userid = $1", userid)
    return user

#проверяем лимит пользователя по дням
async def sql_check_limit_days(userid):
    days = await pool.fetch("SELECT days FROM users WHERE userid = $1", userid)
    return days

#плюсуем дни к лимиту пользователя за покупку премиум
async def sql_plus_days(userid, day):
    await pool.execute("UPDATE users SET days = $1 WHERE userid = $2", day, userid)

#проверяем лимит пользователя по запросам
async def sql_check_limit_requests(userid):
    requests = await pool.fetch("SELECT requests FROM users WHERE userid = $1", userid)
    return requests

#минусуем 1 запрос из лимита пользователя по запросам
async def sql_minus_requests(userid, requests):
    days = await pool.execute("UPDATE users SET requests = $1 WHERE userid = $2", requests, userid)

#плюсуем запросы к лимиту пользователя за покупку премиум
async def sql_plus_requests(userid, request):
    await pool.execute("UPDATE users SET requests = $1 WHERE userid = $2", request, userid)

#добавляем пользователю в поле context написанный им текст
async def sql_add_context(userid, text):
    await pool.execute("UPDATE users SET context = $1 WHERE userid = $2", text, userid)

#добавляем пользователю в поле context написанный им текст
async def sql_get_context(userid):
    context = await pool.fetch("SELECT context FROM users WHERE userid = $1", userid)
    return context[0]['context']

#очишаем поле context у пользователя
async def sql_clear_context(userid, text):
    await pool.execute("UPDATE users SET context = $1 WHERE userid = $2", text, userid)
