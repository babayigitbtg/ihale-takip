import requests
from bs4 import BeautifulSoup

url = "https://www.konya.bel.tr/ihale"

r = requests.get(url, timeout=30)

print("STATUS:", r.status_code)

soup = BeautifulSoup(r.text, "html.parser")

for a in soup.find_all("a"):
    text = a.get_text(strip=True)

    if len(text) > 20:
        print(text)
