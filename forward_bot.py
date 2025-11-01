import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telethon import TelegramClient, events

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

api_id = 26243748
api_hash = "7abdc6cfd59c3c18c70bc5bdf8e22c7b"

TARGET_CHAT_ID = "e_trade_e"

SOURCE_CHAT_ID = "testjqwu"

client = TelegramClient("forward_session", api_id, api_hash)

@client.on(events.NewMessage(chats=SOURCE_CHAT_ID))
async def forward_handler(event):
    try:
        msg = event.message
        await client.send_message(TARGET_CHAT_ID, msg)
        print(f"✅ Переслано сообщение id={msg.id}")
    except Exception as e:
        print(f"⚠️ Ошибка при пересылке: {e}")

print("🚀 Запуск клиента...")
client.start()
print("✅ Клиент успешно запущен и подключен.")
client.run_until_disconnected()
