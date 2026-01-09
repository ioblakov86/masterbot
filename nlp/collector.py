import os
import asyncio
from telethon import TelegramClient, events

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set in environment")

    client = TelegramClient("collector_session", API_ID, API_HASH)

    await client.start(bot_token=BOT_TOKEN)

    print("Telethon connected using bot token")

    @client.on(events.NewMessage)
    async def handler(event):
        print(f"Message: {event.text}")

    await client.run_until_disconnected()

if __name__ == "__main__":
    print("Collector container started")
    print("Starting Telethon...")
    asyncio.run(main())
