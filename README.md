# 🕵️ Ajan Sızma / Agent Infiltration

**[🇹🇷 Türkçe](#tr) | [🇬🇧 English](#en)**

---

<a name="tr"></a>
## 🇹🇷 Türkçe

Python ve `tkinter` ile yazılmış, siyah/beyaz minimalist ve terminal görünümlü bir masaüstü mini oyunu. Bir ajan olarak dört farklı ağdan birine sızmaya çalışırsın: önce bir güvenlik mini oyununu geçer, sonra bir şifre sorusunu çözersin. Ama dikkat: **doğru cevap seni Mehmet Hoca'nın tuzağına düşürür.** 😈

> Okul ödevi olarak hazırlanmış, tamamen kurgusal ve eğlence amaçlı bir projedir.

### Özellikler

- Kimlik oluşturma ve giriş sistemi (kayıt / giriş)
- 4 farklı ağ, her birinin kendi mini oyunu ve soru havuzu
- Geri sayım sayacı, yanlış cevapta süre cezası
- Yanlış cevap verince doğru cevabın gösterilmesi
- Doğru cevapta kırmızı/siyah yanıp sönen "yakalandın" trol ekranı
- Sonuçların JSON dosyasına kaydedilmesi
- Türkçe karakter ve büyük/küçük harf farkını yok sayan cevap kontrolü (`çay` = `ÇAY` = `cay`)
- Harici kütüphane gerektirmez, tek dosyadır

### Gereksinimler

- Python 3.8 veya üzeri
- `tkinter` (Windows ve macOS'ta Python ile birlikte gelir)

Linux'ta `tkinter` yüklü değilse:

```bash
sudo apt install python3-tk
```

### Çalıştırma

```bash
git clone https://github.com/KULLANICI_ADIN/REPO_ADIN.git
cd REPO_ADIN
python ajan_sizma_gelismis.py
```

### Nasıl oynanır?

1. **Kayıt ol** ve ardından aynı kimlikle **giriş yap**.
2. Dört ağdan birini seç.
3. Ağın güvenlik mini oyununu geç.
4. Karşına çıkan soruyu cevapla.
5. Süre dolmadan hayatta kal!

Süre varsayılan olarak 60 saniyedir. Yanlış cevap verirsen süreden 10 saniye düşer. Süre biterse oyun biter.

#### Ağlar ve mini oyunlar

| Ağ | Konu | Mini oyun |
|----|------|-----------|
| A | Üniversite Ağı | **Sinyal Yakalama:** hareket eden sinyale 5 kez tıkla |
| B | Devlet Sırları | **Güvenlik Duvarı:** çubuk yeşil bölgedeyken ATLA'ya bas |
| C | Personel Ağı | **Veri Yolu:** 5 haneli rotayı ezberle ve 2 saniye sonra gir |
| D | Yemekhane Ağı | **Kaba Kuvvet:** butona 15 kez hızlıca tıkla |

### Kontroller

| Tuş | İşlev |
|-----|-------|
| `Enter` | Giriş yap / cevabı gönder / rotayı onayla |
| `Ctrl + Q` | Programdan çık |

Pencerenin sağ üstündeki **X** tuşu bilerek devre dışıdır. Programı kapatmak için `Ctrl + Q` kullan.

### Ayarlar

Dosyanın başındaki sabitlerle oyunu kolayca değiştirebilirsin:

```python
BASLANGIC_SURESI = 60   # başlangıç süresi (saniye)
CEZA = 10               # yanlış cevapta düşen süre
```

Yeni soru eklemek için `KATEGORILER` sözlüğündeki `sorular` listesine şu formatta bir kayıt eklemen yeterli:

```python
{"soru": "Soru metni?", "cevap": "cevap", "veri": "Doğru bilince ekrana çıkan trol mesajı."}
```

### Oluşan dosyalar

Program ilk açıldığında, `.py` dosyasının bulunduğu klasörde şu dosyalar otomatik oluşturulur:

| Dosya | İçerik |
|-------|--------|
| `kullanicilar.json` | Kayıtlı kimlikler ve gizli kodlar |
| `ajan_verileri.json` | Oyun sonuçları (tarih, ajan, sonuç) |

> ⚠️ Gizli kodlar bu projede düz metin olarak saklanır. Gerçek şifrelerini kullanma.

### Proje yapısı

```
.
├── ajan_sizma_gelismis.py   # oyunun tamamı
├── kullanicilar.json        # otomatik oluşur
├── ajan_verileri.json       # otomatik oluşur
└── README.md
```

### Lisans

Bu proje eğitim amaçlıdır. İstediğin gibi inceleyebilir ve geliştirebilirsin.

[⬆ Başa dön](#-ajan-sızma--agent-infiltration)

---

<a name="en"></a>
## 🇬🇧 English

A minimalist black-and-white, terminal-style desktop mini game written in Python with `tkinter`. As a secret agent, you try to infiltrate one of four networks: first you beat a security mini game, then you crack a password question. But be careful: **the correct answer walks you straight into Professor Mehmet's trap.** 😈

> A school project. Completely fictional and made for fun.

### Features

- Identity creation and login system (register / login)
- 4 different networks, each with its own mini game and question pool
- Countdown timer with a time penalty for wrong answers
- The correct answer is revealed when you answer wrong
- A red/black flashing "you got caught" troll screen when you answer correctly
- Results saved to a JSON file
- Answer checking that ignores case and Turkish characters (`çay` = `ÇAY` = `cay`)
- No external libraries needed, single file

### Requirements

- Python 3.8 or newer
- `tkinter` (bundled with Python on Windows and macOS)

If `tkinter` is missing on Linux:

```bash
sudo apt install python3-tk
```

### Running

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
python ajan_sizma_gelismis.py
```

### How to play

1. **Register**, then **log in** with the same identity.
2. Pick one of the four networks.
3. Beat the network's security mini game.
4. Answer the question that appears.
5. Survive before the time runs out!

The timer starts at 60 seconds by default. A wrong answer costs you 10 seconds. If time runs out, the game is over.

#### Networks and mini games

| Network | Theme | Mini game |
|---------|-------|-----------|
| A | University Network | **Signal Catch:** click the moving signal 5 times |
| B | State Secrets | **Firewall:** press JUMP while the bar is in the green zone |
| C | Staff Network | **Data Route:** memorize a 5-digit route and type it after 2 seconds |
| D | Cafeteria Network | **Brute Force:** click the button 15 times as fast as you can |

### Controls

| Key | Action |
|-----|--------|
| `Enter` | Log in / submit answer / confirm route |
| `Ctrl + Q` | Quit the program |

The window's **X** button is intentionally disabled. Use `Ctrl + Q` to close the program.

### Settings

You can tweak the game with the constants at the top of the file:

```python
BASLANGIC_SURESI = 60   # starting time (seconds)
CEZA = 10               # time lost on a wrong answer
```

To add a new question, append an entry in this format to the `sorular` list inside the `KATEGORILER` dictionary:

```python
{"soru": "Question text?", "cevap": "answer", "veri": "Troll message shown on a correct answer."}
```

### Generated files

When the program first starts, these files are created automatically in the same folder as the `.py` file:

| File | Contents |
|------|----------|
| `kullanicilar.json` | Registered identities and secret codes |
| `ajan_verileri.json` | Game results (date, agent, outcome) |

> ⚠️ Secret codes are stored as plain text in this project. Do not use your real passwords.

### Project structure

```
.
├── ajan_sizma_gelismis.py   # the whole game
├── kullanicilar.json        # auto-generated
├── ajan_verileri.json       # auto-generated
└── README.md
```

### License

This project is for educational purposes. Feel free to explore and improve it.

[⬆ Back to top](#-ajan-sızma--agent-infiltration)
