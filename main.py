import requests

# Buraya OpenWeatherMap'ten aldığın API Key'i yapıştır
api_key = "1ca5197dfc20f1b1e12e52d56269529e" 
sehir = "Istanbul"

# Hava durumu verisini çekmek için adresimiz
url = f"http://api.openweathermap.org/data/2.5/weather?q={sehir}&appid={api_key}&units=metric"

try:
    cevap = requests.get(url)
    veri = cevap.json()

    if cevap.status_code == 200:
        sicaklik = veri['main']['temp']
        durum = veri['weather'][0]['description']
        print(f"{sehir} için hava durumu: {sicaklik}°C ve {durum}")
    else:
        print("Eyvah! Bir şeyler ters gitti. API anahtarını kontrol et.")
except Exception as e:
    print(f"Hata olustu: {e}")