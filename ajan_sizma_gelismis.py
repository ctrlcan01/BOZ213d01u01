import tkinter as tk
from tkinter import messagebox
import json
import os
import random
from datetime import datetime

# --- AYARLAR ---
BASLANGIC_SURESI = 60      # saniye (istersen 30 yapabilirsin)
CEZA = 10                  # yanlış cevapta düşen süre
BG = "#050505"
YESIL = "#33ff33"
KIRMIZI = "#ff3333"

# JSON dosyaları, bu .py dosyasının bulunduğu klasöre kaydedilir
KLASOR = os.path.dirname(os.path.abspath(__file__))
KULLANICI_DOSYASI = os.path.join(KLASOR, "kullanicilar.json")
SKOR_DOSYASI = os.path.join(KLASOR, "ajan_verileri.json")

# Program açılır açılmaz dosyalar yoksa hemen oluşturulur
if not os.path.exists(KULLANICI_DOSYASI):
    with open(KULLANICI_DOSYASI, "w", encoding="utf-8") as f:
        json.dump({}, f)
if not os.path.exists(SKOR_DOSYASI):
    with open(SKOR_DOSYASI, "w", encoding="utf-8") as f:
        f.write("")

# --- İÇERİK HAVUZU (Konulara Göre Ayrıldı) ---
KATEGORILER = {
    "A": {
        "ag_adi": "ÜNİVERSİTE AĞI",
        "oyun_turu": "SİNYAL YAKALAMA (Refleks)",
        "sorular": [
            {"soru": "Dersten bırakmak için Mehmet Hoca'nın sevdiği not?", "cevap": "49", "veri": "300 adet kedi fotoğrafı bulundu."},
            {"soru": "Öğrenci işlerinde sabır seviyesi (1-10)?", "cevap": "10", "veri": "Sistemde arıza yok, fişi çekip çaya gittik."}
        ]
    },
    "B": {
        "ag_adi": "DEVLET SIRLARI",
        "oyun_turu": "GÜVENLİK DUVARI (Zamanlama)",
        "sorular": [
            {"soru": "Dünyayı yöneten 4 harfli örgüt? (İpucu: V ile başlar)", "cevap": "vize", "veri": "Uzaylılar yok, herkes yorgun olduğu için öyle sanıyor."},
            {"soru": "Gizli uzay programının bütçesi neye harcandı?", "cevap": "çay", "veri": "Mars biletleri iptal edildi. Parayla çay alındı."}
        ]
    },
    "C": {
        "ag_adi": "PERSONEL AĞI",
        "oyun_turu": "VERİ YOLU (Hafıza)",
        "sorular": [
            {"soru": "Kampüsteki ortalama kedi sayısı? (Sayı gir)", "cevap": "50", "veri": "Kediler aslında rektörlüğe çalışan ajanlardır."},
            {"soru": "Güvenlik görevlisinin en sevdiği kelime?", "cevap": "kimlik", "veri": "Görevlinin gözünde herkes potansiyel tehlikedir."}
        ]
    },
    "D": {
        "ag_adi": "YEMEKHANE AĞI",
        "oyun_turu": "KABA KUVVET (Brute Force)",
        "sorular": [
            {"soru": "Etli yemeğin içindeki et oranı kaçtır? (Sadece sayı)", "cevap": "1", "veri": "1 kg ete 99 kg patates ekle ve dua et."},
            {"soru": "Çorbanın gizli maddesi nedir?", "cevap": "su", "veri": "Çorba %99 su, %1 hayal gücünden oluşmaktadır."}
        ]
    }
}

# --- SİSTEM HAFIZASI ---
durum = {
    "kullanici": "",
    "sure": BASLANGIC_SURESI,
    "secilen_ag": None,
    "oyun_aktif": False,
    "aktif_soru": None,
    "son_soru": None,
    # Zamanlayıcı kimlikleri (tekrar başlatırken iptal etmek için)
    "sayac_id": None,
    "yakalanma_sayaci": None,
    "flas_id": None,
    "mg_id": None,
    # Minigame değişkenleri
    "mg_sayac": 0,
    "mg_yon": 1,
    "mg_aktif": False
}


# --- YARDIMCI FONKSİYONLAR ---
def sadelestir(metin):
    """Büyük/küçük harf ve Türkçe karakter farkını yok sayar (çay = ÇAY = cay)."""
    metin = metin.strip().replace("İ", "i").replace("I", "ı").lower()
    return metin.translate(str.maketrans("çğıöşü", "cgiosu"))


def kullanicilari_oku():
    try:
        with open(KULLANICI_DOSYASI, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def zamanlayicilari_iptal_et():
    """Bekleyen tüm after() işlemlerini iptal eder (çift sayaç hatasını önler)."""
    for anahtar in ("sayac_id", "yakalanma_sayaci", "flas_id", "mg_id"):
        if durum[anahtar] is not None:
            pencere.after_cancel(durum[anahtar])
            durum[anahtar] = None


def mg_iptal():
    if durum["mg_id"] is not None:
        pencere.after_cancel(durum["mg_id"])
        durum["mg_id"] = None


def renk_ayarla(bg, ana_renk, ikincil):
    """Ekranın genel renklerini değiştirir (yanıp sönme efekti için)."""
    pencere.config(bg=bg)
    oyun_cercevesi.config(bg=bg)
    baslik_etiketi.config(bg=bg, fg=ana_renk)
    hosgeldin_etiketi.config(bg=bg, fg=ikincil)
    sure_etiketi.config(bg=bg, fg=ana_renk)
    log_etiketi.config(bg=bg, fg=ana_renk)


def sure_goster():
    renk = KIRMIZI if durum["sure"] <= 10 else "white"
    sure_etiketi.config(text=f"00:{durum['sure']:02d}", fg=renk)


# --- GİRİŞ SİSTEMİ ---
def kayit_ol():
    k_adi = k_adi_giris.get().strip()
    sifre = sifre_giris_kutusu.get().strip()
    if k_adi == "" or sifre == "":
        messagebox.showwarning("HATA", "Veriler boş bırakılamaz.")
        return
    k = kullanicilari_oku()
    if k_adi in k:
        messagebox.showerror("RET", "Bu kimlik zaten var.")
    else:
        k[k_adi] = sifre
        with open(KULLANICI_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(k, f, ensure_ascii=False)
        messagebox.showinfo("ONAY", "Kimlik oluşturuldu. Giriş yapın.")


def giris_yap(event=None):
    k_adi = k_adi_giris.get().strip()
    sifre = sifre_giris_kutusu.get().strip()
    k = kullanicilari_oku()
    if k_adi in k and k[k_adi] == sifre:
        durum["kullanici"] = k_adi
        giris_cercevesi.pack_forget()
        baslik_etiketi.config(text="AJAN SIZMA")
        oyun_cercevesi.pack(pady=10, fill="both", expand=True)
        hosgeldin_etiketi.config(text=f"KİMLİK: AJAN {k_adi.upper()}")
        ag_secim_ekranini_ac()
    else:
        messagebox.showerror("RET", "Geçersiz kimlik.")


# --- 1. AŞAMA: AĞ SEÇİMİ ---
def ag_secim_ekranini_ac():
    zamanlayicilari_iptal_et()
    durum["sure"] = BASLANGIC_SURESI
    durum["oyun_aktif"] = True
    durum["mg_aktif"] = False
    durum["aktif_soru"] = None

    renk_ayarla(BG, "white", "gray")
    sure_goster()
    log_etiketi.config(text="Erişmek istediğiniz ağı seçin...", fg="white")
    tekrar_dene_btn.pack_forget()
    soru_cercevesi.pack_forget()
    minigame_cercevesi.pack_forget()

    ag_cercevesi.pack(pady=20)
    durum["sayac_id"] = pencere.after(1000, geri_sayim)


def ag_sec(ag_kodu):
    if not durum["oyun_aktif"]:
        return
    durum["secilen_ag"] = ag_kodu
    ag_cercevesi.pack_forget()

    kategori = KATEGORILER[ag_kodu]
    log_etiketi.config(text=f"Güvenlik Duvarı Aktif: {kategori['oyun_turu']}")
    minigame_baslat(ag_kodu)


# --- 2. AŞAMA: MİNİ OYUNLAR ---
def minigame_baslat(kod):
    mg_iptal()
    for widget in minigame_cercevesi.winfo_children():
        widget.destroy()
    minigame_cercevesi.pack(pady=10, fill="both", expand=True)
    durum["mg_aktif"] = True

    if kod == "A":  # Refleks
        durum["mg_sayac"] = 5
        mg_bilgi = tk.Label(minigame_cercevesi, text="Hareket eden sinyale 5 kere tıkla!", font=("Courier", 11), bg=BG, fg="white")
        mg_bilgi.pack()

        alan = tk.Frame(minigame_cercevesi, width=300, height=200, bg="#111111")
        alan.pack(pady=10)
        alan.pack_propagate(False)

        btn = tk.Button(alan, text="SİNYAL", bg="red", fg="white", font=("Courier", 8, "bold"))

        def sinyal_kacir():
            if not durum["mg_aktif"]:
                return
            mg_iptal()  # tek bir zamanlayıcı zinciri kalsın
            btn.place(x=random.randint(10, 220), y=random.randint(10, 160))
            durum["mg_id"] = pencere.after(800, sinyal_kacir)

        def sinyal_vur():
            if not durum["mg_aktif"]:
                return
            durum["mg_sayac"] -= 1
            if durum["mg_sayac"] <= 0:
                soru_ekranina_gec()
            else:
                mg_bilgi.config(text=f"Kalan: {durum['mg_sayac']}")
                sinyal_kacir()

        btn.config(command=sinyal_vur)
        sinyal_kacir()

    elif kod == "B":  # Zamanlama
        durum["mg_sayac"] = 0
        durum["mg_yon"] = 1
        tk.Label(minigame_cercevesi, text="Çubuk YEŞİL bölgeye gelince ATLA'ya bas!", font=("Courier", 11), bg=BG, fg="white").pack()

        bar_etiket = tk.Label(minigame_cercevesi, text="", font=("Courier", 20, "bold"), bg=BG, fg="white")
        bar_etiket.pack(pady=20)

        def bar_guncelle():
            if not durum["mg_aktif"]:
                return
            durum["mg_sayac"] += durum["mg_yon"]
            if durum["mg_sayac"] >= 15:
                durum["mg_sayac"] = 15
                durum["mg_yon"] = -1
            elif durum["mg_sayac"] <= 0:
                durum["mg_sayac"] = 0
                durum["mg_yon"] = 1

            gorsel = "[" + "=" * durum["mg_sayac"] + " " * (15 - durum["mg_sayac"]) + "]"
            if 9 <= durum["mg_sayac"] <= 12:  # yeşil (kazanma) bölgesi
                bar_etiket.config(text=gorsel, fg=YESIL)
            else:
                bar_etiket.config(text=gorsel, fg="white")
            durum["mg_id"] = pencere.after(80, bar_guncelle)

        def atla():
            if not durum["mg_aktif"]:
                return
            durum["mg_aktif"] = False
            mg_iptal()
            if 9 <= durum["mg_sayac"] <= 12:
                soru_ekranina_gec()
            else:
                oyunu_bitir("ELENDİN! Güvenlik duvarına çarptın.")

        tk.Button(minigame_cercevesi, text="ATLA (JUMP)", font=("Courier", 14, "bold"), bg="white", fg="black", command=atla).pack()
        bar_guncelle()

    elif kod == "C":  # Hafıza
        gizli_rota = str(random.randint(10000, 99999))
        tk.Label(minigame_cercevesi, text="Rotayı ezberle! 2 saniye sonra silinecek.", font=("Courier", 11), bg=BG, fg="white").pack()

        rota_etiket = tk.Label(minigame_cercevesi, text=gizli_rota, font=("Courier", 35, "bold"), bg=BG, fg=YESIL)
        rota_etiket.pack(pady=20)

        girdi = tk.Entry(minigame_cercevesi, font=("Courier", 16), justify="center", bg="#1a1a1a", fg="white", insertbackground="white")

        def kontrol_et(event=None):
            if not durum["mg_aktif"]:
                return
            durum["mg_aktif"] = False
            if girdi.get().strip() == gizli_rota:
                soru_ekranina_gec()
            else:
                oyunu_bitir(f"ELENDİN! Yanlış rota. (Doğru rota: {gizli_rota})")

        girdi.bind("<Return>", kontrol_et)
        onay_btn = tk.Button(minigame_cercevesi, text="ROTAYI GİR", command=kontrol_et, font=("Courier", 12))

        def rotayi_gizle():
            if not durum["mg_aktif"]:
                return
            rota_etiket.config(text="*****", fg="red")
            girdi.pack(pady=5)
            onay_btn.pack()
            girdi.focus_set()

        durum["mg_id"] = pencere.after(2000, rotayi_gizle)

    elif kod == "D":  # Brute Force
        durum["mg_sayac"] = 15
        tk.Label(minigame_cercevesi, text="Sistemi kırmak için 15 kere HIZLICA tıkla!", font=("Courier", 11), bg=BG, fg="white").pack()

        sayac_etiket = tk.Label(minigame_cercevesi, text="Kalan: 15", font=("Courier", 20, "bold"), bg=BG, fg="red")
        sayac_etiket.pack(pady=10)

        def kir_tikla():
            if not durum["mg_aktif"]:
                return
            durum["mg_sayac"] -= 1
            sayac_etiket.config(text=f"Kalan: {durum['mg_sayac']}")
            if durum["mg_sayac"] <= 0:
                soru_ekranina_gec()

        tk.Button(minigame_cercevesi, text="HACK (TIKLA)", font=("Courier", 16, "bold"), bg="white", command=kir_tikla, pady=20, padx=20).pack()


# --- 3. AŞAMA: BİLGİ SORUSU ---
def soru_ekranina_gec():
    durum["mg_aktif"] = False
    mg_iptal()
    minigame_cercevesi.pack_forget()

    kategori = KATEGORILER[durum["secilen_ag"]]
    # Aynı soru arka arkaya gelmesin
    adaylar = [s for s in kategori["sorular"] if s is not durum["son_soru"]] or kategori["sorular"]
    secilen_soru = random.choice(adaylar)
    durum["aktif_soru"] = secilen_soru
    durum["son_soru"] = secilen_soru

    soru_baslik.config(text=f"HEDEF: {kategori['ag_adi']}")
    soru_metni.config(text=secilen_soru["soru"])
    oyun_sifre_giris.delete(0, tk.END)

    soru_cercevesi.pack(pady=20)
    oyun_sifre_giris.focus_set()
    log_etiketi.config(text="Güvenlik aşıldı. Veri şifresini çöz.", fg=YESIL)


def cevap_kontrol(event=None):
    if not durum["oyun_aktif"] or durum["aktif_soru"] is None:
        return

    tahmin = sadelestir(oyun_sifre_giris.get())
    dogru_cevap = durum["aktif_soru"]["cevap"]
    oyun_sifre_giris.delete(0, tk.END)
    if tahmin == "":
        return

    if tahmin == sadelestir(dogru_cevap):
        # TROL ZAMANI
        durum["oyun_aktif"] = False
        zamanlayicilari_iptal_et()
        soru_cercevesi.pack_forget()
        log_etiketi.config(text=durum["aktif_soru"]["veri"], fg=YESIL)
        durum["yakalanma_sayaci"] = pencere.after(4000, yakalandin_patla)
    else:
        durum["sure"] -= CEZA
        if durum["sure"] <= 0:
            oyunu_bitir(f"ELENDİN! Sistem kilitlendi.\nDoğru cevap: {dogru_cevap}")
        else:
            sure_goster()
            log_etiketi.config(text=f"Yanlış Şifre! -{CEZA} Saniye ceza.\nDoğru cevap: {dogru_cevap}", fg=KIRMIZI)


# --- BİTİŞ VE TROLLER ---
def yakalandin_patla():
    durum["yakalanma_sayaci"] = None
    sure_etiketi.config(text="HACK!")
    log_etiketi.config(text="MEHMET HOCA YAKALADI! ELENDİN!\nIP TESPİT EDİLDİ! BAĞLANTI KESİLİYOR!")
    verileri_kaydet("YAKALANDI")
    yanip_son(8)


def yanip_son(kalan):
    """Ekran kırmızı/siyah yanıp söner, sonra tekrar dene butonu çıkar."""
    if kalan > 0:
        if kalan % 2 == 0:
            renk_ayarla("#cc0000", "black", "black")
        else:
            renk_ayarla(BG, KIRMIZI, KIRMIZI)
        durum["flas_id"] = pencere.after(150, lambda: yanip_son(kalan - 1))
    else:
        renk_ayarla(BG, KIRMIZI, KIRMIZI)
        durum["flas_id"] = None
        tekrar_dene_btn.pack(pady=20)


def geri_sayim():
    if not durum["oyun_aktif"]:
        return
    durum["sure"] -= 1
    if durum["sure"] <= 0:
        mesaj = "ELENDİN. Zaman tükendi."
        if durum["aktif_soru"]:
            mesaj += f"\nDoğru cevap: {durum['aktif_soru']['cevap']}"
        oyunu_bitir(mesaj)
        return
    sure_goster()
    durum["sayac_id"] = pencere.after(1000, geri_sayim)


def oyunu_bitir(mesaj):
    durum["oyun_aktif"] = False
    durum["mg_aktif"] = False
    durum["sure"] = 0
    zamanlayicilari_iptal_et()
    ag_cercevesi.pack_forget()
    minigame_cercevesi.pack_forget()
    soru_cercevesi.pack_forget()

    sure_etiketi.config(text="00:00", fg=KIRMIZI)
    log_etiketi.config(text=mesaj, fg=KIRMIZI)
    verileri_kaydet(mesaj.replace("\n", " "))
    tekrar_dene_btn.pack(pady=20)


def verileri_kaydet(mesaj):
    veri = {"tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ajan": durum["kullanici"], "sonuc": mesaj}
    with open(SKOR_DOSYASI, "a", encoding="utf-8") as dosya:
        json.dump(veri, dosya, ensure_ascii=False)
        dosya.write("\n")


# --- ARAYÜZ (GUI) TASARIMI ---
pencere = tk.Tk()
pencere.title("Sistem Sızma Arayüzü")
pencere.geometry("500x750")
pencere.config(bg=BG)
pencere.attributes('-alpha', 0.90)

# Sağ üstteki X tuşunu devre dışı bırak
pencere.protocol("WM_DELETE_WINDOW", lambda: None)
# X kapalı olduğu için çıkış kısayolu: Ctrl+Q
pencere.bind("<Control-q>", lambda e: pencere.destroy())

baslik_etiketi = tk.Label(pencere, text="AJAN GİRİŞİ", font=("Courier", 35, "bold"), bg=BG, fg="white")
baslik_etiketi.pack(pady=(30, 10))

# 1. GİRİŞ ÇERÇEVESİ
giris_cercevesi = tk.Frame(pencere, bg=BG)
giris_cercevesi.pack(pady=20)
tk.Label(giris_cercevesi, text="KİMLİK:", font=("Courier", 12), bg=BG, fg="white").pack()
k_adi_giris = tk.Entry(giris_cercevesi, font=("Courier", 14), justify="center", bg="#1a1a1a", fg="white", insertbackground="white", relief="flat")
k_adi_giris.pack(pady=5)
tk.Label(giris_cercevesi, text="GİZLİ KOD:", font=("Courier", 12), bg=BG, fg="white").pack()
sifre_giris_kutusu = tk.Entry(giris_cercevesi, font=("Courier", 14), justify="center", show="*", bg="#1a1a1a", fg="white", insertbackground="white", relief="flat")
sifre_giris_kutusu.pack(pady=5)
sifre_giris_kutusu.bind("<Return>", giris_yap)  # Enter ile giriş
btn_c = tk.Frame(giris_cercevesi, bg=BG)
btn_c.pack(pady=15)
tk.Button(btn_c, text="GİRİŞ", font=("Courier", 12, "bold"), bg="white", command=giris_yap).grid(row=0, column=0, padx=10)
tk.Button(btn_c, text="KAYIT", font=("Courier", 12, "bold"), bg="#333333", fg="white", command=kayit_ol).grid(row=0, column=1, padx=10)
k_adi_giris.focus_set()

# OYUN ANA ÇERÇEVESİ
oyun_cercevesi = tk.Frame(pencere, bg=BG)
hosgeldin_etiketi = tk.Label(oyun_cercevesi, font=("Courier", 11), bg=BG, fg="gray")
hosgeldin_etiketi.pack()
sure_etiketi = tk.Label(oyun_cercevesi, text=f"00:{BASLANGIC_SURESI:02d}", font=("Courier", 55, "bold"), fg="white", bg=BG)
sure_etiketi.pack(pady=(10, 5))

# 2. AĞ SEÇİM ÇERÇEVESİ
ag_cercevesi = tk.Frame(oyun_cercevesi, bg=BG)
tk.Label(ag_cercevesi, text="BAĞLANILACAK AĞI SEÇİN", font=("Courier", 13, "bold"), bg=BG, fg="white").pack(pady=10)
for kod, yazi in (("A", "A-AĞI (Üniversite)"), ("B", "B-AĞI (Devlet)"), ("C", "C-AĞI (Personel)"), ("D", "D-AĞI (Yemekhane)")):
    tk.Button(ag_cercevesi, text=yazi, bg="#1a1a1a", fg="white", font=("Courier", 12), width=25,
              command=lambda k=kod: ag_sec(k)).pack(pady=5)

# 3. MİNİ OYUN ÇERÇEVESİ
minigame_cercevesi = tk.Frame(oyun_cercevesi, bg=BG)

# 4. SORU ÇERÇEVESİ
soru_cercevesi = tk.Frame(oyun_cercevesi, bg=BG)
soru_baslik = tk.Label(soru_cercevesi, font=("Courier", 12, "bold"), bg=BG, fg="gray")
soru_baslik.pack(pady=5)
soru_metni = tk.Label(soru_cercevesi, font=("Courier", 11), bg=BG, fg="white", wraplength=400)
soru_metni.pack(pady=10)
oyun_sifre_giris = tk.Entry(soru_cercevesi, font=("Courier", 16), justify="center", bg="#1a1a1a", fg="white", insertbackground="white", relief="flat")
oyun_sifre_giris.pack(pady=5)
oyun_sifre_giris.bind("<Return>", cevap_kontrol)  # Enter ile gönder
tk.Button(soru_cercevesi, text="SİSTEME GÖNDER", font=("Courier", 11, "bold"), bg="white", command=cevap_kontrol).pack(pady=10)

# LOG VE TEKRAR BUTONU
log_etiketi = tk.Label(oyun_cercevesi, text="", font=("Courier", 11, "bold"), bg=BG, fg="white", wraplength=450)
log_etiketi.pack(pady=20)
tekrar_dene_btn = tk.Button(oyun_cercevesi, text="TEKRAR DENE", font=("Courier", 12, "bold"), bg="#1a1a1a", fg="white", command=ag_secim_ekranini_ac)

pencere.mainloop()
