import os
import json
import hashlib
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings()

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

SITES = {
    "Konya Büyükşehir Belediyesi": "https://www.konya.bel.tr/ihale",
    "Konya Valiliği": "https://www.konya.gov.tr/ihale-ilanlari",
    "KOS": "https://www.kos.org.tr/directorate/auctions",
    "ilan.gov.tr": "https://www.ilan.gov.tr/ilan/kategori/9/ihale-duyurulari?aci=62&txv=9&field=publish_time&order=desc"
}


def send_message(text):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": text
        },
        timeout=30
    )


try:
    with open("seen.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except:
    data = {"sites": {}}

changed = False

for site_name, url in SITES.items():

    try:
        r = requests.get(
            url,
            timeout=30,
            verify=False,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        if r.status_code != 200:
            print(site_name, r.status_code)
            continue

        soup = BeautifulSoup(r.text, "html.parser")

        text = soup.get_text(" ", strip=True)

        page_hash = hashlib.md5(
            text.encode("utf-8")
        ).hexdigest()

        old_hash = data["sites"].get(site_name)

        if old_hash is None:
            data["sites"][site_name] = page_hash
            changed = True
            print(site_name, "ilk kayıt")

        elif old_hash != page_hash:

            send_message(
                f"🔔 Yeni ilan/ihale değişikliği tespit edildi\n\n"
                f"Kaynak: {site_name}\n"
                f"Link: {url}"
            )

            data["sites"][site_name] = page_hash
            changed = True

            print(site_name, "değişiklik bulundu")

        else:
            print(site_name, "değişiklik yok")

    except Exception as e:
        print(site_name, str(e))

with open("seen.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
