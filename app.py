import os
import json
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def telegram(msg):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": msg
        },
        timeout=30
    )


def konya_belediye():
    url = "https://www.konya.bel.tr/ihale"

    r = requests.get(url, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")

    text = soup.get_text("\n", strip=True)

    ilanlar = []

    for line in text.split("\n"):
        if "İhale Konusu " in line and " İhale Sahibi " in line:
            baslik = line.split("İhale Konusu ")[1].split(" İhale Sahibi")[0].strip()
            ilanlar.append(baslik)

    return ilanlar


def konya_valilik():
    url = "https://www.konya.gov.tr/ihale-ilanlari"

    r = requests.get(url, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")

    ilanlar = []

    for line in soup.get_text("\n", strip=True).split("\n"):

        line = line.strip()

        if len(line) < 10:
            continue

        if "İşi" in line or "Alımı" in line:
            ilanlar.append(line)

    return list(set(ilanlar))


def kos():
    url = "https://www.kos.org.tr/directorate/auctions"

    r = requests.get(url, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")

    ilanlar = []

    for line in soup.get_text("\n", strip=True).split("\n"):

        line = line.strip()

        if len(line) < 10:
            continue

        if line != "İndirmek İçin Tıklayınız":
            ilanlar.append(line)

    return list(set(ilanlar))


try:
    with open("seen.json", "r", encoding="utf-8") as f:
        seen = json.load(f)
except:
    seen = {
        "Konya Büyükşehir Belediyesi": [],
        "Konya Valiliği": [],
        "KOS": []
    }


SITES = {
    "Konya Büyükşehir Belediyesi": konya_belediye,
    "Konya Valiliği": konya_valilik,
    "KOS": kos
}

for site_name, func in SITES.items():

    try:
        current = func()

        old = set(seen.get(site_name, []))
        new = set(current)

        fark = new - old

        if old:

            for ilan in fark:

                telegram(
                    f"🔔 Yeni İhale\n\n"
                    f"{ilan}\n\n"
                    f"Kaynak: {site_name}"
                )

                print("Yeni:", ilan)

        seen[site_name] = current

    except Exception as e:
        print(site_name, e)

with open("seen.json", "w", encoding="utf-8") as f:
    json.dump(seen, f, ensure_ascii=False, indent=2)
