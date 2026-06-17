import requests
from bs4 import BeautifulSoup

url = "https://www.konya.bel.tr/ihale"

r = requests.get(url, timeout=30)

soup = BeautifulSoup(r.text, "html.parser")

for tag in soup.find_all(["div", "article", "li"]):
    text = tag.get_text(" ", strip=True)

    if "İhale Konusu" in text:
        print("=" * 80)
        print(text[:1000])
