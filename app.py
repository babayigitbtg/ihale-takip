import requests
from bs4 import BeautifulSoup

url = "https://www.kos.org.tr/directorate/auctions"

r = requests.get(url, timeout=30)
soup = BeautifulSoup(r.text, "html.parser")

for a in soup.find_all("a", href=True):
    text = a.get_text(" ", strip=True)

    if len(text) > 10:
        print(text)
