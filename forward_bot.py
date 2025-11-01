import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pyrogram import Client, filters
from pyrogram.types import Message

class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_http():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), PingHandler)
    print(f"HTTP server listening on port {port}")
    server.serve_forever()

t = threading.Thread(target=run_http, daemon=True)
t.start()

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

FORWARD_TO_CHAT_ID = int(os.environ["FORWARD_TO_CHAT_ID"])

client = Client("forwarder_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@client.on_message(filters.text | filters.photo | filters.video | filters.document)
async def forward_messages(_, message: Message):
    try:
        # Пересылаем любое сообщение
        await message.forward(chat_id=FORWARD_TO_CHAT_ID)
        print(f"Переслано сообщение от {message.from_user.id if message.from_user else 'аноним'}")
    except Exception as e:
        print(f"Ошибка пересылки: {e}")


@client.on_message(filters.command("start"))
async def start_handler(_, message: Message):
    await message.reply_text("✅ Бот активен и готов пересылать сообщения.")


if __name__ == "__main__":
    print("Запуск бота...")
    client.start()
    print("Бот успешно запущен и подключен к Telegram API.")
    client.run_until_disconnected()
