"""Media player platform for Holy Quran Media."""

import logging

from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_IDLE, STATE_PAUSED, STATE_PLAYING
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

_LOGGER = logging.getLogger(__name__)

DOMAIN = "quran_media"

# ─── القراء ───────────────────────────────────────────────────────────────────
RECITERS = {
    "مشاري العفاسي | Mishary Alafasy":          "https://server8.mp3quran.net/afs",
    "ماهر المعيقلي | Maher Al Muaiqly":         "https://server12.mp3quran.net/maher",
    "عبدالباسط عبدالصمد | Abdul Basit":         "https://server7.mp3quran.net/basit",
    "سعود الشريم | Saud Al-Shuraim":            "https://server7.mp3quran.net/shur",
    "عبدالرحمن السديس | Abdul Rahman Al-Sudais": "https://server11.mp3quran.net/sds",
    "ناصر القطامي | Nasser Al-Qatami":          "https://server6.mp3quran.net/qtm",
    "فارس عباد | Fares Abbad":                  "https://server7.mp3quran.net/frs",
    "أحمد العجمي | Ahmed Al-Ajmi":              "https://server10.mp3quran.net/ajm",
    "خالد الجليل | Khalid Al-Jalil":            "https://server11.mp3quran.net/jlil",
    "يوسف الشويعي | Yusuf Al-Shuwai'i":         "https://server6.mp3quran.net/shw",
}

# ─── البث المباشر ─────────────────────────────────────────────────────────────
LIVE_STREAMS = {
    "📻 إذاعة القرآن الكريم - السعودية | Saudi Quran Radio":
        "https://Qurango.net/radio/tarateel",
    # أضف هنا مستقبلاً:
    # "📻 إذاعة السنة النبوية | Sunnah Radio": "رابط",
    # "🕌 خطبة الجمعة - الحرم المكي | Makkah Friday": "رابط",
}

# ─── السور ────────────────────────────────────────────────────────────────────
SURAHS = {
    "الفاتحة | Al-Fatihah": 1,
    "البقرة | Al-Baqarah": 2,
    "آل عمران | Aal-Imran": 3,
    "النساء | An-Nisa": 4,
    "المائدة | Al-Ma'idah": 5,
    "الأنعام | Al-An'am": 6,
    "الأعراف | Al-A'raf": 7,
    "الأنفال | Al-Anfal": 8,
    "التوبة | At-Tawbah": 9,
    "يونس | Yunus": 10,
    "هود | Hud": 11,
    "يوسف | Yusuf": 12,
    "الرعد | Ar-Ra'd": 13,
    "إبراهيم | Ibrahim": 14,
    "الحجر | Al-Hijr": 15,
    "النحل | An-Nahl": 16,
    "الإسراء | Al-Isra": 17,
    "الكهف | Al-Kahf": 18,
    "مريم | Maryam": 19,
    "طه | Ta-Ha": 20,
    "الأنبياء | Al-Anbiya": 21,
    "الحج | Al-Hajj": 22,
    "المؤمنون | Al-Mu'minun": 23,
    "النور | An-Nur": 24,
    "الفرقان | Al-Furqan": 25,
    "الشعراء | Ash-Shu'ara": 26,
    "النمل | An-Naml": 27,
    "القصص | Al-Qasas": 28,
    "العنكبوت | Al-'Ankabut": 29,
    "الروم | Ar-Rum": 30,
    "لقمان | Luqman": 31,
    "السجدة | As-Sajdah": 32,
    "الأحزاب | Al-Ahzab": 33,
    "سبأ | Saba": 34,
    "فاطر | Fatir": 35,
    "يس | Ya-Sin": 36,
    "الصافات | As-Saffat": 37,
    "ص | Sad": 38,
    "الزمر | Az-Zumar": 39,
    "غافر | Ghafir": 40,
    "فصلت | Fussilat": 41,
    "الشورى | Ash-Shura": 42,
    "الزخرف | Az-Zukhruf": 43,
    "الدخان | Ad-Dukhan": 44,
    "الجاثية | Al-Jathiyah": 45,
    "الأحقاف | Al-Ahqaf": 46,
    "محمد | Muhammad": 47,
    "الفتح | Al-Fath": 48,
    "الحجرات | Al-Hujurat": 49,
    "ق | Qaf": 50,
    "الذاريات | Adh-Dhariyat": 51,
    "الطور | At-Tur": 52,
    "النجم | An-Najm": 53,
    "القمر | Al-Qamar": 54,
    "الرحمن | Ar-Rahman": 55,
    "الواقعة | Al-Waqi'ah": 56,
    "الحديد | Al-Hadid": 57,
    "المجادلة | Al-Mujadila": 58,
    "الحشر | Al-Hashr": 59,
    "الممتحنة | Al-Mumtahanah": 60,
    "الصف | As-Saf": 61,
    "الجمعة | Al-Jumu'ah": 62,
    "المنافقون | Al-Munafiqun": 63,
    "التغابن | At-Taghabun": 64,
    "الطلاق | At-Talaq": 65,
    "التحريم | At-Tahrim": 66,
    "الملك | Al-Mulk": 67,
    "القلم | Al-Qalam": 68,
    "الحاقة | Al-Haqqah": 69,
    "المعارج | Al-Ma'arij": 70,
    "نوح | Nuh": 71,
    "الجن | Al-Jinn": 72,
    "المزمل | Al-Muzzammil": 73,
    "المدثر | Al-Muddaththir": 74,
    "القيامة | Al-Qiyamah": 75,
    "الإنسان | Al-Insan": 76,
    "المرسلات | Al-Mursalat": 77,
    "النبأ | An-Naba": 78,
    "النازعات | An-Nazi'at": 79,
    "عبس | Abasa": 80,
    "التكوير | At-Takwir": 81,
    "الانفطار | Al-Infitar": 82,
    "المطففين | Al-Mutaffifin": 83,
    "الانشقاق | Al-Inshiqaq": 84,
    "البروج | Al-Buruj": 85,
    "الطارق | At-Tariq": 86,
    "الأعلى | Al-A'la": 87,
    "الغاشية | Al-Ghashiyah": 88,
    "الفجر | Al-Fajr": 89,
    "البلد | Al-Balad": 90,
    "الشمس | Ash-Shams": 91,
    "الليل | Al-Layl": 92,
    "الضحى | Ad-Duha": 93,
    "الشرح | Ash-Sharh": 94,
    "التين | At-Tin": 95,
    "العلق | Al-'Alaq": 96,
    "القدر | Al-Qadr": 97,
    "البينة | Al-Bayyinah": 98,
    "الزلزلة | Az-Zalzalah": 99,
    "العاديات | Al-'Adiyat": 100,
    "القارعة | Al-Qari'ah": 101,
    "التكاثر | At-Takathur": 102,
    "العصر | Al-'Asr": 103,
    "الهمزة | Al-Humazah": 104,
    "الفيل | Al-Fil": 105,
    "قريش | Quraysh": 106,
    "الماعون | Al-Ma'un": 107,
    "الكوثر | Al-Kawthar": 108,
    "الكافرون | Al-Kafirun": 109,
    "النصر | An-Nasr": 110,
    "المسد | Al-Masad": 111,
    "الإخلاص | Al-Ikhlas": 112,
    "الفلق | Al-Falaq": 113,
    "الناس | An-Nas": 114,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up Quran Media Player."""
    entity = QuranMediaPlayer(hass, entry)

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN]["entities"] = [entity]

    async_add_entities([entity], True)


class QuranMediaPlayer(MediaPlayerEntity):
    """Holy Quran Media Player."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.hass = hass
        self._entry = entry
        self._attr_name = "Holy Quran Media Player"
        self._attr_unique_id = "holy_quran_media_player"
        self._state = STATE_IDLE
        self._current_reciter = list(RECITERS.keys())[0]
        self._current_surah = list(SURAHS.keys())[0]
        # ── هنا الفرق: نقرأ البلير المحفوظ من options ──
        self._selected_player = entry.options.get("selected_player", None)
        self._is_live = False
        self._live_stream = list(LIVE_STREAMS.keys())[0]
        self._media_url = ""
        self._update_media_url()

    # ─── URL ──────────────────────────────────────────────────────────────────

    def _update_media_url(self):
        if self._is_live:
            self._media_url = LIVE_STREAMS[self._live_stream]
        else:
            base_url = RECITERS[self._current_reciter]
            surah_number = SURAHS[self._current_surah]
            self._media_url = f"{base_url}/{surah_number:03d}.mp3"

    def _get_available_players(self):
        return [
            eid for eid in self.hass.states.async_entity_ids("media_player")
            if eid != "media_player.holy_quran_media_player"
        ]

    def _resolve_player(self):
        if self._selected_player:
            return self._selected_player
        players = self._get_available_players()
        return players[0] if players else None

    # ─── Properties ───────────────────────────────────────────────────────────

    @property
    def state(self):
        return self._state

    @property
    def source_list(self):
        return list(RECITERS.keys())

    @property
    def source(self):
        return self._current_reciter

    @property
    def sound_mode_list(self):
        return list(SURAHS.keys())

    @property
    def sound_mode(self):
        return self._current_surah

    @property
    def media_title(self):
        if self._is_live:
            return self._live_stream
        return self._current_surah

    @property
    def media_artist(self):
        if self._is_live:
            return "بث مباشر | Live"
        return self._current_reciter

    @property
    def media_content_id(self):
        return self._media_url

    @property
    def extra_state_attributes(self):
        return {
            "available_players": self._get_available_players(),
            "selected_player": self._resolve_player(),
            "is_live": self._is_live,
            "live_streams": list(LIVE_STREAMS.keys()),
            "current_surah_number": SURAHS.get(self._current_surah),
            "media_url": self._media_url,
        }

    @property
    def supported_features(self):
        return (
            MediaPlayerEntityFeature.PLAY
            | MediaPlayerEntityFeature.PAUSE
            | MediaPlayerEntityFeature.STOP
            | MediaPlayerEntityFeature.SELECT_SOURCE
            | MediaPlayerEntityFeature.SELECT_SOUND_MODE
        )

    # ─── Actions ──────────────────────────────────────────────────────────────

    async def async_select_source(self, source):
        if source in RECITERS:
            self._is_live = False
            self._current_reciter = source
            self._update_media_url()
            self.async_write_ha_state()

    async def async_select_sound_mode(self, sound_mode):
        if sound_mode in SURAHS:
            self._current_surah = sound_mode
            self._is_live = False
            self._update_media_url()
            self.async_write_ha_state()

    async def async_media_play(self):
        player = self._resolve_player()
        if not player:
            _LOGGER.warning("quran_media: No media player available")
            return
        await self.hass.services.async_call(
            "media_player", "play_media",
            {
                "entity_id": player,
                "media_content_id": self._media_url,
                "media_content_type": "music",
            },
            blocking=True,
        )
        self._state = STATE_PLAYING
        self.async_write_ha_state()

    async def async_media_pause(self):
        player = self._resolve_player()
        if player:
            await self.hass.services.async_call(
                "media_player", "media_pause", {"entity_id": player}, blocking=True
            )
        self._state = STATE_PAUSED
        self.async_write_ha_state()

    async def async_media_stop(self):
        player = self._resolve_player()
        if player:
            await self.hass.services.async_call(
                "media_player", "media_stop", {"entity_id": player}, blocking=True
            )
        self._state = STATE_IDLE
        self.async_write_ha_state()

    async def async_set_player(self, player_entity_id: str):
        """تحديد البلير وحفظه — يبقى بعد الـ Restart."""
        self._selected_player = player_entity_id
        # حفظ في config_entry.options
        self.hass.config_entries.async_update_entry(
            self._entry,
            options={**self._entry.options, "selected_player": player_entity_id},
        )
        _LOGGER.info("quran_media: player saved as %s", player_entity_id)
        self.async_write_ha_state()

    async def async_play_live(self, stream: str):
        if stream in LIVE_STREAMS:
            self._is_live = True
            self._live_stream = stream
            self._update_media_url()
            await self.async_media_play()

    async def async_play_surah(self, surah: str, reciter: str = None):
        if surah in SURAHS:
            self._current_surah = surah
            self._is_live = False
        if reciter and reciter in RECITERS:
            self._current_reciter = reciter
        self._update_media_url()
        await self.async_media_play()
