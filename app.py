import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

requests.get(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    params={
        "chat_id": CHAT_ID,
        "text": "✅ GitHub Actions üzerinden ilk test mesajı geldi."
    }
)

print("Mesaj gönderildi")
