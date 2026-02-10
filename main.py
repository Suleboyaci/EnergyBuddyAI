
import requests
import schedule
import time
import random

# 1. BİLGİLERİNİ GİR (Burayı doldurmayı unutma!)
WEATHER_API_KEY = "1ca5197dfc20f1b1e12e52d56269529e"
BOT_TOKEN = "8491666951:AAEZTAn6KknBAPpvciStMTu0Wb0tTYzkHSw"
CHAT_ID = "8582582914"
SEHIR = "Istanbul"

# --- 2. TEKNİK PARAMETRELER (Mühendislik Kabulleri) ---
PANEL_KAPASITESI = 5.0  # kW
ELEKTRIK_BIRIM_FIYATI = 2.60  # TL
gunluk_toplam_kazanc = 0.0  # Biriken miktar

# --- 3. ENERJİ TASARRUFU İPUÇLARI ---
ipuclari = [
    "💡 LED ampuller aydınlatma maliyetini %80'e kadar azaltabilir.",
    "🔌 Cihazları 'Stand-by' modunda bırakma, fişten çekmek tasarruf sağlar.",
    "🧺 Çamaşır makinesini tam yükte çalıştırmak su ve enerji tasarrufu sağlar.",
    "🌡️ Isıtıcıyı 1 derece kısmak, enerji faturanda %6 fark yaratabilir.",
    "☀️ Güneşli havalarda perdeleri açarak doğal ısıdan yararlan!"
]

# --- 4. ANA ANALİZ FONKSİYONU ---
def enerji_analizi_yap():
    global gunluk_toplam_kazanc, SEHIR, WEATHER_API_KEY, BOT_TOKEN, CHAT_ID
    
    print(f"\n--- {time.strftime('%H:%M:%S')} | Analiz Başlatılıyor ---")
    
    # Tüm değişkenleri büyük harf (global) halleriyle eşitledim
    url = f"http://api.openweathermap.org/data/2.5/weather?q={SEHIR}&appid={WEATHER_API_KEY}&units=metric"
    
    try:
        cevap = requests.get(url)
        veri = cevap.json()
        
        if cevap.status_code == 200:
            durum = veri['weather'][0]['main']
            sicaklik = veri['main']['temp']
            
            # Hava durumuna göre verimlilik katsayısı
            if durum == "Clear":
                verim = 0.90
                durum_tr = "☀️ Güneşli"
                tavsiye = "Maksimum üretim! Büyük cihazları şimdi çalıştır."
            elif durum == "Clouds":
                verim = 0.40
                durum_tr = "🌤️ Bulutlu"
                tavsiye = "Orta seviye üretim. Planlı kullanım önerilir."
            else:
                verim = 0.15
                durum_tr = f"🌧️ {durum}"
                tavsiye = "Düşük üretim. Gereksiz ışıkları kapat!"

            # Mühendislik Hesaplamaları
            anlik_uretim = PANEL_KAPASITESI * verim
            saatlik_kazanc_hizi = anlik_uretim * ELEKTRIK_BIRIM_FIYATI
            
            # 1 dakikalık periyot için kazanç ekleme
            dakikalik_kazanc = saatlik_kazanc_hizi / 60
            gunluk_toplam_kazanc += dakikalik_kazanc
            
            ipucu = random.choice(ipuclari)
            
            mesaj = (
                f"📊 *ENERGYBUDDY TEKNİK RAPOR*\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"📍 *Konum:* {SEHIR}\n"
                f"🌡️ *Sıcaklık:* {sicaklik}°C\n"
                f"☁️ *Hava:* {durum_tr}\n"
                f"⚡ *Anlık Üretim:* `{anlik_uretim:.2f} kW`\n"
                f"💰 *Kazanç Hızı:* `{saatlik_kazanc_hizi:.2f} TL/saat`\n"
                f"📈 *Bugün Biriken:* `{gunluk_toplam_kazanc:.2f} TL`\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"💡 *Öneri:* {tavsiye}\n\n"
                f"🌟 *Günün İpucu:* {ipucu}"
            )
            
            t_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            requests.get(t_url, params={"chat_id": CHAT_ID, "text": mesaj, "parse_mode": "Markdown"})
            print(f">>> Başarılı: {anlik_uretim:.2f} kW üretim raporlandı.")
            
        else:
            print(f"Hata: API verisi alınamadı. Kod: {cevap.status_code}")
            
    except Exception as e:
        print(f"Hata oluştu: {e}")

# --- 5. SİSTEMİ ÇALIŞTIR ---

# İlk rapor
enerji_analizi_yap()

# Her 1 dakikada bir otomatik çalışma
schedule.every(1).minutes.do(enerji_analizi_yap)

print(f"🚀 EnergyBuddyAI Aktif! (Şehir: {SEHIR})")
print("Durdurmak için Ctrl+C tuşuna bas.")

while True:
    schedule.run_pending()
    time.sleep(1)