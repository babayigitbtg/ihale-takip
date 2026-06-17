import requests

urls = [
    "https://www.konya.gov.tr/ihale-ilanlari",
    "https://www.kos.org.tr/directorate/auctions",
    "https://www.ilan.gov.tr/ilan/kategori/9/ihale-duyurulari?aci=62&txv=9&field=publish_time&order=desc",
    "https://ekapv2.kik.gov.tr/ekap/search"
]

for url in urls:
    try:
        r = requests.get(url, timeout=30)
        print(url)
        print("STATUS:", r.status_code)
        print("-" * 50)
    except Exception as e:
        print(url)
        print("HATA:", e)
        print("-" * 50)
