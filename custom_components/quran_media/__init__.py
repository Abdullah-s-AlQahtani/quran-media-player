"""The Holy Quran Media integration."""

import logging
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.frontend import add_extra_js_url

_LOGGER = logging.getLogger(__name__)
DOMAIN = "quran_media"


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up Quran Media."""
    add_extra_js_url(hass, "/local/community/quran_media/quran-card.js")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up config entry."""

    await hass.config_entries.async_forward_entry_setups(entry, ["media_player"])

    async def handle_select_player(call: ServiceCall):
        """تحديد البلير."""
        player = call.data.get("player")
        for entity in hass.data.get(DOMAIN, {}).get("entities", []):
            await entity.async_set_player(player)
            _LOGGER.info("quran_media: player set to %s", player)

    async def handle_play_live(call: ServiceCall):
        """تشغيل بث مباشر."""
        stream = call.data.get("stream")
        for entity in hass.data.get(DOMAIN, {}).get("entities", []):
            await entity.async_play_live(stream)

    async def handle_play_surah(call: ServiceCall):
        """تشغيل سورة محددة — مفيد للأتوميشن."""
        surah = call.data.get("surah")
        reciter = call.data.get("reciter")
        for entity in hass.data.get(DOMAIN, {}).get("entities", []):
            await entity.async_play_surah(surah, reciter)

    hass.services.async_register(DOMAIN, "select_player", handle_select_player)
    hass.services.async_register(DOMAIN, "play_live", handle_play_live)
    hass.services.async_register(DOMAIN, "play_surah", handle_play_surah)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload entry."""
    return await hass.config_entries.async_unload_platforms(entry, ["media_player"])
