"""Platform for Quran Media Player integration."""
import logging
from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import (
    SUPPORT_PLAY,
    SUPPORT_PAUSE,
    SUPPORT_STOP,
    SUPPORT_SELECT_SOURCE,
)
from homeassistant.const import STATE_PAUSED, STATE_PLAYING, STATE_IDLE

_LOGGER = logging.getLogger(__name__)

# قائمة القراء الافتراضية مع مسارات خوادم mp3quran المستقرة
RECITERS = {
    "مشاري العفاسي": "https://server8.mp3quran.net/afs",
    "ماهر المعيقلي": "https://server12.mp3quran.net/maher",
    "عبدالباسط عبدالصمد (مرتل)": "https://server7.mp3quran.net/basit",
    "سعود الشريم": "https://server7.mp3quran.net/shur",
}

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Quran Media Player platform."""
    _LOGGER.info("Setting up Quran Media Player platform with reciter tracks")
    async_add_entities([QuranMediaPlayer()])


class QuranMediaPlayer(MediaPlayerEntity):
    """Representation of the Holy Quran Media Player."""

    def __init__(self):
        """Initialize the Quran media player."""
        self._name = "Holy Quran Media Player"
        self._state = STATE_IDLE
        self._current_reciter = "مشاري العفاسي"
        self._current_surah_num = 1  # سورة الفاتحة كبداية افتراضية
        self._media_url = ""
        self._update_media_url()

    def _update_media_url(self):
        """تحديث رابط السورة بناءً على القارئ المختار ورقم السورة"""
        base_url = RECITERS[self._current_reciter]
        # تحويل رقم السورة إلى صيغة 3 خانات (مثلاً: 1 تصبح 001، و 11 تصبح 011)
        surah_format = f"{self._current_surah_num:03d}.mp3"
        self._media_url = f"{base_url}/{surah_format}"

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def source_list(self):
        """عرض قائمة القراء المتاحين في النظام كـ Sources"""
        return list(RECITERS.keys())

    @property
    def source(self):
        """القارئ الحالي المتصل بالمشغل"""
        return self._current_reciter

    @property
    def media_title(self):
        """عنوان المادة الصوتية الحالية (رقم السورة)"""
        return f"السورة رقم {self._current_surah_num}"

    @property
    def media_artist(self):
        """اسم القارئ الحالي"""
        return self._current_reciter

    @property
    def media_content_id(self):
        """الرابط المباشر لملف الـ MP3 الحالي لكي تسحبه السماعات"""
        return self._media_url

    @property
    def supported_features(self):
        """الخصائص التي يدعمها المشغل"""
        return SUPPORT_PLAY | SUPPORT_PAUSE | SUPPORT_STOP | SUPPORT_SELECT_SOURCE

    async def async_select_source(self, source):
        """تغيير القارئ من القائمة المنسدلة"""
        if source in RECITERS:
            self._current_reciter = source
            self._update_media_url()
            _LOGGER.info("Changed Quran reciter to: %s", source)
            self.async_write_ha_state()

    async def async_media_play(self):
        """تشغيل البث"""
        self._state = STATE_PLAYING
        _LOGGER.info("Playing Quran link: %s", self._media_url)
        self.async_write_ha_state()

    async def async_media_pause(self):
        """إيقاف مؤقت"""
        self._state = STATE_PAUSED
        self.async_write_ha_state()

    async def async_media_stop(self):
        """إيقاف كامل"""
        self._state = STATE_IDLE
        self.async_write_ha_state()
