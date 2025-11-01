import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_http():
    port = int(os.environ.get("PORT", 8000)) 
    server = HTTPServer(("0.0.0.0", port), PingHandler)
    print(f"HTTP server listening on port {port}")
    server.serve_forever()
    
t = threading.Thread(target=run_http, daemon=True)
t.start()

client.start()
client.run_until_disconnected()


import re
from telethon import TelegramClient, events, errors
api_id = 26243748
api_hash = "3aed6ebb8ff9315b4d1eef9fc8a317a7"
session_name = 'my_forwarder'
source_channel = 'zagovor_likvid'
target_channel = '@_trade_e'
MENTION_REPLACEMENT = '@'
LINK_REPLACEMENT = '@'
client = TelegramClient(session_name, api_id, api_hash)
client = TelegramClient(session_name, api_id, api_hash)

def clean_text(text: str) -> str:
    if not text:
        return text
    text = re.sub(r'@[\w_]+', MENTION_REPLACEMENT, text)
    text = re.sub(r'https?://\S+', LINK_REPLACEMENT, text)
    return text

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    msg = event.message
    try:
        text = msg.message or ''
        new_text = clean_text(text)

        if msg.media:
            await client.send_message(target_channel, new_text, file=msg.media)
        else:
            await client.send_message(target_channel, new_text)

        print(f"✅ Переслано сообщение id={msg.id}")
    except errors.FloodWait as e:
        print(f"⏳ FloodWait: ждём {e.seconds} секунд")
    except Exception as e:
        print("⚠️ Ошибка при пересылке:", e)

def main():
    print("🚀 Запуск...")
    client.start()  
    print("✅ Готово, бот слушает канал...")
    client.run_until_disconnected()

if __name__ == '__main__':
    main()
