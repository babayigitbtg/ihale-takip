import requests

url = "https://ihaleciler.com/tenders/search?workcategory_in=37&workcategory_in=39&workcategory_in=505&workcategory_in=507&province_in=Aksaray&province_in=Karaman&province_in=Konya&province_in=Nev%C5%9Fehir&tender_ts_meta=&buyermeta_ts=&contentlast_gte=&contentlast_lte=&offerend_gte=&offerend_lte=&workterm_gte=&workterm_lte=&workdelivery_gte=&workdelivery_lte=&workpayment_gte=&workpayment_lte=&display=advanced"

r = requests.get(url, timeout=30)

print("STATUS:", r.status_code)
print(r.text[:2000])
