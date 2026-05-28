# 🕌 Holy Quran Media Player

**مشغل القرآن الكريم لـ Home Assistant**

Browse and play the full Holy Quran inside Home Assistant — with reciter selection, surah browsing, live Saudi Quran Radio, and full automation support.

---

## ✨ المميزات | Features

- 📖 **114 سورة كاملة** — Browse and play all 114 surahs
- 🎙️ **10 قراء مشاهير** — 10 world-renowned reciters
- 📻 **إذاعة القرآن السعودية** — Live Saudi Quran Radio stream
- 🔊 **اختيار جهاز التشغيل** — Choose any media player in your home
- 🤖 **دعم الأتوميشن** — Full automation and Blueprint support
- 🌐 **عربي وإنجليزي** — Arabic and English interface
- 🎨 **كارد مخصص جميل** — Beautiful custom Lovelace card

---

## 📦 التثبيت | Installation

### عبر HACS (موصى به) | Via HACS (Recommended)

1. افتح **HACS** في Home Assistant
2. اضغط **Integrations** ثم **+ Explore & Download Repositories**
3. ابحث عن **Holy Quran Media Player**
4. اضغط **Download**
5. أعد تشغيل Home Assistant
6. روح **Settings → Devices & Services → Add Integration**
7. ابحث عن **Holy Quran Media** وأضفه

---

## 🖥️ إضافة الكارد | Add the Card

بعد التثبيت وإعادة التشغيل، الكارد يكون متاح تلقائياً:

1. افتح الداشبورد واضغط **Edit**
2. اضغط **+ Add Card**
3. ابحث عن **Quran Media Player**
4. اضغط عليه — خلاص! ✅

---

## ⚙️ الإعداد الأول | First Setup

بعد إضافة الكارد، حدد جهاز التشغيل:

1. روح **Settings → Devices & Services → Holy Quran Media**
2. اضغط **Configure**
3. اختر الجهاز الذي تريد تشغيل القرآن عليه
4. اضغط **Submit**

---

## 🤖 الأتوميشن | Automation Examples

### تشغيل سورة الكهف كل جمعة

```yaml
automation:
  - alias: "سورة الكهف - كل جمعة"
    trigger:
      - platform: time
        at: "11:00:00"
    condition:
      - condition: time
        weekday:
          - fri
    action:
      - service: quran_media.play_surah
        data:
          surah: "الكهف | Al-Kahf"
          reciter: "مشاري العفاسي | Mishary Alafasy"
```

### تشغيل إذاعة القرآن عند الفجر

```yaml
automation:
  - alias: "إذاعة القرآن - الفجر"
    trigger:
      - platform: sun
        event: sunrise
    action:
      - service: quran_media.play_live
        data:
          stream: "📻 إذاعة القرآن الكريم - السعودية | Saudi Quran Radio"
```

---

## 🎙️ القراء المتاحون | Available Reciters

| القارئ | Reciter |
|--------|---------|
| مشاري العفاسي | Mishary Alafasy |
| ماهر المعيقلي | Maher Al Muaiqly |
| عبدالباسط عبدالصمد | Abdul Basit |
| سعود الشريم | Saud Al-Shuraim |
| عبدالرحمن السديس | Abdul Rahman Al-Sudais |
| ناصر القطامي | Nasser Al-Qatami |
| فارس عباد | Fares Abbad |
| أحمد العجمي | Ahmed Al-Ajmi |
| خالد الجليل | Khalid Al-Jalil |
| يوسف الشويعي | Yusuf Al-Shuwai'i |

---

## 🛠️ الخدمات | Services

| الخدمة | الوصف |
|--------|-------|
| `quran_media.play_surah` | تشغيل سورة محددة |
| `quran_media.play_live` | تشغيل البث المباشر |
| `quran_media.select_player` | اختيار جهاز التشغيل |

---

## 📡 المصادر | Sources

جميع الملفات الصوتية من **MP3Quran.net**

إذاعة القرآن الكريم من **Qurango.net**

---

## 📋 المتطلبات | Requirements

- Home Assistant **2023.1.0** أو أحدث
- اتصال بالإنترنت

---

## 👨‍💻 المطور | Developer

**Abdullah Al-Qahtani** — [@Abdullah-s-AlQahtani](https://github.com/Abdullah-s-AlQahtani)

---

## 📄 الترخيص | License

MIT License
