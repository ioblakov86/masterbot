import os
import asyncio
from aiogram import Bot, Dispatcher, types
import asyncpg

# ==== ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ ====
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DB_DSN = os.getenv("DB_DSN", "postgres://marketbot:marketbot@db:5432/marketbot")

if TOKEN is None:
    raise ValueError("TELEGRAM_BOT_TOKEN not set!")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ==== ФУНКЦИЯ СОХРАНЕНИЯ СООБЩЕНИЙ С ЦЕНОЙ ====
async def save_to_db(message: types.Message, price: float = None):
    conn = await asyncpg.connect(dsn=DB_DSN)
    await conn.execute(
        "INSERT INTO raw_messages(chat_id, message_id, sender, text, price) VALUES($1,$2,$3,$4,$5)",
        message.chat.id,
        message.message_id,
        message.from_user.username,
        message.text,
        price
    )
    await conn.close()

# ==== ОБРАБОТЧИК СООБЩЕНИЙ ====
async def handle_message(message: types.Message):
    # Попробуем извлечь цену из текста (например, числа в сообщении)
    import re
    prices = re.findall(r'\d+', message.text.replace(',', ''))
    price = float(prices[0]) if prices else None

    print(f"New message from {message.from_user.username}: {message.text}, price={price}")
    await save_to_db(message, price)

dp.message.register(handle_message)

# ==== КОМАНДА /top5 ПО ЦЕНЕ ====
async def top5_command(message: types.Message):
    conn = await asyncpg.connect(dsn=DB_DSN)
    
    # Берем топ-5 самых дорогих объявлений
    rows = await conn.fetch(
        "SELECT text, sender, price FROM raw_messages WHERE price IS NOT NULL ORDER BY price DESC LIMIT 5"
    )
    await conn.close()

    if not rows:
        await message.answer("Нет объявлений с ценой.")
        return

    # Первые 4 — без контакта
    for r in rows[:4]:
        await message.answer(f"Объявление: {r['text']}\nЦена: {r['price']}")

    # 5-е объявление — с контактом
    last = rows[4]
    await message.answer(f"ТОП объявление:\n{last['text']}\nЦена: {last['price']}\nКонтакт: {last['sender']}")

# Регистрируем команду
dp.message.register(top5_command, lambda m: m.text and m.text.lower() == "/top5")

# ==== ЗАПУСК БОТА ====
async def main():
    print("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
