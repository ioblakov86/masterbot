from telethon.sync import TelegramClient
from telethon.sessions import StringSession

API_ID = 21879738
API_HASH = "49f3531be2f9b7860b5c941b2ed27b7e"

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print("\n===== TELETHON SESSION =====\n")
    print(client.session.save())
    print("\n============================\n")

