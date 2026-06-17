import requests
from bs4 import BeautifulSoup

url = "https://www.konya.bel.tr/ihale"

r = requests.get(url, timeout=30)
soup = BeautifulSoup(r.text, "html.parser")

cards = soup.find_all(["div", "article", "section"])

for i, card in enumerate(cards[:100]):
    text = card.get_text(" ", strip=True)

    if "İhale Konusu" in text:
        print("\n" + "="*50)
        print("TAG:", card.name)
        print("CLASS:", card.get("class"))
        print(text[:500])
