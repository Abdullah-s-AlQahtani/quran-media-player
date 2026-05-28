"""Config flow for Holy Quran Media."""

from homeassistant import config_entries
from homeassistant.helpers import selector
import voluptuous as vol

DOMAIN = "quran_media"


class QuranMediaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Holy Quran Media."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        return self.async_create_entry(title="Holy Quran Media", data={})

    @staticmethod
    def async_get_options_flow(config_entry):
        return QuranMediaOptionsFlow(config_entry)


class QuranMediaOptionsFlow(config_entries.OptionsFlow):
    """Handle options for Holy Quran Media."""

    def __init__(self, config_entry):
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_player = self._config_entry.options.get("selected_player", "")

        schema = vol.Schema({
            vol.Optional("selected_player", default=current_player): selector.selector({
                "entity": {"domain": "media_player"}
            }),
        })

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
        )
