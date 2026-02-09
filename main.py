
import requests
import schedule
import time

# 1. BİLGİLERİNİ GİR (Burayı doldurmayı unutma!)
weather_api_key = "1ca5197dfc20f1b1e12e52d56269529e"
bot_token = "8491666951:AAEZTAn6KknBAPpvciStMTu0Wb0tTYzkHSw"
chat_id = "8582582914"
sehir = "Istanbul"

def analiz_yap_ve_gonder():
    print("--- Sistem Calisiyor: Veri Cekiliyor ---")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={sehir}&appid={weather_api_key}&units=metric"
    
    try:
        cevap = requests.get(url)
        veri = cevap.json()
        
        if cevap.status_code == 200:
            durum = veri['weather'][0]['main']
            sicaklik = veri['main']['temp']
            mesaj = f"EnergyBuddy Raporu 🚀\nSehir: {sehir}\nDurum: {durum}\nSicaklik: {sicaklik}C\nSistem her 1 dakikada bir kontrol yapacak."
            
            t_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            requests.get(t_url, params={"chat_id": chat_id, "text": mesaj})
            print(">>> Telegram mesaji basariyla gonderildi!")
        else:
            print(f"Hata: API cevap vermedi. Kod: {cevap.status_code}")
            
    except Exception as e:
        print(f"Hata olustu: {e}")

# Kodu calistirdigin an ilk mesaji atsin:
analiz_yap_ve_gonder()

# Sonra her 1 dakikada bir kursun:
schedule.every(1).minutes.do(analiz_yap_ve_gonder)

print("EnergyBuddy aktif! Kapatmak icin Ctrl+C yapabilirsin.")

while True:
    schedule.run_pending()
    time.sleep(1)