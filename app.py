import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings()

url = "https://www.ilan.gov.tr/ilan/kategori/9/ihale-duyurulari?aci=62&txv=9&field=publish_time&order=desc"

r = requests.get(
    url,
    verify=False,
    timeout=30
)

soup = BeautifulSoup(r.text, "html.parser")

text = soup.get_text("\n", strip=True)

for line in text.split("\n"):
    if len(line) > 20:
        print(line)
