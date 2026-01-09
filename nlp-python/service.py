import asyncio
from aiogram import Bot, Dispatcher, types
import asyncpg
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DB_DSN = "postgres://marketbot:marketbot@db:5432/marketbot"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def save_to_db(chat_id, message):
    conn = await asyncpg.connect(dsn=DB_DSN)
    await conn.execute(
        "INSERT INTO raw_messages(chat_id, message_id, sender, text) VALUES($1,$2,$3,$4)",
        chat_id, message.message_id, message.from_user.username, message.text
    )
    await conn.close()

@dp.message_handler()
async def handle_message(message: types.Message):
    await save_to_db(message.chat.id, message)

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
