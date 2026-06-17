import requests

url = "url = "https://www.konya.bel.tr/ihale""

r = requests.get(url, timeout=30)

print("STATUS:", r.status_code)
print(r.text[:2000])
