import requests
from bs4 import BeautifulSoup

url = "https://www.konya.bel.tr/ihale"

r = requests.get(url, timeout=30)
soup = BeautifulSoup(r.text, "html.parser")

for tag in soup.find_all(True):
    text = tag.get_text(" ", strip=True)

    if "Karahüyük Mahallesi" in text:
        print("=" * 50)
        print("TAG:", tag.name)
        print("CLASS:", tag.get("class"))
        print("ID:", tag.get("id"))
        print(text[:300])
        break
