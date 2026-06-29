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

    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=60
    )

    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(" ", strip=True)

    ilanlar = []

    parts = text.split("İhale Konusu")

    for part in parts[1:]:
        if "İhale Sahibi" in part:
            baslik = part.split("İhale Sahibi")[0].strip()

            if len(baslik) > 10:
                ilanlar.append(baslik)

    return list(set(ilanlar))


def konya_valilik():
    url = "https://www.konya.gov.tr/ihale-ilanlari"

    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30
    )

    soup = BeautifulSoup(r.text, "html.parser")

    ilanlar = []

    for line in soup.get_text("\\n", strip=True).split("\\n"):
        line = line.strip()

        if len(line) < 10:
            continue

        if (
            "İşi" in line
            or "Alımı" in line
            or "İhalesi" in line
            or "İhale" in line
        ):
            ilanlar.append(line)

    return list(set(ilanlar))


def kos():
    url = "https://www.kos.org.tr/directorate/auctions"

    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30
    )

    soup = BeautifulSoup(r.text, "html.parser")

    ilanlar = []

    for line in soup.get_text("\\n", strip=True).split("\\n"):
        line = line.strip()

        if len(line) < 10:
            continue

        if line == "İndirmek İçin Tıklayınız":
            continue

        ilanlar.append(line)

    return list(set(ilanlar))


DEFAULT_SEEN = {
    "Konya Büyükşehir Belediyesi": [],
    "Konya Valiliği": [],
    "KOS": []
}

try:
    with open("seen.json", "r", encoding="utf-8") as f:
        seen = json.load(f)
except Exception:
    seen = DEFAULT_SEEN

SITES = {
    "Konya Büyükşehir Belediyesi": konya_belediye,
    "Konya Valiliği": konya_valilik,
    "KOS": kos
}

for site_name, func in SITES.items():

    try:

        current = func()

        print(f"{site_name} -> Toplam ilan: {len(current)}")

        old = set(seen.get(site_name, []))
        new = set(current)

        yeni_ilanlar = new - old

        print(f"{site_name} -> Seen: {len(old)}")
        print(f"{site_name} -> Yeni ilan: {len(yeni_ilanlar)}")

        if len(old) > 0:

            for ilan in sorted(yeni_ilanlar):

                telegram(
                    f"🔔 Yeni İhale\n\n"
                    f"{ilan}\n\n"
                    f"Kaynak: {site_name}"
                )

                print(f"YENI IHALE -> {site_name} -> {ilan}")

        seen[site_name] = current

    except Exception as e:

        print(f"HATA ({site_name}): {e}")

with open("seen.json", "w", encoding="utf-8") as f:
    json.dump(
        seen,
        f,
        ensure_ascii=False,
        indent=2
    )

print("Kontrol tamamlandi")
