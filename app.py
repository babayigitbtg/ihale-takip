import requests
from bs4 import BeautifulSoup

url = "https://www.konya.bel.tr/ihale"

r = requests.get(url, timeout=30)

soup = BeautifulSoup(r.text, "html.parser")

for h in soup.find_all(["h1", "h2", "h3", "h4", "h5", "a"]):
    text = h.get_text(" ", strip=True)

    if len(text) > 20:
        print(text)
