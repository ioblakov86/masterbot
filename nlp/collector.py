import os
import asyncio
from telethon import TelegramClient, events

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
DB_DSN = os.getenv("DB_DSN", "postgres://marketbot:marketbot@db:5432/marketbot")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def main():
    if not API_ID or not API_HASH:
        raise RuntimeError("API_ID or API_HASH not set")

    client = TelegramClient("collector_session", API_ID, API_HASH)

    await client.start()

    print("Telethon connected using bot token")

    @client.on(events.NewMessage)
    async def handler(event):
        print(f"Message: {event.text}")

    await client.run_until_disconnected()

if __name__ == "__main__":
    print("Collector container started")
    print("Starting Telethon...")
    asyncio.run(main())
