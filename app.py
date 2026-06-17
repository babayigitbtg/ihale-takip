import requests
from bs4 import BeautifulSoup

url = "https://www.kos.org.tr/directorate/auctions"

r = requests.get(url, timeout=30)

soup = BeautifulSoup(r.text, "html.parser")

text = soup.get_text("\n", strip=True)

for line in text.split("\n"):
    if len(line) > 20:
        print(line)
