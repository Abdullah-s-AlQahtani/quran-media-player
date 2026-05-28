"""Platform for Quran Media Player integration."""
import logging
from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import (
    SUPPORT_PLAY,
    SUPPORT_PAUSE,
    SUPPORT_STOP,
    SUPPORT_VOLUME_SET,
    SUPPORT_VOLUME_MUTE,
)
from homeassistant.const import STATE_PAUSED, STATE_PLAYING, STATE_IDLE

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Quran Media Player platform."""
    _LOGGER.info("Setting up Quran Media Player platform")
    async_add_entities([QuranMediaPlayer()])

    class QuranMediaPlayer(MediaPlayerEntity):
        """Representation of a Quran Media Player."""

        def __init__(self):
            """Initialize the media player."""
            self._name = "Holy Quran Media Player"
            self._state = STATE_IDLE
            self._volume = 0.5
            self._is_muted = False

        @property
        def name(self):
            """Return the name of the device."""
            return self._name

        @property
        def state(self):
            """Return the state of the device."""
            return self._state

        @property
        def volume_level(self):
            """Volume level of the media player (0..1)."""
            return self._volume

        @property
        def is_volume_muted(self):
            """Boolean if volume is currently muted."""
            return self._is_muted

        @property
        def supported_features(self):
            """Flag media player features that are supported."""
            return SUPPORT_PLAY | SUPPORT_PAUSE | SUPPORT_STOP | SUPPORT_VOLUME_SET | SUPPORT_VOLUME_MUTE

        async def async_media_play(self):
            """Send play command."""
            self._state = STATE_PLAYING
            self.async_write_ha_state()

        async def async_media_pause(self):
            """Send pause command."""
            self._state = STATE_PAUSED
            self.async_write_ha_state()

        async def async_media_stop(self):
            """Send stop command."""
            self._state = STATE_IDLE
            self.async_write_ha_state()

        async def async_set_volume_level(self, volume):
            """Set volume level, range 0..1."""
            self._volume = volume
            self.async_write_ha_state()

        async def async_mute_volume(self, mute):
            """Mute the volume."""
            self._is_muted = mute
            self.async_write_ha_state()
