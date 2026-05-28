"""The Holy Quran Media integration."""
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "quran_media"

async def async_setup(hass, config):
    """Set up the Quran Media component."""
    _LOGGER.info("Initializing Holy Quran Media integration")
    return True
